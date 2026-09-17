from rapidfuzz import fuzz

# GOAL : find exact passage in the text
def find_target_chunk(target: str, chunks: list[dict]) -> tuple[dict | None, float]:
    best_chunk = None
    best_score = 0

    for chunk in chunks:
        score = fuzz.partial_ratio(target.lower(), chunk["text"].lower())
        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk, best_score