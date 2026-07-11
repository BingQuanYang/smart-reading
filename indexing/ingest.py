import os
from typing import List

from config.setting import QaConfig
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile


class PdfIngestor:
    def __init__(self, config: QaConfig):
        self.config = config

    def ingest(self, pdf_bytes: bytes) -> List[Document]:
        # 二进制写入临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(pdf_bytes)
            temp.flush()
            temp_path = temp.name
        try:
            # 文档加载
            documents = self._load(temp_path)
            # 拆分
            chunks = self._split(documents)
            return chunks
        finally:
            os.unlink(temp_path)

    def _load(self, file_path: str) -> list[Document]:
        """
        加载PDF文件
        :param file_path:
        :return:
        """
        return PyMuPDFLoader(file_path=file_path).load()

    def _split(self, documents: List[Document]) -> List[Document]:
        """
        文档切分
        :param documents:
        :return:
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            is_separator_regex=True,
            separators=["(?<=。)", "(?<=！)", "(?<=？)", "(?<=：)", "(?<=，)", " ", "\n"],
        )
        return splitter.split_documents(documents)
