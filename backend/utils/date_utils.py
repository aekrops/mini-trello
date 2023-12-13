from datetime import datetime


def convert_iso_to_datetime(iso_str):
    try:
        return datetime.fromisoformat(iso_str) if iso_str else None
    except ValueError:
        return None
