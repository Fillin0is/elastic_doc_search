from elasticsearch import Elasticsearch

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent

INDEX_NAME = "alta_index"
MODEL_PATH = PROJECT_ROOT / 'models/all-mpnet-base-v2'

# non-auth:
# es = Elasticsearch('http://localhost:9200')

# auth:
es = Elasticsearch(
    'http://localhost:9200',
    basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
)