import os

# 定义根目录
base_dir = r"C:\Users\lyz\Desktop\crawler\WiSec"

# 初始化所有文件数量的总和
grand_total = 0

# 遍历根目录下的每个文件夹
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    if os.path.isdir(folder_path):
        # 获取当前文件夹中的所有文件（只统计文件，不论后缀）
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        count = len(files)
        
        # 输出当前文件夹的文件数量
        print(f"{folder_name} 文件夹中的文件总数: {count}")
        
        # 累加总的文件数量
        grand_total += count

# 输出所有文件夹的文件总数量
print(f"所有文件夹共有文件: {grand_total}")