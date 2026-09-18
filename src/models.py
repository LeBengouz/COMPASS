"""
LLM used should produce a list of concept.
Each concept output follow prerequisite class structure
"""

from pydantic import BaseModel, Field

class Prerequisite(BaseModel):
    concept: str
    reason: str # why it will help understand the passage target
    depends_on: list[str] # other prerequisite
    source_type: str
    search_queries: list[str] = Field(min_length=1, max_length=3, description=("Between 1 and 3 concise search queries for learning this concept.")) # what to look for on scholar
    checkpoint: str # question to help user make sure he understands


class PrerequisiteMap(BaseModel):
    target: str
    prerequisites: list[Prerequisite]