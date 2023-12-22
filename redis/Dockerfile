FROM redis:alpine

HEALTHCHECK --interval=30s --timeout=10s \
  CMD redis-cli ping || exit 1