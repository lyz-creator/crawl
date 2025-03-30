# NDSS 论文爬虫

本仓库包含用于爬取不同年份的网络和分布式系统安全（NDSS）研讨会论文的 Python 脚本。每个脚本旨在获取特定年份会议论文集的论文。

## 内容

- `count.py`：一个实用工具脚本，用于统计论文数量。
- `ndss1997-2015.py`：用于爬取 1997 至 2015 年 NDSS 论文的脚本。
- `ndss2016.py`：用于爬取 2016 年 NDSS 论文的脚本。
- `ndss2017.py`：用于爬取 2017 年 NDSS 论文的脚本。
- `ndss2018.py`：用于爬取 2018 年 NDSS 论文的脚本。
- `ndss2019-2024.py`：用于爬取 2019 至 2024 年 NDSS 论文的脚本。

## 使用方法

每个脚本可以独立运行以爬取相应年份的论文。在运行脚本之前，请确保已安装必要的依赖项。

1. **克隆仓库**：
   ```bash
   git clone https://github.com/your-username/ndss-paper-scraper.git
   cd ndss-paper-scraper
   ```
   
2. **安装依赖项**：
   ```bash
   pip install -r requirements.txt
   ```
   
3. **运行脚本**：
   ```bash
   python ndss2017.py
   ```
   将 ndss2017.py 替换为你想要爬取的年份对应的脚本。