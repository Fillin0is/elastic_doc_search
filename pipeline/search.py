from sentence_transformers import SentenceTransformer

from config import es, MODEL_PATH, INDEX_NAME


def get_embedding(text: str) -> list[float]:
    model = SentenceTransformer(str(MODEL_PATH))
    return model.encode(text)

query = "текст про таможенную декларацию"
embedded_query = get_embedding(query)

result = es.search(
    index=INDEX_NAME,
    knn={
        'field': 'text_vector',
        'query_vector': embedded_query,
        'num_candidates': 100,
        'k': 3,
    }
)

hits = result.body["hits"]["hits"]
for hit in hits:
    print(f'Filename : {hit["_source"]["title"]}')
    print(f'Text: {hit["_source"]["content"]}')
    print(f'Score : {hit["_score"]}')
    print('*' * 50)