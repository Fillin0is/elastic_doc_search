import os
from pathlib import Path
from elasticsearch import Elasticsearch


PROJECT_ROOT = Path(__file__).parent.parent

RAW_DATA = PROJECT_ROOT / "data/raw"
MODEL_PATH = PROJECT_ROOT / 'models/all-mpnet-base-v2'
PROCESSED_DATA = PROJECT_ROOT / "data/processed/data_processed.json"

INDEX_NAME = "alta_index"

# non-auth:
# es = Elasticsearch('http://localhost:9200')

# auth:
es = Elasticsearch(
    'http://localhost:9200',
    basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
)