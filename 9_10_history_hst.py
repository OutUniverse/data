import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import glob

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# === 1. 设置参数 ===
data_folder = "./data"  # 数据文件夹路径
file_pattern = "hsi-*.xlsx"  # 文件模式，匹配所有hsi-开头的Excel文件
base_year = 2024  # 用作基准的年份，所有数据将映射到这一年

# === 2. 获取所有数据文件 ===
file_paths = glob.glob(os.path.join(data_folder, file_pattern))
print(f"找到 {len(file_paths)} 个数据文件: {[os.path.basename(f) for f in file_paths]}")

# === 3. 读取和处理所有文件 ===
all_data = {}

for file_path in file_paths:
    try:
        # 从文件名提取年份
        file_name = os.path.basename(file_path)
        year = int(''.join(filter(str.isdigit, file_name)))
        
        # 读取数据
        df = pd.read_excel(file_path)
        
        # 标准化列名
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # 获取列名
        date_col = next((c for c in df.columns if 'date' in c or '日期' in c), None)
        high_col = next((c for c in df.columns if 'high' in c or '高' in c), None)
        low_col = next((c for c in df.columns if 'low' in c or '低' in c), None)
        
        if not all([date_col, high_col, low_col]):
            print(f"警告: 文件 {file_name} 缺少必要的列")
            continue
        
        # 日期格式化
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 只保留9-12月的数据
        df = df[(df[date_col].dt.month >= 9)].copy()
        
        # 删除空值
        df = df.dropna(subset=[date_col, high_col, low_col]).reset_index(drop=True)
        
        # 为数据创建统一的日期（使用基准年份，方便比较）
        df['plot_date'] = pd.to_datetime(
            base_year * 10000 + df[date_col].dt.month * 100 + df[date_col].dt.day, 
            format='%Y%m%d'
        )
        
        # 存储处理后的数据
        all_data[year] = df
        
        print(f"成功处理 {year} 年数据: {len(df)} 个数据点")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

# === 4. 检查是否有数据 ===
if not all_data:
    print("没有找到有效数据，请检查文件路径和格式")
    exit()

# === 5. 绘制 K 线图 ===
plt.figure(figsize=(14, 8))

# 生成颜色列表
years = sorted(all_data.keys())
colors = plt.cm.tab10(range(len(years)))  # 使用tab10颜色映射

for i, year in enumerate(years):
    df = all_data[year]
    color = colors[i]
    
    # 绘制K线
    plt.vlines(df['plot_date'], df[low_col], df[high_col], 
               color=color, linewidth=1.2, alpha=0.7, label=str(year))
    
    # 绘制中点线
    plt.plot(df['plot_date'], (df[high_col] + df[low_col]) / 2, 
             color=color, linewidth=0.8, alpha=0.7)

# 设置 x 轴范围和刻度
all_plot_dates = pd.concat([df['plot_date'] for df in all_data.values()])
start_date = all_plot_dates.min()
end_date = all_plot_dates.max()
plt.xlim(start_date, end_date)

# 设置 x 轴刻度为每月的第一天
from matplotlib.dates import MonthLocator, DateFormatter
ax = plt.gca()
ax.xaxis.set_major_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))

# 旋转 x 轴标签以避免重叠
plt.xticks(rotation=45)

plt.title(f"恒生科技指数 K 线图比较 ({len(years)}年9-12月)")
plt.xlabel("月份-日期")
plt.ylabel("价格")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="年份", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# === 6. 可选：保存合并的数据 ===
# 如果需要进一步分析，可以保存合并的数据
# output_path = os.path.join(data_folder, "combined_data.csv")
# combined_df = pd.concat([df.assign(year=year) for year, df in all_data.items()], ignore_index=True)
# combined_df.to_csv(output_path, index=False)
# print(f"合并数据已保存到: {output_path}")