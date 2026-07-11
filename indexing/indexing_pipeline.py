"""
构建索引流水线:PDF ->切分->Embedding->持久化Chroma
 输出: file_hash
"""
from langchain_community.embeddings import DashScopeEmbeddings

from config.setting import QaConfig
from indexing.storeage import PdfBytesStore
from indexing.ingest import PdfIngestor
from indexing.vectorstorage import VectorStoreManage


class IndexingPipeline:
    def __init__(self, config: QaConfig):
        self.config = config
        self.store = PdfBytesStore()
        self.ingest = PdfIngestor(config)

    def build_from_bytes(self, pdf_bytes, dashscope_api_key: str) -> str:
        # 1.存储临时文件 计算hash,并存储
        file_hash = self.store.compute_hash(pdf_bytes)
        self.store.store(pdf_bytes, file_hash)
        # 2. 加载 & 切分文档
        chunks = self.ingest.ingest(pdf_bytes)
        # 3.构建 / 加载向量库 (传入 chunks 会新建)
        embeddings = DashScopeEmbeddings(
            model=self.config.embedding_model,
            dashscope_api_key=dashscope_api_key
        )
        vector_store = VectorStoreManage(self.config, embeddings)
        # 存储chunks
        vector_store.load_or_build(file_hash, chunks=chunks)
        return file_hash

    def build_from_file(self, pdf_path: str, dashscope_api_key: str) -> str:
        """
        从文件路劲构建索引
        :param pdf_path:
        :param dashscope_api_key:
        :return:
        """
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return self.build_from_bytes(pdf_bytes, dashscope_api_key)
