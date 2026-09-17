import re


# Chunk : part of the document
# Chunking : split the document following Titles, parts etc.

def split_per_paragraphs(markdown: str) -> list[str]:
    # temporary simple function
    blocks = re.split(r"\n\s*\n", markdown)
    paragraphs = []
    for block in blocks:
        block = block.strip()
        if len(block) < 80:
            continue
        paragraphs.append(block)

    return paragraphs


# Transforming string to objects
def create_chunks(paragraphs):
    """
    Each paragraph become a numerated object

    ToDo : improvements in data in those chunks

    input
        paragraphs : list[str]
    output
        chunks : list[dict]
    """

    chunks = []
    for index, paragraph in enumerate(paragraphs):
        chunks.append({"id": index, "text": paragraph})

    return chunks