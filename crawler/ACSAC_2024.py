# ACSAC_2024
import os
import requests
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置 Selenium 使用 Chrome 浏览器
options = webdriver.ChromeOptions()
options.headless = True  # 不打开浏览器窗口

# 创建 WebDriver 实例
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 目标网页 URL
url = "https://www.computer.org/csdl/proceedings/acsac/2024/25bv2xFWBfG"  

# 下载目录
download_folder = r"C:\Users\DGT_X\Desktop\crawler\ACSAC_2024"

# 如果下载目录不存在，创建该目录
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

def sanitize_filename(title):
    """清理文件名，使其合法"""
    return re.sub(r'[<>:"/\\|?*]', '_', title)

try:
    # 加载网页
    driver.get(url)
    # 等待页面加载完成
    time.sleep(3)  # 根据页面加载速度调整等待时间

    # 尝试找到并点击“接受”按钮
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "osano-cm-accept"))
        )
        accept_button.click()  # 点击“接受”按钮
        print("点击了'接受'按钮")
    except Exception:
        print("未找到'接受'按钮，跳过此步骤")

    # 等待页面更新，可能是加载更多内容后，点击“Load All”按钮
    try:
        load_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "dark-link.pointer"))
        )
        load_all_button.click()  # 点击“Load All”按钮
        print("点击了'Load All'按钮")
    except Exception:
        print("未找到'Load All'按钮，跳过此步骤")

    # 等待更多内容加载
    time.sleep(3)

    # 抓取所有 class="article-title" 的 a 标签
    article_titles = driver.find_elements(By.CLASS_NAME, 'article-title')
    print(f"找到 {len(article_titles)} 个符合条件的 a 标签。")
    
    # 输出每个 a 标签的标题、链接和 PDF 下载链接
    for idx, a_tag in enumerate(article_titles, start=1):
        title = a_tag.text.strip()  # 获取文章标题
        href = a_tag.get_attribute('href')  # 获取文章链接
        print(f"{idx}. Title: {title}")
        print(f"   Link: {href}")
        
        # 提取文章 ID，并构造 PDF 下载链接
        match = re.search(r'/([^/]+)/([^/]+)$', href)
        if match:
            paper_id = match.group(2)  # 获取文章 ID（URL 中的最后一部分）
            pdf_url = f"https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/{paper_id}/pdf"
            print(f"   PDF Link: {pdf_url}")

            # 下载 PDF 文件
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                # 使用论文标题作为文件名，确保路径安全
                sanitized_title = sanitize_filename(title)
                pdf_path = os.path.join(download_folder, f"{sanitized_title}.pdf")

                # 保存 PDF 文件
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"已保存 PDF：{pdf_path}")
            else:
                print(f"PDF 下载失败: {pdf_url}")

        # 随机等待 3 到 5 秒之间
        wait_time = random.uniform(20, 30)
        print(f"等待 {wait_time:.2f} 秒...")
        time.sleep(wait_time)

finally:
    driver.quit()  # 关闭浏览器