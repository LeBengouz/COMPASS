from src.pdf_parser import pdf_to_markdown

text = pdf_to_markdown("data/papers/attention_is_all_you_need.pdf")

print(text[:5000])