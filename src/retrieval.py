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
    section_context = get_section_context(target_chunk, chunks)

    local_ids = {chunk["id"] for chunk in local_context}

    section_context = [ chunk for chunk in section_context if chunk["id"] not in local_ids ]
    excluded_ids = local_ids | { chunk["id"] for chunk in section_context }

    query_embedding = embedding_model.encode([target_text])
    _, indices = vector_index.search(query_embedding, k=5)

    semantic_context = [chunks[i] for i in indices[0] if chunks[i]["id"] not in excluded_ids] # eviter doublons

    return {
        "target": target_chunk,
        "local": local_context,
        "section": section_context,
        "semantic": semantic_context,
    }


def transform_chunks_to_text(chunks):
    """
    chunks : list of dictionaries representing each chunk

    output : 1 string containing all context chunks
    """
    parts = []

    for chunk in chunks:
        section = chunk.get("section", "Unknown section")

        parts.append( 
            f'[Chunk {chunk["id"]}] '
            f'[Section: {section}] '
            f'{chunk["text"]}' )

    return "\n\n---\n\n".join(parts)



def get_section_context(target_chunk, chunks, max_distance: int = 4):
    """
    If the target is in a section, Get surrounding chunks in this section
    returns : list of chunks in the same section 
    """
    target_section = target_chunk["section"]
    target_id = target_chunk["id"]

    section_chunks = [chunk for chunk in chunks if (
        chunk["section"] == target_section 
        and abs(chunk["id"] - target_id) <= max_distance
        )
    ]

    return section_chunks