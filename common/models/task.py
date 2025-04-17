from dataclasses import dataclass, field
from rococo.models import VersionedModel
from typing import ClassVar, Optional
from datetime import datetime


@dataclass
class Task(VersionedModel):
    use_type_checking: ClassVar[bool] = True

    person_id: str = field(default=None)
    title: str = field(default=None)
    description: Optional[str] = field(default=None)
    is_completed: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(
        self,
        include_version=False,
        convert_datetime_to_iso_string=True,
        convert_uuids=False,
    ):
        data = {
            "entity_id": self.entity_id,
            "title": self.title,
            "description": self.description,
            "is_completed": self.is_completed,
            "person_id": self.person_id,
        }

        # Handle datetime fields
        if convert_datetime_to_iso_string:
            data["created_at"] = (
                self.created_at.isoformat() if self.created_at else None
            )
            data["updated_at"] = (
                self.updated_at.isoformat() if self.updated_at else None
            )
        else:
            data["created_at"] = self.created_at
            data["updated_at"] = self.updated_at

        if include_version:
            data.update(
                {
                    "version": self.version,
                    "previous_version": self.previous_version,
                    "active": self.active,
                    "changed_by_id": self.changed_by_id,
                    "changed_on": self.changed_on,
                }
            )

        return data
