from enum import Enum, auto

class Status(Enum):
    CREATED = "created"
    PUBLISHED = "published"
    DELETED = "deleted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class FilterType(Enum):
    UPDATED_DATE = auto()
    CREATED_DATE = auto()
    TITLE = auto()
    DESCRIPTION = auto()
    TAGS = auto()
    AUTHOR = auto()
    STATUS = Status
    