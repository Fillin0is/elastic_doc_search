from sentence_transformers import SentenceTransformer

from config import EMBED_MODEL_PATH


def len_json(file: str) -> int:
    with open(file, 'r', encoding='utf-8') as f:
        len_str = f.readlines()
    
    print(len(len_str))

def install_embed_model():
    '''Download embedding model for KNN-search'''
    model = SentenceTransformer("intfloat/multilingual-e5-large")
    model.save(str(EMBED_MODEL_PATH))
    print(f'Модель скачана в {str(EMBED_MODEL_PATH)}')

def exist_index():
    pass


if __name__ == "__main__":
    install_embed_model()