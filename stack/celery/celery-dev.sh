#!/bin/sh

exec >> /var/log/celery/worker.log 2>&1

watchmedo auto-restart \
  --patterns="*.py" \
  --recursive \
  --directory=/app \
  -- celery -A app worker -l info
