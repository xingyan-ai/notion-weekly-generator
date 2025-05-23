#!/usr/bin/env python3
"""
Notion 数据库操作辅助工具
快速访问和管理你的 Notion 数据库
"""

import json
import os
from pathlib import Path

class NotionHelper:
    def __init__(self):
        self.config_file = Path("notion_config.json")
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_database_id(self, alias="articles"):
        """获取数据库 ID"""
        if alias == "articles" or alias == "default":
            return self.config["notion"]["quick_access"]["default_database"]
        
        # 如果是具体的数据库名称
        for db_key, db_info in self.config["notion"]["databases"].items():
            if db_key == alias or db_info["name"] == alias:
                return db_info["id"]
        
        return None
    
    def get_api_token(self):
        """获取 API Token"""
        return self.config["notion"]["api_token"]
    
    def list_databases(self):
        """列出所有配置的数据库"""
        print("📚 已配置的 Notion 数据库：")
        print("=" * 50)
        
        for db_key, db_info in self.config["notion"]["databases"].items():
            print(f"🔹 {db_info['name']}")
            print(f"   ID: {db_info['id']}")
            print(f"   描述: {db_info['description']}")
            print(f"   别名: {db_key}")
            print()
    
    def get_database_info(self, alias="articles"):
        """获取数据库详细信息"""
        db_id = self.get_database_id(alias)
        if not db_id:
            return None
        
        for db_key, db_info in self.config["notion"]["databases"].items():
            if db_info["id"] == db_id:
                return db_info
        return None
    
    def add_database(self, name, database_id, description="", alias=None):
        """添加新的数据库配置"""
        if alias is None:
            alias = name.lower().replace(" ", "_")
        
        new_db = {
            "id": database_id,
            "name": name,
            "description": description,
            "created_date": "2025-05-23",
            "last_updated": "2025-05-23"
        }
        
        self.config["notion"]["databases"][alias] = new_db
        self.save_config()
        print(f"✅ 数据库 '{name}' 已添加，别名: {alias}")
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

def main():
    """主函数 - 命令行界面"""
    helper = NotionHelper()
    
    print("🚀 Notion 数据库助手")
    print("=" * 30)
    
    while True:
        print("\n选择操作：")
        print("1. 查看所有数据库")
        print("2. 获取默认数据库 ID")
        print("3. 获取数据库详细信息")
        print("4. 添加新数据库")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            helper.list_databases()
        
        elif choice == "2":
            db_id = helper.get_database_id()
            print(f"📋 默认数据库 ID: {db_id}")
        
        elif choice == "3":
            alias = input("请输入数据库别名 (默认: articles): ").strip() or "articles"
            info = helper.get_database_info(alias)
            if info:
                print(f"\n📊 数据库信息:")
                print(f"名称: {info['name']}")
                print(f"ID: {info['id']}")
                print(f"描述: {info['description']}")
            else:
                print("❌ 未找到该数据库")
        
        elif choice == "4":
            name = input("数据库名称: ").strip()
            db_id = input("数据库 ID: ").strip()
            desc = input("描述 (可选): ").strip()
            alias = input("别名 (可选): ").strip()
            
            helper.add_database(name, db_id, desc, alias or None)
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

# 便捷函数
def get_default_database_id():
    """快速获取默认数据库 ID"""
    helper = NotionHelper()
    return helper.get_database_id()

def get_api_token():
    """快速获取 API Token"""
    helper = NotionHelper()
    return helper.get_api_token()

if __name__ == "__main__":
    main() 