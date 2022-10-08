from sqlmodel import SQLModel, Field


class UserEvent(SQLModel, table=True):
    user_id: int = Field(
        foreign_key="user.id", primary_key=True
    )
    event_id: int = Field(
        foreign_key="event.id", primary_key=True
    )
