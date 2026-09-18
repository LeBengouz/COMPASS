"""
Récupérer le contexte utile à plusieurs niveaux (paragraphes, sous-sections etc.)
"""

def get_local_context(target_id: int, chunks: list[dict], window: int = 1):
    """
    Get previous and next paragraph. 
    Usefull after "find_target_chunk" since we have target-chunk's id 

    output : previous paragraph -> passage -> next paragraph
    """
    start = max(0, target_id - window)

    end = min(len(chunks), target_id + window + 1)

    return chunks[start:end]