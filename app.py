import streamlit as st
import pandas as pd
import io


def make_excel(table, keyword):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        table.to_excel(writer, sheet_name=f'Genes_{keyword}', index=False)

    return buffer


# --- Inicio ---
st.set_page_config(page_title='Sal da Terra Database', layout='wide')

st.markdown("""
        <style>
                #MainMenu {visibility: hidden; }
                footer {visibility: hidden;}
                .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.title('Dados Gliricidia e Beldroega')

st.subheader('Os dados foram anotados pelo BlastKOALA')

#------------------------------------------
col_a, col_b = st.columns(2)
# --- Upload Gliricidia ---
gliricidia = col_a.file_uploader('Insira o arquivo de Gliricidia', accept_multiple_files=False)
# --- Upload Beldroega ---
beldroega = col_b.file_uploader('Insira o arquivo de Beldroega', accept_multiple_files=False)
#------------------------------------------

keyword = st.text_input('Qual palavra procurar nas definições?', '')

col1, col2 = st.columns(2)
# --- Coluna 1 - Gliricidia
with col1:
    if gliricidia:
        gliri = pd.read_csv(gliricidia)
        search_gliri = gliri.loc[gliri['KO_Definition'].str.contains(keyword, case=False)].copy()
        search_gliri.sort_values(by='KO_Definition', inplace=True)
        search_gliri.reset_index(drop=True, inplace=True)

        st.write(f'Há um total de {search_gliri.shape[0]} genes com a palavra: "{keyword}" em Gliricídia.')

        st.write(search_gliri)

        excel_gliri = make_excel(search_gliri, keyword)

        st.download_button(label=f'Download {keyword} Genes em Gliricidia',
                           data=excel_gliri,
                           file_name=f'Download_{keyword}_Genes.xlsx',
                           mime="application/vnd.ms-excel")

# --- Coluna 2 - Beldroega
with col2:
    if beldroega:
        beld = pd.read_csv(beldroega)
        search_beld = beld.loc[beld['KO_Definition'].str.contains(keyword, case=False)].copy()
        search_beld.sort_values(by='KO_Definition', inplace=True)
        search_beld.reset_index(drop=True, inplace=True)

        st.write(f'Há um total de {search_beld.shape[0]} genes com a palavra: "{keyword}" em Beldroega.')

        st.write(search_beld)

        excel_beld = make_excel(search_beld, keyword)

        st.download_button(label=f'Download {keyword} Genes em Beldroega',
                           data=excel_beld,
                           file_name=f'Download_{keyword}_Genes.xlsx',
                           mime="application/vnd.ms-excel")
