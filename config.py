import os


PGSQL_HOST = os.getenv("PGSQL_HOST") or "localhost"
PGSQL_PORT = os.getenv("PGSQL_PORT") or "5432"
PGSQL_USER = os.getenv("PGSQL_USER") or "admin"
PGSQL_PASSWORD = os.getenv("PGSQL_PASSWORD") or "iotlab"
PGSQL_DB_NAME = os.getenv("PGSQL_DB_NAME") or "vega"

CLICKHOUSE_DB_NAME = os.getenv("CLICKHOUSE_DB_NAME") or "vega"
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST") or "localhost"
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT") or "19000"
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER") or "default"
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD") or None

DEBUG = False if os.getenv("DEBUG") == "false".lower() else True
