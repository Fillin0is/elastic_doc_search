import streamlit as st

import requests


API_URL = "http://api:8000"

st.markdown("""
<style>
mark { background-color: yellow; }
mark.knn { background-color: lightblue; }
</style>
""", unsafe_allow_html=True)

st.title("Альта-Поиск")

query = st.text_input("Введите запрос:")

if st.button("Искать"):
    response = requests.get(f"{API_URL}/search", params={"query": query})

    if response.status_code == 200:
        documents = response.json()

        for doc_data in documents.values():
            with st.expander(f'Файл: {doc_data["filename"]}, Результат совпадения: {doc_data["score"]}'):
                st.markdown(doc_data["full_text"], unsafe_allow_html=True)
    else:
        st.error("Ошибка при поиске")