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
    Local context = targeted chunk + previous and next chunks
    Semantic context = chunks talking of the same subject

    ToDO : context using markdown titles ? (sections)
    """
    local_context = get_local_context(target_chunk["id"], chunks)
    query_embedding = embedding_model.encode([target_text])

    scores, indices = vector_index.search(query_embedding, k=5)
    local_ids = {chunk["id"] for chunk in local_context}

    semantic_context = [chunks[i] for i in indices[0] if chunks[i]["id"] not in local_ids] # eviter doublons

    return {
        "target": target_chunk,
        "local": local_context,
        "semantic": semantic_context,
    }


def transform_chunks_to_text(chunks):
    """
    chunks : list of dictionaries representing each chunk

    output : 1 string containing all context chunks
    """
    texts = []
    for chunk in chunks:
        texts.append(chunk["text"])
    return "\n\n---\n\n".join(texts)