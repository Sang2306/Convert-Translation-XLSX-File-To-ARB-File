import json
import streamlit as st
import pandas as pd

st.title("Convert xlsx file to multiple separate arb files")

uploaded_file = st.file_uploader(label="Let's upload you excel language translation file",
                                 type='xlsx',
                                 key="language_file")
text_to_update = st.empty()

if st.button('Submit'):
    text_to_update.text('In processing...')
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        multilanguage = pd.read_excel(bytes_data, engine="openpyxl")
        list_columns = multilanguage.columns.to_list()
        list_columns.remove("key")

        lang: dict = {}

        for col in list_columns:
            keys = dict.fromkeys(multilanguage['key'].to_list())
            values = multilanguage[col].to_list()
            for key, value in zip(keys, values):
                lang[key] = value
            st.write(f"> Extracting for language code {col}. Done!")
            st.download_button(f'Download app_{col}.arb', file_name=f'app_{col}.arb',
                               data=json.dumps(lang, indent=4, ensure_ascii=False), mime='application/json')
        text_to_update.text('Done!')
