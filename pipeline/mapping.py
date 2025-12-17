INDEX_SETTINGS = {
    "index": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}


MAPPING = {
    'properties': {
        'doc_id': {'type': 'keyword'},
        'chunk_id': {'type': 'keyword'},
        'chunk_index': {'type': 'integer'},
        'total_chunks': {'type': 'integer'},

        'filename': {'type': 'keyword', 'ignore_above': 256},
        'filepath': {'type': 'keyword', 'ignore_above': 512},
        'author': {'type': 'keyword', 'ignore_above': 128},
        'created_at': {'type': 'date'},

        'chunk_text': {
            'type': 'text',
            'analyzer': 'russian',
            'fields': {
                'keyword': {'type': 'keyword', 'ignore_above': 256}
            }
        },

        'text_vector': {
            'type': 'dense_vector',
            'dims': 768,
            'index': True,
            'similarity': 'cosine'
        }
    }
}
