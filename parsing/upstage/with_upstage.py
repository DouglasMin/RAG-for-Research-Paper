import os
from dotenv import load_dotenv
from langchain_upstage import UpstageDocumentParseLoader

# 환경 변수 로드
load_dotenv()

# UpstageDocumentParseLoader 사용을 위한 API 키 설정
os.environ["UPSTAGE_API_KEY"] = os.getenv("UPSTAGE_API_KEY")

# 파일 경로 설정 (기존 PDF 파일 사용)
pdf_path = "example_pdf.pdf"
loader = UpstageDocumentParseLoader(
    file_path=pdf_path,
    ocr="auto",  # OCR 옵션 설정
    coordinates=True,  # 레이아웃 요소의 바운딩 박스 좌표 반환
    output_format="html",  # 출력 형식 설정
)

# 문서 로드
documents = loader.load()

# 각 페이지별로 HTML 파일로 저장
output_dir = "parsed_pages_html"
os.makedirs(output_dir, exist_ok=True)

for i, doc in enumerate(documents):
    output_path = os.path.join(output_dir, f"page_{i+1}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc.page_content)
    print(f"페이지 {i+1}의 데이터가 {output_path}에 저장되었습니다.")