#!/usr/bin/env python3
"""Independent Tablekeeper Stage 1 HTTP verification; no production imports.

Run only after exact-SHA release. Container runner mode:
  python campaign.py http --source URL --destination URL --out summary.json
Oracle calibration (no production execution): python campaign.py calibrate
All credentials and opaque exports stay in memory; output contains case outcomes only.
"""
import argparse
import copy
import datetime as dt
from decimal import Decimal
import json
import re
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
DAY = "2080-06-06"
WEEK = "mon tue wed thu fri sat sun".split()
PASSWORD = secrets.token_urlsafe(24)


def encode_json(value):
    """Exact JSON numbers, including finite magnitudes beyond binary64 range."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("non-JSON numeric value")
        return str(value)
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k) + ":" + encode_json(v) for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ",".join(encode_json(v) for v in value) + "]"
    return json.dumps(value, allow_nan=False)


def fixture(zone="Europe/Berlin", opens="18:00", closes="23:00", slot=30, duration=90):
    return {
        "users": [{"id": x, "email": x + "@verifier.invalid", "password": PASSWORD,
                   "display_name": x} for x in ("ada", "bob")],
        "restaurants": [{"id": "r", "name": "Independent fixture", "timezone": zone,
                         "slot_minutes": slot, "reservation_duration_minutes": duration,
                         "cancellation_cutoff_minutes": 120,
                         "opening_hours": [{"weekday": w, "opens": opens, "closes": closes}
                                           for w in WEEK],
                         "tables": [{"id": "z", "label": "Z", "capacity": 4},
                                    {"id": "a", "label": "A", "capacity": 2},
                                    {"id": "m", "label": "M", "capacity": 6}]}],
        "reservations": []}


def body(table="z", at="18:00", day=DAY, party=2, restaurant="r"):
    return {"restaurant_id": restaurant, "table_id": table,
            "starts_at_local": day + "T" + at, "party_size": party}


def resolve(local, zone):
    """First occurrence; round trip rejects nonexistent wall-clock values."""
    naive = dt.datetime.strptime(local, "%Y-%m-%dT%H:%M")
    aware = naive.replace(tzinfo=ZoneInfo(zone), fold=0)
    if aware.astimezone(UTC).astimezone(ZoneInfo(zone)).replace(tzinfo=None) != naive:
        return None
    return aware


def overlaps(a, b, c, d):
    return a < d and c < b


def instant_seconds(value):
    """Independent unbounded integer instant; handles UTC year 0/10000 crossings."""
    parsed = dt.datetime.fromisoformat(value)
    offset = parsed.utcoffset()
    check(offset is not None, "timestamp lacks explicit offset")
    return (parsed.toordinal() * 86400 + parsed.hour * 3600 + parsed.minute * 60 + parsed.second
            - int(offset.total_seconds()))


def audit(rows):
    check(isinstance(rows, list), "reservation list has wrong shape")
    required = {"reservation_id", "reference", "restaurant_id", "table_id", "starts_at", "ends_at", "status"}
    check(all(isinstance(r, dict) and required <= r.keys() for r in rows), "reservation list missing fields")
    check(len({r["reference"] for r in rows}) == len(rows), "duplicate reservation reference in state")
    check(len({r["reservation_id"] for r in rows}) == len(rows), "duplicate reservation identity in state")
    try:
        starts = [instant_seconds(r["starts_at"]) for r in rows]
        ends = [instant_seconds(r["ends_at"]) for r in rows]
    except ValueError:
        raise CheckFailure("invalid reservation timestamp")
    check(starts == sorted(starts, reverse=True), "list is not descending by absolute start instant")
    for i, r in enumerate(rows):
        check(r["status"] in ("confirmed", "cancelled"), "invalid reservation status")
        check(ends[i] > starts[i], "non-positive occupancy interval")
        for j in range(i):
            other = rows[j]
            if (r["status"] == other["status"] == "confirmed"
                    and (r["restaurant_id"], r["table_id"]) == (other["restaurant_id"], other["table_id"])):
                check(not overlaps(starts[i], ends[i], starts[j], ends[j]), "confirmed state has overlapping occupancy")


def oracle(fx, date, party, occupied=()):
    """Enumerate wall grid; independently compare UTC half-open occupancy."""
    r = fx["restaurants"][0]
    weekday = WEEK[dt.date.fromisoformat(date).weekday()]
    hours = next((h for h in r["opening_hours"] if h["weekday"] == weekday), None)
    if not hours:
        return []
    zone = ZoneInfo(r["timezone"])
    opening = dt.datetime.fromisoformat(date + "T" + hours["opens"])
    closing = resolve(date + "T" + hours["closes"], r["timezone"])
    assert closing is not None, "oracle fixture uses existent closing time"
    candidate = opening
    slots = []
    while candidate < closing.replace(tzinfo=None):
        local = candidate.isoformat(timespec="minutes")
        start = resolve(local, r["timezone"])
        if start is not None:
            start_utc = start.astimezone(UTC)
            end_utc = start_utc + dt.timedelta(minutes=r["reservation_duration_minutes"])
            if end_utc <= closing.astimezone(UTC):
                available = []
                for table in r["tables"]:
                    if table["capacity"] < party:
                        continue
                    taken = any(x["restaurant_id"] == r["id"] and x["table_id"] == table["id"] and x["status"] == "confirmed"
                                and overlaps(start_utc, end_utc,
                                             dt.datetime.fromisoformat(x["starts_at"]).astimezone(UTC),
                                             dt.datetime.fromisoformat(x["ends_at"]).astimezone(UTC))
                                for x in occupied)
                    if not taken:
                        available.append(table["id"])
                slots.append({"starts_at_local": local, "starts_at": start.isoformat(),
                              "available_table_ids": available})
        candidate += dt.timedelta(minutes=r["slot_minutes"])
    return slots


class CheckFailure(Exception):
    pass


def check(value, message):
    if not value:
        raise CheckFailure(message)


class API:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.timings = []
        self.lock = threading.Lock()

    def request(self, method, path, value=None, token=None, key=None, raw=None):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        if key is not None:
            headers["Idempotency-Key"] = key
        data = raw if raw is not None else (None if value is None else encode_json(value).encode())
        request = urllib.request.Request(self.url + path, data=data, method=method, headers=headers)
        before = time.monotonic()
        timeout = 10 if path.startswith("/_test/") else 5
        try:
            response = urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            status = response.status
            payload = response.read()
            content_type = response.headers.get("Content-Type", "").lower()
        elapsed = time.monotonic() - before
        with self.lock:
            self.timings.append((path, elapsed))
        check(elapsed <= timeout, "request exceeded stated timeout: " + path)
        check(status < 500, "5xx response: " + method + " " + path)
        if status == 204:
            check(payload == b"", "204 has a response body")
            return status, None
        check("application/json" in content_type and "charset=utf-8" in content_type.replace(" ", ""),
              "JSON UTF-8 response content type missing: " + path)
        try:
            parsed = json.loads(payload, parse_float=Decimal)
        except ValueError:
            raise CheckFailure("non-JSON response: " + path)
        if status >= 400:
            check(isinstance(parsed, dict) and isinstance(parsed.get("error"), dict)
                  and isinstance(parsed["error"].get("code"), str)
                  and isinstance(parsed["error"].get("message"), str), "invalid error envelope")
        return status, parsed

    def expect(self, status, method, path, value=None, token=None, key=None, code=None, raw=None):
        got, data = self.request(method, path, value, token, key, raw)
        check(got == status, f"{method} {path}: expected {status}, observed {got}"
              + (" code=" + str(data.get("error", {}).get("code")) if isinstance(data, dict) else ""))
        if code:
            check(data["error"]["code"] == code,
                  f"{method} {path}: expected code {code}, observed {data['error']['code']}")
        return data

    def reset(self, fx):
        self.expect(204, "POST", "/_test/reset", fx)

    def login(self, user="ada", password=None):
        result = self.expect(200, "POST", "/auth/login",
                             {"email": user + "@verifier.invalid", "password": PASSWORD if password is None else password})
        check(isinstance(result.get("token"), str) and result["token"], "login token absent")
        return result["token"]

    def book(self, token, value=None, key="book", status=201, code=None):
        result = self.expect(status, "POST", "/reservations", value or body(), token, key, code)
        if status in (200, 201):
            for field in ("reservation_id", "restaurant_id", "table_id", "reference", "created_at"):
                check(isinstance(result.get(field), str), "reservation field absent: " + field)
            check(len(result["reservation_id"]) <= 64, "reservation id exceeds 64")
            check(re.fullmatch("[A-Z0-9]{6,12}", result["reference"]) is not None, "reference format")
            for field in ("starts_at", "ends_at", "created_at"):
                check(dt.datetime.fromisoformat(result[field]).utcoffset() is not None, "timestamp lacks offset")
        return result

    def reservations(self, token):
        rows = self.expect(200, "GET", "/reservations", token=token)["reservations"]
        audit(rows)
        return rows

    def availability(self, day=DAY, party=2):
        query = urllib.parse.urlencode({"restaurant_id": "r", "date": day, "party_size": party})
        return self.expect(200, "GET", "/availability?" + query)["slots"]


class Campaign:
    def __init__(self, source, destination, control=None, third=None, legacy=None):
        self.api = API(source)
        self.dest = API(destination)
        self.results = []
        self.control = Path(control) if control else None
        self.third = API(third) if third else None
        self.legacy = API(legacy) if legacy else None

    def fresh(self, fx=None):
        self.fx = fx or fixture()
        self.api.reset(self.fx)
        self.token = self.api.login()
        return self.api, self.token

    def public_auth_reset(self):
        a, token = self.fresh()
        a.expect(200, "GET", "/health")
        a.expect(200, "GET", "/restaurants?ignored=x", token="unknown")
        actual = a.expect(200, "GET", "/restaurants/r")
        for k in ("slot_minutes", "reservation_duration_minutes", "cancellation_cutoff_minutes", "opening_hours", "tables"):
            check(actual[k] == self.fx["restaurants"][0][k], "restaurant detail differs: " + k)
        a.expect(404, "GET", "/restaurants/absent", code="not_found")
        a.expect(401, "GET", "/reservations", code="unauthenticated")
        a.expect(401, "GET", "/reservations", token="unknown", code="unauthenticated")
        for credential in (None, "", "unknown"):
            for method, path, value, key in (
                    ("POST", "/reservations", body(), "auth-check"),
                    ("GET", "/reservations/ABSENT", None, None),
                    ("POST", "/reservations/ABSENT/cancel", None, None),
                    ("PATCH", "/reservations/ABSENT", {"party_size": 1}, None),
                    ("POST", "/reservation-moves", {"moves": [{"reference": "ABSENT"}]}, "auth-check")):
                a.expect(401, method, path, value, credential, key, "unauthenticated")
        a.expect(401, "POST", "/auth/login", {"email": "ada@verifier.invalid", "password": PASSWORD + "!"}, code="unauthenticated")
        signup = {"email": "new@verifier.invalid", "password": PASSWORD, "display_name": "New", "ignored": []}
        new = a.expect(201, "POST", "/auth/signup", signup)
        a.expect(409, "POST", "/auth/signup", signup, code="email_taken")
        a.expect(422, "POST", "/auth/signup", {**signup, "email": "short@verifier.invalid", "password": PASSWORD[:7]}, code="validation_failed")
        a.expect(422, "POST", "/auth/signup", {**signup, "email": "invalid"}, code="validation_failed")
        a.expect(400, "POST", "/auth/signup", {**signup, "email": 7}, code="malformed_request")
        second = a.login()
        a.expect(200, "GET", "/reservations", token=token)
        a.expect(200, "GET", "/reservations", token=second)
        a.reset(self.fx)
        for old in (token, second, new["token"]):
            a.expect(401, "GET", "/reservations", token=old, code="unauthenticated")
        check(a.reservations(a.login()) == [], "reset retained bookings")

    def ignored_numeric_receipt_boundaries(self):
        a, token = self.fresh()
        # Valid JSON exponent syntax must remain harmless in unknown fields.
        raw_fixture = encode_json(self.fx)[:-1].encode() + b',"ignored":1e309}'
        a.expect(204, "POST", "/_test/reset", raw=raw_fixture)
        token = a.login()
        raw = encode_json(body())[:-1].encode() + b',"ignored":1e309}'
        created = a.expect(201, "POST", "/reservations", token=token, key="huge-number", raw=raw)
        check(a.expect(200, "POST", "/reservations", token=token, key="huge-number", raw=raw) == created,
              "large ignored number receipt replay changed")
        changed = raw.replace(b"1e309", b"1e310")
        a.expect(409, "POST", "/reservations", token=token, key="huge-number", raw=changed, code="idempotency_key_reuse")
        snapshot = a.expect(200, "GET", "/_test/export")
        self.dest.expect(204, "POST", "/_test/import", snapshot)
        check(self.dest.expect(200, "POST", "/reservations", token=token, key="huge-number", raw=raw) == created,
              "large-number receipt transfer changed")
        self.dest.expect(409, "POST", "/reservations", token=token, key="huge-number", raw=changed,
                         code="idempotency_key_reuse")
        for invalid in (b'{"ignored":NaN}', b'{"ignored":Infinity}'):
            a.expect(400, "POST", "/_test/reset", raw=invalid, code="malformed_request")

    def calendar_extremes(self):
        fx = fixture("UTC", slot=1440)
        a, token = self.fresh(fx)
        for day in ("0001-01-01", "9999-12-31"):
            expected = [{"starts_at_local": day + "T18:00", "starts_at": day + "T18:00:00+00:00",
                         "available_table_ids": ["z", "a", "m"]}]
            check(a.availability(day) == expected, "calendar boundary availability: " + day)
            reservation = a.book(token, body(day=day), "calendar-" + day)
            check(reservation["starts_at_local"] == day + "T18:00", "calendar boundary booking changed date")

    def numeric_equivalence_and_precision(self):
        vectors = [("1e309", "10e308", "1e310"),
                   ("1e-1000", "10e-1001", "0"),
                   ("1.0000000000000000001", "1.00000000000000000010", "1.0"),
                   ("9007199254740993.0", "90071992547409930e-1", "9007199254740992.0")]
        for i, (first, equivalent, different) in enumerate(vectors):
            a, token = self.fresh()
            def raw(number):
                return encode_json(body())[:-1].encode() + b',"ignored":{"numeric":' + number.encode() + b'}}'
            made = a.expect(201, "POST", "/reservations", token=token, key="exact", raw=raw(first))
            check(a.expect(200, "POST", "/reservations", token=token, key="exact", raw=raw(equivalent)) == made,
                  "equivalent numeric encoding not a replay")
            a.expect(409, "POST", "/reservations", token=token, key="exact", raw=raw(different), code="idempotency_key_reuse")
            a.expect(200, "POST", "/reservations/" + made["reference"] + "/cancel", token=token)
            snapshot = a.expect(200, "GET", "/_test/export")
            self.dest.expect(204, "POST", "/_test/import", snapshot)
            check(self.dest.expect(200, "POST", "/reservations", token=token, key="exact", raw=raw(equivalent)) == made,
                  "import rounded numeric receipt or changed historical response")
            self.dest.expect(409, "POST", "/reservations", token=token, key="exact", raw=raw(different), code="idempotency_key_reuse")
            check(self.dest.reservations(token)[0]["status"] == "cancelled", "numeric replay resurrected reservation")
        a, token = self.fresh()
        first = a.book(token, {**body(), "party_size": Decimal("2.0"), "ignored": [False, 0]}, "integer-value")
        check(a.book(token, {**body(), "party_size": 2, "ignored": [False, 0]}, "integer-value", 200) == first,
              "integer-valued numeric representation not equivalent")
        a.book(token, {**body(), "party_size": 2, "ignored": [0, False]}, "integer-value", 409, "idempotency_key_reuse")
        fx = fixture()
        fx["restaurants"][0]["tables"][0]["capacity"] = Decimal("1e400")
        a, token = self.fresh(fx)
        giant = a.book(token, body(party=Decimal("1e400")), "giant-party")
        check(giant["party_size"] == Decimal("1e400"), "giant valid party value changed")
        query_party = 10 ** 400
        check(a.availability(party=query_party) == oracle(fx, DAY, query_party, [giant]), "giant capacity/party oracle")
        a.book(token, body("z", at="19:30", party=query_party + 1), "over-capacity", 422, "party_exceeds_capacity")
        a.book(token, body("m", party=Decimal("1e-1000")), "fractional-tiny", 422, "validation_failed")
        fx = fixture(slot=Decimal("1e1000"))
        a, token = self.fresh(fx)
        check(len(a.availability()) == 1, "giant positive slot should yield exactly opening slot")
        a.book(token, body(), "giant-grid")
        a.book(token, body("m", at="18:30"), "off-giant-grid", 422, "not_on_slot_grid")
        fx = fixture(duration=Decimal("1e1000"))
        a, token = self.fresh(fx)
        check(a.availability() == [], "giant duration cannot fit opening window")
        a.book(token, body(), "duration-outside", 422, "outside_opening_hours")

    def terminal_zone_instants(self):
        for zone, day, opens, closes, duration, at in (
                ("America/New_York", "9999-12-31", "21:00", "23:59", 60, "22:00"),
                ("Etc/GMT-8", "0001-01-01", "00:00", "04:00", 90, "00:00")):
            fx = fixture(zone, opens, closes, duration=duration)
            a, token = self.fresh(fx)
            start = dt.datetime.fromisoformat(day + "T" + opens)
            close = dt.datetime.fromisoformat(day + "T" + closes)
            expected = []
            first_minute = start.hour * 60 + start.minute
            last_minute = close.hour * 60 + close.minute - duration
            midnight = dt.datetime.fromisoformat(day + "T00:00")
            for minute in range(first_minute, last_minute + 1, 30):
                candidate = midnight + dt.timedelta(minutes=minute)
                expected.append({"starts_at_local": candidate.isoformat(timespec="minutes"),
                                 "starts_at": candidate.replace(tzinfo=ZoneInfo(zone)).isoformat(),
                                 "available_table_ids": ["z", "a", "m"]})
            check(a.availability(day) == expected, "terminal zone availability or offset mismatch")
            made = a.book(token, body(at=at, day=day), "terminal-zone")
            check(instant_seconds(made["ends_at"]) - instant_seconds(made["starts_at"]) == duration * 60,
                  "terminal zone elapsed duration incorrect")
            a.book(token, body(at="22:30" if zone == "America/New_York" else "00:30", day=day),
                   "terminal-overlap", 409, "table_unavailable")
            rows = a.reservations(token)
            snapshot = a.expect(200, "GET", "/_test/export")
            self.dest.expect(204, "POST", "/_test/import", snapshot)
            check(self.dest.reservations(token) == rows, "terminal zone import changed reservation")
            check(self.dest.book(token, body(at=at, day=day), "terminal-zone", 200) == made,
                  "terminal zone receipt lost after import")

    def offset_ordering_and_amendment(self):
        fx = fixture()
        other = copy.deepcopy(fx["restaurants"][0])
        other.update(id="ny", timezone="America/New_York")
        fx["restaurants"].append(other)
        a, token = self.fresh(fx)
        items = [a.book(token, body(at="18:30", restaurant="ny"), "ny"),
                 a.book(token, body("m", at="21:00"), "berlin-late"),
                 a.book(token, body(at="19:00"), "berlin-early")]
        rows = a.reservations(token)
        check([r["reference"] for r in rows] == [r["reference"] for r in items], "offset-aware list ordering")
        a.expect(200, "PATCH", "/reservations/" + items[2]["reference"], {"starts_at_local": DAY + "T21:30"}, token)
        check([r["reference"] for r in a.reservations(token)] == [items[0]["reference"], items[2]["reference"], items[1]["reference"]],
              "amendment failed to update absolute list order")

    def cancelled_after_cutoff_temporal(self):
        zone = next(z for z in ("UTC", "Etc/GMT+6") if dt.datetime.now(ZoneInfo(z)).hour != 23)
        fx = fixture(zone, "00:00", "23:59", slot=1, duration=1)
        fx["restaurants"][0]["cancellation_cutoff_minutes"] = 0
        a, token = self.fresh(fx)
        now = dt.datetime.now(ZoneInfo(zone))
        target = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
        if (target - now).total_seconds() < 15:
            target += dt.timedelta(minutes=1)
        value = {**body(), "starts_at_local": target.replace(tzinfo=None).isoformat(timespec="minutes")}
        original = a.book(token, value, "temporal-original")
        cancelled = a.expect(200, "POST", "/reservations/" + original["reference"] + "/cancel", token=token)
        replacement = a.book(token, value, "temporal-replacement")
        while dt.datetime.now(UTC) <= target.astimezone(UTC):
            time.sleep(.2)
        check(a.expect(200, "POST", "/reservations/" + original["reference"] + "/cancel", token=token) == cancelled,
              "repeat cancellation after cutoff failed or changed state")
        a.expect(409, "PATCH", "/reservations/" + replacement["reference"], {"starts_at_local": DAY + "T18:00"},
                 token, code="cutoff_passed")
        check(a.expect(200, "GET", "/reservations/" + replacement["reference"], token=token) == replacement,
              "repeat cancellation freed or modified replacement reservation")

    def availability_oracle(self):
        for slot, duration in ((30, 90), (17, 43), (45, 120)):
            fx = fixture(opens="18:10", closes="23:10", slot=slot, duration=duration)
            a, token = self.fresh(fx)
            for party in (1, 2, 3, 4, 5, 6, 7):
                check(a.availability(party=party) == oracle(fx, DAY, party), "empty availability oracle mismatch")
            start = oracle(fx, DAY, 2)[1]["starts_at_local"]
            reservation = a.book(token, {**body(), "starts_at_local": start})
            for party in (1, 3, 7):
                check(a.availability(party=party) == oracle(fx, DAY, party, [reservation]), "occupied availability oracle mismatch")
            a.expect(200, "POST", "/reservations/" + reservation["reference"] + "/cancel", token=token)
            check(a.availability() == oracle(fx, DAY, 2), "cancel did not release occupancy")
        fx = fixture()
        fx["restaurants"][0]["opening_hours"] = []
        a, _ = self.fresh(fx)
        check(a.availability() == [], "closed day has slots")

    def validation(self):
        a, token = self.fresh()
        for party in (False, True, "2", 0, -1, 1.25, None, [], {}):
            a.book(token, {**body(), "party_size": party}, "party", 422, "validation_failed")
        for local in ("2080-06-06T18:00Z", "2080-06-06T18:00:00", "2080-06-06T18:00+02:00", "2080-02-30T18:00", "2080-6-6T18:00"):
            a.book(token, {**body(), "starts_at_local": local}, "local", 422, "validation_failed")
        for field in ("restaurant_id", "table_id", "starts_at_local"):
            a.book(token, {**body(), field: 123}, "type", 400, "malformed_request")
            absent = body()
            del absent[field]
            a.book(token, absent, "missing", 422, "validation_failed")
        a.expect(400, "POST", "/reservations", token=token, key="json", raw=b"{", code="malformed_request")
        for key in (None, ""):
            a.book(token, body(), key, 400, "missing_idempotency_key")
        a.book(token, body(), "x" * 256, 422, "validation_failed")
        a.book(token, body(), "x" * 255)
        a.book(token, body("m"), "y")
        for value in ("4.0", "1e9", "+4", "-1", "0", "true", ""):
            q = urllib.parse.urlencode({"restaurant_id": "r", "date": DAY, "party_size": value})
            a.expect(422, "GET", "/availability?" + q, code="validation_failed")
        for query in ("restaurant_id=r&date=" + DAY, "restaurant_id=r&party_size=2", "date=" + DAY + "&party_size=2",
                      "restaurant_id=r&date=2080-02-30&party_size=2"):
            a.expect(422, "GET", "/availability?" + query, code="validation_failed")

    def booking_boundaries_privacy(self):
        a, token = self.fresh()
        a.book(token, body(at="18:01"), "grid", 422, "not_on_slot_grid")
        a.book(token, body(at="17:30"), "hours", 422, "outside_opening_hours")
        a.book(token, body(at="22:00"), "end", 422, "outside_opening_hours")
        a.book(token, body("a", party=3), "capacity", 422, "party_exceeds_capacity")
        a.book(token, body("absent"), "missing", 404, "not_found")
        first = a.book(token, {**body(), "unknown": {"value": True}}, "first")
        second = a.book(token, body(at="19:30"), "touching")
        a.book(token, body(at="19:00"), "overlap", 409, "table_unavailable")
        other = a.login("bob")
        for method, suffix, value in (("GET", "", None), ("POST", "/cancel", None), ("PATCH", "", {"party_size": 1})):
            a.expect(404, method, "/reservations/" + first["reference"] + suffix, value, other, code="not_found")
        rows = a.reservations(token)
        check([x["reference"] for x in rows] == [second["reference"], first["reference"]], "descending reservation order")
        a.expect(200, "POST", "/reservations/" + first["reference"] + "/cancel", token=token)
        a.expect(200, "POST", "/reservations/" + first["reference"] + "/cancel", token=token)
        a.expect(409, "PATCH", "/reservations/" + first["reference"], {}, token, code="reservation_cancelled")
        a.book(token, body(), "freed")
        check(len(a.reservations(token)) == 3, "cancelled record omitted or duplicate booking")

    def receipt_semantics(self):
        a, token = self.fresh()
        request = {**body(), "ignored": {"a": 1, "b": 2}}
        original = a.book(token, request, "receipt")
        raw = json.dumps(dict(reversed(list(request.items()))), indent=3).encode()
        replay = a.expect(200, "POST", "/reservations", token=token, key="receipt", raw=raw)
        check(replay == original, "JSON-value replay differs")
        a.book(token, {**request, "party_size": False}, "receipt", 409, "idempotency_key_reuse")
        a.book(token, {**request, "restaurant_id": "absent"}, "receipt", 409, "idempotency_key_reuse")
        a.book(token, {**request, "ignored": 3}, "receipt", 409, "idempotency_key_reuse")
        a.expect(200, "PATCH", "/reservations/" + original["reference"], {"table_id": "m"}, token)
        check(a.book(token, request, "receipt", 200) == original, "amendment changed stored receipt")
        a.expect(200, "POST", "/reservations/" + original["reference"] + "/cancel", token=token)
        check(a.book(token, request, "receipt", 200) == original, "cancellation changed stored receipt")
        other = a.login("bob")
        a.book(other, request, "receipt")
        a.book(token, body("m", at="18:01"), "failed", 422, "not_on_slot_grid")
        a.book(token, body("m"), "failed")
        a.book(token, body("m"), "conflict", 409, "table_unavailable")
        a.book(token, body("a"), "conflict")
        # Same method, key and JSON body on another path is a fresh operation.
        confirmed = next(x for x in a.reservations(token) if x["status"] == "confirmed")
        a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": confirmed["reference"]}]}, token, "receipt")
        hybrid = {**body("m", at="19:30"), "moves": [{"reference": confirmed["reference"]}]}
        hybrid_create = a.book(token, hybrid, "same-body-cross-path")
        hybrid_move = a.expect(201, "POST", "/reservation-moves", hybrid, token, "same-body-cross-path")
        check(a.book(token, hybrid, "same-body-cross-path", 200) == hybrid_create, "cross-path create receipt overwritten")
        check(a.expect(200, "POST", "/reservation-moves", hybrid, token, "same-body-cross-path") == hybrid_move,
              "cross-path batch receipt overwritten")

    def amendments_atomic_cutoff(self):
        a, token = self.fresh()
        first = a.book(token, body(), "first")
        second = a.book(token, body("m"), "second")
        path = "/reservations/" + first["reference"]
        before = a.reservations(token)
        a.expect(409, "PATCH", path, {"table_id": "m"}, token, code="table_unavailable")
        check(a.reservations(token) == before, "failed amendment changed records")
        check(a.availability() == oracle(self.fx, DAY, 2, before), "failed amendment changed occupancy")
        changed = a.expect(200, "PATCH", path, {"table_id": "a", "party_size": 1, "ignored": True}, token)
        for field in ("reference", "reservation_id", "created_at"):
            check(changed[field] == first[field], "amendment changed identity/timestamp")
        a.book(token, body(), "released")
        # Historical creation is valid; current start controls cancellation/amendment cutoff.
        past = a.book(token, body("a", day="2000-01-01"), "past")
        for method, suffix, value in (("POST", "/cancel", None), ("PATCH", "", {"party_size": 999})):
            a.expect(409, method, "/reservations/" + past["reference"] + suffix, value, token, code="cutoff_passed")
        check(a.expect(200, "GET", "/reservations/" + past["reference"], token=token) == past,
              "cutoff rejection modified reservation")
        # Book inside cutoff and outside cutoff using UTC restaurant and minute precision.
        fx = fixture(zone="UTC", opens="00:00", closes="23:59", slot=1, duration=1)
        fx["restaurants"][0]["cancellation_cutoff_minutes"] = 60
        a, token = self.fresh(fx)
        now = dt.datetime.now(UTC)
        for delta, expected in ((30, 409), (90, 200)):
            local = (now + dt.timedelta(minutes=delta)).strftime("%Y-%m-%dT%H:%M")
            item = a.book(token, {**body(), "starts_at_local": local}, "cutoff-" + str(delta))
            a.expect(expected, "POST", "/reservations/" + item["reference"] + "/cancel", token=token,
                     code="cutoff_passed" if expected == 409 else None)

    def dst_oracle(self):
        for zone, spring, fall, repeated, first_offset, after_offset in (
                ("Europe/Berlin", "2026-03-29", "2026-10-25", "02:30", "+02:00", "+01:00"),
                ("America/New_York", "2026-03-08", "2026-11-01", "01:30", "-04:00", "-05:00")):
            fx = fixture(zone, "00:00", "06:00")
            a, token = self.fresh(fx)
            for date in (spring, fall):
                check(a.availability(date) == oracle(fx, date, 2), "DST availability oracle: " + zone + " " + date)
            a.book(token, body(day=spring, at="02:30"), "gap", 422, "invalid_local_time")
            reservation = a.book(token, body(day=fall, at=repeated), "fold")
            start = resolve(fall + "T" + repeated, zone)
            end = (start.astimezone(UTC) + dt.timedelta(minutes=90)).astimezone(ZoneInfo(zone))
            check(reservation["starts_at"] == start.isoformat(), "repeated time did not resolve first occurrence")
            check(reservation["ends_at"] == end.isoformat(), "duration not absolute across fallback")
            check(reservation["starts_at"].endswith(first_offset) and reservation["ends_at"].endswith(after_offset),
                  "fallback offsets incorrect")
            check(a.availability(fall) == oracle(fx, fall, 2, [reservation]), "DST occupancy oracle")
            spring_res = a.book(token, body("m", "01:30", spring), "spring-absolute")
            check((dt.datetime.fromisoformat(spring_res["ends_at"]).astimezone(UTC)
                   - dt.datetime.fromisoformat(spring_res["starts_at"]).astimezone(UTC)).total_seconds() == 5400,
                  "spring duration not absolute")

    def dst_closing_instant_boundaries(self):
        for zone, day, closes, rejected in (
                ("Europe/Berlin", "2026-03-29", "03:30", "01:30"),
                ("America/New_York", "2026-03-08", "03:30", "01:30"),
                ("Europe/Berlin", "2026-10-25", "02:30", "01:30"),
                ("America/New_York", "2026-11-01", "01:30", "00:30")):
            fx = fixture(zone, "00:00", closes)
            a, token = self.fresh(fx)
            expected = oracle(fx, day, 2)
            check(a.availability(day) == expected, "DST duration fitting did not use resolved closing instant")
            made = a.book(token, {**body(), "starts_at_local": expected[0]["starts_at_local"]}, "closing-fit")
            closing = resolve(day + "T" + closes, zone).astimezone(UTC)
            check(dt.datetime.fromisoformat(made["ends_at"]).astimezone(UTC) <= closing, "booking exceeds resolved close")
            a.book(token, body("m", at=rejected, day=day), "closing-outside", 422, "outside_opening_hours")

    def moves_atomic_precedence(self):
        a, token = self.fresh()
        initial = [a.book(token, body(t), "initial-" + t) for t in ("z", "a", "m")]
        request = {"moves": [{"reference": r["reference"], "table_id": t}
                             for r, t in zip(initial, ("a", "m", "z"))]}
        response = a.expect(201, "POST", "/reservation-moves", request, token, "cycle")
        check([x["table_id"] for x in response["reservations"]] == ["a", "m", "z"], "cycle order/state")
        for before, after in zip(initial, response["reservations"]):
            for field in ("reservation_id", "reference", "created_at", "starts_at", "ends_at"):
                check(before[field] == after[field], "batch changed retained field " + field)
        check(a.expect(200, "POST", "/reservation-moves", request, token, "cycle") == response, "batch receipt changed")
        before = a.reservations(token)
        bad = {"moves": [{"reference": initial[0]["reference"], "table_id": "z"},
                         {"reference": initial[1]["reference"], "party_size": 999}]}
        a.expect(422, "POST", "/reservation-moves", bad, token, "failed-batch", "party_exceeds_capacity")
        check(a.reservations(token) == before, "failed batch partial records")
        check(a.availability() == oracle(self.fx, DAY, 2, before), "failed batch partial occupancy")
        a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": initial[0]["reference"]}]}, token, "failed-batch")
        conflict = {"moves": [{"reference": initial[0]["reference"], "table_id": "z"}]}
        a.expect(409, "POST", "/reservation-moves", conflict, token, "conflict", "table_unavailable")
        unchanged = {"moves": [{"reference": initial[0]["reference"], "table_id": "m"},
                               {"reference": initial[1]["reference"]}]}
        a.expect(409, "POST", "/reservation-moves", unchanged, token, "unchanged-occupancy", "table_unavailable")
        check(a.reservations(token) == before, "unchanged listed booking lost occupancy")
        precedence = {"moves": [{"reference": initial[0]["reference"], "party_size": 999},
                                {"reference": initial[1]["reference"], "starts_at_local": DAY + "T18:01"}]}
        a.expect(422, "POST", "/reservation-moves", precedence, token, "prec", "party_exceeds_capacity")
        a.expect(422, "POST", "/reservation-moves", {"moves": list(reversed(precedence["moves"]))},
                 token, "prec-reversed", "not_on_slot_grid")
        a.expect(409, "POST", "/reservation-moves", {"moves": []}, token, "cycle", "idempotency_key_reuse")
        for value in (None, [], {}, "bad"):
            a.expect(422, "POST", "/reservation-moves", {"moves": value}, token, "invalid", "validation_failed")
        a.expect(422, "POST", "/reservation-moves", {}, token, "missing-moves", "validation_failed")
        for moves in ([], [{"reference": initial[0]["reference"]}] * 2,
                      [{"reference": 7}], [{}], [{"reference": "ABSENT"}] * 9):
            a.expect(422, "POST", "/reservation-moves", {"moves": moves}, token, "shape", "validation_failed")
        a.expect(404, "POST", "/reservation-moves", {"moves": [{"reference": "ABSENT"}]}, token, "unknown", "not_found")
        a.expect(404, "POST", "/reservation-moves", request, a.login("bob"), "foreign", "not_found")
        no_op = a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": r["reference"]} for r in initial]}, token, "noop")
        current = {r["reference"]: r for r in before}
        check(no_op["reservations"] == [current[r["reference"]] for r in initial], "no-op changed values")
        reversed_array = {"moves": [{"reference": r["reference"]} for r in reversed(initial)]}
        a.expect(409, "POST", "/reservation-moves", reversed_array, token, "noop", "idempotency_key_reuse")
        a.expect(200, "POST", "/reservations/" + initial[0]["reference"] + "/cancel", token=token)
        check(a.expect(200, "POST", "/reservation-moves", request, token, "cycle") == response,
              "batch receipt changed after cancellation")
        a.expect(409, "POST", "/reservation-moves", {"moves": [{"reference": initial[0]["reference"]}]},
                 token, "cancelled", "reservation_cancelled")

    def moves_eight_and_restaurant_scope(self):
        fx = fixture()
        fx["restaurants"][0]["tables"] = [{"id": "t" + str(i), "label": str(i), "capacity": 4} for i in range(8)]
        second = copy.deepcopy(fx["restaurants"][0])
        second["id"] = "other"
        second["tables"] = [{"id": "elsewhere", "label": "Other", "capacity": 4}]
        fx["restaurants"].append(second)
        a, token = self.fresh(fx)
        items = [a.book(token, body("t" + str(i)), "eight-" + str(i)) for i in range(8)]
        moves = {"moves": [{"reference": r["reference"], "table_id": "t" + str((i + 1) % 8)} for i, r in enumerate(items)]}
        changed = a.expect(201, "POST", "/reservation-moves", moves, token, "eight")
        check(len(changed["reservations"]) == 8, "eight moves not all returned")
        a.book(token, body("elsewhere"), "foreign-table", 404, "not_found")
        other = a.book(token, body("elsewhere", restaurant="other"), "other")
        before = a.reservations(token)
        a.expect(422, "POST", "/reservation-moves", {"moves": [{"reference": items[0]["reference"]},
                                                               {"reference": other["reference"]}]}, token,
                 "mixed", "validation_failed")
        check(a.reservations(token) == before, "mixed restaurant request changed state")

    def duplicate_table_ids_and_short_seed_password(self):
        fx = fixture()
        short = PASSWORD[:3]
        fx["users"][1]["password"] = short
        other = copy.deepcopy(fx["restaurants"][0])
        other["id"] = "other"
        other["name"] = "Shared table identifiers"
        fx["restaurants"].append(other)
        a, token = self.fresh(fx)
        short_token = a.login("bob", short)
        a.expect(200, "GET", "/reservations", token=short_token)
        first = a.book(token, body(), "namespace-r")
        other_fixture = copy.deepcopy(fx)
        other_fixture["restaurants"] = [other]
        query = "/availability?restaurant_id=other&date=" + DAY + "&party_size=2"
        available = a.expect(200, "GET", query)["slots"]
        check(available == oracle(other_fixture, DAY, 2, [first]), "other restaurant shares occupancy by table ID")
        check(available[0]["available_table_ids"] == ["z", "a", "m"], "first restaurant blocked other restaurant")
        second = a.book(token, body(restaurant="other"), "namespace-other")
        check(first["reference"] != second["reference"], "duplicate generated references across restaurant namespaces")
        before = a.reservations(token)
        a.expect(422, "POST", "/reservation-moves", {"moves": [{"reference": first["reference"]},
                                                               {"reference": second["reference"]}]},
                 token, "namespace-mixed", "validation_failed")
        check(a.reservations(token) == before, "mixed namespace batch changed records")
        snapshot = a.expect(200, "GET", "/_test/export")
        d = self.dest
        d.expect(204, "POST", "/_test/import", snapshot)
        check(d.reservations(token) == before, "import lost restaurant/table namespace identity")
        check(d.reservations(short_token) == [], "import changed short seeded owner's state")
        check(d.reservations(d.login("bob", short)) == [], "import imposed signup password length on seeded account")
        check(d.book(token, body(), "namespace-r", 200) == first, "import lost first namespace receipt")
        check(d.book(token, body(restaurant="other"), "namespace-other", 200) == second, "import lost second namespace receipt")
        d.expect(200, "POST", "/reservations/" + first["reference"] + "/cancel", token=token)
        check(d.expect(200, "GET", query)["slots"] == oracle(other_fixture, DAY, 2, [second]),
              "cancelling one restaurant changed another restaurant occupancy")
        check(d.availability() == oracle(fx, DAY, 2), "cancel did not free selected restaurant namespace")

    def seed_ids_and_batch_cutoff(self):
        fx = fixture()
        fx["users"][0]["id"] = "u" * 64
        fx["restaurants"][0]["tables"][0]["id"] = "t" * 64
        seeded = {**body("t" * 64), "id": "s" * 64, "reference": "SEED01", "user_id": "u" * 64}
        fx["reservations"] = [seeded]
        a, token = self.fresh(fx)
        rows = a.reservations(token)
        check(len(rows) == 1 and rows[0]["reservation_id"] == "s" * 64 and rows[0]["reference"] == "SEED01",
              "seeded identity or 64-character ID lost")
        check(a.expect(200, "GET", "/reservations/SEED01", token=token) == rows[0], "seeded reference lookup")
        check(a.availability() == oracle(fx, DAY, 2, rows), "seeded occupancy missing")
        a.book(token, body("t" * 64), "seed-overlap", 409, "table_unavailable")
        new = a.book(token, body("t" * 64, at="19:30"), "seed-boundary")
        overlap = {"moves": [{"reference": "SEED01", "table_id": "m"},
                              {"reference": new["reference"], "table_id": "m", "starts_at_local": DAY + "T18:30"}]}
        before = a.reservations(token)
        a.expect(409, "POST", "/reservation-moves", overlap, token, "result-overlap", "table_unavailable")
        check(a.reservations(token) == before, "resulting overlap partially committed")
        past = a.book(token, body("a", day="2000-01-01"), "historical")
        request = {"moves": [{"reference": past["reference"], "party_size": 999},
                             {"reference": new["reference"], "table_id": "m"}]}
        before = a.reservations(token)
        a.expect(409, "POST", "/reservation-moves", request, token, "cutoff-batch", "cutoff_passed")
        check(a.reservations(token) == before, "batch cutoff changed state")
        earlier = {"moves": [{"reference": new["reference"], "party_size": 999},
                             {"reference": past["reference"], "party_size": 999}]}
        a.expect(422, "POST", "/reservation-moves", earlier, token, "earlier-before-cutoff", "party_exceeds_capacity")
        a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": new["reference"]}]}, token, "cutoff-batch")

    def patch_and_batch_field_validation(self):
        a, token = self.fresh()
        item = a.book(token, body(), "validation-seed")
        path = "/reservations/" + item["reference"]
        initial = a.reservations(token)
        invalid = [("party_size", False, 422, "validation_failed"),
                   ("party_size", "2", 422, "validation_failed"),
                   ("party_size", 0, 422, "validation_failed"),
                   ("party_size", 99, 422, "party_exceeds_capacity"),
                   ("table_id", 7, 400, "malformed_request"),
                   ("table_id", "absent", 404, "not_found"),
                   ("starts_at_local", 7, 400, "malformed_request"),
                   ("starts_at_local", DAY + "T18:00Z", 422, "validation_failed"),
                   ("starts_at_local", DAY + "T18:01", 422, "not_on_slot_grid"),
                   ("starts_at_local", DAY + "T22:00", 422, "outside_opening_hours")]
        for i, (field, value, status, code) in enumerate(invalid):
            a.expect(status, "PATCH", path, {field: value}, token, code=code)
            a.expect(status, "POST", "/reservation-moves", {"moves": [{"reference": item["reference"], field: value}]},
                     token, "field-" + str(i), code)
            check(a.reservations(token) == initial, "invalid field mutation changed records")
            check(a.availability() == oracle(self.fx, DAY, 2, initial), "invalid field mutation changed occupancy")
        noop = {"moves": [{"reference": item["reference"], "ignored": True}]}
        for key in (None, ""):
            a.expect(400, "POST", "/reservation-moves", noop, token, key, "missing_idempotency_key")
        a.expect(422, "POST", "/reservation-moves", noop, token, "x" * 256, "validation_failed")
        a.expect(201, "POST", "/reservation-moves", noop, token, "x" * 255)
        a.expect(201, "POST", "/reservation-moves", noop, token, "x")
        # Both amendment interfaces must apply the same skipped-time rule.
        fx = fixture("Europe/Berlin", "00:00", "06:00")
        fx["restaurants"][0]["cancellation_cutoff_minutes"] = 0
        a, token = self.fresh(fx)
        future = a.book(token, body(at="01:00", day=DAY), "dst-source")
        changes = {"starts_at_local": "2026-03-29T02:30"}
        a.expect(422, "PATCH", "/reservations/" + future["reference"], changes, token, code="invalid_local_time")
        a.expect(422, "POST", "/reservation-moves", {"moves": [{"reference": future["reference"], **changes}]},
                 token, "dst-move", "invalid_local_time")

    def parallel(self, functions):
        barrier = threading.Barrier(len(functions))
        def run(function):
            barrier.wait(timeout=15)
            return function()
        with ThreadPoolExecutor(max_workers=len(functions)) as pool:
            return list(pool.map(run, functions))

    def concurrency_identical_50(self):
        a, token = self.fresh()
        results = self.parallel([lambda: a.request("POST", "/reservations", body(), token, "same")] * 50)
        check(sorted(s for s, _ in results) == [200] * 49 + [201], "identical 50 requests not one 201 and 49 replays")
        check(all(v == results[0][1] for _, v in results), "concurrent identical responses differ")
        check(len(a.reservations(token)) == 1, "concurrent replay duplicated state")

    def concurrency_distinct_50(self):
        a, token = self.fresh()
        results = self.parallel([lambda i=i: a.request("POST", "/reservations", body(), token, "distinct-" + str(i))
                                 for i in range(50)])
        check(sorted(s for s, _ in results) == [201] + [409] * 49, "contention must admit exactly one booking")
        check(all(v["error"]["code"] == "table_unavailable" for s, v in results if s == 409), "wrong contention error")
        check(len(a.reservations(token)) == 1, "contention duplicated bookings")
        rejected = next(i for i, (s, _) in enumerate(results) if s == 409)
        a.book(token, body("m"), "distinct-" + str(rejected))

    def concurrency_changed_key_50(self):
        a, token = self.fresh()
        requests = [body("z" if i % 2 else "m") for i in range(50)]
        results = self.parallel([lambda request=request: a.request("POST", "/reservations", request, token, "contended-key")
                                 for request in requests])
        winners = [v for s, v in results if s == 201]
        check(len(winners) == 1, "changed-key race has multiple first uses")
        winner = winners[0]
        for request, (s, value) in zip(requests, results):
            if request["table_id"] == winner["table_id"]:
                check(s in (200, 201) and value == winner, "matching concurrent receipt differs")
            else:
                check(s == 409 and value["error"]["code"] == "idempotency_key_reuse", "changed concurrent receipt did not conflict")
        check(len(a.reservations(token)) == 1, "changed-key race created extra booking")

    def concurrency_batch_snapshot(self):
        a, token = self.fresh()
        bookings = [a.book(token, body(t), "seed-" + t) for t in ("z", "a")]
        swap = {"moves": [{"reference": bookings[0]["reference"], "table_id": "a"},
                          {"reference": bookings[1]["reference"], "table_id": "z"}]}
        # Coordinated writer/replays + readers: each read must be wholly before or after swap.
        results = self.parallel([lambda: a.request("POST", "/reservation-moves", swap, token, "swap")] * 25
                                + [lambda: a.request("GET", "/reservations", token=token)] * 25)
        writes = results[:25]
        check(sorted(s for s, _ in writes) == [200] * 24 + [201], "batch concurrency receipt semantics")
        check(all(v == writes[0][1] for _, v in writes), "batch concurrent responses differ")
        before = {r["reference"]: r["table_id"] for r in bookings}
        after = {bookings[0]["reference"]: "a", bookings[1]["reference"]: "z"}
        for status, result in results[25:]:
            check(status == 200, "concurrent reader failed")
            got = {r["reference"]: r["table_id"] for r in result["reservations"]}
            check(got in (before, after), "reader observed partial atomic batch")
        check({r["reference"]: r["table_id"] for r in a.reservations(token)} == after, "batch final state")

    def concurrency_signup_and_users(self):
        a, token = self.fresh()
        signup = {"email": "racing@verifier.invalid", "password": PASSWORD[:8], "display_name": "Racing"}
        results = self.parallel([lambda: a.request("POST", "/auth/signup", signup)] * 20)
        check(sorted(s for s, _ in results) == [201] + [409] * 19, "duplicate signup race created multiple users")
        check(all(v["error"]["code"] == "email_taken" for s, v in results if s == 409), "duplicate signup race error")
        a.expect(200, "POST", "/auth/login", {"email": signup["email"], "password": signup["password"]})
        other = a.login("bob")
        results = self.parallel([lambda: a.request("POST", "/reservations", body(), token, "owner-key"),
                                 lambda: a.request("POST", "/reservations", body(), other, "owner-key")])
        check(sorted(s for s, _ in results) == [201, 409], "cross-owner table contention")
        check(len(a.reservations(token)) + len(a.reservations(other)) == 1, "cross-owner duplicate occupancy")

    def export_atomic_batch(self):
        a, token = self.fresh()
        old = [a.book(token, body(t), "export-seed-" + t) for t in ("z", "a")]
        swap = {"moves": [{"reference": old[0]["reference"], "table_id": "a"},
                          {"reference": old[1]["reference"], "table_id": "z"}]}
        exported_before = a.expect(200, "GET", "/_test/export")
        check(a.reservations(token) == sorted(old, key=lambda x: x["starts_at"], reverse=True)
              or {r["reference"]: r for r in a.reservations(token)} == {r["reference"]: r for r in old},
              "read-only export changed records")
        results = self.parallel([lambda: a.request("POST", "/reservation-moves", swap, token, "snapshot-swap")]
                                + [lambda: a.request("GET", "/_test/export")] * 20)
        check(results[0][0] == 201, "snapshot-racing swap failed")
        after = results[0][1]
        old_map = {r["reference"]: r["table_id"] for r in old}
        new_map = {r["reference"]: r["table_id"] for r in after["reservations"]}
        for status, snapshot in results[1:]:
            check(status == 200, "concurrent export failed")
            self.dest.expect(204, "POST", "/_test/import", snapshot)
            records = self.dest.reservations(token)
            mapping = {r["reference"]: r["table_id"] for r in records}
            check(mapping in (old_map, new_map), "snapshot contains torn batch records")
            replay_status, replay = self.dest.request("POST", "/reservation-moves", swap, token, "snapshot-swap")
            check(replay_status == (201 if mapping == old_map else 200), "snapshot tore receipt from batch effect")
            check(replay == after, "snapshot batch receipt lost original values")
        self.dest.expect(204, "POST", "/_test/import", exported_before)
        check({r["reference"]: r["table_id"] for r in self.dest.reservations(token)} == old_map,
              "old export mutated after source swap")

    def control_replacement_races(self):
        a, token = self.fresh()
        old = a.book(token, body(), "old")
        replacement = fixture()
        replacement["users"] = [{"id": "fresh", "email": "fresh@verifier.invalid", "password": PASSWORD, "display_name": "Fresh"}]
        replacement["restaurants"][0]["name"] = "Replacement generation"
        results = self.parallel([lambda: a.request("POST", "/_test/reset", replacement)]
                                + [lambda i=i: a.request("POST", "/reservations", body("m", at="19:30"), token, "racing-" + str(i))
                                   for i in range(20)])
        check(results[0][0] == 204, "racing reset failed")
        check(all(s in (201, 409, 401) for s, _ in results[1:]), "racing reset write status cannot serialize")
        a.expect(401, "GET", "/reservations", token=token, code="unauthenticated")
        a.expect(401, "POST", "/auth/login", {"email": "ada@verifier.invalid", "password": PASSWORD}, code="unauthenticated")
        fresh_token = a.login("fresh")
        check(a.reservations(fresh_token) == [], "reset left old records under new generation")
        check(a.expect(200, "GET", "/restaurants/r")["name"] == "Replacement generation", "reset retained old config")
        check(a.availability() == oracle(replacement, DAY, 2), "reset left old occupancy")
        a.book(fresh_token, body(), "old")
        # Import and authenticated writes similarly admit a complete serialization only.
        snapshot = a.expect(200, "GET", "/_test/export")
        a, token = self.fresh()
        results = self.parallel([lambda: a.request("POST", "/_test/import", snapshot)]
                                + [lambda i=i: a.request("POST", "/reservations", body("m"), token, "import-race-" + str(i))
                                   for i in range(20)])
        check(results[0][0] == 204, "racing import failed")
        check(all(s in (201, 409, 401) for s, _ in results[1:]), "racing import write status cannot serialize")
        a.expect(401, "GET", "/reservations", token=token, code="unauthenticated")
        records = a.reservations(fresh_token)
        check(len(records) == 1, "import mixed source and destination generations")
        check(a.availability() == oracle(replacement, DAY, 2, records), "import mixed occupancy generations")

    def patch_batch_cancel_replay_races(self):
        a, token = self.fresh()
        initial = a.book(token, body(), "original")
        batch = {"moves": [{"reference": initial["reference"], "table_id": "a"}]}
        results = self.parallel([lambda: a.request("PATCH", "/reservations/" + initial["reference"], {"table_id": "m"}, token),
                                 lambda: a.request("POST", "/reservation-moves", batch, token, "racing-batch")])
        check(results[0][0] == 200 and results[1][0] == 201, "PATCH/batch overlap failed")
        rows = a.reservations(token)
        check(len(rows) == 1 and rows[0]["table_id"] in ("a", "m"), "PATCH/batch state cannot serialize")
        check(a.availability() == oracle(self.fx, DAY, 2, rows), "PATCH/batch occupancy differs from state")
        results = self.parallel([lambda: a.request("POST", "/reservations/" + initial["reference"] + "/cancel", token=token)]
                                + [lambda: a.request("POST", "/reservations", body(), token, "original")] * 20)
        check(results[0][0] == 200 and all(s == 200 and r == initial for s, r in results[1:]),
              "cancel/replay race changed receipt")
        rows = a.reservations(token)
        check(len(rows) == 1 and rows[0]["status"] == "cancelled", "replay resurrected cancelled booking")
        check(a.availability() == oracle(self.fx, DAY, 2), "cancel/replay race retained occupancy")

    def legacy_direct_snapshot_continuity(self):
        check(self.legacy is not None, "legacy compatibility endpoint was not configured")
        source = self.legacy
        source.reset(fixture())
        token, second_token = source.login(), source.login()
        create_request = body()
        created = source.book(token, create_request, "legacy-create")
        moves = {"moves": [{"reference": created["reference"], "table_id": "m"}]}
        moved = source.expect(201, "POST", "/reservation-moves", moves, token, "legacy-batch")
        source.expect(200, "POST", "/reservations/" + created["reference"] + "/cancel", token=token)
        before = source.reservations(token)
        snapshot = source.expect(200, "GET", "/_test/export")
        if self.control:
            (self.control / "pause-legacy").write_text("ready\n")
            deadline = time.monotonic() + 30
            while not (self.control / "legacy-unavailable").exists():
                if time.monotonic() >= deadline:
                    raise OSError("legacy source-unavailable handshake failed")
                time.sleep(.1)
        d = self.dest
        d.reset(fixture())
        destination_token = d.login()
        d.book(destination_token, body("a"), "destination-only")
        d.expect(204, "POST", "/_test/import", snapshot)
        check(d.reservations(token) == before and d.reservations(second_token) == before,
              "legacy direct-object import changed records or sessions")
        check(d.reservations(d.login()) == before, "legacy import lost hashed-password login")
        d.expect(401, "GET", "/reservations", token=destination_token, code="unauthenticated")
        check(d.book(token, create_request, "legacy-create", 200) == created, "legacy original create receipt lost")
        check(d.expect(200, "POST", "/reservation-moves", moves, token, "legacy-batch") == moved,
              "legacy original batch receipt lost")
        check(d.reservations(token) == before, "legacy historical replay changed cancelled state")
        check(d.availability() == oracle(fixture(), DAY, 2), "legacy cancelled record occupied table")

    def control_receipt_erasure(self):
        a, old_token = self.fresh()
        old = a.book(old_token, body(), "reset-erased-create")
        a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": old["reference"]}]},
                 old_token, "reset-erased-batch")
        a.reset(fixture())
        token = a.login()
        a.expect(401, "GET", "/reservations", token=old_token, code="unauthenticated")
        created = a.book(token, body(), "reset-erased-create")
        a.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": created["reference"], "table_id": "m"}]},
                 token, "reset-erased-batch")
        wanted = a.expect(200, "GET", "/_test/export")
        d = self.dest
        d.reset(fixture())
        destination_token = d.login()
        destination_only = d.book(destination_token, body("a"), "destination-erased-create")
        d.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": destination_only["reference"]}]},
                 destination_token, "destination-erased-batch")
        d.expect(204, "POST", "/_test/import", wanted)
        d.expect(401, "GET", "/reservations", token=destination_token, code="unauthenticated")
        incoming = d.book(token, body(), "destination-erased-create")
        d.expect(201, "POST", "/reservation-moves", {"moves": [{"reference": incoming["reference"], "party_size": 1}]},
                 token, "destination-erased-batch")
        check(len(d.reservations(token)) == 2, "erased-key first uses duplicated or retained destination state")

    def snapshot_import_receipts(self):
        a, token = self.fresh()
        old_token = a.login()
        create_request = body()
        created = a.book(token, create_request, "create-receipt")
        batch_request = {"moves": [{"reference": created["reference"], "table_id": "m"}]}
        batch = a.expect(201, "POST", "/reservation-moves", batch_request, token, "batch-receipt")
        a.book(token, body("a", at="18:01"), "failed-key", 422, "not_on_slot_grid")
        rows = a.reservations(token)
        exported = a.expect(200, "GET", "/_test/export")
        check(exported.get("track") == "tablekeeper" and exported.get("format_version") == 1
              and isinstance(exported.get("state"), dict), "export envelope")
        frozen = copy.deepcopy(exported)
        a.expect(200, "POST", "/reservations/" + created["reference"] + "/cancel", token=token)
        a.book(token, body(), "post-snapshot")
        check(exported == frozen, "export object changed after source writes")
        if self.control:
            (self.control / "pause-source").write_text("ready\n")
            deadline = time.monotonic() + 30
            while not (self.control / "source-unavailable").exists():
                if time.monotonic() >= deadline:
                    raise OSError("orchestration did not make source unavailable")
                time.sleep(.1)
        d = self.dest
        d.reset(fixture())
        destination_token = d.login()
        d.book(destination_token, body("a"), "old-destination")
        d.expect(201, "POST", "/auth/signup", {"email": "destination@verifier.invalid", "password": PASSWORD, "display_name": "D"})
        for repeat in range(2):
            d.expect(204, "POST", "/_test/import", frozen)
            check(d.reservations(token) == rows, "import regenerated or duplicated reservation state")
            check(d.reservations(old_token) == rows, "import lost existing session")
            check(d.reservations(d.login()) == rows, "import lost hashed-password login")
            d.expect(401, "GET", "/reservations", token=destination_token, code="unauthenticated")
            d.expect(401, "POST", "/auth/login", {"email": "destination@verifier.invalid", "password": PASSWORD}, code="unauthenticated")
            check(d.book(token, create_request, "create-receipt", 200) == created, "import lost original create receipt")
            check(d.expect(200, "POST", "/reservation-moves", batch_request, token, "batch-receipt") == batch,
                  "import lost original batch receipt")
            d.book(token, body("a"), "failed-key")
        before = d.reservations(token)
        invalid = ({}, {**frozen, "track": "wrong"}, {**frozen, "format_version": 2},
                   {**frozen, "state": None}, {**frozen, "state": []})
        for value in invalid:
            d.expect(422, "POST", "/_test/import", value, code="validation_failed")
            check(d.reservations(token) == before, "invalid import changed state")
            check(d.book(token, create_request, "create-receipt", 200) == created, "invalid import changed receipt")
            check(d.reservations(d.login()) == before, "invalid import changed hashed login")
        d.expect(400, "POST", "/_test/import", raw=b"{", code="malformed_request")
        check(d.reservations(token) == before, "malformed import changed state")
        # Re-export imported state and transfer again with original source unavailable.
        chained = d.expect(200, "GET", "/_test/export")
        third = self.third or d
        third.reset(fixture())
        third.expect(204, "POST", "/_test/import", chained)
        check(third.reservations(token) == before, "re-export/import chain changed records")
        check(third.reservations(third.login()) == before, "re-export chain lost hashed login")
        check(third.book(token, create_request, "create-receipt", 200) == created, "re-export chain lost create receipt")
        check(third.expect(200, "POST", "/reservation-moves", batch_request, token, "batch-receipt") == batch,
              "re-export chain lost batch receipt")
        d.reset(fixture())
        d.expect(401, "GET", "/reservations", token=token, code="unauthenticated")
        check(d.reservations(d.login()) == [], "reset retained imported state")

    def run(self, selected=None):
        names = ("ignored_numeric_receipt_boundaries", "calendar_extremes", "numeric_equivalence_and_precision",
                     "terminal_zone_instants", "public_auth_reset", "availability_oracle", "validation", "booking_boundaries_privacy",
                     "receipt_semantics", "amendments_atomic_cutoff", "dst_oracle", "dst_closing_instant_boundaries", "moves_atomic_precedence",
                     "moves_eight_and_restaurant_scope", "duplicate_table_ids_and_short_seed_password",
                     "seed_ids_and_batch_cutoff", "patch_and_batch_field_validation",
                     "concurrency_identical_50", "concurrency_distinct_50",
                     "concurrency_changed_key_50", "concurrency_batch_snapshot", "concurrency_signup_and_users",
                     "export_atomic_batch", "control_replacement_races", "patch_batch_cancel_replay_races",
                     "offset_ordering_and_amendment", "cancelled_after_cutoff_temporal",
                     "legacy_direct_snapshot_continuity", "control_receipt_erasure", "snapshot_import_receipts")
        if not self.legacy:
            names = tuple(name for name in names if name != "legacy_direct_snapshot_continuity")
        if selected:
            check(all(name in names for name in selected), "unknown selected campaign case")
        for name in (selected or names):
            start = time.monotonic()
            try:
                getattr(self, name)()
                outcome = {"case": name, "status": "PASS"}
            except CheckFailure as exc:
                outcome = {"case": name, "status": "FAIL", "classification": "PRODUCT DEFECT", "detail": str(exc)}
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
                outcome = {"case": name, "status": "ERROR", "classification": "INCONCLUSIVE", "detail": type(exc).__name__}
            except Exception as exc:
                outcome = {"case": name, "status": "ERROR", "classification": "VERIFIER DEFECT", "detail": type(exc).__name__}
            outcome["seconds"] = round(time.monotonic() - start, 3)
            self.results.append(outcome)
            print(json.dumps(outcome), flush=True)
        timings = self.api.timings + self.dest.timings + (self.third.timings if self.third else []) + (self.legacy.timings if self.legacy else [])
        return {"campaign": "independent-stage-1", "cases": self.results, "requests": len(timings),
                "max_regular_request_seconds": round(max((x for p, x in timings if not p.startswith("/_test/")), default=0), 4),
                "max_control_request_seconds": round(max((x for p, x in timings if p.startswith("/_test/")), default=0), 4),
                "all_passed": all(x["status"] == "PASS" for x in self.results)}


def calibrate():
    """Controlled decision variants; all run without a production process."""
    a = dt.datetime(2080, 1, 1, 18, tzinfo=UTC)
    b = a + dt.timedelta(minutes=90)
    check(not overlaps(a, b, b, b + dt.timedelta(minutes=90)), "oracle rejects half-open adjacency")
    check(overlaps(a, b, b - dt.timedelta(minutes=1), b + dt.timedelta(minutes=90)), "oracle misses overlap")
    # Mutant closed-interval predicate must be distinguishable at adjacency.
    closed_mutant = lambda s, e, x, y: s <= y and x <= e
    check(closed_mutant(a, b, b, b + dt.timedelta(minutes=90)) != overlaps(a, b, b, b + dt.timedelta(minutes=90)),
          "VERIFIER COVERAGE GAP: closed-interval mutant")
    for zone, local in (("Europe/Berlin", "2026-03-29T02:30"), ("America/New_York", "2026-03-08T02:30")):
        check(resolve(local, zone) is None, "oracle accepts nonexistent time")
    for zone, local in (("Europe/Berlin", "2026-10-25T02:30"), ("America/New_York", "2026-11-01T01:30")):
        first = resolve(local, zone)
        second_mutant = first.replace(fold=1)
        check(first.astimezone(UTC) != second_mutant.astimezone(UTC), "VERIFIER COVERAGE GAP: second-occurrence mutant")
        absolute_end = (first.astimezone(UTC) + dt.timedelta(minutes=90)).astimezone(ZoneInfo(zone))
        wall_mutant = first + dt.timedelta(minutes=90)
        check(absolute_end.astimezone(UTC) != wall_mutant.astimezone(UTC), "VERIFIER COVERAGE GAP: wall-duration mutant")
    fx = fixture()
    slots = oracle(fx, DAY, 3)
    check(slots[0]["available_table_ids"] == ["z", "m"], "oracle table capacity/order")
    check(slots[-1]["starts_at_local"].endswith("21:30"), "oracle closing boundary")
    first = {"restaurant_id": "other", "table_id": "z", "status": "confirmed",
             "starts_at": DAY + "T18:00:00+02:00", "ends_at": DAY + "T19:30:00+02:00"}
    check(oracle(fx, DAY, 2, [first])[0]["available_table_ids"] == ["z", "a", "m"],
          "VERIFIER COVERAGE GAP: cross-restaurant table-ID contamination")
    encoded = encode_json(json.loads('{"ignored":1e309}', parse_float=Decimal))
    check("Infinity" not in encoded and json.loads(encoded, parse_float=Decimal)["ignored"] == Decimal("1e309"),
          "verifier lost finite large JSON number")
    precise, rounded = Decimal("1.0000000000000000001"), Decimal("1.0")
    check(precise != rounded and float(precise) == float(rounded), "numeric precision mutant calibration ineffective")
    close_fixture = fixture("Europe/Berlin", "00:00", "03:30")
    correct = oracle(close_fixture, "2026-03-29", 2)
    wall_fit_mutant = dt.datetime(2026, 3, 29, 1, 30) + dt.timedelta(minutes=90) <= dt.datetime(2026, 3, 29, 3, 30)
    check(wall_fit_mutant and "2026-03-29T01:30" not in [s["starts_at_local"] for s in correct],
          "VERIFIER COVERAGE GAP: wall-clock closing fit")
    check(instant_seconds("9999-12-31T23:00:00-05:00") - instant_seconds("9999-12-31T22:00:00-05:00") == 3600,
          "terminal unbounded instant oracle failed")
    print(json.dumps({"calibration": "PASS", "controlled_variants_detected":
                      ["closed interval", "second repeated occurrence", "wall-clock duration",
                       "cross-restaurant table contamination", "binary64 numeric equality collapse", "wall-clock closing fit"],
                      "scope": "oracle calibration only; no production mutation"}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("calibrate", "http"))
    parser.add_argument("--source")
    parser.add_argument("--destination")
    parser.add_argument("--third")
    parser.add_argument("--legacy")
    parser.add_argument("--control")
    parser.add_argument("--cases", nargs="+")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.mode == "calibrate":
        calibrate()
        return 0
    if not all((args.source, args.destination, args.out)):
        parser.error("http requires --source, --destination, --out")
    report = Campaign(args.source, args.destination, args.control, args.third, args.legacy).run(args.cases)
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
