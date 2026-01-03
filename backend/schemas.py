from pydantic import BaseModel
from typing import List, Optional

class ResumeResponse(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    recommended_jobs: List[str]
    