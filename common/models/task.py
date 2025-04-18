from dataclasses import dataclass, field
from rococo.models import VersionedModel
from typing import ClassVar, Optional
from datetime import datetime
import uuid


@dataclass
class Task(VersionedModel):
    use_type_checking: ClassVar[bool] = True

    person_id: str = field(default=None)
    title: str = field(default=None)

    description: Optional[str] = field(default=None)
    is_completed: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    version: str = field(default_factory=lambda: str(uuid.uuid4()).replace("-", ""))
    previous_version: str = field(default="00000000000000000000000000000000")
    active: bool = field(default=True)
    changed_on: datetime = field(default_factory=datetime.utcnow)
    changed_by_id: str = field(default="system")  # or Optional[str] if needed
