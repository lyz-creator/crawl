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

# 定义需要爬取的年份列表
years = [2019, 2020, 2021, 2022, 2023, 2024]

# 下载根目录
root_download_folder = r"C:\Users\lyz\Desktop\crawler\NDSS"

# 循环处理每个年份
for year in years:
    # 目标网页 URL
    url = f"https://www.ndss-symposium.org/ndss{year}/accepted-papers/"

    # 下载目录为每个年份创建一个单独的文件夹
    download_folder = os.path.join(root_download_folder, f"NDSS_{year}")
    
    # 如果下载目录不存在，创建该目录
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    try:
        # 发送 HTTP 请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 HTML 内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到所有 <a class="paper-link-abs"> 标签
        paper_links = soup.find_all('a', class_='paper-link-abs')

        if not paper_links:
            print(f"未找到 {year} 年的论文链接。")

        for a_tag in paper_links:
            # 提取论文详情页面的链接
            href = a_tag.get('href')

            # 提取论文标题
            title = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
            
            # 构建完整的论文 URL
            paper_url = href if href.startswith("http") else f"https://www.ndss-symposium.org{href}"
            print(f'{year}年论文 URL: {paper_url}')
            print(f'Title: {title}')

            # 访问论文详情页面
            paper_response = requests.get(paper_url)
            paper_response.raise_for_status()

            # 解析论文页面内容
            paper_soup = BeautifulSoup(paper_response.content, 'html.parser')

            # 查找 PDF 下载链接
            pdf_link_tag = paper_soup.find('a', class_='btn btn-light btn-sm pdf-button')
            if pdf_link_tag:
                pdf_url = pdf_link_tag.get('href')
                pdf_url = pdf_url if pdf_url.startswith('http') else f"https://www.ndss-symposium.org{pdf_url}"
                print(f"PDF 链接: {pdf_url}")

                # 下载 PDF 文件
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    # 确保文件名合法
                    sanitized_title = sanitize_filename(title)
                    pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")

                    # 保存 PDF 文件
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                    print(f"已保存 PDF：{pdf_path}")
                else:
                    print(f"PDF 下载失败: {pdf_url}")
            else:
                print(f"未能找到 PDF 链接：{paper_url}")

            # 随机延迟 1 到 3 秒
            time.sleep(random.randint(1, 3))
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误 ({year}): {e}")
    except Exception as e:
        print(f"发生未知错误 ({year}): {e}")
