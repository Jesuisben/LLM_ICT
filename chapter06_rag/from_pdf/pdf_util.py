"""
pdf_util.py

PDF 관련 기능

1. 업로드한 PDF 저장
2. PDF 읽기
"""

import os

from langchain_community.document_loaders import PyPDFLoader


####################################################
# PDF 저장
####################################################
def save_uploaded_pdf(uploaded_file):
    """
    Streamlit에서 업로드한 PDF를 temp 폴더에 저장

    Parameters
    ----------
    uploaded_file : UploadedFile
        st.file_uploader()가 반환한 객체

    Returns
    -------
    str
        저장된 PDF 파일 경로
    """

    os.makedirs("temp", exist_ok=True)

    pdf_path = os.path.join(
        "temp",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return pdf_path


####################################################
# PDF 읽기
####################################################
def load_pdf(pdf_path):
    """
    PDF를 읽어서 LangChain Document 리스트 반환

    Parameters
    ----------
    pdf_path : str
        PDF 파일 경로

    Returns
    -------
    list[Document]
        LangChain Document 객체 리스트
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents