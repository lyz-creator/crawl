import os

# 定义根目录
base_dir = r"C:\Users\lyz\Desktop\crawler\NDSS"

# 初始化总的PDF文件数量
total_pdfs = 0

# 遍历根目录下的每个文件夹
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    if os.path.isdir(folder_path):
        # 统计当前文件夹中的PDF文件数量
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        pdf_count = len(pdf_files)
        
        # 输出当前文件夹的PDF数量
        print(f"{folder_name} 文件夹中的PDF数量: {pdf_count}")
        
        # 累加总的PDF数量
        total_pdfs += pdf_count

# 输出总的PDF文件数量
print(f"总共有PDF文件: {total_pdfs}")
