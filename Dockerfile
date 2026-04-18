# Use a slim Python image for a small footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the script and necessary files
COPY hath_monitor.py .
COPY hath-monitor.service .
COPY LICENSE .
COPY README.md .
COPY i18n/ ./i18n/

# Create a volume for the database and config to persist data
# Users should mount their config.toml and hath_monitor.db to /app
VOLUME ["/app"]

# Install tomli as a fallback (though Python 3.11+ has tomllib)
RUN pip install --no-cache-dir tomli

# Run the monitor in daemon mode by default
ENTRYPOINT ["python", "hath_monitor.py"]
CMD ["--daemon"]
