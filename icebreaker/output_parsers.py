from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class PersonIntel(BaseModel):
    summary: str = Field(..., description="A short summary of the person")
    interesting_facts: List[str] = Field(
        ..., description="The interesting facts about the person"
    )
    topics_of_interest: List[str] = Field(
        ..., description="The topics of interest of the person"
    )
    ice_breakers: List[str] = Field(..., description="The ice breakers for the person")

    def to_dict(self):
        return {
            "summary": self.summary,
            "interesting_facts": self.interesting_facts,
            "topics_of_interest": self.topics_of_interest,
            "ice_breakers": self.ice_breakers,
        }


person_intel_parser = PydanticOutputParser(pydantic_object=PersonIntel)
