from docx import Document

from pathlib import Path
from datetime import datetime


def process_docx_folder(file: Path):
    try:
        doc = Document(str(file))
        full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() and para.text != ''])
        return {
            'filename': file.name,
            'filepath': str(file),
            'full_text': full_text,
            'author': doc.core_properties.author or 'Unknown', 
            'created_at': datetime.fromtimestamp(file.stat().st_ctime).isoformat()
        }
    except Exception as ex:
        print(f'Error processing {file}, {ex}')
        return None
        

def process_folder(folder_path: str) -> list[str]:
    folder = Path(folder_path)
    texts = []
    for fold in folder.iterdir():
        for file in fold.glob("*.docx"):
            result = process_docx_folder(file)
            if result:
                texts.append(result)
    return texts
