#!/usr/bin/env python3
"""
Notion 数据库查询辅助函数
专门用于获取已归档的文章数据
"""

import json
import logging
from datetime import datetime, timedelta
from notion_helper import NotionHelper

class NotionQueryHelper:
    def __init__(self):
        self.helper = NotionHelper()
        self.db_id = self.helper.get_database_id()
        
    def get_archived_articles_by_date_range(self, start_date, end_date):
        """
        根据日期范围获取已归档的文章
        
        Args:
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
            
        Returns:
            list: 文章列表
        """
        try:
            # 这里需要使用 MCP Notion API 进行查询
            # 由于我们已经配置了 MCP，可以直接调用
            
            # 构建查询条件
            filter_conditions = {
                "and": [
                    {
                        "property": "状态",
                        "select": {
                            "equals": "已归档"
                        }
                    },
                    {
                        "property": "添加日期",
                        "date": {
                            "on_or_after": start_date.isoformat()
                        }
                    },
                    {
                        "property": "添加日期", 
                        "date": {
                            "on_or_before": end_date.isoformat()
                        }
                    }
                ]
            }
            
            # 注意：这里需要实际调用 MCP API
            # 目前先返回模拟数据，实际使用时需要替换
            
            logging.info(f"查询条件: {json.dumps(filter_conditions, indent=2, ensure_ascii=False)}")
            
            # 模拟返回数据
            mock_articles = [
                {
                    "title": "AI驱动的产品创新策略",
                    "summary": "探讨如何利用AI技术推动产品创新，包括用户研究、需求分析和功能设计的新方法。",
                    "url": "https://example.com/ai-product-innovation",
                    "category": "产品设计",
                    "importance": "高",
                    "archived_date": start_date.strftime('%Y-%m-%d'),
                    "tags": ["AI", "产品管理", "创新"]
                },
                {
                    "title": "2024年增长黑客最新趋势",
                    "summary": "分析当前最有效的用户增长策略，包括病毒式营销、推荐系统和社群运营的实战案例。",
                    "url": "https://example.com/growth-hacking-2024", 
                    "category": "增长&运营",
                    "importance": "高",
                    "archived_date": (start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                    "tags": ["增长", "营销", "用户获取"]
                },
                {
                    "title": "Claude 3.5 Sonnet 深度体验报告",
                    "summary": "全面测试Claude 3.5 Sonnet在代码生成、文本创作和逻辑推理方面的能力表现。",
                    "url": "https://example.com/claude-3-5-review",
                    "category": "AI大模型", 
                    "importance": "中",
                    "archived_date": (start_date + timedelta(days=2)).strftime('%Y-%m-%d'),
                    "tags": ["Claude", "AI模型", "评测"]
                }
            ]
            
            logging.info(f"找到 {len(mock_articles)} 篇已归档文章")
            return mock_articles
            
        except Exception as e:
            logging.error(f"查询文章时出错: {str(e)}")
            return []
    
    def get_this_week_archived_articles(self):
        """获取本周已归档的文章"""
        today = datetime.now()
        # 获取本周一
        monday = today - timedelta(days=today.weekday())
        # 获取本周日
        sunday = monday + timedelta(days=6)
        
        logging.info(f"查询本周文章: {monday.strftime('%Y-%m-%d')} 到 {sunday.strftime('%Y-%m-%d')}")
        
        return self.get_archived_articles_by_date_range(monday, sunday)
    
    def get_last_week_archived_articles(self):
        """获取上周已归档的文章"""
        today = datetime.now()
        # 获取上周一
        last_monday = today - timedelta(days=today.weekday() + 7)
        # 获取上周日
        last_sunday = last_monday + timedelta(days=6)
        
        logging.info(f"查询上周文章: {last_monday.strftime('%Y-%m-%d')} 到 {last_sunday.strftime('%Y-%m-%d')}")
        
        return self.get_archived_articles_by_date_range(last_monday, last_sunday)
    
    def format_article_for_newsletter(self, raw_article):
        """
        将从 Notion 获取的原始文章数据格式化为周刊所需格式
        
        Args:
            raw_article (dict): 从 Notion API 获取的原始文章数据
            
        Returns:
            dict: 格式化后的文章数据
        """
        try:
            # 提取标题
            title = ""
            if "properties" in raw_article and "标题" in raw_article["properties"]:
                title_prop = raw_article["properties"]["标题"]
                if title_prop["type"] == "title" and title_prop["title"]:
                    title = title_prop["title"][0]["text"]["content"]
            
            # 提取摘要
            summary = ""
            if "properties" in raw_article and "总结（AI 摘要）" in raw_article["properties"]:
                summary_prop = raw_article["properties"]["总结（AI 摘要）"]
                if summary_prop["type"] == "rich_text" and summary_prop["rich_text"]:
                    summary = summary_prop["rich_text"][0]["text"]["content"]
            
            # 提取URL
            url = ""
            if "properties" in raw_article and "URL" in raw_article["properties"]:
                url_prop = raw_article["properties"]["URL"]
                if url_prop["type"] == "url" and url_prop["url"]:
                    url = url_prop["url"]
            
            # 提取分类
            category = ""
            if "properties" in raw_article and "分类（人工）" in raw_article["properties"]:
                category_prop = raw_article["properties"]["分类（人工）"]
                if category_prop["type"] == "multi_select" and category_prop["multi_select"]:
                    category = category_prop["multi_select"][0]["name"]
            
            # 提取重要度
            importance = ""
            if "properties" in raw_article and "重要度" in raw_article["properties"]:
                importance_prop = raw_article["properties"]["重要度"]
                if importance_prop["type"] == "select" and importance_prop["select"]:
                    importance = importance_prop["select"]["name"]
            
            # 提取添加日期
            archived_date = ""
            if "properties" in raw_article and "添加日期" in raw_article["properties"]:
                date_prop = raw_article["properties"]["添加日期"]
                if date_prop["type"] == "date" and date_prop["date"]:
                    archived_date = date_prop["date"]["start"][:10]  # 只取日期部分
            
            formatted_article = {
                "title": title,
                "summary": summary,
                "url": url,
                "category": category,
                "importance": importance,
                "archived_date": archived_date
            }
            
            return formatted_article
            
        except Exception as e:
            logging.error(f"格式化文章数据时出错: {str(e)}")
            return None

def test_query():
    """测试查询功能"""
    print("🧪 测试 Notion 查询功能")
    print("=" * 40)
    
    helper = NotionQueryHelper()
    
    # 测试获取本周文章
    print("\n📅 获取本周已归档文章:")
    this_week_articles = helper.get_this_week_archived_articles()
    
    for i, article in enumerate(this_week_articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   分类: {article['category']}")
        print(f"   重要度: {article['importance']}")
        print(f"   归档日期: {article['archived_date']}")
        print(f"   摘要: {article['summary'][:100]}...")
    
    print(f"\n✅ 共找到 {len(this_week_articles)} 篇文章")

if __name__ == "__main__":
    test_query() 