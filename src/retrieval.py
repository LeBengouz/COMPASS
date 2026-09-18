"""
Récupérer le contexte utile à plusieurs niveaux (paragraphes, sous-sections etc.)
"""

def get_local_context(target_id: int, chunks: list[dict], window: int = 1):
    """
    Get previous and next paragraph = strcutural context (according to document)
    Usefull after "find_target_chunk" since we have target-chunk's id 

    output : previous paragraph -> passage -> next paragraph
    """
    start = max(0, target_id - window)
    end = min(len(chunks), target_id + window + 1)

    return chunks[start:end]


def retrieve_context(target_text, target_chunk, chunks, embedding_model, vector_index):
    """
    Get strcutural AND semantic context
    semantic context = chunks talking of the same subject

    ToDO : context using markdown titles ? (sections)
    """
    local_context = get_local_context(target_chunk["id"], chunks)
    query_embedding = embedding_model.encode([target_text])

    scores, indices = vector_index.search(query_embedding, k=5)
    semantic_context = [chunks[i] for i in indices[0]]

    return {
        "target": target_chunk,
        "local": local_context,
        "semantic": semantic_context,
    }