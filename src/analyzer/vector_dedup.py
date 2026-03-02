"""向量去重模块 - 基于语义相似度的去重"""
import os
import logging
import numpy as np
from typing import List, Optional
import pickle

logger = logging.getLogger(__name__)

# 使用国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'


class VectorDedup:
    """向量去重器
    
    使用 sentence-transformers 将文本编码为向量，
    通过余弦相似度检测重复内容。
    """
    
    def __init__(self, model_name: str = None):
        """初始化向量去重器
        
        Args:
            model_name: 模型名称，默认优先使用 Qwen2.5-0.5B-Instruct，
                       fallback 到 paraphrase-multilingual-MiniLM-L12-v2
        """
        self.model = None
        self.model_name = model_name
        self._initialized = False
        
    def _lazy_init(self):
        """延迟初始化模型（只在第一次使用时加载）"""
        if self._initialized:
            return
            
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            logger.error("sentence-transformers 未安装，请运行: pip install sentence-transformers")
            raise
        
        # 尝试加载优先模型
        # 主模型为多语言模型，fallback 为中文专用模型
        models_to_try = [
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",  # 主模型
            "shibing624/text2vec-base-chinese",  # 中文 fallback
        ]
        
        if self.model_name:
            models_to_try.insert(0, self.model_name)
        
        for model_name in models_to_try:
            try:
                logger.info(f"尝试加载模型: {model_name}")
                self.model = SentenceTransformer(model_name, trust_remote_code=True)
                self.model_name = model_name
                logger.info(f"✓ 成功加载模型: {model_name}")
                break
            except Exception as e:
                logger.warning(f"✗ 加载模型 {model_name} 失败: {e}")
                continue
        
        if not self.model:
            raise RuntimeError("无法加载任何向量模型")
        
        self._initialized = True
    
    def encode(self, text: str) -> Optional[bytes]:
        """将文本编码为向量
        
        Args:
            text: 要编码的文本
        
        Returns:
            向量的字节表示（用于数据库存储），失败返回 None
        """
        if not text or not text.strip():
            return None
            
        try:
            self._lazy_init()
            
            # 编码为向量
            embedding = self.model.encode(text.strip(), convert_to_numpy=True)
            
            # 转换为 bytes 存储（使用 pickle）
            return pickle.dumps(embedding)
            
        except Exception as e:
            logger.error(f"文本编码失败: {e}")
            return None
    
    def decode(self, embedding_bytes: bytes) -> Optional[np.ndarray]:
        """从字节解码向量
        
        Args:
            embedding_bytes: 存储的向量字节
        
        Returns:
            numpy 数组，失败返回 None
        """
        try:
            return pickle.loads(embedding_bytes)
        except Exception as e:
            logger.error(f"向量解码失败: {e}")
            return None
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算两个向量的余弦相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
        
        Returns:
            相似度分数 [0, 1]
        """
        # 确保是 numpy 数组
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        # 计算余弦相似度
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def check_duplicate(
        self, 
        new_embedding: bytes, 
        existing_embeddings: List[bytes], 
        threshold: float = 0.95
    ) -> bool:
        """检查新向量是否与已有向量重复
        
        Args:
            new_embedding: 新向量（字节格式）
            existing_embeddings: 已有向量列表（字节格式）
            threshold: 相似度阈值，超过此值视为重复
        
        Returns:
            True 表示重复，False 表示不重复
        """
        if not existing_embeddings:
            return False
        
        # 解码新向量
        new_vec = self.decode(new_embedding)
        if new_vec is None:
            return False
        
        # 与每个已有向量比较
        for existing_emb in existing_embeddings:
            existing_vec = self.decode(existing_emb)
            if existing_vec is None:
                continue
            
            similarity = self.cosine_similarity(new_vec, existing_vec)
            
            if similarity >= threshold:
                logger.debug(f"发现重复内容，相似度: {similarity:.3f}")
                return True
        
        return False


# 全局单例
_vector_dedup_instance = None


def get_vector_dedup() -> VectorDedup:
    """获取全局向量去重器实例（单例模式）
    
    Returns:
        VectorDedup 实例
    """
    global _vector_dedup_instance
    
    if _vector_dedup_instance is None:
        _vector_dedup_instance = VectorDedup()
    
    return _vector_dedup_instance
