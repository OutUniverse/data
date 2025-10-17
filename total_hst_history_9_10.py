import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# 1. 替换为你的文件实际路径（Mac路径示例：/Users/你的用户名/文档/hst-2016-2025.xlsx）
df = pd.read_excel("./data/hst-2016-2025.xlsx", sheet_name='恒生科技指數歷史數據')

# 2. 数据预处理（保持不变）
df['日期'] = pd.to_datetime(df['日期'])
# df_filtered = df[df['日期'].dt.month.isin([9, 10, 11, 12])]  # 筛选9-12月数据
df_filtered = df.copy()

# 3. 关键调整：减小画布尺寸+降低分辨率（适配Mac屏幕）
plt.rcParams['figure.dpi'] = 150  # 从300降至150，减少像素量
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Heiti TC']  # 适配Mac中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号乱码

# 4. 创建图形：缩小figsize（宽8英寸、高4英寸，Mac普通屏幕可完整显示）
fig, ax = plt.subplots(figsize=(8, 4))  # 核心调整：原(12,6)→(8,4)

# 5. 绘图逻辑（保持不变）
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
years = sorted(df_filtered['日期'].dt.year.unique())

for i, year in enumerate(years):
    year_data = df_filtered[df_filtered['日期'].dt.year == year]
    # 统一年份为2000年，确保横轴仅显示月日
    x = year_data['日期'].apply(lambda dt: dt.replace(year=2000))
    x = mdates.date2num(x)
    y_high = year_data['高']
    y_low = year_data['低']
    y_mid = (y_high + y_low) / 2

    # 绘制高低线（K线）和中间连线
    ax.vlines(x, y_low, y_high, color=colors[i % len(colors)], label=str(year), linewidth=0.8)  # 减细线宽避免拥挤
    ax.plot(x, y_mid, color=colors[i % len(colors)], linestyle='--', alpha=0.5, linewidth=0.5)

# 6. 坐标轴与图例调整（避免超出屏幕）
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))
plt.xticks(rotation=0)  # 月份标签不旋转，节省横向空间

# 图例移至下方（原右侧易超出屏幕）
ax.legend(title='year', loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=5)  # 水平排列节省纵向空间

# 7. 标题与网格（保持简洁）
ax.set_title('hst indx', fontsize=10)
ax.set_xlabel('month', fontsize=9)
ax.set_ylabel('index', fontsize=9)
ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5)

# 8. 自动调整布局（关键：防止标签被截断）
plt.tight_layout()  # 自动适配所有元素位置
plt.subplots_adjust(bottom=0.2)  # 预留底部空间放图例

# 9. 显示图形
plt.show()