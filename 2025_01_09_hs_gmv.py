import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mdates
from datetime import timedelta

excel_file = pd.ExcelFile('./data/hs_01_10.xlsx')

df = excel_file.parse('sheet1')

# 转换成交量为数值型
df['成交量'] = df['成交量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)

# 将日期转换为 matplotlib 可接受的格式
df['日期'] = df['日期'].map(mdates.date2num)

# 准备绘制 K 线图的数据
ohlc = df[['日期', '開市', '收市', '高', '低']].copy()  # 使用copy避免修改原始数据

# 将K线图的日期往前移动
ohlc['日期'] = ohlc['日期']

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 创建主图和副图
fig, ax1 = plt.subplots(figsize=(16, 8))
ax2 = ax1.twinx()

# 绘制 K 线图 - 使用移动后的日期
candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# 计算 K 线图的中线并绘制折线图 - 使用移动后的日期
midline = (ohlc['高'] + ohlc['低']) / 2
ax1.plot(ohlc['日期'], midline, color='blue', label='middle', linewidth=0.3)

# 在副图上绘制成交量折线图 - 保持原始日期不变或也相应移动
# 如果希望成交量图也一起移动，使用：ax2.plot(ohlc['日期'], df['成交量'], color='orange', label='gmv')
# 如果希望成交量图保持原始位置，使用：
ax2.plot(df['日期'], df['成交量'], color='orange', label='gmv', linewidth=0.3)

# 设置 x 轴为日期格式
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

# 设置标题和轴标签
ax1.set_title('hstech index gmv relation')
ax1.set_xlabel('date')
ax1.set_ylabel('index')
ax2.set_ylabel('gmv')

# 添加图例 - 使用更小的字体和紧凑布局
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
legend = ax2.legend(lines + lines2, labels + labels2, loc='upper left', 
                   fontsize='small',  # 使用小号字体
                   frameon=True,      # 显示边框
                   fancybox=False,    # 不使用圆角边框
                   framealpha=0.8,    # 设置透明度
                   borderpad=0.5,     # 减少边框内边距
                   labelspacing=0.3,  # 减少标签之间的间距
                   handlelength=1.0,  # 减少图例句柄长度
                   handletextpad=0.5) # 减少句柄和文本之间的间距

# 如果需要进一步缩小图例框，可以调整图例的边框
if legend:
    legend.get_frame().set_linewidth(0.5)  # 减小边框线宽

plt.tight_layout()  # 自动调整布局，使图例不会超出边界
plt.show()