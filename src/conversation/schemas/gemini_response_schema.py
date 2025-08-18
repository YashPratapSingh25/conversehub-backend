from pydantic import BaseModel
from src.core.common_schemas import BaseSchema

class Scores(BaseModel):
    clarity : int
    confidence : int
    grammar : int
    vocabulary : int
    relevance : int


class Feedback(BaseModel):
    clarity: str
    confidence: str
    grammar: str
    vocabulary: str
    relevance: str
    strength: str
    weakness: str
    rephrased_text: str
    improvement_tip: str
    scores: Scores


class GeminiResponse(BaseModel):
    topic: str
    reply: str
    feedback: Feedback
