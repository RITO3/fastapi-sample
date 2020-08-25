import dataclasses
from datetime import datetime


@dataclasses.dataclass(frozen=True)
class AuditTime:
    created_at: datetime
    updated_at: datetime
