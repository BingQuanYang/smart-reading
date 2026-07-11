import hashlib


class PdfBytesStore:

    def store(self, pdf_bytes: bytes, file_hash: str) -> str:
        """
        将PDF 字节保存为临时文件
        :param pdf_bytes: PDF的原始字节数据
        :file_hash: 文件内容的MD5哈希值
        :return: 临时文件路径
        """
        temp_path = f"tem_{file_hash}.pdf"
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes)
        return temp_path

    def compute_hash(self, pdf_bytes: bytes) -> str:
        return hashlib.md5(pdf_bytes).hexdigest()
