import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mdates

excel_file = pd.ExcelFile('./data/hst-2025-01-10.xlsx')

df = excel_file.parse('恒生科技指數歷史數據')

# 转换成交量为数值型
df['成交量'] = df['成交量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)

# 将日期转换为 matplotlib 可接受的格式
df['日期'] = df['日期'].map(mdates.date2num)

# 准备绘制 K 线图的数据
ohlc = df[['日期', '開市', '收市', '高', '低']]

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']

# 创建主图和副图
fig, ax1 = plt.subplots(figsize=(16, 8))
ax2 = ax1.twinx()

# 绘制 K 线图
candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# 计算 K 线图的中线并绘制折线图
midline = (ohlc['高'] + ohlc['低']) / 2
ax1.plot(df['日期'], midline, color='blue', label='中线')

# 在副图上绘制成交量折线图
ax2.plot(df['日期'], df['成交量'], color='orange', label='成交量')

# 设置 x 轴为日期格式
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 设置标题和轴标签
ax1.set_title('恒生科技指数K线图与成交量折线图')
ax1.set_xlabel('日期')
ax1.set_ylabel('指数')
ax2.set_ylabel('成交量')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.show()