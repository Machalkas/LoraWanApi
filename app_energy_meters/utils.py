from fastapi import HTTPException


def get_clickhouse_writer_or_raise(metric):
    ch_writer = globals.clickhouse_writers.get(metric)
    if ch_writer is None:
        raise HTTPException(404, f"Metric {metric} not found")
    return ch_writer
