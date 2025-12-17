def len_json(file: str) -> int:
    with open(file, 'r', encoding='utf-8') as f:
        len_str = f.readlines()
    
    print(len(len_str))

len_json('data/processed/data_processed.json')