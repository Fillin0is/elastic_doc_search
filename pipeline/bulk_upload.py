import json

from config import es, PROCESSED_DATA, INDEX_NAME
from mapping import MAPPING, INDEX_SETTINGS


def create_index():
    """Создать индекс с маппингом (удаляет старый если есть)"""
    es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    
    es.indices.create(
        index=INDEX_NAME, 
        settings=INDEX_SETTINGS, 
        mappings=MAPPING
    )
    print(f"Index '{INDEX_NAME}' created")


def bulk_upload(batch_size=100):
    """Загрузить данные в Elasticsearch"""
    with open(PROCESSED_DATA, 'r', encoding='utf-8') as f:
        processed_data = json.load(f)

    total_indexed = 0

    for i in range(0, len(processed_data), batch_size):
        batch = processed_data[i:i+batch_size]

        operations = []
        for doc in batch:
            operations.append({'index': {'_index': INDEX_NAME}})
            operations.append(doc)

        response = es.bulk(operations=operations)

        if response['errors']:
            print(f'Batch {i // batch_size}: Error')
            for item in response['items']:
                if 'error' in item['index']:
                    print(f"  {item['index']['error']}")
        else:
            print(f'Batch {i // batch_size} OK ({len(batch)} docs)')

        total_indexed += len(batch)

    print(f'\nTotal indexed: {total_indexed}')
    return total_indexed


if __name__ == '__main__':
    create_index()
    bulk_upload()