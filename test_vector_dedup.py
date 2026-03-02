#!/usr/bin/env python3
"""
测试向量去重功能

验证：
1. 相同内容不同标题能被去重
2. 不同内容不会被误判为重复
"""
import sys
sys.path.insert(0, '/Users/damin1206/.openclaw/workspace/stock-sentiment')

from src.analyzer.vector_dedup import VectorDedup

def test_basic_encoding():
    """测试基本编码功能"""
    print("=" * 60)
    print("测试 1: 基本编码功能")
    print("=" * 60)
    
    dedup = VectorDedup()
    
    text = "这是一条测试新闻"
    embedding = dedup.encode(text)
    
    if embedding:
        print(f"✓ 成功编码文本: {text}")
        print(f"  向量大小: {len(embedding)} bytes")
        return True
    else:
        print(f"✗ 编码失败")
        return False


def test_cosine_similarity():
    """测试余弦相似度计算"""
    print("\n" + "=" * 60)
    print("测试 2: 余弦相似度计算")
    print("=" * 60)
    
    dedup = VectorDedup()
    
    # 测试用例
    test_cases = [
        {
            "text1": "股市大涨，投资者情绪高涨",
            "text2": "股票市场大幅上涨，投资人信心增强",
            "expected": "相似"
        },
        {
            "text1": "今天天气很好",
            "text2": "量子力学是物理学的一个重要分支",
            "expected": "不相似"
        },
        {
            "text1": "苹果公司发布新款iPhone",
            "text2": "苹果公司推出最新款手机产品",
            "expected": "相似"
        }
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        emb1 = dedup.encode(case["text1"])
        emb2 = dedup.encode(case["text2"])
        
        if not emb1 or not emb2:
            print(f"✗ 用例 {i}: 编码失败")
            all_passed = False
            continue
        
        vec1 = dedup.decode(emb1)
        vec2 = dedup.decode(emb2)
        
        similarity = dedup.cosine_similarity(vec1, vec2)
        
        # 相似度 > 0.8 认为是相似内容
        is_similar = similarity > 0.8
        expected_similar = case["expected"] == "相似"
        
        status = "✓" if is_similar == expected_similar else "✗"
        print(f"{status} 用例 {i}:")
        print(f"  文本1: {case['text1']}")
        print(f"  文本2: {case['text2']}")
        print(f"  相似度: {similarity:.4f}")
        print(f"  预期: {case['expected']}, 实际: {'相似' if is_similar else '不相似'}")
        
        if is_similar != expected_similar:
            all_passed = False
    
    return all_passed


def test_duplicate_detection():
    """测试重复检测功能"""
    print("\n" + "=" * 60)
    print("测试 3: 重复检测（阈值 0.95）")
    print("=" * 60)
    
    dedup = VectorDedup()
    
    # 已有新闻向量库
    existing_news = [
        "央行宣布降准降息，释放流动性支持实体经济",
        "科技板块集体上涨，半导体领涨两市",
        "国际贸易局势缓和，全球股市普涨"
    ]
    
    existing_embeddings = []
    for news in existing_news:
        emb = dedup.encode(news)
        if emb:
            existing_embeddings.append(emb)
    
    print(f"已建立 {len(existing_embeddings)} 条新闻向量库\n")
    
    # 测试新新闻
    test_news = [
        {
            "title": "央行降准降息支持实体经济",
            "summary": "中国人民银行今日宣布下调存款准备金率，同时降低利率，以释放更多流动性支持实体经济发展。",
            "expected_duplicate": True,
            "reason": "与'央行宣布降准降息...'内容相同"
        },
        {
            "title": "某科技公司发布新品",
            "summary": "某科技公司今日在北京举行发布会，推出了一款全新的智能硬件产品，引起市场关注。",
            "expected_duplicate": False,
            "reason": "全新内容，不重复"
        }
    ]
    
    all_passed = True
    for news in test_news:
        text = f"{news['title']} {news['summary'][:200]}"
        new_emb = dedup.encode(text)
        
        is_duplicate = dedup.check_duplicate(new_emb, existing_embeddings, threshold=0.95)
        expected = news["expected_duplicate"]
        
        status = "✓" if is_duplicate == expected else "✗"
        print(f"{status} 测试: {news['title']}")
        print(f"  预期: {'重复' if expected else '不重复'} ({news['reason']})")
        print(f"  实际: {'重复' if is_duplicate else '不重复'}")
        
        if is_duplicate != expected:
            all_passed = False
    
    return all_passed


def main():
    """运行所有测试"""
    print("\n开始测试向量去重功能...\n")
    
    results = []
    
    # 测试 1: 基本编码
    results.append(("基本编码功能", test_basic_encoding()))
    
    # 测试 2: 余弦相似度
    results.append(("余弦相似度计算", test_cosine_similarity()))
    
    # 测试 3: 重复检测
    results.append(("重复检测功能", test_duplicate_detection()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
