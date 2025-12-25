from sentence_transformers import SentenceTransformer

from config import es, EMBED_MODEL_PATH, INDEX_NAME


def get_embedding(text: str) -> list[float]:
    model = SentenceTransformer(str(EMBED_MODEL_PATH))
    return model.encode(text)

def test_search(query: str):
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
        print(f'Filename : {hit["_source"]["filename"]}')
        print(f'Text: {hit["_source"]["chunk_text"]}')
        print(f'Score : {hit["_score"]}')
        print('*' * 50)


if __name__ == "__main__":
    test_search("текст про таможенную декларацию")