from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AssistantCreate(BaseModel):
    name: str = Field(..., max_length=64)
    system_prompt: str

class AssistantOut(BaseModel):
    id: int
    name: str
    system_prompt: str
    model_config = ConfigDict(from_attributes=True)

class ChatCreate(BaseModel):
    assistant_id: int

class ChatOut(BaseModel):
    id: int
    assistant_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
