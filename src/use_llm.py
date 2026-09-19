import os
from dotenv import load_dotenv
from openai import OpenAI

from src.models import PrerequisiteMap, Prerequisite


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prerequisite_map(
        target_passage: str,
        local_context: str,
        section_context: str,
        semantic_context: str,
        background: str,
    ) -> PrerequisiteMap: 
    user_input = f""" 
    TARGET PASSAGE 
    
    {target_passage} 
    
    LOCAL CONTEXT FROM THE PAPER 
    
    {local_context} 

    CONTEXT FROM THE SAME SECTION

    {section_context}
    
    OTHER SEMANTICALLY RELATED PASSAGES FROM THE PAPER 
    
    {semantic_context} 
    
    USER BACKGROUND {background}
    """ 

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=""" 
            You are part of COMPASS, a pedagogical tool for understanding scientific papers. 
            
            Your goal is NOT to explain the target passage. 
            Your goal is to identify the minimum prerequisite knowledge the user needs 
            in order to understand the target passage by themselves. 
            
            Rules:
            - Return only essential prerequisites.
            - Prefer a complete prerequisite map.
            - Do not include concepts that the user's background clearly indicates they already know.
            - Distinguish concepts explicitly present in the paper from inferred prerequisite knowledge.
            - Dependencies must be logically coherent.
            - Each prerequisite must include 1 to 3 concise search queries.
            - Each prerequisite must include one checkpoint question.
            - Do not write a course.
            - Do not provide a detailed explanation of the target passage.
            - Use source_type "explicit" only when the concept is directly mentioned in the provided paper context.
            - Use source_type "inferred" when it is not explicitly stated but is required as prerequisite knowledge
            - "A depends_on B" means that understanding B is genuinely required before learning A.
            - Do not use depends_on merely because two concepts are related or appear in the same explanation. If independant, leave depends_on empty.

            Concept naming rules: 
            - The "concept" field must contain the shortest standard name of the prerequisite concept.
            - Prefer canonical textbook terminology.
            - Prefer widely used abbreviations or canonical names when they are standard in the field.
            - Use a noun or a short noun phrase, not a sentence or an explanation (Usually 1 to 5 words).
            - Avoid adding contextual explanations if not needed to define a concept.
            - Put explanations and contextual details in the "reason" field, not in "concept".
            - The "reason" should explain why the prerequisite is needed, without teaching or explaining the prerequisite itself.
            - Keep the reason to one short sentence.
            - If a shorter established concept name exists, always prefer it.
            """, 
        input=user_input,
        text_format=PrerequisiteMap,
    )
    return response.output_parsed