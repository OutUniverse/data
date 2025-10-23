import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mdates
from datetime import timedelta

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 创建主图和副图
fig, ax1 = plt.subplots(figsize=(16, 8))
ax2 = ax1.twinx()

# 读取并处理第一个文件 (hts_01_10.xlsx)
excel_file1 = pd.ExcelFile('./data/hts_01_10.xlsx')
df1 = excel_file1.parse('sheet1')
df1['成交量'] = df1['成交量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)
df1['日期'] = df1['日期'].map(mdates.date2num)
ohlc1 = df1[['日期', '開市', '收市', '高', '低']].copy()

# 绘制第一个文件的K线图
candlestick_ohlc(ax1, ohlc1.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# 计算并绘制第一个文件的中线 - 使用蓝色
midline1 = (ohlc1['高'] + ohlc1['低']) / 2
ax1.plot(ohlc1['日期'], midline1, color='blue', label='HTS Middle', linewidth=0.8)

# 在副图上绘制第一个文件的成交量 - 使用橙色
ax2.plot(df1['日期'], df1['成交量'], color='orange', label='HTS GMV', linewidth=0.8)

# 读取并处理第二个文件 (hs_01_10.xlsx)
excel_file2 = pd.ExcelFile('./data/hs_01_10.xlsx')
df2 = excel_file2.parse('sheet1')
df2['成交量'] = df2['成交量'].replace({'B': '*1e9', 'M': '*1e6'}, regex=True).map(pd.eval).astype(float)
df2['日期'] = df2['日期'].map(mdates.date2num)
ohlc2 = df2[['日期', '開市', '收市', '高', '低']].copy()

# 绘制第二个文件的K线图 - 使用不同的透明度区分
candlestick_ohlc(ax1, ohlc2.values, width=0.4, colorup='darkgreen', colordown='darkred', alpha=0.6)

# 计算并绘制第二个文件的中线 - 使用紫色
midline2 = (ohlc2['高'] + ohlc2['低']) / 2
ax1.plot(ohlc2['日期'], midline2, color='purple', label='HS Middle', linewidth=0.8)

# 在副图上绘制第二个文件的成交量 - 使用青色
ax2.plot(df2['日期'], df2['成交量'], color='cyan', label='HS GMV', linewidth=0.8)

# 设置 x 轴为日期格式
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

# 设置标题和轴标签
ax1.set_title('HTS and HS Index GMV Relation')
ax1.set_xlabel('Date')
ax1.set_ylabel('Index')
ax2.set_ylabel('GMV')

# 添加图例 - 合并所有图例项
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# 合并两个轴的图例
all_lines = lines1 + lines2
all_labels = labels1 + labels2

legend = ax2.legend(all_lines, all_labels, loc='upper left', 
                   fontsize='small',
                   frameon=True,
                   fancybox=False,
                   framealpha=0.8,
                   borderpad=0.5,
                   labelspacing=0.3,
                   handlelength=1.0,
                   handletextpad=0.5)

if legend:
    legend.get_frame().set_linewidth(0.5)

plt.tight_layout()
plt.show()