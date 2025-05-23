#!/usr/bin/env python3
"""
超级个体周刊生成器
基于 Notion 数据库自动生成周刊内容
"""

import json
from datetime import datetime, timedelta
from notion_helper import NotionHelper
import re

# 添加发布器导入
try:
    from weekly_publisher import WeeklyPublisher
except ImportError:
    WeeklyPublisher = None

class WeeklyGenerator:
    def __init__(self):
        self.helper = NotionHelper()
        self.db_id = self.helper.get_database_id()
        
        # 初始化发布器
        self.publisher = WeeklyPublisher() if WeeklyPublisher else None
        
        # 内容分类关键词映射
        self.category_keywords = {
            "AI前沿动态": [
                "人工智能", "AI", "机器学习", "深度学习", "大模型", "GPT", "Claude", 
                "Agent", "LLM", "神经网络", "算法", "模型", "训练", "推理"
            ],
            "本周AI工具": [
                "工具", "软件", "应用", "平台", "插件", "扩展", "效率", "自动化",
                "生产力", "助手", "机器人", "API", "服务"
            ],
            "产品力提升": [
                "产品设计", "用户体验", "UX", "需求分析", "产品策略", "产品管理",
                "用户研究", "产品思维", "MVP", "迭代", "功能", "交互"
            ],
            "运营&增长": [
                "增长", "运营", "营销", "用户获取", "留存", "转化", "流量", "推广",
                "社群", "内容营销", "SEO", "数据分析", "指标", "策略"
            ],
            "优秀设计赏析": [
                "设计", "UI", "视觉", "界面", "交互设计", "品牌", "创意", "美学",
                "排版", "色彩", "图标", "插画", "动效"
            ],
            "超级个体洞察": [
                "个人成长", "技能", "认知", "思维", "学习", "效率", "时间管理",
                "个人品牌", "职业发展", "自我提升", "习惯", "方法论"
            ]
        }
    
    def classify_article(self, title, summary):
        """基于标题和摘要对文章进行分类"""
        content = f"{title} {summary}".lower()
        
        # 计算每个分类的匹配分数
        scores = {}
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in content:
                    score += 1
            scores[category] = score
        
        # 返回得分最高的分类
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return "超级个体洞察"  # 默认分类
    
    def get_weekly_articles(self, weeks_back=1):
        """获取最近几周的已归档文章"""
        # 这里需要调用 Notion API 获取文章
        # 由于我们已经有了数据库查询的例子，这里模拟返回数据
        
        # 实际实现中，你需要：
        # 1. 调用 Notion API 查询数据库
        # 2. 筛选状态为"已归档"的文章
        # 3. 筛选时间在最近一周的文章
        # 4. 返回文章列表
        
        return [
            {
                "title": "取消订阅的 5 大原因",
                "summary": "用户取消应用订阅的主要原因包括使用不足（37%）、成本问题（35%）、找到更好的替代品（10%）、技术问题（7%）和账单错误（高达28%）。",
                "url": "https://www.revenuecat.com/blog/growth/subscription-app-churn-reasons-how-to-fix/",
                "category": "增长&运营",
                "importance": "高"
            },
            {
                "title": "AI Evolves to Achieve Artificial Innovation",
                "summary": "文章讨论了人工智能（AI）的创新能力，指出AI已经能够自主发明新算法和解决方案，颠覆了传统观点。",
                "url": "https://patmcguinness.substack.com/p/ai-evolves-to-achieve-artificial",
                "category": "AI大模型",
                "importance": "中"
            },
            {
                "title": "Weekly Designers Update #506",
                "summary": "本周设计师更新第506期介绍了多个设计灵感项目，包括Gucci的沉浸式3D丝巾画廊和先进的网络安全解决方案。",
                "url": "https://muz.li/blog/weekly-designers-update-506/",
                "category": "设计交互",
                "importance": "高"
            }
        ]
    
    def generate_weekly_content_from_articles(self, articles, week_number=None):
        """基于真实文章数据生成周刊内容"""
        if week_number is None:
            week_number = datetime.now().isocalendar()[1]
        
        # 分类文章
        categorized_articles = self.categorize_articles(articles)
        
        # 生成周刊内容
        content = f"""# 超级个体周刊 第{week_number:02d}期
> 让每个人都成为独当一面的超级个体

## 🎯 本周导读

哈喽大家好！又到了周刊时间。

这周我从 Notion 数据库里筛选出了 {len(articles)} 篇值得一读的文章。说实话，每次整理这些内容的时候，我都会有新的收获。这期的内容涵盖了AI最新动态、实用工具推荐，还有一些让我重新思考的观点。

废话不多说，直接开始吧！

"""

        # 按优先级生成各个分类的内容
        priority_order = ["AI前沿动态", "本周AI工具", "产品力提升", "运营&增长", "优秀设计赏析", "超级个体洞察"]
        
        for category in priority_order:
            if categorized_articles[category]:
                content += self.generate_section_natural(category, categorized_articles[category])
        
        # 添加推荐部分
        high_importance_articles = [a for a in articles if a.get("importance") == "高"]
        if high_importance_articles:
            content += "\n## 📚 本周推荐\n\n"
            content += f"**如果你只能看一篇**，我推荐《{high_importance_articles[0]['title']}》。\n\n"
            content += f"为什么？{high_importance_articles[0]['summary'][:50]}... 这种数据驱动的分析方法，真的可以直接用到实际工作中。\n\n"
        
        # 添加结尾
        content += f"""## 🎉 写在最后

这是第 {week_number:02d} 期周刊，感觉每期都在进步。

最近在思考一个问题：信息这么多，到底什么才是真正有价值的？我觉得不是那些看起来很厉害的理论，而是那些能让你立刻行动起来的洞察。

希望这期内容能给你带来一些启发。如果有什么想法，随时来找我聊聊。

**下周预告**：我在研究一些新的AI工具，还有关于个人品牌建设的思考。如果你也在关注这些话题，下周见！

---
💌 觉得有用的话，转发给朋友吧  
💬 想交流的话，加我微信：[待补充]  

**感谢你花时间看完这期内容！**

---
*超级个体周刊 - 每周日更新*  
*第{week_number:02d}期 | {datetime.now().strftime('%Y年%m月%d日')}*"""
        
        return content
    
    def categorize_articles(self, articles):
        """将文章按照超级个体周刊的分类进行归类"""
        categorized = {
            "AI前沿动态": [],
            "本周AI工具": [],
            "产品力提升": [],
            "运营&增长": [],
            "优秀设计赏析": [],
            "超级个体洞察": []
        }
        
        for article in articles:
            # 使用AI分类算法
            category = self.classify_article(article["title"], article["summary"])
            
            # 映射到标准分类
            if "AI" in article.get("category", "") or "大模型" in article.get("category", ""):
                if "工具" in article["title"] or "工具" in article["summary"]:
                    categorized["本周AI工具"].append(article)
                else:
                    categorized["AI前沿动态"].append(article)
            elif "增长" in article.get("category", "") or "运营" in article.get("category", ""):
                categorized["运营&增长"].append(article)
            elif "设计" in article.get("category", ""):
                categorized["优秀设计赏析"].append(article)
            elif "产品" in article.get("category", ""):
                categorized["产品力提升"].append(article)
            else:
                categorized["超级个体洞察"].append(article)
        
        return categorized
    
    def generate_section_natural(self, category, articles):
        """生成单个分类的自然化内容"""
        if not articles:
            return ""
        
        # 分类图标映射
        icons = {
            "AI前沿动态": "🤖",
            "本周AI工具": "🛠️",
            "产品力提升": "🚀",
            "运营&增长": "📈",
            "优秀设计赏析": "🎨",
            "超级个体洞察": "💡"
        }
        
        # 自然化的开场白
        intros = {
            "AI前沿动态": "这周AI圈又有新动态了，",
            "本周AI工具": "发现了几个不错的工具，",
            "产品力提升": "关于产品这块，",
            "运营&增长": "运营增长方面，",
            "优秀设计赏析": "设计这块让我眼前一亮的是，",
            "超级个体洞察": "最后聊聊个人成长，"
        }
        
        section = f"\n## {icons.get(category, '📋')} {category}\n\n"
        section += intros.get(category, "这周看到一些有意思的内容，")
        
        for i, article in enumerate(articles):
            if i == 0:
                section += f"先说说《{article['title']}》这篇文章。\n\n"
            else:
                section += f"\n还有《{article['title']}》，"
            
            # 添加个人化的点评
            section += f"{article['summary']}\n\n"
            
            if category == "本周AI工具":
                section += f"- **推荐指数**: {'⭐' * (5 if article.get('importance') == '高' else 4 if article.get('importance') == '中' else 3)}\n"
            
            section += f"- **原文链接**: [{article['title']}]({article['url']})\n\n"
        
        return section
    
    def generate_section(self, category, articles):
        """生成单个分类的内容"""
        if not articles:
            return ""
        
        # 分类图标映射
        icons = {
            "AI前沿动态": "🤖",
            "本周AI工具": "🛠️",
            "产品力提升": "🚀",
            "运营&增长": "📈",
            "优秀设计赏析": "🎨",
            "超级个体洞察": "💡"
        }
        
        section = f"\n## {icons.get(category, '📋')} {category}\n\n"
        
        for article in articles:
            section += f"### {article['title']}\n"
            section += f"{article['summary']}\n\n"
            if category == "本周AI工具":
                section += f"- **推荐指数**: {'⭐' * (5 if article.get('importance') == '高' else 4 if article.get('importance') == '中' else 3)}\n"
            section += f"- **原文链接**: [{article['title']}]({article['url']})\n\n"
        
        return section
    
    def generate_weekly_content(self, week_number=None):
        """生成完整的周刊内容"""
        if week_number is None:
            week_number = datetime.now().isocalendar()[1]
        
        # 获取文章数据
        articles = self.get_weekly_articles()
        
        # 分类文章
        categorized_articles = self.categorize_articles(articles)
        
        # 生成周刊内容
        content = f"""# 超级个体周刊 第{week_number}期
> 让每个人都成为独当一面的超级个体

## 🎯 本周导读

本周为大家精选了{len(articles)}篇优质文章，涵盖AI前沿动态、实用工具推荐、产品运营策略等多个维度。特别关注了用户留存策略、AI创新能力突破，以及最新的设计趋势。这些内容将帮助你在超级个体的成长路径上更进一步。

"""

        # 按优先级生成各个分类的内容
        priority_order = ["AI前沿动态", "本周AI工具", "产品力提升", "运营&增长", "优秀设计赏析", "超级个体洞察"]
        
        for category in priority_order:
            if categorized_articles[category]:
                content += self.generate_section(category, categorized_articles[category])
        
        # 添加推荐部分
        high_importance_articles = [a for a in articles if a["importance"] == "高"]
        if high_importance_articles:
            content += "\n## 📚 本周推荐\n\n"
            content += f"- **必读文章**: {high_importance_articles[0]['title']}\n"
            content += f"- **核心观点**: {high_importance_articles[0]['summary'][:100]}...\n"
            content += f"- **推荐理由**: 高价值内容，值得深度阅读和实践\n\n"
        
        # 添加结尾
        content += """---
💌 如果这期内容对你有帮助，欢迎转发给更多朋友  
🔗 往期周刊: [查看往期内容]  
💬 交流群: [加入超级个体成长群]  

**下期预告**: 我们将深入探讨AI Agent的实际应用案例，以及如何构建个人知识管理系统。

---
*超级个体周刊 - 每周五与你相约*
"""
        
        return content
    
    def save_weekly_content(self, content, week_number=None):
        """保存周刊内容到文件"""
        if week_number is None:
            week_number = datetime.now().isocalendar()[1]
        
        filename = f"超级个体周刊_第{week_number}期_{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 周刊内容已保存到: {filename}")
        return filename

def main():
    """主函数"""
    generator = WeeklyGenerator()
    
    print("🚀 超级个体周刊生成器")
    print("=" * 40)
    
    while True:
        print("\n选择操作：")
        print("1. 生成本周周刊")
        print("2. 生成指定周期周刊")
        print("3. 预览分类效果")
        print("4. 生成并发布到 Notion 📰")
        print("5. 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            print("\n📝 正在生成本周周刊...")
            content = generator.generate_weekly_content()
            print("\n" + "="*50)
            print(content)
            print("="*50)
            
            save = input("\n是否保存到文件？(y/N): ").strip().lower()
            if save == 'y':
                filename = generator.save_weekly_content(content)
                
                # 询问是否发布到 Notion
                if generator.publisher:
                    publish = input("\n是否同时发布到 Notion？(y/N): ").strip().lower()
                    if publish == 'y':
                        result = generator.publisher.publish_weekly_to_notion(content)
                        if result['success']:
                            print(f"✅ 已发布到 Notion: {result['url']}")
                        else:
                            print(f"❌ 发布失败: {result['error']}")
        
        elif choice == "2":
            week_num = input("请输入周数 (1-52): ").strip()
            try:
                week_num = int(week_num)
                if 1 <= week_num <= 52:
                    content = generator.generate_weekly_content(week_num)
                    print(f"\n📝 第{week_num}周周刊内容：")
                    print("="*50)
                    print(content)
                    print("="*50)
                    
                    save = input("\n是否保存到文件？(y/N): ").strip().lower()
                    if save == 'y':
                        filename = generator.save_weekly_content(content, week_num)
                        
                        # 询问是否发布到 Notion
                        if generator.publisher:
                            publish = input("\n是否同时发布到 Notion？(y/N): ").strip().lower()
                            if publish == 'y':
                                result = generator.publisher.publish_weekly_to_notion(content, week_num)
                                if result['success']:
                                    print(f"✅ 已发布到 Notion: {result['url']}")
                                else:
                                    print(f"❌ 发布失败: {result['error']}")
                else:
                    print("❌ 请输入1-52之间的数字")
            except ValueError:
                print("❌ 请输入有效的数字")
        
        elif choice == "3":
            print("\n🔍 文章分类预览：")
            articles = generator.get_weekly_articles()
            categorized = generator.categorize_articles(articles)
            
            for category, article_list in categorized.items():
                print(f"\n📂 {category} ({len(article_list)}篇)")
                for article in article_list:
                    print(f"  - {article['title']}")
        
        elif choice == "4":
            if not generator.publisher:
                print("❌ 发布器未初始化，请检查 weekly_publisher.py 文件")
                continue
                
            print("\n📰 生成并发布周刊到 Notion...")
            
            # 生成周刊内容
            content = generator.generate_weekly_content()
            week_number = datetime.now().isocalendar()[1]
            
            # 保存到文件
            filename = generator.save_weekly_content(content)
            print(f"📄 已保存到文件: {filename}")
            
            # 发布到 Notion
            print("🚀 正在发布到 Notion...")
            result = generator.publisher.publish_weekly_to_notion(content)
            
            if result['success']:
                print(f"✅ 发布成功!")
                print(f"📄 页面标题: {result['title']}")
                print(f"🔗 页面链接: {result['url']}")
                print(f"📊 数据库ID: {result['database_id']}")
            else:
                print(f"❌ 发布失败: {result['error']}")
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main() 