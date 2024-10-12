import os
import re
from dotenv import load_dotenv
from markdownify import markdownify
from langchain_upstage import UpstageDocumentParseLoader

load_dotenv()

# Directory for storing parsed Markdown files
output_dir = "parsed_pages"
os.makedirs(output_dir, exist_ok=True)

def remove_headers_and_footers(text):
    """Remove unnecessary headers and footers using regex."""
    lines = text.splitlines()
    cleaned_lines = [
        line for line in lines
        if not re.match(r'^(Page \d+|Document Title|Footer Text|Copyright|Licensed to:|Issue Ref:)', line, re.IGNORECASE)
    ]
    return "\n".join(cleaned_lines)

def extract_and_convert_to_markdown(pdf_path):
    """Extract content from PDF and convert to Markdown."""
    loader = UpstageDocumentParseLoader(
        pdf_path,
        split="page",
        ocr=True,
        coordinates=True
    )
    documents = loader.load()
    markdown_pages = []

    for i, doc in enumerate(documents, start=1):
        print(f"Processing document {i}")
        print(f"Document attributes: {dir(doc)}")
        
        # Access page_content
        if hasattr(doc, 'page_content'):
            content = doc.page_content
        else:
            print(f"Warning: Unable to extract content from document {i}")
            continue

        # Clean and convert text to Markdown
        cleaned_text = remove_headers_and_footers(content)
        markdown_text = markdownify(cleaned_text)

        # Handle metadata
        page_number = i
        if hasattr(doc, 'metadata'):
            print(f"Metadata: {doc.metadata}")
            page_number = doc.metadata.get("page_number", i)

        # Append tables and figures in Markdown format (if applicable)
        if hasattr(doc, 'chunks'):
            for element in doc.chunks:
                if element.type == "table":
                    markdown_text += f"\n\n{markdownify(element.text)}\n"
                elif element.type == "figure":
                    markdown_text += f'\n\n<figure><img src="{element.src}" alt="Figure from page {page_number}"></figure>\n'

        markdown_pages.append({
            "page": page_number,
            "markdown": markdown_text
        })

    return markdown_pages

# Extract and save content as Markdown files
pdf_path = "datasets/example_pdf.pdf"
markdown_pages = extract_and_convert_to_markdown(pdf_path)

for page in markdown_pages:
    output_path = os.path.join(output_dir, f"page_{page['page']}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page['markdown'] + "\n\n")
    print(f"Page {page['page']} data saved to {output_path}.")