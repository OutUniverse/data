import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
import os

# 设置适合Mac屏幕的图形参数
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['figure.figsize'] = [10, 6]

excel_file = pd.ExcelFile('./data/hst_01_11.xlsx')
df = excel_file.parse('hst_01_11')

# 转换成交量为数值型
df['交易量'] = df['交易量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)

# 新增：转换总交易量为数值型（与交易量处理逻辑一致）
df['总交易量'] = df['总交易量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)

# 新增：计算交易量占总交易量的百分比（保留2位小数）
df['交易量占比(%)'] = (df['交易量'] / df['总交易量'] * 100).round(2)

# 将日期转换为 matplotlib 可接受的格式
df['日期'] = df['日期'].map(mdates.date2num)

# 准备绘制 K 线图的数据
ohlc = df[['日期', '开盘', '收盘', '高', '低']].copy()

# 创建主图和副图
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()  # 成交量轴
ax3 = ax1.twinx()  # 新增：百分比专用轴（避免与成交量刻度冲突）

# 调整ax3的位置，避免与ax2的y轴重叠
ax3.spines['right'].set_position(('outward', 60))

# 绘制中点连线
midline = (ohlc['高'] + ohlc['低']) / 2
ax1.plot(ohlc['日期'], midline, color='blue', label='middle', linewidth=1.0)

# 添加开盘价折线图（绿色）
ax1.plot(ohlc['日期'], ohlc['开盘'], color='green', label='open', linewidth=1.0)

# 添加收盘价折线图（红色）
ax1.plot(ohlc['日期'], ohlc['收盘'], color='red', label='close', linewidth=1.0)

# 在副图上绘制成交量折线图
ax2.plot(df['日期'], df['交易量'], color='orange', label='gmv', linewidth=1.0)

# 新增：绘制交易量占比百分比折线图（紫色）
# ax3.plot(df['日期'], df['交易量占比(%)'], color='purple', label='hst/hs(%)', linewidth=1.0)

# 设置 x 轴为日期格式
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

# 设置标题和轴标签
ax1.set_title('hstech index gmv relation', fontsize=12)
ax1.set_xlabel('date', fontsize=10)
ax1.set_ylabel('index', fontsize=10)
ax2.set_ylabel('gmv', fontsize=10)
ax3.set_ylabel('hst/hs', fontsize=10)  # 新增：百分比轴标签

# 减小坐标轴标签字体大小
ax1.tick_params(axis='both', which='major', labelsize=8)
ax2.tick_params(axis='both', which='major', labelsize=8)
ax3.tick_params(axis='both', which='major', labelsize=8, colors='purple')  # 百分比轴刻度设为紫色区分

# 整合所有图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()  # 新增：百分比图例
legend = ax2.legend(lines + lines2 + lines3, labels + labels2 + labels3, 
                   loc='upper left', 
                   fontsize=8,
                   frameon=True,
                   framealpha=0.8)

# 调整布局
plt.tight_layout(pad=1.0)

# 生成带时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"hstech_chart_{timestamp}.png"

# 确保输出目录存在
output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存图片
filepath = os.path.join(output_dir, filename)
plt.savefig(filepath, dpi=150, bbox_inches='tight')
print(f"图表已保存为: {filepath}")

# 显示图形
plt.show(block=True)