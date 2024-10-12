import os
import json
from dotenv import load_dotenv
import ast
from bs4 import BeautifulSoup


# Load environment variables
load_dotenv()
os.environ["UPSTAGE_API_KEY"] = os.getenv('UPSTAGE_API_KEY')

from llama_index.readers.upstage import UpstageLayoutAnalysisReader

file_path = "datasets/divided/page_1.pdf"

reader = UpstageLayoutAnalysisReader(
    use_ocr=True, exclude=["header", "footer"]
)

docs = reader.load_data(
    file_path=file_path, 
    split="element"
)

processed_data = []

for doc in docs:
    item = {}
    item['id'] = doc.id_
    item['page'] = doc.metadata.get('page', None)
    
    # 요소의 타입을 결정합니다.
    text_content = doc.text.strip()
    if '<h1' in text_content:
        item['type'] = 'heading'
    elif '<p' in text_content:
        # 스타일이나 카테고리를 통해 세부 타입 결정
        if 'data-category=\'paragraph\'' in text_content:
            if 'font-size:18px' in text_content:
                item['type'] = 'subheading'
            else:
                item['type'] = 'paragraph'
        else:
            item['type'] = 'paragraph'
    elif '<table' in text_content:
        item['type'] = 'table'
    elif '<img' in text_content or '<figure' in text_content:
        item['type'] = 'figure'
    else:
        item['type'] = 'paragraph'  # 기본값
    
    # bounding_box를 파싱하여 리스트로 변환합니다.
    bounding_box_str = doc.metadata.get('bounding_box', '[]')
    bounding_box = ast.literal_eval(bounding_box_str)
    item['bounding_box'] = bounding_box

    # 필요한 텍스트나 콘텐츠를 추출합니다.
    if item['type'] in ['heading', 'subheading', 'paragraph', 'footer']:
        # 태그를 유지하여 HTML로 저장합니다.
        item['html'] = text_content
        # 텍스트만 필요한 경우를 위해 추가적으로 추출합니다.
        soup = BeautifulSoup(text_content, 'html.parser')
        item['text'] = soup.get_text(separator='\n')
    elif item['type'] in ['table', 'figure']:
        # 비문단 요소의 경우 감지된 OCR 내용을 HTML로 저장합니다.
        item['html'] = text_content
        # 필요에 따라 추가 처리를 수행할 수 있습니다.
    else:
        # 기타 요소의 경우에도 HTML로 저장합니다.
        item['html'] = text_content

    processed_data.append(item)

# 결과를 JSON 파일로 저장합니다.
with open('processed_data.json', 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)