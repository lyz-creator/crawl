# Crawl - 学术论文爬虫工具

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Crawl 是一个用于爬取学术会议论文的Python工具集，包含静态网页和动态网页两种爬取方案。

## 功能特性

- 🌐 双模式支持：提供静态网页和动态网页两种爬取方案
- 📑 PDF下载：自动识别并下载论文PDF文件
- 🛡️ 反爬处理：内置随机延迟和请求头管理
- 📂 文件管理：自动清理文件名并分类保存
- 🚦 自动化流程：一键式运行，自动处理异常

## 项目结构
crawl/
├── static_crawler/ # 静态网页爬虫
│ ├── usenix_crawler.py # USENIX Security爬虫
│ └── ... # 其他静态网站爬虫
├── dynamic_crawler/ # 动态网页爬虫
│ ├── ieee_crawler.py # IEEE S&P爬虫
│ └── ... # 其他动态网站爬虫
├── utils/ # 工具函数
│ ├── file_utils.py # 文件处理工具
│ └── web_utils.py # 网络请求工具
├── config.yaml # 配置文件
└── requirements.txt # 依赖文件

复制

## 快速开始

### 安装依赖

```bash
git clone https://github.com/lyz-creator/crawl.git
cd crawl
pip install -r requirements.txt
静态网页爬虫使用
python
复制
# 示例：爬取USENIX Security 2024论文
python static_crawler/usenix_crawler.py
动态网页爬虫使用
python
复制
# 示例：爬取IEEE S&P 2024论文
python dynamic_crawler/ieee_crawler.py
配置说明
复制并修改配置文件模板：

bash
复制
cp config.example.yaml config.yaml
主要配置项：

yaml
复制
download:
  base_path: "/path/to/download/folder"  # 下载根目录
  subfolders:  # 各会议子目录
    usenix: "USENIX_Security"
    ieee: "IEEE_S&P"

delay:
  min: 1  # 最小延迟(秒)
  max: 5  # 最大延迟(秒)

selenium:
  headless: true  # 是否使用无头模式
  timeout: 10     # 元素等待超时(秒)
技术细节
静态网页爬虫特点
基于Requests+BeautifulSoup

支持多级页面跳转

自动文件名清理

轻量级实现

动态网页爬虫特点
基于Selenium WebDriver

自动处理Cookie和弹窗

支持AJAX内容加载

完善的异常处理

贡献指南
欢迎通过Issue或PR贡献代码，请遵循以下规范：

新爬虫应放在对应类别的目录下

保持代码风格一致(PEP 8)

添加必要的注释和文档

测试爬虫的稳定性

免责声明
本项目仅用于学术研究目的，请遵守目标网站的robots.txt协议和使用条款。过度请求可能导致IP被封禁，使用者需自行承担风险。

许可证
MIT License © lyz-creator
