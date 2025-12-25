from elasticsearch import Elasticsearch

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent

RAW_DATA = PROJECT_ROOT / "data/raw"
EMBED_MODEL_PATH = PROJECT_ROOT / 'models/multilingual-e5-large'
PROCESSED_DATA = PROJECT_ROOT / "data/processed/data_processed.json"

INDEX_NAME = "alta_index"

# non-auth:
# es = Elasticsearch('http://localhost:9200')

# auth:
es = Elasticsearch(
    'http://localhost:9200',
    basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
)