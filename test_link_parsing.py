#!/usr/bin/env python3
"""
测试链接解析功能
"""

from weekly_publisher_mcp import WeeklyPublisherMCP

def test_link_parsing():
    """测试链接解析功能"""
    print("🧪 测试链接解析功能")
    print("=" * 40)
    
    publisher = WeeklyPublisherMCP()
    
    # 测试不同的文本格式
    test_cases = [
        "- **原文链接**: [Claude 3.5 Sonnet 深度体验报告](https://example.com/claude-3-5-review)",
        "这是一个包含[链接](https://example.com)的段落。",
        "**粗体文本**和普通文本",
        "没有任何格式的普通文本",
        "多个链接：[链接1](https://example1.com)和[链接2](https://example2.com)",
        "混合格式：**粗体**和[链接](https://example.com)在一起"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}: {test_text}")
        rich_text = publisher.parse_rich_text(test_text)
        
        print("解析结果:")
        for j, element in enumerate(rich_text):
            print(f"  {j+1}. {element}")
        print("-" * 40)

def test_full_content():
    """测试完整内容转换"""
    print("\n🧪 测试完整内容转换")
    print("=" * 40)
    
    publisher = WeeklyPublisherMCP()
    
    test_content = """# 超级个体周刊 第21期
> 让每个人都成为独当一面的超级个体

## 🤖 AI前沿动态

这周AI圈又有新动态了，先说说《Claude 3.5 Sonnet 深度体验报告》这篇文章。

- **原文链接**: [Claude 3.5 Sonnet 深度体验报告](https://example.com/claude-3-5-review)

## 📈 运营&增长

运营增长方面，先说说《2024年增长黑客最新趋势》这篇文章。

- **原文链接**: [2024年增长黑客最新趋势](https://example.com/growth-hacking-2024)"""
    
    blocks = publisher.markdown_to_notion_blocks(test_content)
    
    print(f"生成了 {len(blocks)} 个块:")
    for i, block in enumerate(blocks, 1):
        print(f"\n块 {i}: {block['type']}")
        if 'rich_text' in block.get(block['type'], {}):
            rich_text = block[block['type']]['rich_text']
            for j, element in enumerate(rich_text):
                if 'link' in element.get('text', {}):
                    print(f"  包含链接: {element['text']['content']} -> {element['text']['link']['url']}")
                else:
                    print(f"  文本: {element['text']['content']}")

if __name__ == "__main__":
    test_link_parsing()
    test_full_content() 