import os.path
from typing import List

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config.setting import QaConfig


class VectorStoreManager:

    def __init__(self, config: QaConfig, embeddings: DashScopeEmbeddings):
        self.__config = config
        self.__embeddings = embeddings

    def load_or_build(self, file_hash: str, chunks: List[Document] = None) -> Chroma:
        """
        加载或者构建向量数据库
        :param file_hash: PDF哈希文件名称
        :param chunks: chunks
        :return:
        """
        # 创建向量数据库
        persist_dir = os.path.join(self.__config.chroma_root_dir, file_hash)
        collection_name = f"pdf_qa_{file_hash}"
        store = Chroma(
            persist_directory=persist_dir,
            collection_name=collection_name,
            embedding_function=self.__embeddings,
            collection_metadata={"hnsw:space": "cosine"}  # 相识度算法 余弦相识度
        )
        # 如果集合存在 数据则直接返回
        if store._collection.count() > 0:
            return store
        if not chunks:
            raise ValueError("向量库不存在且未提供 chunks ")

        # 构建向量数据库
        store.add_documents(
            documents=chunks,
            ids=[f"id-{idx}" for idx in range(1, len(chunks) + 1)]
        )
        return store
