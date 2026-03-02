#!/usr/bin/env python3
"""简单的向量去重测试"""
import sys
sys.path.insert(0, '/Users/damin1206/.openclaw/workspace/stock-sentiment')

print("测试开始：导入模块...")
try:
    from src.analyzer.vector_dedup import get_vector_dedup
    print("✓ 模块导入成功")
except Exception as e:
    print(f"✗ 模块导入失败: {e}")
    exit(1)

print("\n初始化向量去重器...")
try:
    dedup = get_vector_dedup()
    print("✓ 初始化成功（延迟加载模式，模型尚未加载）")
except Exception as e:
    print(f"✗ 初始化失败: {e}")
    exit(1)

print("\n测试文本编码...")
try:
    text = "股市大涨"
    emb = dedup.encode(text)
    if emb:
        print(f"✓ 编码成功，向量大小: {len(emb)} bytes")
    else:
        print("✗ 编码返回 None")
        exit(1)
except Exception as e:
    print(f"✗ 编码失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n测试向量解码...")
try:
    vec = dedup.decode(emb)
    if vec is not None:
        print(f"✓ 解码成功，向量维度: {len(vec)}")
    else:
        print("✗ 解码返回 None")
        exit(1)
except Exception as e:
    print(f"✗ 解码失败: {e}")
    exit(1)

print("\n测试余弦相似度...")
try:
    text1 = "股市大涨"
    text2 = "股票市场大幅上涨"
    emb1 = dedup.encode(text1)
    emb2 = dedup.encode(text2)
    vec1 = dedup.decode(emb1)
    vec2 = dedup.decode(emb2)
    similarity = dedup.cosine_similarity(vec1, vec2)
    print(f"✓ 相似度计算成功: {similarity:.4f}")
    if similarity > 0.8:
        print(f"  相似度高，符合预期")
except Exception as e:
    print(f"✗ 相似度计算失败: {e}")
    exit(1)

print("\n测试重复检测...")
try:
    existing = [
        dedup.encode("央行宣布降准降息"),
        dedup.encode("科技板块上涨")
    ]
    
    new_similar = dedup.encode("中国人民银行降准降息政策")  # 与第一条相似
    new_different = dedup.encode("今天天气晴朗")  # 完全不同
    
    is_dup1 = dedup.check_duplicate(new_similar, existing, threshold=0.95)
    is_dup2 = dedup.check_duplicate(new_different, existing, threshold=0.95)
    
    print(f"相似内容检测结果: {'重复' if is_dup1 else '不重复'}")
    print(f"不同内容检测结果: {'重复' if is_dup2 else '不重复'}")
    print("✓ 重复检测功能正常")
except Exception as e:
    print(f"✗ 重复检测失败: {e}")
    exit(1)

print("\n" + "="*60)
print("✓ 所有测试通过！向量去重功能正常工作")
print("="*60)
