import os

from config.setting import QaConfig
from indexing.indexing_pipeline import IndexingPipeline

config = QaConfig()
indexing_pipeline = IndexingPipeline(config)
pdf_path = "E:\project\py\smart-reading\data\sample_document.pdf"

file_hash = indexing_pipeline.build_from_file(pdf_path, os.getenv("DASHSCOPE_API_KEY"))

print(f"索引构建完成,file_hash:{file_hash}")

