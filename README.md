# Notion Weekly Generator

> 基于 Notion MCP API 的智能周刊生成系统

一个自动化的内容策展和周刊生成工具，专为"超级个体周刊"设计。通过 Notion 数据库管理文章，使用 AI 智能分类，自动生成人性化的周刊内容。

## ✨ 功能特性

### 🤖 智能内容管理
- **Notion MCP 集成**：直接连接 Notion 数据库，实时同步文章数据
- **AI 智能分类**：基于关键词和语义分析自动分类文章
- **状态管理**：支持文章的完整生命周期管理（草稿→已归档→已发布）

### 📰 周刊生成
- **自动化生成**：一键生成完整的周刊内容
- **人性化写作**：自然流畅的表达，避免机械化模板
- **多模块支持**：
  - 🤖 AI前沿动态
  - 🛠️ 本周AI工具
  - 🚀 产品力提升
  - 📈 运营&增长
  - 🎨 优秀设计赏析
  - 💡 超级个体洞察

### 🔗 格式支持
- **Markdown 链接**：完美支持 `[文本](URL)` 格式
- **富文本格式**：粗体、斜体、引用等格式
- **Notion 块转换**：自动转换为 Notion 原生格式

### 🎨 封面设计
- **多邻国主题封面**：现代材料设计风格
- **双格式输出**：主封面(2.35:1) + 朋友圈封面(1:1)
- **一键下载**：集成 html2canvas 实现高质量图片导出

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/xingyan-ai/notion-weekly-generator.git
cd notion-weekly-generator

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 Notion

1. 复制配置文件模板：
```bash
cp notion_config.example.json notion_config.json
```

2. 获取 Notion API Token：
   - 访问 [Notion Developers](https://developers.notion.com/)
   - 创建新的集成
   - 复制 API Token

3. 配置数据库：
   - 在 Notion 中创建文章管理数据库
   - 在 Notion 中创建周刊发布数据库
   - 将数据库 ID 填入配置文件

### 3. 配置 MCP (可选)

如果使用 Cursor 编辑器：

```bash
# 运行 MCP 配置脚本
python setup_notion_mcp.py
```

### 4. 开始使用

```bash
# 生成周刊
python weekly_generator.py

# 生成并发布到 Notion
python generate_and_publish.py

# 测试链接解析
python test_link_parsing.py
```

## 📁 项目结构

```
notion-weekly-generator/
├── README.md                          # 项目说明
├── requirements.txt                   # Python 依赖
├── .gitignore                         # Git 忽略文件
├── notion_config.example.json         # 配置文件模板
│
├── 核心功能/
│   ├── weekly_generator.py            # 周刊生成器
│   ├── weekly_publisher_mcp.py        # MCP 发布器
│   ├── generate_and_publish.py        # 一键生成发布
│   └── notion_query_helper.py         # Notion 查询助手
│
├── 工具脚本/
│   ├── setup_notion_mcp.py           # MCP 配置脚本
│   ├── test_link_parsing.py          # 链接解析测试
│   └── weekly_scheduler.py           # 定时任务
│
├── 设计工具/
│   └── duolingo_growth_cover.html    # 封面设计工具
│
├── 文档/
│   ├── 超级个体周刊PRD.md            # 产品需求文档
│   └── 周刊01.md                     # 示例周刊
│
└── 配置/
    └── .cursor/                      # Cursor 编辑器配置
        ├── mcp.json                  # MCP 服务器配置
        └── rules/                    # 自定义规则
```

## 🔧 配置说明

### Notion 数据库结构

#### 文章数据库字段：
- **标题** (title): 文章标题
- **分类（人工）** (multi_select): 手动分类标签
- **重要度** (select): 高/中/低
- **总结（AI 摘要）** (rich_text): AI 生成的摘要
- **添加日期** (date): 文章添加时间
- **URL** (url): 原文链接
- **状态** (select): 草稿/已归档/已发布

#### 周刊数据库字段：
- **周刊标题** (title): 周刊标题
- **期号** (number): 期数
- **生成日期** (date): 生成时间
- **状态** (status): 发布状态

## 🎯 使用场景

### 个人内容策展
- 收集和整理优质文章
- 智能分类和标签管理
- 定期生成个人周刊

### 团队知识分享
- 团队内容协作
- 知识库建设
- 定期分享最新动态

### 自媒体运营
- 内容素材管理
- 自动化内容生成
- 多平台发布

## 🔄 工作流程

1. **内容收集**：在 Notion 数据库中添加文章
2. **AI 分类**：系统自动分析并分类文章
3. **状态管理**：将文章标记为"已归档"
4. **周刊生成**：运行生成器创建周刊内容
5. **格式转换**：自动转换为 Notion 格式
6. **一键发布**：发布到指定的 Notion 数据库

## 🛠️ 技术栈

- **Python 3.8+**：核心开发语言
- **Notion API**：数据库操作
- **MCP (Model Context Protocol)**：Cursor 集成
- **正则表达式**：文本解析和格式化
- **HTML/CSS/JavaScript**：封面设计工具

## 📝 更新日志

### v1.0.0 (2025-05-23)
- ✅ 初始版本发布
- ✅ Notion MCP API 集成
- ✅ 智能文章分类
- ✅ Markdown 链接支持
- ✅ 封面设计工具
- ✅ 完整的周刊生成流程

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Notion API](https://developers.notion.com/) - 强大的数据库 API
- [Cursor](https://cursor.sh/) - 优秀的 AI 编程工具
- [html2canvas](https://html2canvas.hertzen.com/) - 网页截图工具

---

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！** 