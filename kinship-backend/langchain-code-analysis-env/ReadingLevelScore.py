from marvin import ai_model
from typing import Optional, List
import datetime
import pydantic
from pydantic import BaseModel, Field

reading_level_context = """ 
K-1st (5-6): Simple reading, images. Lexile BR120L-295L.
1st-2nd (6-7): Independent reading. Lexile 190L-530L.
2nd-3rd (7-8): Longer reading, complex books. Lexile 420L-820L.
3rd-5th (8-10): Complex vocabulary, chapter books. Lexile 520L-1010L.
5th-8th (10-13): Text interpretation, varied genres. Lexile 830L-1010L.
8th-12th (13-18): Advanced themes, adult literature. Lexile 925L-1200L+.
INSTRUCTIONS: Score how well the message is within the reading level of the child from 0 to 100.
"""


class ReadingLevel(pydantic.BaseModel):
    start_grade: str = Field(..., description="the start grade in school for the child of the reading level")
    end_grade: str = Field(..., description="the end grade in school for the child of the reading level")
    description: str = Field(..., description="the description of the reading level")


@ai_model(instructions=reading_level_context)
class ReadingLevelScore(pydantic.BaseModel):
    score: int = Field(...,
                       description="The score of how well the message is within the reading level of the child from 0 to 100")
    reading_level: str = Field(...,
                               description="The reading level of the message based on information provided about the child")
    reading_level_context: str = Field(..., description="The context of the reading level score")
    outlier_words: str = Field(..., description="words that are above the reading level of the child in the message")
