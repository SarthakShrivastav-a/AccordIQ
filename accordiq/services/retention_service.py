from __future__ import annotations

def retention_cutoff_days(retention_days: int) -> int | None:
    return None if retention_days == 0 else retention_days
