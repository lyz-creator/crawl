import os
import time
import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize_filename(name):
    """将文件名中的非法字符替换为下划线"""
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def wait_for_new_pdf_and_rename(download_dir, old_files, new_filename, timeout=120):
    """
    等待下载目录出现新的 PDF 文件，一旦出现且文件大小稳定，就重命名为 new_filename.pdf。
    超时后返回 None。
    """
    start_time = time.time()
    while True:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - old_files
        pdf_candidates = [f for f in new_files if f.lower().endswith('.pdf')]
        if pdf_candidates:
            pdf_file = pdf_candidates[0]
            pdf_path = os.path.join(download_dir, pdf_file)

            # 等待文件大小稳定
            stable_count = 0
            last_size = -1
            while stable_count < 6:
                if not os.path.exists(pdf_path):
                    break
                size = os.path.getsize(pdf_path)
                if size == last_size:
                    stable_count += 1
                else:
                    stable_count = 0
                last_size = size
                time.sleep(5)

            safe_name = sanitize_filename(new_filename) + ".pdf"
            new_path = os.path.join(download_dir, safe_name)
            if os.path.exists(pdf_path):
                os.rename(pdf_path, new_path)
                return new_path
            else:
                return None

        if time.time() - start_time > timeout:
            return None
        time.sleep(1)

def create_driver(download_dir):
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "plugins.always_open_pdf_externally": True,  
        "download.prompt_for_download": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

def get_all_volume_links(driver, main_url):
    driver.get(main_url)
    time.sleep(3)
    # 滚动页面以确保加载全部内容
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    # 尝试点击“Show more volumes”（若有）
    try:
        show_more_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='show-more-volumes']")
        show_more_btn.click()
        time.sleep(2)
    except Exception:
        pass

    # 首先尝试 ul#kb-nav-volumes
    volume_elements = driver.find_elements(By.CSS_SELECTOR, "ul#kb-nav-volumes li a")
    print("[调试] kb-nav-volumes 找到数量：", len(volume_elements))
    # 若为 0，再尝试 section[data-test='other-volumes']
    if len(volume_elements) == 0:
        volume_elements = driver.find_elements(By.CSS_SELECTOR, "section[data-test='other-volumes'] li a")
        print("[调试] other-volumes 找到数量：", len(volume_elements))

    volume_links = []
    for elem in volume_elements:
        link = elem.get_attribute("href")
        if link and "/book/" in link:
            if not link.startswith("http"):
                link = "https://link.springer.com" + link
            volume_links.append(link)
    print("[调试] 最终卷链接列表：", volume_links)
    return volume_links

def get_chapter_links(driver, volume_url):
    driver.get(volume_url)
    time.sleep(3)
    # 只抓取以 /chapter/ 开头的链接（避免直接抓到 PDF 链接）
    chapter_elems = driver.find_elements(By.CSS_SELECTOR, "li[data-test='chapter'] a[href^='/chapter/']")
    chapter_links = []
    for elem in chapter_elems:
        href = elem.get_attribute("href")
        if href and "/chapter/" in href:
            if not href.startswith("http"):
                href = "https://link.springer.com" + href
            chapter_links.append(href)
    print(f"[调试] {volume_url} 下发现章节数：{len(chapter_links)}")
    return chapter_links

def download_pdf(driver, chapter_url, download_dir):
    driver.get(chapter_url)
    # 尝试获取章节标题
    try:
        title_elem = driver.find_element(By.TAG_NAME, 'h1')
        chapter_title = title_elem.text.strip()
    except Exception:
        chapter_title = "Unknown_Chapter"

    # 获取下载前目录中已有的文件列表
    old_files = set(os.listdir(download_dir))
    
    try:
        wait = WebDriverWait(driver, 10)
        pdf_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-track-action='Pdf download']")))
        pdf_button.click()
        print(f"[下载触发] {chapter_title} → {chapter_url}")
    except Exception as e:
        print(f"[错误] {chapter_url} 未找到下载按钮：{e}")
        return

    # 等待 PDF 下载完成并重命名
    result_path = wait_for_new_pdf_and_rename(download_dir, old_files, chapter_title)
    if result_path:
        print(f"[完成] 保存为: {os.path.basename(result_path)}")
    else:
        print(f"[警告] {chapter_title} 下载超时或重命名失败。")

def main(url, output_dir, include_all):
    os.makedirs(output_dir, exist_ok=True)
    driver = create_driver(output_dir)

    # 处理主卷以及其他卷（如果 --all 参数指定）
    volume_urls = [url]
    if include_all:
        extra = get_all_volume_links(driver, url)
        volume_urls.extend(extra)

    print("【发现卷】总共处理卷数：", len(volume_urls))

    for vol_url in volume_urls:
        print("\n[处理卷]:", vol_url)
        chapter_links = get_chapter_links(driver, vol_url)
        for chap_url in chapter_links:
            download_pdf(driver, chap_url, output_dir)

    driver.quit()
    print("\n✅ 所有下载任务已完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--output', type=str, default='downloads')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    main(args.url, args.output, args.all)




#2024#  python ASIACRYPT.py --url https://link.springer.com/book/10.1007/978-981-96-0875-1 --output C:/Users/DGT_X/Desktop/crawler/ASIACRYPT/2024 --all 
#2023#  python ASIACRYPT.py --url https://link.springer.com/book/10.1007/978-981-99-8721-4 --output C:/Users/DGT_X/Desktop/crawler/ASIACRYPT/2023 --all 
#2022#  python ASIACRYPT.py --url https://link.springer.com/book/10.1007/978-3-031-22963-3 --output C:/Users/DGT_X/Desktop/crawler/ASIACRYPT/2022 --all 
#2021#  python ASIACRYPT.py --url https://link.springer.com/book/10.1007/978-3-030-92062-3 --output C:/Users/DGT_X/Desktop/crawler/ASIACRYPT/2021 --all 
#2020#  python ASIACRYPT.py --url https://link.springer.com/book/10.1007/978-3-030-64837-4 --output C:/Users/DGT_X/Desktop/crawler/ASIACRYPT/2020 --all 