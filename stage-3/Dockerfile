FROM python:3.13-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY domain.py service.py server.py json_value.py ./
COPY public ./public
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8080
USER 65534:65534
EXPOSE 8080
CMD ["python", "server.py"]
