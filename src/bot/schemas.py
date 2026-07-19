from pydantic import BaseModel


class ReactionRoleRule(BaseModel):
    channel_id: int
    message_id: int
    emoji: str
    role_id: int

    restricted_roles: set[int]
    """Если какая-то из ролей пользователя присутствует в этом списке,
    то целевая роль не выдаётся.
    """
