import os
from elasticsearch import Elasticsearch

RAW_DATA = "data/raw"
MODEL_PATH = 'models/all-mpnet-base-v2'
PROCESSED_DATA = "data/processed/data_processed.json"

INDEX_NAME = "alta_index"

# non-auth:
# es = Elasticsearch('http://localhost:9200')

# auth:
es = Elasticsearch(
    'http://localhost:9200',
    basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
)