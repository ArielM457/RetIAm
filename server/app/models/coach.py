from pydantic import BaseModel, Field


class ReminderResponse(BaseModel):
    id: str | None = None
    kind: str
    tone: str
    delivery_channel: str
    message: str
    scheduled_for: str
    status: str


class ReminderGenerationResponse(BaseModel):
    reminders: list[ReminderResponse] = Field(default_factory=list)
    workiq_context: dict = Field(default_factory=dict)
