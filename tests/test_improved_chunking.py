from src.pdf_parser import pdf_to_markdown
from src.chunking import split_per_paragraphs, create_chunks


markdown = pdf_to_markdown("data/papers/attention_is_all_you_need.pdf")

paragraphs = split_per_paragraphs(markdown)
chunks = create_chunks(paragraphs)

for chunk in chunks[:20]:

    print(
        chunk["id"],
        "->",
        chunk["section"]
    )

    print(
        chunk["text"][:100]
    )

    print()