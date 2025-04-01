# Crawl - 学术论文爬虫

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Crawl 是一个用于爬取学术会议论文的Python代码示例，包含静态网页和动态网页两种爬取方案。

## 静态网页爬虫 - [USENIX Security 2024 示例](https://github.com/lyz-creator/crawl/blob/main/crawler/Security2024.py)
- 基于Requests+BeautifulSoup
- 自动文件名清理
```bash
pip install requests beautifulsoup4
python crawler/Security2024.py
```
#### 输出示例
![image](https://github.com/user-attachments/assets/4ccd18f7-af8d-4fc5-85f9-f62dd915f4f0)


## 动态网页爬虫 - [IEEE S&P 2024 示例](https://github.com/lyz-creator/crawl/blob/main/crawler/S%26P2024.py)
- 基于Selenium WebDriver
- 支持AJAX内容加载
```bash
pip install selenium undetected-chromedriver requests
python crawler/S&P2024.py
```
#### 输出示例
![image](https://github.com/user-attachments/assets/6d984df4-9fca-4348-a548-707069b16a72)


## 免责声明
本项目仅用于学术研究目的，请遵守目标网站的robots.txt协议和使用条款。过度请求可能导致IP被封禁，使用者需自行承担风险。

## 许可证
[MIT License](https://opensource.org/license/mit) © lyz-creator
