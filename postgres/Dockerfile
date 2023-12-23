FROM postgres:alpine3.19

HEALTHCHECK \
    --interval=15s \
    --retries=6 \
    --start-period=6s \
    --timeout=6s \
    CMD pg_isready -U "${POSTGRES_USER}" || exit 1