#!/usr/bin/env python3
"""
数据库迁移脚本：为 news 表添加 embedding 字段

运行方法：
    python add_embedding_field.py
"""
import sqlite3
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent / "data" / "stocks.db"


def migrate():
    """执行数据库迁移"""
    if not DB_PATH.exists():
        print(f"✗ 数据库文件不存在: {DB_PATH}")
        print("  提示：请先运行应用初始化数据库")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(news)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'embedding' in columns:
            print("✓ embedding 字段已存在，无需迁移")
            return True
        
        # 添加 embedding 字段
        print("正在添加 embedding 字段...")
        cursor.execute("ALTER TABLE news ADD COLUMN embedding BLOB")
        conn.commit()
        
        print("✓ 成功添加 embedding 字段")
        return True
        
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    success = migrate()
    exit(0 if success else 1)
