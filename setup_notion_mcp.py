#!/usr/bin/env python3
"""
Notion MCP 自动配置脚本
帮助用户快速配置 Notion MCP 服务器
"""

import json
import os
import platform
from pathlib import Path

def get_claude_config_path():
    """获取 Claude Desktop 配置文件路径"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        return Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "claude" / "claude_desktop_config.json"

def get_cursor_config_path():
    """获取 Cursor MCP 配置文件路径"""
    return Path.cwd() / ".cursor" / "mcp.json"

def create_notion_config(api_token):
    """创建 Notion MCP 配置"""
    return {
        "mcpServers": {
            "notionApi": {
                "command": "npx",
                "args": ["-y", "@notionhq/notion-mcp-server"],
                "env": {
                    "OPENAPI_MCP_HEADERS": f'{{"Authorization": "Bearer {api_token}", "Notion-Version": "2022-06-28"}}'
                }
            }
        }
    }

def update_config_file(config_path, new_config):
    """更新配置文件"""
    try:
        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有配置
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        else:
            existing_config = {}
        
        # 合并配置
        if "mcpServers" not in existing_config:
            existing_config["mcpServers"] = {}
        
        existing_config["mcpServers"].update(new_config["mcpServers"])
        
        # 写入配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ 配置文件更新失败: {e}")
        return False

def main():
    print("🚀 Notion MCP 自动配置工具")
    print("=" * 50)
    
    # 获取 API Token
    print("\n📝 首先，你需要获取 Notion API Token：")
    print("1. 访问 https://www.notion.so/my-integrations")
    print("2. 点击 'New Integration'")
    print("3. 创建集成并复制 token（以 ntn_ 开头）")
    print("4. 在 Notion 中将集成连接到你想要访问的页面")
    
    api_token = input("\n🔑 请输入你的 Notion API Token: ").strip()
    
    if not api_token.startswith("ntn_"):
        print("⚠️  警告：Token 通常以 'ntn_' 开头，请确认输入正确")
        confirm = input("是否继续？(y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 配置已取消")
            return
    
    # 创建配置
    config = create_notion_config(api_token)
    
    # 选择配置目标
    print("\n🎯 选择要配置的应用：")
    print("1. Claude Desktop")
    print("2. Cursor")
    print("3. 两者都配置")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    success_count = 0
    
    if choice in ["1", "3"]:
        # 配置 Claude Desktop
        claude_path = get_claude_config_path()
        print(f"\n📁 Claude 配置文件路径: {claude_path}")
        
        if update_config_file(claude_path, config):
            print("✅ Claude Desktop 配置成功！")
            success_count += 1
        else:
            print("❌ Claude Desktop 配置失败")
    
    if choice in ["2", "3"]:
        # 配置 Cursor
        cursor_path = get_cursor_config_path()
        print(f"\n📁 Cursor 配置文件路径: {cursor_path}")
        
        if update_config_file(cursor_path, config):
            print("✅ Cursor 配置成功！")
            success_count += 1
        else:
            print("❌ Cursor 配置失败")
    
    # 显示结果和后续步骤
    print("\n" + "=" * 50)
    if success_count > 0:
        print("🎉 配置完成！")
        print("\n📋 后续步骤：")
        print("1. 重启 Claude Desktop 或 Cursor")
        print("2. 在应用中查看工具列表，确认 'notionApi' 出现")
        print("3. 在 Notion 中确保集成已连接到相应页面")
        print("\n💡 使用示例：")
        print("- '请将这段内容保存到我的 Notion 页面'")
        print("- '从我的项目数据库中查找所有待办任务'")
        print("- '在我的笔记中创建一个新页面'")
    else:
        print("❌ 配置失败，请检查错误信息并重试")
    
    print("\n🔒 安全提醒：")
    print("- 不要分享你的 API Token")
    print("- 只给集成访问必要的页面")
    print("- 如有安全疑虑，及时重新生成 token")

if __name__ == "__main__":
    main() 