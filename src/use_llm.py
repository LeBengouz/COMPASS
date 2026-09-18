import os
from dotenv import load_dotenv
from openai import OpenAI

from src.models import PrerequisiteMap, Prerequisite


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prerequisite_map(
        target_passage: str,
        local_context: str,
        semantic_context: str,
        background: str,
    ) -> PrerequisiteMap: 
    user_input = f""" 
    TARGET PASSAGE 
    
    {target_passage} 
    
    LOCAL CONTEXT FROM THE PAPER 
    
    {local_context} 
    
    SEMANTICALLY RELATED PASSAGES FROM THE PAPER 
    
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
            - Prefer a short prerequisite map.
            - Do not include concepts that the user's background clearly indicates they already know.
            - Distinguish concepts explicitly present in the paper from inferred prerequisite knowledge.
            - Dependencies must be logically coherent.
            - Each prerequisite must include 1 to 3 concise search queries.
            - Each prerequisite must include one checkpoint question.
            - Do not write a course.
            - Do not provide a detailed explanation of the target passage.

            Concept naming rules: 
            - The "concept" field must contain the shortest standard name of the prerequisite concept.
            - Prefer canonical textbook terminology.
            - Use a noun or a short noun phrase, not a sentence or an explanation.
            - Usually use 1 to 5 words.
            - Avoid adding contextual explanations if not needed to define a concept.
            - Put explanations and contextual details in the "reason" field, not in "concept".
            - If a shorter established concept name exists, always prefer it.
            """, 
        input=user_input,
        text_format=PrerequisiteMap,
    )
    return response.output_parsed