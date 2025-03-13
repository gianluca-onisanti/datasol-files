import streamlit as st
import tempfile
import os
import zipfile
import io
from datetime import datetime
from utils import *

st.set_page_config(page_title="Datasol Files", page_icon='assets/favicon.ico')

with open('assets/styles.css', 'r') as f:
    css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Menu lateral com botões
st.sidebar.image("assets/datasol_files.png", width=235)

if st.sidebar.button("Conversor PDF para PDF/A"):
    st.session_state.page = "01"
if st.sidebar.button("Assinatura de Arquivos"):
    st.session_state.page = "02"
if st.sidebar.button("Página 3"):
    st.session_state.page = "03"
if st.sidebar.button("Página 4"):
    st.session_state.page = "04"

# Inicializa a página padrão
if 'page' not in st.session_state:
    st.session_state.page = "01"

if st.session_state.page == "01":
    st.title("Conversor PDF para PDF/A")

    uploaded_files = st.file_uploader(
        label="Carregue um ou mais PDFs",
        type=["pdf"],
        help="Apenas arquivos PDF são permitidos",
        accept_multiple_files=True,
    )

    if uploaded_files:
        pdfa_files = []
        temp_files = []

        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_input:
                tmp_input.write(uploaded_file.getvalue())
                input_path = tmp_input.name
                temp_files.append(input_path)

            output_path = input_path.replace(".pdf", "_pdfa.pdf")
            result = convert_to_pdfa(input_path, output_path)

            if result.returncode == 0:
                pdfa_files.append((uploaded_file.name.replace(".pdf", "_PDF-A.pdf"), output_path))
            else:
                st.error(f"Falha na conversão de {uploaded_file.name}")
                st.code(result.stderr)

        if pdfa_files:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for file_name, file_path in pdfa_files:
                    zip_file.write(file_path, file_name)

            zip_buffer.seek(0)
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.download_button(
                label="Baixar ZIP com PDFs/A",
                data=zip_buffer,
                file_name=f"Conversão_{now}.zip",
                mime="application/zip",
            )

        # Limpeza dos arquivos temporários
        for temp_file in temp_files:
            os.unlink(temp_file)
        for _, file_path in pdfa_files:
            os.unlink(file_path)

elif st.session_state.page == "02":
    st.title("Assinatura de Arquivos")
    st.write("...")

elif st.session_state.page == "03":
    st.title("Página 3")
    st.write("...")

elif st.session_state.page == "04":
    st.title("Página 4")
    st.write("...")