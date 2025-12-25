from elasticsearch import Elasticsearch

import os
from pathlib import Path


INDEX_NAME = "alta_index"

# inside Docker: /app/models/...
# local: ../models/... от api/
EMBED_MODEL_PATH = Path(__file__).parent / 'models/multilingual-e5-large'

# non-auth:
# es = Elasticsearch('http://localhost:9200')

# auth:
es = Elasticsearch(
    'http://elasticsearch:9200',
    basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
)