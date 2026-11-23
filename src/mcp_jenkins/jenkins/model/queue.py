from pydantic import BaseModel, field_validator


class Queue(BaseModel):
    discoverableItems: list
    items: list['QueueItem']


class QueueItemExecutable(BaseModel):
    # Jenkins omits nothing here once a queued item starts building, but the fields stay optional so
    # that one unexpected item cannot fail validation of a whole queue listing.
    number: int | None = None
    url: str | None = None


class QueueItem(BaseModel):
    id: int
    inQueueSince: int
    url: str
    why: str | None

    task: 'QueueItemTask'
    executable: QueueItemExecutable | None = None

    @field_validator('executable', mode='before')
    @classmethod
    def _empty_executable_is_none(cls, value: dict | None) -> dict | None:
        # Jenkins returns an empty object while the item is still waiting in the queue.
        return None if value == {} else value


class QueueItemTask(BaseModel):
    fullDisplayName: str = None
    name: str = None
    url: str = None
