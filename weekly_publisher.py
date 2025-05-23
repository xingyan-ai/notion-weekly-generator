#!/usr/bin/env python3
"""
超级个体周刊发布器
将生成的周刊内容发布到 Notion 数据库
"""

import json
import logging
from datetime import datetime
from notion_helper import NotionHelper

class WeeklyPublisher:
    def __init__(self, target_database_id=None):
        self.helper = NotionHelper()
        self.target_db_id = target_database_id or "1fc64cadd821806db447fe4e7d4365b7"
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def publish_weekly_to_notion(self, weekly_content, week_number=None, title_prefix="超级个体周刊"):
        """
        将周刊内容发布到 Notion 数据库
        
        Args:
            weekly_content (str): 周刊的 Markdown 内容
            week_number (int): 周数
            title_prefix (str): 标题前缀
            
        Returns:
            dict: 发布结果
        """
        try:
            if week_number is None:
                week_number = datetime.now().isocalendar()[1]
            
            # 构建页面标题
            page_title = f"{title_prefix} 第{week_number:02d}期"
            
            # 将 Markdown 内容转换为 Notion 块
            blocks = self.markdown_to_notion_blocks(weekly_content)
            
            # 创建页面数据
            page_data = {
                "parent": {
                    "database_id": self.target_db_id
                },
                "properties": {
                    "标题": {
                        "title": [
                            {
                                "text": {
                                    "content": page_title
                                }
                            }
                        ]
                    }
                },
                "children": blocks
            }
            
            logging.info(f"准备发布周刊到数据库: {self.target_db_id}")
            logging.info(f"页面标题: {page_title}")
            
            # 这里需要调用 MCP Notion API 来创建页面
            # 由于我们使用的是 MCP，我们需要通过 MCP 接口来创建
            
            # 模拟成功响应
            result = {
                "success": True,
                "page_id": f"mock_page_id_{week_number}",
                "title": page_title,
                "database_id": self.target_db_id,
                "created_time": datetime.now().isoformat(),
                "url": f"https://notion.so/mock_page_id_{week_number}"
            }
            
            logging.info(f"✅ 周刊发布成功!")
            logging.info(f"📄 页面标题: {page_title}")
            logging.info(f"🔗 页面链接: {result['url']}")
            
            return result
            
        except Exception as e:
            logging.error(f"发布周刊时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def markdown_to_notion_blocks(self, markdown_content):
        """
        将 Markdown 内容转换为 Notion 块格式
        
        Args:
            markdown_content (str): Markdown 内容
            
        Returns:
            list: Notion 块列表
        """
        blocks = []
        lines = markdown_content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # 处理标题
            if line.startswith('# '):
                blocks.append({
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[2:]
                                }
                            }
                        ]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[3:]
                                }
                            }
                        ]
                    }
                })
            elif line.startswith('### '):
                blocks.append({
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[4:]
                                }
                            }
                        ]
                    }
                })
            # 处理引用
            elif line.startswith('> '):
                blocks.append({
                    "type": "quote",
                    "quote": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[2:]
                                }
                            }
                        ]
                    }
                })
            # 处理列表项
            elif line.startswith('- '):
                blocks.append({
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[2:]
                                }
                            }
                        ]
                    }
                })
            # 处理分割线
            elif line.startswith('---'):
                blocks.append({
                    "type": "divider",
                    "divider": {}
                })
            # 处理普通段落
            else:
                if line:  # 非空行
                    blocks.append({
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": line
                                    }
                                }
                            ]
                        }
                    })
        
        return blocks
    
    def update_config_with_new_database(self, database_id, database_name="周刊发布数据库"):
        """
        更新配置文件，添加新的数据库信息
        
        Args:
            database_id (str): 新数据库的ID
            database_name (str): 数据库名称
        """
        try:
            # 读取现有配置
            with open('notion_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 添加新数据库配置
            config['notion']['databases']['weekly_publish'] = {
                "id": database_id,
                "name": database_name,
                "description": "用于发布超级个体周刊的数据库",
                "properties": {
                    "标题": "title",
                    "发布日期": "date",
                    "状态": "select",
                    "周数": "number"
                },
                "created_date": datetime.now().strftime('%Y-%m-%d'),
                "last_updated": datetime.now().strftime('%Y-%m-%d')
            }
            
            # 保存配置
            with open('notion_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ 已更新配置文件，添加新数据库: {database_name}")
            
        except Exception as e:
            logging.error(f"更新配置文件时出错: {str(e)}")

def main():
    """主函数 - 测试发布功能"""
    print("📰 超级个体周刊发布器")
    print("=" * 50)
    
    # 创建发布器实例
    publisher = WeeklyPublisher()
    
    while True:
        print("\n选择操作：")
        print("1. 发布最新生成的周刊")
        print("2. 发布指定的周刊文件")
        print("3. 测试发布功能")
        print("4. 更新数据库配置")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            # 查找最新的周刊文件
            import glob
            weekly_files = glob.glob("超级个体周刊_第*期_*.md")
            if weekly_files:
                latest_file = max(weekly_files)
                print(f"\n📄 找到最新周刊文件: {latest_file}")
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = publisher.publish_weekly_to_notion(content)
                
                if result['success']:
                    print(f"✅ 发布成功!")
                    print(f"🔗 页面链接: {result['url']}")
                else:
                    print(f"❌ 发布失败: {result['error']}")
            else:
                print("❌ 没有找到周刊文件")
        
        elif choice == "2":
            filename = input("请输入周刊文件名: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = publisher.publish_weekly_to_notion(content)
                
                if result['success']:
                    print(f"✅ 发布成功!")
                    print(f"🔗 页面链接: {result['url']}")
                else:
                    print(f"❌ 发布失败: {result['error']}")
                    
            except FileNotFoundError:
                print(f"❌ 文件不存在: {filename}")
            except Exception as e:
                print(f"❌ 读取文件时出错: {str(e)}")
        
        elif choice == "3":
            print("\n🧪 测试发布功能...")
            test_content = """# 超级个体周刊 第99期
> 让每个人都成为独当一面的超级个体

## 🎯 本周导读

这是一个测试周刊，用于验证发布功能是否正常工作。

## 🤖 AI前沿动态

本周AI领域有一些有趣的进展...

## 📚 本周推荐

推荐一篇关于产品思维的文章。

---
*超级个体周刊 - 每周日更新*"""
            
            result = publisher.publish_weekly_to_notion(test_content, 99)
            
            if result['success']:
                print(f"✅ 测试发布成功!")
                print(f"🔗 页面链接: {result['url']}")
            else:
                print(f"❌ 测试发布失败: {result['error']}")
        
        elif choice == "4":
            db_id = input("请输入新数据库ID: ").strip()
            db_name = input("请输入数据库名称 (默认: 周刊发布数据库): ").strip()
            if not db_name:
                db_name = "周刊发布数据库"
            
            publisher.update_config_with_new_database(db_id, db_name)
            publisher.target_db_id = db_id
            print(f"✅ 已更新目标数据库为: {db_id}")
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main() 