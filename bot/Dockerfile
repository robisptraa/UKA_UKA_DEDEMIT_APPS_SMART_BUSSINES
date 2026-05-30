# =============================================================
# Telegram Bot - Lightweight Python Alpine Image
# =============================================================
FROM python:3.11-alpine AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Alpine: install minimal C libs for some Python packages
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cleanup build tools to reduce image size
RUN apk del gcc musl-dev libffi-dev && \
    rm -rf /root/.cache

COPY bot/ ./bot/

# Create non-root user
RUN addgroup -S botgroup && adduser -S botuser -G botgroup
USER botuser

HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import bot; print('ok')" || exit 1

CMD ["python", "-m", "bot.main"]
