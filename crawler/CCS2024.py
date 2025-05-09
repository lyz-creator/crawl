# CSS 若IP无访问权限，建议下载论文集：https://dl.acm.org/doi/pdf/10.1145/3658644

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 设置 Chrome 驱动选项
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")  # 让浏览器在无头模式下运行
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# 设置自定义的 User-Agent
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
# chrome_options.add_argument(f"user-agent={user_agent}")

# 启动 Chrome 浏览器，webdriver-manager 会自动管理 ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 目标网页 URL
url = "https://dl.acm.org/doi/proceedings/10.1145/3658644"

# 打开网页
driver.get(url)

# 给页面加载一些时间，防止加载失败
time.sleep(3)

# 获取并输出 User-Agent
actual_user_agent = driver.execute_script("return navigator.userAgent;")
print(f"实际 User-Agent: {actual_user_agent}")

# 输出一些调试信息
print(f"请求 URL: {url}")
print(f"页面标题: {driver.title}")

# 获取网页的 HTML 内容
html_content = driver.page_source

# 解析 HTML 内容
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有 class="section__title accordion-tabbed__control left-bordered-title" 的 a 标签
a_tags = soup.find_all('a', class_='section__title accordion-tabbed__control left-bordered-title')

# 输出找到的 a 标签数量
print(f"找到 {len(a_tags)} 个 <a> 标签，class='section__title accordion-tabbed__control left-bordered-title'。")

# 输出每个标签的标题
for a_tag in a_tags:
    title = a_tag.get_text(strip=True)
    print(f"标题: {title}")

# 关闭浏览器
driver.quit()
