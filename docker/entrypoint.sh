#!/bin/sh
exec "$@"
alembic upgrade heads
break
