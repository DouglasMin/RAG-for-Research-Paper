from langchain_upstage import UpstageLayoutAnalysisLoader
import os

# 파일 경로
file_path = "example_pdf.pdf"

# 문서 로더 설정
loader = UpstageLayoutAnalysisLoader(
    file_path,
    output_type="text",
    split="page",
    use_ocr=True,
    exclude=["header", "footer"],
)

# 문서 로드
docs = loader.load()

# 결과 출력 및 Markdown 파일로 저장
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for i, doc in enumerate(docs):
    print(doc)
    
    # Markdown 파일로 저장
    output_file = os.path.join(output_dir, f"page_{i+1}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Page {i+1}\n\n")
        f.write(doc.page_content)

print(f"처리된 페이지가 {output_dir} 디렉토리에 저장되었습니다.")