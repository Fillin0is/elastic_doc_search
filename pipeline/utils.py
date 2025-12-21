from sentence_transformers import SentenceTransformer

from config import MODEL_PATH


def len_json(file: str) -> int:
    with open(file, 'r', encoding='utf-8') as f:
        len_str = f.readlines()
    
    print(len(len_str))

def install_embed_model():
    '''Download embedding model for KNN-search'''
    model = SentenceTransformer("all-mpnet-base-v2")
    model.save(str(MODEL_PATH))
    print(f'Модель скачана в {str(MODEL_PATH)}')

def exist_index():
    pass
