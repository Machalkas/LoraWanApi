import json
import os

SECRET_KEY = os.getenv("SECRET_KEY", "very_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


PGSQL_HOST = os.getenv("PGSQL_HOST", "localhost")
PGSQL_PORT = os.getenv("PGSQL_PORT", "5432")
PGSQL_USER = os.getenv("PGSQL_USER", "admin")
PGSQL_PASSWORD = os.getenv("PGSQL_PASSWORD", "admin")
PGSQL_DB_NAME = os.getenv("PGSQL_DB_NAME", "vega")

CLICKHOUSE_DB_NAME = os.getenv("CLICKHOUSE_DB_NAME", "vega")
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "19000")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_MAX_COUNT = int(os.getenv("CLICKHOUSE_MAX_COUNT", 1000))
CLICKHOUSE_TIMEOUT = int(os.getenv("CLICKHOUSE_TIMEOUT", 30))

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPICS_TO_SUBSCRIBE = [ topic.strip() for topic in os.getenv("MQTT_TOPICKS_TO_SUBSCRIBE", "statistic, device/#").split(",")]

IS_DEBUG = False if os.getenv("DEBUG") == "false".lower() else True

POWER_TABLE_QUERY = f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.power (`datetime` DateTime, `counter` UInt32, `phase_a` Nullable(Float64), `phase_b` Nullable(Float64), `phase_c` Nullable(Float64), `total` Nullable(Float64)) ENGINE = Log()"
TRAFFIC_TABLE_QUERY = f"CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB_NAME}.traffic (`datetime` DateTime, `counter` UInt32, `traffic_plan_1` Nullable(Float64), `traffic_plan_2` Nullable(Float64), `traffic_plan_3` Nullable(Float64), `traffic_plan_4` Nullable(Float64), `total` Nullable(Float64), `current_traffic` Nullable(Int32)) ENGINE = Log()"

DEFAULT_ROLES: list = [topic.strip().upper() for topic in os.getenv("user", "admin").split(",")]
DEFAULT_ADMIN_USER: dict = json.loads(os.getenv("DEFAULT_ADMIN_USER", '{"username": "admin", "email": null, "password": "qwerty123"}'))

DT_FORMAT = "%Y-%m-%d %H:%M:%S"
