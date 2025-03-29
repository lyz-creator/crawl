# Crawl - 学术论文爬虫工具

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Crawl 是一个用于爬取学术会议论文的Python代码示例，包含静态网页和动态网页两种爬取方案。

## 静态网页爬虫 - USENIX Security 2024 示例
```bash
pip install requests beautifulsoup4
python crawler/Security2024.py
```
## 动态网页爬虫 - IEEE S&P 2024 示例
```bash
pip install selenium webdriver-manager requests
python crawler/S&P2024.py
```

## 技术细节

### 静态网页爬虫特点
- 基于Requests+BeautifulSoup
- 支持多级页面跳转  
- 自动文件名清理

### 动态网页爬虫特点  
- 基于Selenium WebDriver
- 自动处理Cookie和弹窗
- 支持AJAX内容加载

## 免责声明
本项目仅用于学术研究目的，请遵守目标网站的robots.txt协议和使用条款。过度请求可能导致IP被封禁，使用者需自行承担风险。

## 许可证
[MIT License](LICENSE) © lyz-creator
