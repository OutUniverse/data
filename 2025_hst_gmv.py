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

excel_file = pd.ExcelFile('./data/hst_01_10.xlsx')
df = excel_file.parse('hst_01_10')

# 转换成交量为数值型
df['交易量'] = df['交易量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)

# 将日期转换为 matplotlib 可接受的格式
df['日期'] = df['日期'].map(mdates.date2num)

# 准备绘制 K 线图的数据
ohlc = df[['日期', '开盘', '收盘', '高', '低']].copy()

# 创建主图和副图
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# 隐藏K线图，只绘制中点连线
midline = (ohlc['高'] + ohlc['低']) / 2
ax1.plot(ohlc['日期'], midline, color='blue', label='middle', linewidth=1.0)

# 在副图上绘制成交量折线图
ax2.plot(df['日期'], df['交易量'], color='orange', label='gmv', linewidth=1.0)

# 设置 x 轴为日期格式
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

# 设置标题和轴标签
ax1.set_title('hstech index gmv relation', fontsize=12)
ax1.set_xlabel('date', fontsize=10)
ax1.set_ylabel('index', fontsize=10)
ax2.set_ylabel('gmv', fontsize=10)

# 减小坐标轴标签字体大小
ax1.tick_params(axis='both', which='major', labelsize=8)
ax2.tick_params(axis='both', which='major', labelsize=8)

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
legend = ax2.legend(lines + lines2, labels + labels2, loc='upper left', 
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
plt.show(block=True)  # block=True 确保程序等待窗口关闭