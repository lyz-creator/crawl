import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random

# 清理文件名，使其合法
def sanitize_filename(title):
    """清理文件名，使其合法"""
    return re.sub(r'[<>:"/\\|?*]', '_', title)

# 目标网页 URLs（包含2022, 2023, 2024年）
urls = {
    "2024_Summer": "https://www.usenix.org/conference/usenixsecurity24/summer-accepted-papers",
    "2024_Fall": "https://www.usenix.org/conference/usenixsecurity24/fall-accepted-papers",
    "2023_Summer": "https://www.usenix.org/conference/usenixsecurity23/summer-accepted-papers",
    "2023_Fall": "https://www.usenix.org/conference/usenixsecurity23/fall-accepted-papers",
    "2022_Summer": "https://www.usenix.org/conference/usenixsecurity22/summer-accepted-papers",
    "2022_Fall": "https://www.usenix.org/conference/usenixsecurity22/fall-accepted-papers",
    "2022_Winter": "https://www.usenix.org/conference/usenixsecurity22/winter-accepted-papers",
    "2021_Summer": "https://www.usenix.org/conference/usenixsecurity21/summer-accepted-papers",
    "2021_Fall": "https://www.usenix.org/conference/usenixsecurity21/fall-accepted-papers", 
    "2020_Spring": "https://www.usenix.org/conference/usenixsecurity20/spring-accepted-papers",
    "2020_Summer": "https://www.usenix.org/conference/usenixsecurity20/summer-accepted-papers",
    "2020_Fall": "https://www.usenix.org/conference/usenixsecurity20/fall-accepted-papers",
    "2019_Fall": "https://www.usenix.org/conference/usenixsecurity19/fall-accepted-papers"
}

# 下载目录的根路径
base_folder = r"C:\Users\lyz\Desktop\crawler\Security"

# 自定义请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 遍历所有 URL
for key, url in urls.items():
    # 提取年份和季节信息
    year, season = key.split('_')
    
    # 确定保存路径，例如：C:\Users\lyz\Desktop\crawler\Security\Security_2024\Summer
    download_folder = os.path.join(base_folder, f"Security_{year}", season)
    
    # 如果下载目录不存在，创建该目录
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    print(f"\n正在爬取 {year} 年 {season} 论文列表...")

    # 发送 HTTP 请求获取网页内容
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有包含 <div class="field-item odd"> 和 <div class="field-item even"> 标签
        divs = soup.find_all('div', class_=lambda c: c in ['field-item odd', 'field-item even'])
        
        for div in divs:
            # 找到 h2 标签中的 a 标签
            h2 = div.find('h2')
            if h2:
                a_tag = h2.find('a')
                if a_tag and a_tag.get('href'):
                    title = a_tag.get_text(strip=True)
                    paper_page_link = 'https://www.usenix.org' + a_tag.get('href')
                    
                    # 清理文件名
                    sanitized_title = sanitize_filename(title)
                    
                    # 输出标题和链接
                    print(f"\n[{year} {season}] 标题: {sanitized_title}")
                    print(f"URL: {paper_page_link}")
                    
                    # 随机延迟 1 到 3 秒，避免请求过快
                    time.sleep(random.randint(0, 1))
                    
                    try:
                        # 访问论文页面
                        paper_response = requests.get(paper_page_link, headers=headers)
                        paper_response.raise_for_status()  # 确保请求成功
                        
                        # 解析论文页面
                        paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
                        
                        # 查找 PDF 下载链接
                        pdf_div = paper_soup.find('div', class_='field-name-field-presentation-pdf')
                        
                        if not pdf_div:
                            # 查找所有包含 PDF 链接的 a 标签
                            pdf_links = paper_soup.find_all('a', href=lambda href: href and '.pdf' in href)
                            pdf_link_tag = pdf_links[0] if pdf_links else None
                        else:
                            pdf_link_tag = pdf_div.find('a')
                        
                        if pdf_link_tag and pdf_link_tag.get('href'):
                            pdf_link = pdf_link_tag.get('href')
                            
                            # 判断是否为完整 URL
                            if not pdf_link.startswith('http'):
                                pdf_link = 'https://www.usenix.org' + pdf_link
                            
                            print(f"PDF 链接: {pdf_link}")
                            
                            # 下载 PDF 文件
                            try:
                                pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
                                if pdf_response.status_code == 200:
                                    # 确保文件名不超过 Windows 最大长度限制
                                    if len(sanitized_title) > 200:
                                        sanitized_title = sanitized_title[:200]
                                    
                                    pdf_filename = f"{sanitized_title}.pdf"
                                    pdf_path = os.path.join(download_folder, pdf_filename)
                                    
                                    with open(pdf_path, 'wb') as f:
                                        f.write(pdf_response.content)
                                    print(f"已成功下载 PDF: {pdf_filename}")
                                else:
                                    print(f"下载 PDF 失败，状态码: {pdf_response.status_code}")
                            except Exception as e:
                                print(f"下载 PDF 时出错: {str(e)}")
                        else:
                            print("未找到 PDF 下载链接")
                    except requests.exceptions.TooManyRedirects:
                        print(f"跳过 [{year} {season}] 论文，遇到 TooManyRedirects 错误。")
                        continue  # 跳过当前这篇文章
                    except Exception as e:
                        print(f"访问论文页面时出错: {str(e)}")
                    
                    # 随机延迟 2 到 5 秒，避免请求过快被封
                    time.sleep(random.randint(0, 1))
    else:
        print(f'请求网页失败，状态码：{response.status_code}')
