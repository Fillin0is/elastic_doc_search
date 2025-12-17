from parse_docx_documents import process_folder


def clean_data(folder_path: str):
    data_documents = process_folder(folder_path)

    for document in data_documents:
        document['full_text'] = document['full_text'].replace('\n', ' ').replace('\xa0', '')

    return data_documents