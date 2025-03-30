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

# 目标网页 URL
url = "https://www.ndss-symposium.org/ndss2018/accepted-papers/"

# 下载目录
download_folder = r"C:\Users\lyz\Desktop\crawler\NDSS\NDSS_2018"

# 如果下载目录不存在，创建该目录
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

try:
    # 发送 HTTP 请求
    response = requests.get(url)
    # 检查请求是否成功
    response.raise_for_status()  # 如果请求失败，会抛出异常

    # 解析 HTML 内容
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 找到所有 <h3 class="wp-block-heading"> 标签，获取论文标题
    paper_titles = soup.find_all('h3', class_='wp-block-heading')
    
    if not paper_titles:
        print("未找到任何论文标题。")
    
    for title_tag in paper_titles:
        title = title_tag.get_text(strip=True)
        print(f"论文标题: {title}")
        
        # 找到每篇论文的下载链接 <p class="paper-link-abs">
        paper_link_tag = title_tag.find_next('p', class_='paper-link-abs')
        if paper_link_tag:
            a_tag = paper_link_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                pdf_url = a_tag['href']
                # 输出 PDF 链接
                print(f"PDF 链接: {pdf_url}")
                
                # 下载 PDF 文件
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    # 使用 sanitize_filename 确保文件名合法
                    sanitized_title = sanitize_filename(title)
                    pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")
                    
                    # 保存 PDF 文件
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                    print(f"已保存 PDF：{pdf_path}")
                else:
                    print(f"PDF 下载失败: {pdf_url}")
            else:
                print(f"未找到有效的 PDF 链接：{title}")
        else:
            print(f"未找到 PDF 链接：{title}")
        
        # 随机延迟 1 到 3 秒
        time.sleep(random.randint(1, 3))

except requests.exceptions.RequestException as e:
    print(f"请求过程中发生错误: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")
