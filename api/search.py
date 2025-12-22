from sentence_transformers import SentenceTransformer

from config import es, INDEX_NAME, MODEL_PATH


def get_embedding(query: str) -> list[float]:
    model = SentenceTransformer(str(MODEL_PATH))
    return model.encode(query)

def search_documents(query: str):
    query_embedding = get_embedding(query)

    result = es.search(
        index=INDEX_NAME,
        knn={
            'field': 'text_vector',
            'query_vector': query_embedding,
            'num_candidates': 100, 
            'k': 5 
        }
    )

    hits = result.body["hits"]["hits"]

    documents = {}
    for hit in hits:
        doc_id = hit["_source"]["doc_id"]
        if doc_id not in documents:
            documents[doc_id] = {
                "doc_id": doc_id,
                "filename": hit["_source"]["filename"],
                "best_score": hit["_score"],
                "chunks": []
            }
        documents[doc_id]["chunks"].append({
            "chunk_text": hit["_source"]["chunk_text"],
            "chunk_index": hit["_source"]["chunk_index"],
            "score": hit["_score"]
        })

    return sorted(documents.values(), key=lambda x: x["best_score"], reverse=True)

def get_document_chunks(knn_documents: dict):
    full_documents = {}
    for document in knn_documents:
        result = es.search(
            index=INDEX_NAME,
            query={"term": {"doc_id": document["doc_id"]}},
            sort=[{"chunk_index": "asc"}],
            size=100
        )

        full_documents[document["doc_id"]] = {
            "doc_id": document["doc_id"],
            "filename": document["filename"],
            "score": document["best_score"],
            "full_text": result.body["hits"]["hits"]
        }

    return full_documents

if __name__ == '__main__':
    results = search_documents('Таможенная декларация Российской Федерации')
    print("RESULT")
    print(results)
    print()

    full = get_document_chunks(results)
    print()
    print(full)