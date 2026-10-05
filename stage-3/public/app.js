'use strict';

(() => {
  const main = document.getElementById('main');
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const hook = name => `data-testid="${escape(name)}"`;
  const sessionKey = 'tablekeeper-session';
  const today = new Date();
  const dateValue = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
  let user = null;
  try {
    const stored = JSON.parse(sessionStorage.getItem(sessionKey));
    if (stored && typeof stored.token === 'string' && typeof stored.display_name === 'string' && typeof stored.user_id === 'string') user = stored;
  } catch (_) { /* A session still works in memory when browser storage is unavailable. */ }
  const state = {
    route: location.pathname, user, userGeneration: 0, authGeneration: 0, authError: '', authBusy: false,
    restaurants: [], restaurantsStatus: 'loading', restaurantsError: '',
    query: {restaurant: '', date: dateValue, party: '2'},
    searchGeneration: 0, refreshGeneration: 0, searchStatus: 'idle', searchError: '', results: null,
    booking: null, intentGeneration: 0,
    lookupGeneration: 0, lookupValue: new URLSearchParams(location.search).get('reference') || '', lookupBusy: false,
    lookupError: '', detail: null, cancelBusy: false
  };

  class Refusal extends Error {
    constructor(status, payload) { super(payload?.error?.message || 'The request could not be completed. Please check your details.'); this.status = status; this.code = payload?.error?.code; }
  }
  function friendlyRefusal(error) {
    return ({
      unauthenticated: 'Please sign in to continue.',
      email_taken: 'There is already an account with this email. Please sign in instead.',
      validation_failed: 'Please check your details and try again.',
      party_exceeds_capacity: 'This seating does not have room for that many guests. Choose a larger table or a combined seating option.',
      outside_opening_hours: 'That visit falls outside the restaurant’s opening hours. Please choose an offered time.',
      not_on_slot_grid: 'Please choose one of the restaurant’s offered reservation times.',
      invalid_local_time: 'That local time is not available. Please choose another time.',
      combination_not_allowed: 'These tables cannot be reserved together. Please choose an offered seating option.',
      idempotency_key_reuse: 'These details do not match the original request. Change your selection before making a new reservation.'
    })[error.code] || error.message;
  }
  async function api(path, options = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch(path, {cache: 'no-store', ...options, signal: controller.signal});
      // A missing/unreadable response cannot prove a booking outcome, even after commit.
      const payload = await response.json();
      if (!response.ok) throw new Refusal(response.status, payload);
      return payload;
    } finally { clearTimeout(timer); }
  }
  const authHeaders = token => ({'Content-Type':'application/json', 'Authorization':`Bearer ${token}`});
  function requestKey() {
    const bytes = new Uint8Array(20);
    crypto.getRandomValues(bytes);
    return 'tk-' + Array.from(bytes, n => n.toString(16).padStart(2,'0')).join('');
  }
  function setUser(next) {
    state.user = next;
    state.userGeneration++;
    state.authError = '';
    state.booking = null;
    state.intentGeneration++;
    state.lookupGeneration++;
    state.detail = null;
    state.lookupBusy = false;
    state.cancelBusy = false;
    state.lookupError = '';
    try { next ? sessionStorage.setItem(sessionKey, JSON.stringify(next)) : sessionStorage.removeItem(sessionKey); } catch (_) {}
  }
  function navigate(path, push = true) {
    if (push) history.pushState(null, '', path);
    state.route = location.pathname;
    state.authGeneration++;
    state.authBusy = false;
    state.authError = '';
    state.searchGeneration++;
    state.refreshGeneration++;
    if (state.searchStatus === 'loading') state.searchStatus = state.results ? 'ready' : 'idle';
    state.booking = null;
    state.intentGeneration++;
    state.lookupGeneration++;
    state.lookupValue = new URLSearchParams(location.search).get('reference') || '';
    state.lookupError = '';
    state.lookupBusy = false;
    state.cancelBusy = false;
    state.detail = null;
    render();
    main.focus({preventScroll:true});
    window.scrollTo(0,0);
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-nav]');
    if (link && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && event.button === 0) {
      event.preventDefault(); navigate(link.getAttribute('href'));
    }
  });
  window.addEventListener('popstate', () => navigate(location.pathname + location.search, false));

  function localDate(value) {
    const [year, month, day] = value.split('-').map(Number);
    if (!year || !month || !day) return value;
    const date = new Date(0); date.setUTCFullYear(year,month-1,day); date.setUTCHours(12,0,0,0);
    return new Intl.DateTimeFormat('en', {weekday:'short',month:'short',day:'numeric',year:'numeric',timeZone:'UTC'}).format(date);
  }
  const localTime = value => String(value || '').slice(11,16);
  const members = reservation => Array.isArray(reservation.table_ids) ? reservation.table_ids : [reservation.table_id];
  const tableName = (restaurant, ids) => ids.map(id => restaurant.tables.find(table => table.id === id)?.label ?? id).join(' & ');
  const seatName = (restaurant, ids) => `${ids.length > 1 ? 'Tables' : 'Table'} ${tableName(restaurant, ids)}`;
  function seatingOptions(restaurant) {
    return [
      ...restaurant.tables.map(table => ({ids:[table.id], capacity:table.capacity})),
      ...(restaurant.combinable || []).map(ids => ({ids:[...ids], capacity:ids.reduce((sum,id) => sum + (restaurant.tables.find(table => table.id === id)?.capacity || 0),0)}))
    ];
  }
  const sameMembers = (a,b) => a.length === b.length && a.every((id,index) => id === b[index]);
  const loading = text => `<div class="loading" role="status"><span class="spinner" aria-hidden="true"></span>${escape(text)}</div>`;
  const errorBox = (name,text) => text ? `<div class="notice error" role="alert" ${hook(name)}>${escape(text)}</div>` : '';
  function renderHeader() {
    document.getElementById('navigation').innerHTML = [['/','Find a table'],['/lookup','Your reservation']].map(([path,label]) => `<a href="${path}" data-nav ${state.route === path ? 'aria-current="page"' : ''}>${label}</a>`).join('');
    document.getElementById('account').innerHTML = state.user
      ? `<span class="account-name" ${hook('current-user')}>Hello, ${escape(state.user.display_name)}</span><button class="quiet-button" ${hook('logout-button')}>Sign out</button>`
      : `<a href="/login" data-nav ${state.route === '/login' ? 'aria-current="page"' : ''}>Sign in</a><a class="signup-link" href="/signup" data-nav ${state.route === '/signup' ? 'aria-current="page"' : ''}>Join us</a>`;
    document.querySelector('[data-testid="logout-button"]')?.addEventListener('click', () => {
      state.authGeneration++; state.authBusy = false; setUser(null); render();
    });
  }
  function render() {
    renderHeader();
    document.title = ({'/':'Find a table','/signup':'Join us','/login':'Welcome back','/lookup':'Your reservation'}[state.route] || 'Find a table') + ' · Tablekeeper';
    if (state.route === '/login' || state.route === '/signup') renderAuth();
    else if (state.route === '/lookup') renderLookup();
    else renderSearch();
  }

  function renderAuth() {
    const signup = state.route === '/signup';
    const prefix = signup ? 'signup' : 'login';
    main.innerHTML = `<div class="auth-layout"><section class="auth-story"><p class="eyebrow">${signup ? 'THE START OF SOMETHING GOOD' : 'YOUR NEXT EVENING AWAITS'}</p><h1>${signup ? 'There’s a place<br>for you here.' : 'Good to have<br>you back.'}</h1><p>${signup ? 'A favourite corner, a table for two, or room for everyone. Make a little space for the moments that matter.' : 'Find your next table, revisit a reservation and leave the rest of the evening to good company.'}</p><div class="story-rule">A lovely evening starts with a seat.</div></section><section class="panel auth-panel"><h2>${signup ? 'Make yourself at home' : 'Welcome back'}</h2><p class="intro">${signup ? 'Create your account to reserve a table.' : 'Sign in to reserve and manage your tables.'}</p><form id="auth-form" class="stack-form">${signup ? `<div class="field"><label for="display-name">Your name</label><input id="display-name" name="display_name" autocomplete="name" required ${hook('signup-display-name')}></div>` : ''}<div class="field"><label for="auth-email">Email address</label><input id="auth-email" name="email" type="email" autocomplete="email" required ${hook(prefix+'-email')}></div><div class="field"><label for="auth-password">Password</label><input id="auth-password" name="password" type="password" autocomplete="${signup ? 'new-password' : 'current-password'}" required ${signup ? 'minlength="8" aria-describedby="password-help"' : ''} ${hook(prefix+'-password')}>${signup ? '<p id="password-help" class="help-text">At least 8 characters.</p>' : ''}</div><div id="auth-feedback">${errorBox('auth-error',state.authError)}</div><button class="primary" ${hook(prefix+'-submit')} ${state.authBusy ? 'disabled' : ''}>${state.authBusy ? 'One moment…' : signup ? 'Create your account' : 'Sign in'}</button></form><p class="auth-switch">${signup ? 'Already have a place here? <a href="/login" data-nav>Sign in</a>' : 'New to Tablekeeper? <a href="/signup" data-nav>Create an account</a>'}</p></section></div>`;
    document.getElementById('auth-form').addEventListener('submit', async event => {
      event.preventDefault(); if (state.authBusy) return;
      const form = event.currentTarget;
      const payload = {email:form.elements.email.value, password:form.elements.password.value};
      if (signup) payload.display_name = form.elements.display_name.value;
      const generation = ++state.authGeneration;
      const userGeneration = state.userGeneration;
      state.authBusy = true; state.authError = '';
      document.getElementById('auth-feedback').innerHTML = '';
      const button = form.querySelector('button'); button.disabled = true; button.textContent = 'One moment…';
      try {
        const response = await api('/auth/'+prefix, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
        if (generation !== state.authGeneration || userGeneration !== state.userGeneration) return;
        if (!response.token || typeof response.display_name !== 'string') throw new Error('Unreadable authentication response');
        setUser({token:response.token,user_id:response.user_id,display_name:response.display_name});
        navigate('/');
      } catch (error) {
        if (generation !== state.authGeneration || userGeneration !== state.userGeneration) return;
        state.authError = error instanceof Refusal ? error.code === 'unauthenticated' ? 'We could not sign you in. Please check your email and password.' : friendlyRefusal(error) : 'We could not reach the restaurant service. Please try signing in again.';
        document.getElementById('auth-feedback').innerHTML = errorBox('auth-error',state.authError);
      } finally {
        if (generation === state.authGeneration) { state.authBusy = false; button.disabled = false; button.textContent = signup ? 'Create your account' : 'Sign in'; }
      }
    });
  }

  function renderSearch() {
    main.innerHTML = `<section class="hero"><div><p class="eyebrow">GOOD EVENINGS BEGIN HERE</p><h1>A little room for<br>a lovely evening.</h1><p>Find your restaurant, choose your moment, and settle in.<br>A table for two or a little more room for your people.</p></div><div class="table-art" aria-hidden="true"><span class="plate one"></span><span class="plate two"></span><span class="stem"></span><span class="art-caption">Come together. Stay a while.</span></div></section><section class="panel search-panel" aria-label="Find a table"><form id="search-form" class="search-form"><div class="field"><label for="restaurant">Your restaurant</label><select id="restaurant" name="restaurant" required ${hook('restaurant-select')} ${state.restaurantsStatus !== 'ready' || !state.restaurants.length ? 'disabled' : ''}>${state.restaurants.length ? state.restaurants.map(r => `<option value="${escape(r.id)}" ${r.id === state.query.restaurant ? 'selected' : ''}>${escape(r.name)}</option>`).join('') : `<option value="">${state.restaurantsStatus === 'loading' ? 'Finding our restaurants…' : 'No restaurants available'}</option>`}</select></div><div class="field"><label for="search-date">When</label><input id="search-date" name="date" type="date" required value="${escape(state.query.date)}" ${hook('date-input')}></div><div class="field"><label for="search-party">Guests</label><input id="search-party" name="party" type="number" min="1" step="1" required value="${escape(state.query.party)}" ${hook('party-size-input')}></div><button class="primary" ${hook('search-button')} ${state.restaurantsStatus !== 'ready' || !state.restaurants.length ? 'disabled' : ''}>Find a table <span aria-hidden="true">↗</span></button></form><p class="search-note">Browse freely. Sign in when you’re ready to reserve. All times are local to your restaurant.</p>${state.restaurantsError ? `<div class="notice error" role="alert">${escape(state.restaurantsError)} <button class="quiet-button" id="retry-restaurants">Try again</button></div>` : ''}<div id="browse-auth-feedback">${errorBox('auth-error',state.authError)}</div></section><section id="results" class="results" aria-label="Available tables" aria-live="polite"></section><div id="booking-region"></div>`;
    document.getElementById('retry-restaurants')?.addEventListener('click', loadRestaurants);
    const form = document.getElementById('search-form');
    form.addEventListener('input', () => { state.query = {restaurant:form.elements.restaurant.value,date:form.elements.date.value,party:form.elements.party.value}; });
    form.addEventListener('change', () => { state.query = {restaurant:form.elements.restaurant.value,date:form.elements.date.value,party:form.elements.party.value}; });
    form.addEventListener('submit', event => { event.preventDefault(); runSearch({restaurant:form.elements.restaurant.value,date:form.elements.date.value,party:form.elements.party.value}); });
    renderResults(); renderBooking();
  }
  async function loadRestaurants() {
    state.restaurantsStatus = 'loading'; state.restaurantsError = '';
    if (state.route === '/') renderSearch();
    try {
      const response = await api('/restaurants');
      if (!Array.isArray(response.restaurants)) throw new Error('Unreadable restaurant list');
      state.restaurants = response.restaurants; state.restaurantsStatus = 'ready';
      if (!state.restaurants.some(r => r.id === state.query.restaurant)) state.query.restaurant = state.restaurants[0]?.id || '';
    } catch (_) { state.restaurantsStatus = 'error'; state.restaurantsError = 'We could not load the restaurants. Please try again.'; }
    if (state.route === '/') renderSearch();
  }
  async function fetchSnapshot(query) {
    const params = new URLSearchParams({restaurant_id:query.restaurant,date:query.date,party_size:String(query.party)});
    const [restaurant, availability] = await Promise.all([
      api('/restaurants/'+encodeURIComponent(query.restaurant)), api('/availability?'+params)
    ]);
    if (!Array.isArray(restaurant.tables) || !Array.isArray(availability.slots) || availability.restaurant_id !== query.restaurant || availability.date !== query.date) throw new Error('Unreadable availability');
    return {query:Object.freeze({...query}),restaurant,availability};
  }
  async function runSearch(query) {
    const generation = ++state.searchGeneration;
    state.refreshGeneration++;
    state.query = {...query}; state.results = null; state.searchStatus = 'loading'; state.searchError = '';
    state.booking = null; state.intentGeneration++; state.authError = '';
    document.getElementById('browse-auth-feedback').innerHTML = '';
    renderResults(); renderBooking();
    try {
      const snapshot = await fetchSnapshot(query);
      if (generation !== state.searchGeneration) return;
      state.results = snapshot; state.searchStatus = 'ready';
    } catch (error) {
      if (generation !== state.searchGeneration) return;
      state.searchStatus = 'error'; state.searchError = error instanceof Refusal ? error.message : 'We could not check those tables. Please try your search again.';
    }
    if (state.route === '/') renderResults();
  }
  function renderResults() {
    const container = document.getElementById('results'); if (!container) return;
    if (state.searchStatus === 'loading') { container.innerHTML = loading('Setting a place for you. Checking available tables…'); return; }
    if (state.searchStatus === 'error') { container.innerHTML = errorBox('search-error',state.searchError); return; }
    if (!state.results) {
      container.innerHTML = `<div class="empty-state"><div class="empty-emblem" aria-hidden="true">◌</div><h2>Your evening, your table.</h2><p>${state.restaurantsStatus === 'ready' && !state.restaurants.length ? 'There are no restaurants to browse just yet. Please check back soon.' : 'Choose a restaurant and date above. We’ll find a little room for you.'}</p></div>`; return;
    }
    const {restaurant,availability,query} = state.results;
    const heading = `<div class="section-heading"><div><h2>${escape(restaurant.name)}</h2><p>${escape(localDate(query.date))} · ${escape(query.party)} ${Number(query.party) === 1 ? 'guest' : 'guests'} · ${escape(restaurant.timezone)}</p></div><div class="legend"><span><i aria-hidden="true"></i>Available</span><span class="taken"><i aria-hidden="true"></i>Unavailable</span></div></div>`;
    if (!availability.slots.length) {
      container.innerHTML = heading + `<div class="empty-state" ${hook('no-slots')}><div class="empty-emblem" aria-hidden="true">◌</div><h2>A quiet day at this table.</h2><p>No reservation times are offered on this date. Try another day for your evening together.</p></div>`; return;
    }
    const options = seatingOptions(restaurant);
    container.innerHTML = heading + `<div ${hook('availability-grid')}>${availability.slots.map((slot,index) => `<section class="slot-row" aria-label="Tables at ${escape(localTime(slot.starts_at_local))}"><div class="slot-time"><strong>${escape(localTime(slot.starts_at_local))}</strong><small>local time</small></div><div class="slot-choices">${options.map((option,seatIndex) => {
      const available = option.ids.length === 1 ? slot.available_table_ids.includes(option.ids[0]) : (slot.available_options || []).some(candidate => sameMembers(candidate.table_ids,option.ids));
      const selected = state.booking && sameMembers(state.booking.ids,option.ids) && state.booking.local === slot.starts_at_local;
      return `<button type="button" class="slot-cell ${option.ids.length === 2 ? 'combo' : ''}" ${hook('slot-'+option.ids.join('+')+'-'+localTime(slot.starts_at_local))} data-available="${available}" data-slot-index="${index}" data-seat-index="${seatIndex}" aria-pressed="${Boolean(selected)}" aria-label="${escape(seatName(restaurant,option.ids)+', '+localTime(slot.starts_at_local)+', '+(available ? 'available' : 'unavailable'))}" ${available ? '' : 'disabled'}><strong>${escape(seatName(restaurant,option.ids))}</strong><small>Seats up to ${escape(option.capacity)}</small><span class="seat-state">${selected ? 'Your selection' : available ? 'Reserve this table' : 'Unavailable'}</span></button>`;
    }).join('')}</div></section>`).join('')}</div>${state.searchError ? errorBox('search-error',state.searchError) : ''}`;
    container.querySelectorAll('button[data-available="true"]').forEach(button => button.addEventListener('click', () => {
      if (!state.user) {
        state.authError = 'Please sign in to reserve your table.';
        document.getElementById('browse-auth-feedback').innerHTML = `<div class="notice error" role="alert" ${hook('auth-error')}>${escape(state.authError)} <a href="/login" data-nav>Sign in</a> or <a href="/signup" data-nav>join us</a>.</div>`; return;
      }
      const ids = options[Number(button.dataset.seatIndex)].ids;
      const local = availability.slots[Number(button.dataset.slotIndex)].starts_at_local;
      // Clicking the already selected cell is not a change to the booking intent.
      if (!state.booking || !sameMembers(state.booking.ids,ids) || state.booking.local !== local) {
        state.booking = {snapshot:state.results,ids:[...ids],local,party:String(query.party),generation:++state.intentGeneration,attempt:null,feedback:'',outcome:'idle',confirmation:null};
      }
      renderResults(); renderBooking();
      document.getElementById('booking-heading')?.focus({preventScroll:true});
      document.getElementById('booking-region')?.scrollIntoView({behavior:'smooth',block:'nearest'});
    }));
  }

  function renderBooking() {
    const region = document.getElementById('booking-region'); if (!region) return;
    const booking = state.booking; if (!booking) { region.innerHTML = ''; return; }
    const {restaurant,availability} = booking.snapshot;
    region.innerHTML = `<section class="panel booking-panel" ${hook('booking-form')} aria-labelledby="booking-heading"><div class="booking-heading"><div><p class="step-label">YOUR PLACE FOR THE EVENING</p><h2 id="booking-heading" tabindex="-1">Make it a reservation.</h2><p class="booking-summary" ${hook('booking-summary')}>${escape(restaurant.name)} · ${escape(seatName(restaurant,booking.ids))} · ${escape(localDate(booking.local.slice(0,10)))} at ${escape(localTime(booking.local))}</p></div></div><form id="booking-fields"><div class="booking-fields"><div class="field"><label for="booking-seat">Your seating</label><select id="booking-seat" name="seat" ${hook('booking-seating')}>${seatingOptions(restaurant).map(option => `<option value="${escape(JSON.stringify(option.ids))}" ${sameMembers(option.ids,booking.ids) ? 'selected' : ''}>${escape(seatName(restaurant,option.ids))} · seats ${escape(option.capacity)}</option>`).join('')}</select></div><div class="field"><label for="booking-time">Your time</label><select id="booking-time" name="time" ${hook('booking-time')}>${availability.slots.map(slot => `<option value="${escape(slot.starts_at_local)}" ${slot.starts_at_local === booking.local ? 'selected' : ''}>${escape(localTime(slot.starts_at_local))}</option>`).join('')}</select></div><div class="field"><label for="booking-party">Guests</label><input id="booking-party" name="party" type="number" min="1" step="1" required value="${escape(booking.party)}" ${hook('booking-party-size')}></div></div><div id="booking-feedback" aria-live="polite"></div><div class="booking-actions"><button class="primary" ${hook('booking-submit')}>Confirm reservation</button><p>Your table is reserved only when a confirmation comes back. A ${escape(restaurant.reservation_duration_minutes)}-minute visit, in ${escape(restaurant.timezone)}.</p></div></form><div id="confirmation-region" aria-live="polite"></div></section>`;
    const form = document.getElementById('booking-fields');
    form.elements.party.addEventListener('input', () => {
      if (booking.party !== form.elements.party.value) { booking.party = form.elements.party.value; changeIntent(booking); updateBookingFeedback(); }
    });
    for (const field of ['seat','time']) form.elements[field].addEventListener('change', () => {
      if (field === 'seat') booking.ids = JSON.parse(form.elements.seat.value); else booking.local = form.elements.time.value;
      changeIntent(booking); renderResults(); renderBooking(); document.getElementById(field === 'seat' ? 'booking-seat' : 'booking-time').focus();
    });
    form.addEventListener('submit', event => { event.preventDefault(); submitBooking(booking); });
    updateBookingFeedback();
  }
  function changeIntent(booking) {
    booking.generation = ++state.intentGeneration;
    booking.attempt = null; booking.feedback = ''; booking.outcome = 'idle'; booking.confirmation = null;
  }
  function updateBookingFeedback() {
    const booking = state.booking; const feedback = document.getElementById('booking-feedback');
    if (!booking || !feedback) return;
    feedback.innerHTML = booking.outcome === 'uncertain'
      ? `<div class="notice uncertain" role="status" ${hook('booking-uncertain')}><strong>We’re still unsure whether your table was reserved.</strong>Keep these details unchanged and retry to check the original request. ${escape(booking.feedback)}</div>`
      : booking.outcome === 'rejected' ? errorBox('booking-error',booking.feedback)
      : booking.outcome === 'sending' ? loading('Confirming your place at the table…') : '';
    const button = document.querySelector('[data-testid="booking-submit"]');
    button.disabled = booking.outcome === 'sending';
    button.textContent = booking.outcome === 'sending' ? 'Confirming…' : booking.outcome === 'uncertain' ? 'Retry this reservation' : booking.outcome === 'confirmed' ? 'Check this confirmation' : 'Confirm reservation';
    const confirmationRegion = document.getElementById('confirmation-region');
    const reservation = booking.confirmation;
    confirmationRegion.innerHTML = reservation && booking.outcome === 'confirmed' ? `<section class="confirmation" ${hook('confirmation')}><div><h3>You have a place at the table.</h3><p ${hook('confirmation-details')}>${escape(booking.snapshot.restaurant.name)} · ${escape(seatName(booking.snapshot.restaurant,members(reservation)))} · ${escape(localDate(reservation.starts_at_local.slice(0,10)))} at ${escape(localTime(reservation.starts_at_local))}</p><p ${hook('confirmation-tables')}>${escape(seatName(booking.snapshot.restaurant,members(reservation)))}</p></div><div class="reference-block"><small>Your reservation reference</small><div class="reference" ${hook('confirmation-reference')}>${escape(reservation.reference)}</div><a href="/lookup?reference=${encodeURIComponent(reservation.reference)}" data-nav>View your reservation ↗</a></div></section>` : '';
  }
  async function submitBooking(booking) {
    if (state.booking !== booking || booking.outcome === 'sending') return;
    if (!state.user) { booking.outcome = 'rejected'; booking.feedback = 'Please sign in before reserving your table.'; updateBookingFeedback(); return; }
    if (!booking.attempt) {
      const body = {restaurant_id:booking.snapshot.restaurant.id};
      // Preserve the legacy single-selector request, including across backend upgrades.
      if (booking.ids.length === 1) body.table_id = booking.ids[0]; else body.table_ids = [...booking.ids];
      body.starts_at_local = booking.local; body.party_size = Number(booking.party);
      booking.attempt = Object.freeze({key:requestKey(),body:JSON.stringify(body),token:state.user.token,userGeneration:state.userGeneration,generation:booking.generation});
    }
    const attempt = booking.attempt;
    const current = () => state.booking === booking && booking.attempt === attempt && state.userGeneration === attempt.userGeneration && booking.generation === attempt.generation;
    booking.outcome = 'sending'; booking.feedback = ''; booking.confirmation = null; updateBookingFeedback();
    try {
      const response = await api('/reservations', {method:'POST',headers:{...authHeaders(attempt.token),'Idempotency-Key':attempt.key},body:attempt.body});
      if (!current()) return;
      if (typeof response.reference !== 'string' || typeof response.starts_at_local !== 'string' || (!Array.isArray(response.table_ids) && typeof response.table_id !== 'string')) throw new Error('Unreadable confirmation');
      booking.confirmation = response; booking.outcome = 'confirmed';
    } catch (error) {
      if (!current()) return;
      booking.confirmation = null;
      if (error instanceof Refusal) {
        booking.outcome = 'rejected';
        booking.feedback = error.code === 'table_unavailable' ? 'That table was just reserved by someone else. We’re checking the latest availability. Your choices are kept below; choose another table or time.' : friendlyRefusal(error);
        if (error.code === 'table_unavailable') refreshAvailability(booking);
      } else { booking.outcome = 'uncertain'; booking.feedback = 'The connection ended before we could read a confirmation.'; }
    }
    if (current()) updateBookingFeedback();
  }
  async function refreshAvailability(booking) {
    const searchGeneration = state.searchGeneration;
    const refreshGeneration = ++state.refreshGeneration;
    const snapshot = state.results;
    if (!snapshot) return;
    try {
      const refreshed = await fetchSnapshot(snapshot.query);
      if (searchGeneration !== state.searchGeneration || refreshGeneration !== state.refreshGeneration || state.results !== snapshot) return;
      state.results = refreshed; state.searchError = '';
      // Deliberately update only results: retain the active form, inputs and attempt.
      if (state.route === '/') renderResults();
    } catch (_) {
      if (searchGeneration !== state.searchGeneration || refreshGeneration !== state.refreshGeneration || state.results !== snapshot) return;
      state.searchError = 'The latest availability could not be loaded. Your form is kept; try searching again when you’re ready.';
      if (state.route === '/') renderResults();
    }
  }

  function renderLookup() {
    main.innerHTML = `<section class="lookup-layout"><p class="eyebrow">YOUR EVENING, ALL IN ONE PLACE</p><h1>A table to look forward to.</h1><p class="intro">Find your reservation with the reference from your confirmation. Review your details or let the restaurant know your plans have changed.</p><section class="panel"><form id="lookup-form" class="lookup-form"><div class="field"><label for="lookup-reference">Reservation reference</label><input id="lookup-reference" name="reference" autocomplete="off" spellcheck="false" required value="${escape(state.lookupValue)}" ${hook('lookup-reference-input')}></div><button class="primary" ${hook('lookup-submit')}>Find my reservation</button></form>${!state.user ? '<p class="search-note">Please <a href="/login" data-nav>sign in</a> to see your reservation.</p>' : ''}</section><div id="lookup-feedback" aria-live="polite"></div><div id="reservation-region"></div></section>`;
    const form = document.getElementById('lookup-form');
    form.elements.reference.addEventListener('input', () => {
      state.lookupValue = form.elements.reference.value;
      state.lookupGeneration++; state.detail = null; state.lookupError = ''; state.lookupBusy = false; state.cancelBusy = false;
      renderLookupFeedback(); renderReservation();
    });
    form.addEventListener('submit', event => { event.preventDefault(); lookup(form.elements.reference.value.trim()); });
    renderLookupFeedback(); renderReservation();
  }
  function renderLookupFeedback() {
    const region = document.getElementById('lookup-feedback'); if (!region) return;
    region.innerHTML = state.lookupBusy ? loading('Finding your reservation…') : errorBox('reservation-error',state.lookupError);
  }
  async function lookup(reference) {
    const generation = ++state.lookupGeneration;
    const userGeneration = state.userGeneration;
    state.lookupValue = reference; state.lookupError = ''; state.detail = null; state.cancelBusy = false;
    if (!state.user) { state.lookupError = 'Please sign in to look up your reservation.'; renderLookupFeedback(); renderReservation(); return; }
    const token = state.user.token;
    state.lookupBusy = true; renderLookupFeedback(); renderReservation();
    const current = () => generation === state.lookupGeneration && userGeneration === state.userGeneration;
    try {
      const reservation = await api('/reservations/'+encodeURIComponent(reference), {headers:authHeaders(token)});
      if (!current()) return;
      const restaurant = await api('/restaurants/'+encodeURIComponent(reservation.restaurant_id));
      if (!current()) return;
      state.detail = {reservation,restaurant};
    } catch (error) {
      if (!current()) return;
      state.lookupError = error instanceof Refusal ? error.status === 404 ? 'We could not find that reservation in your account. Please check the reference.' : error.message : 'We could not load your reservation. Please try again.';
    } finally {
      if (current()) { state.lookupBusy = false; renderLookupFeedback(); renderReservation(); }
    }
  }
  function renderReservation() {
    const region = document.getElementById('reservation-region'); if (!region) return;
    if (!state.detail) { region.innerHTML = ''; return; }
    const {reservation,restaurant} = state.detail;
    region.innerHTML = `<section class="panel reservation-card" ${hook('reservation-detail')}><div class="detail-top"><p class="step-label">YOUR RESERVATION</p><span class="status-pill ${reservation.status === 'cancelled' ? 'cancelled' : ''}" ${hook('reservation-status')}>${escape(reservation.status)}</span></div><h2 class="detail-title">${escape(restaurant.name)}</h2><p class="detail-date">${escape(localDate(reservation.starts_at_local.slice(0,10)))} at ${escape(localTime(reservation.starts_at_local))} · ${escape(restaurant.timezone)}</p><dl class="detail-grid"><div><dt>Your seating</dt><dd ${hook('reservation-tables')}>${escape(seatName(restaurant,members(reservation)))}</dd></div><div><dt>Guests</dt><dd>${escape(reservation.party_size)}</dd></div><div><dt>Reference</dt><dd>${escape(reservation.reference)}</dd></div><div><dt>Your visit</dt><dd>${escape(restaurant.reservation_duration_minutes)} minutes</dd></div></dl>${reservation.status === 'confirmed' ? `<div class="cancel-actions"><button class="secondary" ${hook('reservation-cancel-button')} ${state.cancelBusy ? 'disabled' : ''}>${state.cancelBusy ? 'Cancelling…' : 'Cancel reservation'}</button><p>Changes are allowed until ${escape(restaurant.cancellation_cutoff_minutes)} minutes before your reservation.</p></div>` : '<div class="notice">This reservation has been cancelled. We hope to see you another evening.</div><p class="auth-switch"><a href="/" data-nav>Find another table ↗</a></p>'}</section>`;
    region.querySelector('[data-testid="reservation-cancel-button"]')?.addEventListener('click', cancelReservation);
  }
  async function cancelReservation() {
    if (!state.detail || !state.user || state.cancelBusy) return;
    const detail = state.detail;
    const generation = state.lookupGeneration;
    const userGeneration = state.userGeneration;
    const current = () => generation === state.lookupGeneration && userGeneration === state.userGeneration && state.detail === detail;
    const token = state.user.token;
    state.cancelBusy = true; state.lookupError = ''; renderReservation(); renderLookupFeedback();
    try {
      const response = await api('/reservations/'+encodeURIComponent(detail.reservation.reference)+'/cancel', {method:'POST',headers:authHeaders(token),body:'{}'});
      if (!current()) return;
      if (response.status !== 'cancelled') throw new Error('Unconfirmed cancellation');
      detail.reservation = response;
    } catch (error) {
      if (!current()) return;
      state.lookupError = error instanceof Refusal ? error.code === 'cutoff_passed' ? 'This reservation is too close to its start time to cancel. Your table is still confirmed.' : error.message : 'We could not confirm the cancellation. Look up this reference again to check its current status.';
    } finally {
      if (current()) { state.cancelBusy = false; renderLookupFeedback(); renderReservation(); }
    }
  }

  render();
  loadRestaurants();
})();
