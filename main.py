import streamlit as st
import pandas as pd
import csv

from transforms import change_date_format

st.set_page_config(page_title="Raiffeisen Account CSV processor", page_icon=":chart:")
st.title("Raiffeisen Account CSV processor")
st.subheader("Upload your CSV file")

transforms = {
    'Könyvelés dátuma': lambda x: change_date_format(x),
    'Értéknap': lambda x: change_date_format(x)
}

drop_columns = ['Típus']

rows_to_skip = 0
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
    content = uploaded_file.getvalue().decode("latin-1").splitlines()
    reader = csv.reader(content, delimiter=';', quotechar='"')
    for i, row in enumerate(reader):
        if "Könyvelt tételek" in row:
            rows_to_skip = i + 1

    df = pd.read_csv(uploaded_file, sep=";", encoding="latin-1", skiprows=rows_to_skip)
    df = df[df['Összeg'].notna()]
    df.drop(columns=drop_columns, inplace=True)

    for column, fn in transforms.items():
        if column in df.columns:
            df[column] = df[column].apply(fn)


    st.markdown("---")
    st.dataframe(df)