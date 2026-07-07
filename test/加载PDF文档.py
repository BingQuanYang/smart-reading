from langchain_community.document_loaders import PyMuPDFLoader

pdf_path = '../data/sample_document.pdf'
pdf_loader = PyMuPDFLoader(pdf_path)
docs = pdf_loader.load()
print(type(docs))  # <class 'list'>
print(len(docs))  # 6
print(type(docs[0]))  # <class 'langchain_core.documents.base.Document'>

"""
page_content: 内容
metadata:元数据
"""

for doc in docs:
    print(doc)
