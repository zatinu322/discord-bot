from pydantic import BaseModel


class ReactionRoleRule(BaseModel):
    channel_id: int
    message_id: int
    emoji: str
    role_id: int
