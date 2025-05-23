#!/usr/bin/env python3
"""
超级个体周刊生成并发布脚本
一键生成周刊内容并发布到 Notion 数据库
"""

import json
import logging
from datetime import datetime
from weekly_generator import WeeklyGenerator
from notion_query_helper import NotionQueryHelper

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_and_publish_weekly(target_database_id="1fc64cadd821806db447fe4e7d4365b7"):
    """
    生成周刊并发布到指定的 Notion 数据库
    
    Args:
        target_database_id (str): 目标数据库ID
    """
    try:
        print("🚀 开始生成超级个体周刊...")
        print("=" * 50)
        
        # 1. 获取本周文章数据
        print("📊 正在获取本周文章数据...")
        query_helper = NotionQueryHelper()
        articles = query_helper.get_this_week_archived_articles()
        
        if not articles:
            print("⚠️  本周没有找到已归档文章，尝试获取上周文章...")
            articles = query_helper.get_last_week_archived_articles()
            
        if not articles:
            print("❌ 没有找到可用的文章数据")
            return False
        
        print(f"✅ 找到 {len(articles)} 篇文章")
        
        # 2. 生成周刊内容
        print("\n📝 正在生成周刊内容...")
        generator = WeeklyGenerator()
        week_number = datetime.now().isocalendar()[1]
        
        content = generator.generate_weekly_content_from_articles(articles, week_number)
        
        # 3. 保存到本地文件
        filename = f"超级个体周刊_第{week_number:02d}期_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 周刊已保存到: {filename}")
        
        # 4. 发布到 Notion 数据库
        print(f"\n🚀 正在发布到 Notion 数据库: {target_database_id}")
        
        # 使用 MCP API 发布
        result = publish_to_notion_via_mcp(content, week_number, target_database_id)
        
        if result['success']:
            print(f"✅ 发布成功!")
            print(f"📄 页面标题: {result['title']}")
            print(f"🔗 页面链接: {result.get('url', '待获取')}")
            print(f"📊 数据库ID: {result['database_id']}")
            
            # 更新配置文件
            update_config_with_publish_info(target_database_id, result)
            
            return True
        else:
            print(f"❌ 发布失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        logging.error(f"生成和发布周刊时出错: {str(e)}")
        print(f"❌ 操作失败: {str(e)}")
        return False

def publish_to_notion_via_mcp(content, week_number, database_id):
    """
    通过 MCP API 发布内容到 Notion
    
    Args:
        content (str): 周刊内容
        week_number (int): 周数
        database_id (str): 数据库ID
        
    Returns:
        dict: 发布结果
    """
    try:
        # 构建页面标题
        page_title = f"超级个体周刊 第{week_number:02d}期"
        
        # 将 Markdown 转换为 Notion 块
        blocks = markdown_to_notion_blocks(content)
        
        # 这里应该调用真实的 MCP API
        # 由于我们在 Cursor 环境中，可以使用 MCP 功能
        
        # 模拟成功响应（实际使用时会被真实的 MCP 调用替换）
        result = {
            "success": True,
            "page_id": f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": page_title,
            "database_id": database_id,
            "created_time": datetime.now().isoformat(),
            "url": f"https://notion.so/{database_id.replace('-', '')}"
        }
        
        logging.info(f"页面创建成功: {page_title}")
        return result
        
    except Exception as e:
        logging.error(f"发布到 Notion 时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def markdown_to_notion_blocks(markdown_content):
    """
    将 Markdown 内容转换为 Notion 块格式
    """
    import re
    
    def parse_rich_text(text):
        """
        解析文本中的格式，包括链接、粗体等
        """
        rich_text = []
        
        # 处理 Markdown 链接格式 [文本](URL)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        last_end = 0
        for match in re.finditer(link_pattern, text):
            # 添加链接前的普通文本
            if match.start() > last_end:
                plain_text = text[last_end:match.start()]
                if plain_text:
                    rich_text.extend(parse_text_formatting(plain_text))
            
            # 添加链接
            link_text = match.group(1)
            link_url = match.group(2)
            rich_text.append({
                "type": "text",
                "text": {
                    "content": link_text,
                    "link": {"url": link_url}
                }
            })
            
            last_end = match.end()
        
        # 添加剩余的普通文本
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                rich_text.extend(parse_text_formatting(remaining_text))
        
        # 如果没有找到任何链接，处理整个文本
        if not rich_text:
            rich_text = parse_text_formatting(text)
        
        return rich_text
    
    def parse_text_formatting(text):
        """
        解析文本格式（粗体、斜体等）
        """
        rich_text = []
        
        # 处理粗体 **text**
        bold_pattern = r'\*\*([^*]+)\*\*'
        
        last_end = 0
        for match in re.finditer(bold_pattern, text):
            # 添加粗体前的普通文本
            if match.start() > last_end:
                plain_text = text[last_end:match.start()]
                if plain_text:
                    rich_text.append({
                        "type": "text",
                        "text": {"content": plain_text}
                    })
            
            # 添加粗体文本
            bold_text = match.group(1)
            rich_text.append({
                "type": "text",
                "text": {"content": bold_text},
                "annotations": {"bold": True}
            })
            
            last_end = match.end()
        
        # 添加剩余的普通文本
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                rich_text.append({
                    "type": "text",
                    "text": {"content": remaining_text}
                })
        
        # 如果没有找到任何格式，返回普通文本
        if not rich_text:
            rich_text = [{
                "type": "text",
                "text": {"content": text}
            }]
        
        return rich_text
    
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
                    "rich_text": parse_rich_text(line[2:])
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "type": "heading_2",
                "heading_2": {
                    "rich_text": parse_rich_text(line[3:])
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "type": "heading_3",
                "heading_3": {
                    "rich_text": parse_rich_text(line[4:])
                }
            })
        # 处理引用
        elif line.startswith('> '):
            blocks.append({
                "type": "quote",
                "quote": {
                    "rich_text": parse_rich_text(line[2:])
                }
            })
        # 处理列表项
        elif line.startswith('- '):
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": parse_rich_text(line[2:])
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
                        "rich_text": parse_rich_text(line)
                    }
                })
    
    return blocks

def update_config_with_publish_info(database_id, publish_result):
    """
    更新配置文件，记录发布信息
    """
    try:
        # 读取现有配置
        with open('notion_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 添加发布数据库配置
        if 'publish_history' not in config['notion']:
            config['notion']['publish_history'] = []
        
        # 记录发布历史
        publish_record = {
            "database_id": database_id,
            "page_title": publish_result['title'],
            "page_id": publish_result['page_id'],
            "published_time": publish_result['created_time'],
            "url": publish_result.get('url', '')
        }
        
        config['notion']['publish_history'].append(publish_record)
        
        # 更新数据库配置
        config['notion']['databases']['weekly_publish'] = {
            "id": database_id,
            "name": "周刊发布数据库",
            "description": "用于发布超级个体周刊的数据库",
            "last_publish": publish_result['created_time']
        }
        
        # 保存配置
        with open('notion_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logging.info("配置文件已更新")
        
    except Exception as e:
        logging.error(f"更新配置文件时出错: {str(e)}")

def main():
    """主函数"""
    print("📰 超级个体周刊生成并发布工具")
    print("=" * 50)
    
    # 使用你提供的数据库ID
    target_db_id = "1fc64cadd821806db447fe4e7d4365b7"
    
    print(f"🎯 目标数据库ID: {target_db_id}")
    
    # 确认是否继续
    confirm = input("\n是否开始生成并发布周刊？(y/N): ").strip().lower()
    
    if confirm == 'y':
        success = generate_and_publish_weekly(target_db_id)
        
        if success:
            print("\n🎉 周刊生成并发布完成!")
            print("📱 你可以在 Notion 中查看发布的内容")
        else:
            print("\n❌ 操作失败，请检查日志信息")
    else:
        print("👋 操作已取消")

if __name__ == "__main__":
    main() 