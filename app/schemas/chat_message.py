from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: int
    text: str
    author_id: int


