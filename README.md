# AI Article Scorer - AI文章质量评分工具

<p align="center">
  <a href="https://github.com/wynn2025/ai-article-scorer/stargazers">
    <img src="https://img.shields.io/github/stars/wynn2025/ai-article-scorer?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/wynn2025/ai-article-scorer/watchers">
    <img src="https://img.shields.io/github/watchers/wynn2025/ai-article-scorer?style=social" alt="GitHub Watchers">
  </a>
  <a href="https://github.com/wynn2025/ai-article-scorer/forks">
    <img src="https://img.shields.io/github/forks/wynn2025/ai-article-scorer?style=social" alt="GitHub Forks">
  </a>
  <a href="https://github.com/wynn2025/ai-article-scorer/issues">
    <img src="https://img.shields.io/github/issues/wynn2025/ai-article-scorer" alt="GitHub Issues">
  </a>
  <a href="https://github.com/wynn2025/ai-article-scorer/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/wynn2025/ai-article-scorer" alt="License">
  </a>
</p>

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请给一个Star！你的支持是我持续更新的动力 ⭐</strong>
</p>

<p align="center">
  <a href="https://github.com/wynn2025/ai-article-scorer"><strong>🚀 立即使用</strong></a> •
  <a href="https://github.com/wynn2025/ai-article-scorer/issues"><strong>🐛 报告Bug</strong></a> •
  <a href="https://github.com/wynn2025/ai-article-scorer/issues"><strong>💡 功能建议</strong></a> •
  <a href="#贡献指南"><strong>🤝 贡献代码</strong></a>
</p>

---

> 命令行工具，对Markdown技术文章进行8维度质量评分，无需AI API，纯规则引擎。发稿前30秒自检，自媒体人必备神器。

---

## ✨ 核心特性

- **🎯 8维度智能评分** - 标题质量、开头吸引、文章结构、可读性、代码示例、SEO优化、互动引导、原创性
- **⚡ 零依赖运行** - 纯Python 3.7+，无需安装任何第三方包，无需API Key
- **📊 可视化报告** - ASCII进度条 + 评分等级（S/A/B/C/D/F），一目了然
- **🔍 批量处理** - 支持单文件、指定标题、批量目录、JSON输出、报告保存
- **📈 实用性极高** - 适用于自媒体、技术博客、内容团队、写作教学等场景

---

## 🎯 适用场景

| 场景 | 说明 | 收益 |
|------|------|------|
| **自媒体作者** | 发稿前快速自检，提升内容质量 | 增加阅读量、点赞、转发 |
| **技术博主** | 技术文章质量把关，建立专业形象 | 提升个人品牌影响力 |
| **内容团队** | 团队文章审核标准统一 | 提高整体内容质量 |
| **写作教学** | 辅助写作练习，反馈质量指标 | 帮助学员快速提升 |

---

## 📸 效果展示

<!-- 
![评分报告示例](docs/screenshots/score-report.png)
![批量处理](docs/screenshots/batch-mode.png)
-->

---

## 🚀 快速开始

### 安装

```bash
# 无需额外依赖，Python 3.7+即可
pip install -r requirements.txt  # 无额外依赖
```

### 使用方法

```bash
# 单文件评分
python main.py article.md

# 指定标题
python main.py article.md --title "自定义标题"

# JSON输出
python main.py article.md --json

# 批量评分
python main.py ./articles/ --batch

# 保存报告
python main.py article.md --output report.txt
```

---

## 📋 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 标题质量 | 15% | 长度、数字、疑问句等 |
| 开头吸引 | 12% | 首句短小、hook效果 |
| 文章结构 | 13% | H2标题数、列表使用 |
| 可读性 | 12% | 句子长度、加粗标记 |
| 代码示例 | 10% | 代码块数量、语言标签 |
| SEO优化 | 10% | 链接数量、文章长度 |
| 互动引导 | 10% | 关注/点赞/评论CTA |
| 原创性 | 08% | 数据引用、独特内容 |

---

## 📊 输出示例

```
=======================================================
  AI Article Quality Report
=======================================================

  Score: 72.5/100  Grade: B (good)
  Words: ~1500  Reading: ~4min

  [████████████████░░░░░░] 72.5%

-------------------------------------------------------
  Dimensions:
-------------------------------------------------------
  title_quality  [■■■■■■■■■■■■■■■□□□□□]  75.0 (w15%)
  opening_hook   [■■■■■■■■■■■□□□□□□□□□]  60.0 (w12%)
  article_structure [■■■■■■■■■■■■■■□□□□]  70.0 (w13%)
  readability    [■■■■■■■■■■■■■□□□□□□□]  65.0 (w12%)
  code_examples  [■■■■■■■■■■■□□□□□□□□□]  60.0 (w10%)
  seo_optimization [■■■■■■■■■■■■■■□□□□]  75.0 (w10%)
  engagement_cta [■■■■■■■■■■■■■■■■□□□□]  80.0 (w10%)
  originality    [■■■■■■■■■■■■□□□□□□□□□]  65.0 (w8%)
```

---

## 🏆 评分等级

| 等级 | 分数范围 | 说明 |
|------|----------|------|
| S | 90-100 | 顶级好文 |
| A | 80-89 | 优秀文章 |
| B | 70-79 | 良好 |
| C | 60-69 | 及格 |
| D | 50-59 | 需改进 |
| F | 0-49 | 不合格 |

---

## 🌟 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 开源协议

MIT License - 可商用

---

<div align="center">

## 💰 购买支持

如果这个项目对你有帮助，可以考虑：

- ⭐ **给个Star** - 这是对我最大的支持！
- 💰 **闲鱼购买** - 获取完整源码 + 详细文档 + 终身更新
- 🤝 **赞助项目** - 支持持续开发

**闲鱼购买链接**: [AI文章质量评分工具](https://goofish.com/item/xxx) ¥9.9（原价¥39.9，限时特惠）

---

**⭐ 如果觉得有用，请给一个Star！你的支持是我持续更新的动力 ⭐**

[![GitHub Stars](https://img.shields.io/github/stars/wynn2025/ai-article-scorer?style=social)](https://github.com/wynn2025/ai-article-scorer/stargazers)

</div>
