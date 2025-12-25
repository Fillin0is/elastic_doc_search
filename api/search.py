from sentence_transformers import SentenceTransformer

from config import es, INDEX_NAME, EMBED_MODEL_PATH


def get_embedding(query: str) -> list[float]:
    model = SentenceTransformer(str(EMBED_MODEL_PATH))
    return model.encode(query)

def search_documents(query: str):
    query_embedding = get_embedding(query)

    result = es.search(
        index=INDEX_NAME,
        query={
            "match": {
                "chunk_text": query
            }
        },
        knn={
            "field": "text_vector",
            "query_vector": query_embedding,
            "num_candidates": 100, 
            "k": 10
        },
        size=5,
        highlight={
            "fields": {
                "chunk_text": {
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"],
                    "fragment_size": 500,
                    "number_of_fragments": 0
                }
            }
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
                "best_score": round(hit["_score"], 2),
                "chunks": []
            }
        documents[doc_id]["chunks"].append({
            "chunk_text": hit["_source"]["chunk_text"],
            "chunk_index": hit["_source"]["chunk_index"],
            "score": round(hit["_score"], 2),
            "highlights": hit.get("highlight", {}).get("chunk_text", []),
            "is_knn_only": not bool(hit.get("highlight", {}).get("chunk_text", []))
        })

    return sorted(documents.values(), key=lambda x: x["best_score"], reverse=True)

def get_document_chunks(knn_documents: dict):
    full_documents = {}
    for document in knn_documents:

        highlighted_chunks = {}
        knn_only_chunks = {}
        for chunk in document["chunks"]:
            print(f"chunk {chunk['chunk_index']}: highlights={bool(chunk['highlights'])}, is_knn_only={chunk['is_knn_only']}")
            print(f"chunk {chunk['chunk_index']}: highlights={chunk['highlights'][:100] if chunk['highlights'] else 'empty'}")
            if chunk["highlights"]:
                highlighted_chunks[chunk["chunk_index"]] = chunk["highlights"][0]
            elif chunk["is_knn_only"]:
                knn_only_chunks[chunk["chunk_index"]] = chunk["chunk_text"]

        print(f"highlighted_chunks: {list(highlighted_chunks.keys())}")
        print(f"knn_only_chunks: {list(knn_only_chunks.keys())}")

        result = es.search(
            index=INDEX_NAME,
            query={"term": {"doc_id": document["doc_id"]}},
            sort=[{"chunk_index": "asc"}],
            size=100
        )

        full_text_parts = []
        for hit in result.body["hits"]["hits"]:
            idx = hit["_source"]["chunk_index"]
            if idx in highlighted_chunks:
                full_text_parts.append(highlighted_chunks[idx])
            elif idx in knn_only_chunks:
                full_text_parts.append(f'<mark>{knn_only_chunks[idx]}</mark>')
            else:
                full_text_parts.append(hit["_source"]["chunk_text"])

        full_documents[document["doc_id"]] = {
            "doc_id": document["doc_id"],
            "filename": document["filename"],
            "score": document["best_score"],
            "full_text": ' '.join(full_text_parts)
        }

    return full_documents


if __name__ == '__main__':
    results = search_documents('Таможенная декларация Российской Федерации')

    full = get_document_chunks(results)

    for data in full.values():
        print(data)
        print()