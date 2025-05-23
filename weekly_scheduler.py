#!/usr/bin/env python3
"""
超级个体周刊定时调度器
每周日自动生成周刊
"""

import schedule
import time
import json
import logging
from datetime import datetime, timedelta
from weekly_generator import WeeklyGenerator
from notion_helper import NotionHelper
from notion_query_helper import NotionQueryHelper

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weekly_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class WeeklyScheduler:
    def __init__(self):
        self.generator = WeeklyGenerator()
        self.helper = NotionHelper()
        self.query_helper = NotionQueryHelper()
        self.db_id = self.helper.get_database_id()
        
    def get_archived_articles_this_week(self):
        """获取本周已归档的文章"""
        try:
            logging.info("开始获取本周已归档文章...")
            
            # 使用真实的 Notion 查询
            articles = self.query_helper.get_this_week_archived_articles()
            
            if not articles:
                logging.warning("本周没有找到已归档的文章")
                # 如果本周没有文章，尝试获取上周的文章
                logging.info("尝试获取上周的文章...")
                articles = self.query_helper.get_last_week_archived_articles()
                
                if articles:
                    logging.info(f"使用上周的 {len(articles)} 篇文章")
                else:
                    logging.warning("上周也没有找到已归档的文章")
            
            return articles
            
        except Exception as e:
            logging.error(f"获取文章时出错: {str(e)}")
            return []
    
    def generate_weekly_newsletter(self):
        """生成周刊的主要函数"""
        try:
            logging.info("开始生成周刊...")
            
            # 获取本周已归档文章
            articles = self.get_archived_articles_this_week()
            
            if not articles:
                logging.warning("没有找到已归档的文章，跳过周刊生成")
                return False
            
            # 计算周数
            week_number = datetime.now().isocalendar()[1]
            
            # 生成周刊内容
            content = self.generator.generate_weekly_content_from_articles(articles, week_number)
            
            # 保存周刊文件
            filename = f"超级个体周刊_第{week_number:02d}期_{datetime.now().strftime('%Y%m%d')}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logging.info(f"✅ 周刊生成成功: {filename}")
            
            # 发送通知（可选）
            self.send_notification(filename, len(articles))
            
            return True
            
        except Exception as e:
            logging.error(f"生成周刊时出错: {str(e)}")
            return False
    
    def send_notification(self, filename, article_count):
        """发送生成完成通知"""
        try:
            # 这里可以集成邮件通知、微信通知等
            message = f"""
📰 超级个体周刊自动生成完成！

📄 文件名: {filename}
📊 文章数量: {article_count}篇
⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

请查看生成的周刊文件。
            """
            
            logging.info("通知信息:")
            logging.info(message)
            
            # TODO: 在这里添加实际的通知发送逻辑
            # 比如发送邮件、企业微信、钉钉等
            
        except Exception as e:
            logging.error(f"发送通知时出错: {str(e)}")
    
    def test_generation(self):
        """测试周刊生成功能"""
        logging.info("🧪 执行测试生成...")
        return self.generate_weekly_newsletter()
    
    def preview_articles(self):
        """预览本周的文章"""
        try:
            print("\n📋 预览本周已归档文章:")
            print("=" * 50)
            
            articles = self.get_archived_articles_this_week()
            
            if not articles:
                print("❌ 没有找到已归档的文章")
                return
            
            for i, article in enumerate(articles, 1):
                print(f"\n{i}. 📄 {article['title']}")
                print(f"   🏷️  分类: {article.get('category', '未分类')}")
                print(f"   ⭐ 重要度: {article.get('importance', '未设置')}")
                print(f"   📅 归档日期: {article.get('archived_date', '未知')}")
                print(f"   📝 摘要: {article['summary'][:100]}...")
                print(f"   🔗 链接: {article['url']}")
            
            print(f"\n✅ 共找到 {len(articles)} 篇文章")
            
        except Exception as e:
            print(f"❌ 预览文章时出错: {str(e)}")

def job():
    """定时任务执行的函数"""
    logging.info("🚀 定时任务开始执行...")
    scheduler = WeeklyScheduler()
    success = scheduler.generate_weekly_newsletter()
    
    if success:
        logging.info("✅ 定时任务执行成功")
    else:
        logging.error("❌ 定时任务执行失败")

def main():
    """主函数"""
    print("🤖 超级个体周刊定时调度器")
    print("=" * 50)
    
    # 创建调度器实例
    scheduler_instance = WeeklyScheduler()
    
    while True:
        print("\n选择操作：")
        print("1. 立即测试生成周刊")
        print("2. 预览本周文章")
        print("3. 启动定时调度 (每周日 09:00)")
        print("4. 查看调度状态")
        print("5. 停止并退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            print("\n🧪 开始测试生成...")
            success = scheduler_instance.test_generation()
            if success:
                print("✅ 测试生成成功！")
            else:
                print("❌ 测试生成失败，请检查日志")
        
        elif choice == "2":
            scheduler_instance.preview_articles()
        
        elif choice == "3":
            print("\n⏰ 启动定时调度...")
            print("📅 调度时间: 每周日 09:00")
            print("📝 日志文件: weekly_scheduler.log")
            print("⚠️  按 Ctrl+C 停止调度")
            
            # 设置定时任务 - 每周日上午9点执行
            schedule.every().sunday.at("09:00").do(job)
            
            # 也可以设置其他时间，比如：
            # schedule.every().sunday.at("21:00").do(job)  # 每周日晚上9点
            # schedule.every().monday.at("08:00").do(job)  # 每周一早上8点
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                print("\n⏹️  定时调度已停止")
                break
        
        elif choice == "4":
            print("\n📊 调度状态:")
            jobs = schedule.get_jobs()
            if jobs:
                for job in jobs:
                    print(f"  - {job}")
            else:
                print("  当前没有活跃的调度任务")
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main() 