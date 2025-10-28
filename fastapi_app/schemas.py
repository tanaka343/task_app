from pydantic import BaseModel,Field,ConfigDict
from datetime import date


class ItemCreate(BaseModel):
        title     : str = Field(min_length=2,max_length=20,examples=["買い物"])
        content   : str = Field(min_length=2,max_length=20,examples=["アボカド"])
        due_date  : date = Field(examples=["2025-10-26"])
        completed : bool = Field(examples=[False])


class ItemResponse(BaseModel):
        title     : str = Field(min_length=2,max_length=20,examples=["買い物"])
        content   : str = Field(min_length=2,max_length=20,examples=["アボカド"])
        due_date  : date = Field(examples=["2025-10-26"])
        completed : bool = Field(examples=[False])

        model_config = ConfigDict(from_attributes=True)
