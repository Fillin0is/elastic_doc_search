from sentence_transformers import SentenceTransformer
import json

from config import RAW_DATA, MODEL_PATH
from clean import clean_data


def chunk_text(text: str, chunk_size: int = 50, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        if len(chunk_words) > 50:
            chunk = ' '.join(chunk_words)
            chunks.append(chunk)

    return chunks if chunks else [text]


def process_documents_with_chunks(documents: dict[dict]) -> dict[dict]:
    processed = []

    for doc in documents:
        doc_id = doc['filepath']
        text = doc['full_text']
        chunks = chunk_text(text, chunk_size=400, overlap=50)
    
        for idx, chunk in enumerate(chunks):
            chunk_doc = {
                'doc_id': doc_id,
                'chunk_id': f'{doc_id}_chunk{idx}',
                'chunk_index': idx,
                'total_chunks': len(chunks),

                'filename': doc['filename'],
                'filepath': doc['filepath'],
                'author': doc['author'],
                'created_at': doc['created_at'],

                'chunk_text': chunk
            }
            processed.append(chunk_doc)
        
    return processed
    

def generate_embeddings(chunks, model_path=MODEL_PATH, batch_size=32):
    print(f'Loading model from {model_path}')
    model = SentenceTransformer(model_path)

    texts = [chunk['chunk_text'] for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True # Normalisation for cosine similarity
    )

    for chunk, embedding in zip(chunks, embeddings):
        chunk['text_vector'] = embedding.tolist()
    
    return chunks


if __name__ == '__main__':
    # 1. Loading and cleaning data
    print("Loading and cleaning documents...")
    data_documents = clean_data(RAW_DATA)
    print(f'Loaded {len(data_documents)} documents')

    # 2. Chunking data
    print('Chunking documents...')
    chunks = process_documents_with_chunks(data_documents)
    print(f'Created {len(chunks)} chunks')

    # 3. Generating embeddings
    chunks_with_embeddings = generate_embeddings(chunks)

    # 4. Saving
    with open('data/processed/data_processed.json', 'w', encoding='utf-8') as f:
        json.dump(chunks_with_embeddings, f, indent=4, ensure_ascii=False)

    print('Data saved!')
