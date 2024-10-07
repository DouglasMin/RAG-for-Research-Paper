#LLamaParse를 이용하는 방법
#PDF -> MD파일로 변환 후

'''
딜레마.
PDF 파일은 항상 텍스트만 있는 것이 아님
도표나 그래프 등 단순 OCR로는 추출할 수 없는 데이터가 존재

이러한 것들을
1. 인식
2. 도표를 텍스트화 한 다음 똑같은 위치에 넣기
3. 도표 내용을 요약한 것을 텍스트로 변환 후 동일한 위치에 삽입?

마크 다운 형식으로 표현하면 좋을 듯

'''

# LLamaParser 사용

import os
import nest_asyncio
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# 파서 설정
parser = LlamaParse(
    result_type="markdown",  # "markdown"과 "text" 사용 가능
    num_workers=8,  # worker 수 (기본값: 4)
    verbose=True,
    language="en",
)

# SimpleDirectoryReader를 사용하여 파일 파싱
file_extractor = {".pdf": parser}

# LlamaParse로 파일 파싱
documents = SimpleDirectoryReader(
    input_files=["datasets/example_pdf.pdf"],
    file_extractor=file_extractor,
).load_data()

print(documents)

# Save parsed data as a markdown file
output_path = "parsed_output.md"

with open(output_path, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc.text + "\n\n")

print(f"Parsed data has been saved to {output_path}")