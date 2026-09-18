import re


# Chunk : part of the document
# Chunking : split the document following Titles, parts etc.

def split_per_paragraphs(markdown: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", markdown)
    paragraphs = []
    current_section = "Unknown section"
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # dernier titre de section
        if re.match(r"^#{1,6}\s+", block):
            current_section = re.sub(r"^#{1,6}\s+", "", block).strip()

            continue
        if len(block) < 80:
            continue
        
        paragraphs.append({"text": block, "section": current_section})

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
        chunks.append({"id": index, "text": paragraph["text"], "section": paragraph["section"]})

    return chunks