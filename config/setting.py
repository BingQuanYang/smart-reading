from dataclasses import dataclass


@dataclass(frozen=True)
class QaConfig:
    # 1.大模型相关参数
    # 1.1通义千问大模型
    llm_model: str = "qwen3-max"
    # 1.2温度参数
    llm_temperature: float = 0.2

    # 2.Embedding 配置
    # 向量模型
    embedding_model: str = "text-embedding-v1"
    # chunk大小(字符数)
    chunk_size: int = 800
    # chunk重叠字符数
    chunk_overlap: int = 120

    # 3.送入LLM的上下文最大长度
    context_max_chars: int = 1024
    # 4.chroma
    chroma_root_dir: str = ".chroma"
