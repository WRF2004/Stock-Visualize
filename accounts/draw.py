import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64


def Opening_and_closing_price_average_bar_chart(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'open_price', 'close_price']]
    average = data_to_use.groupby('stock_code').mean()


    plt.figure(figsize=(30, 15))
    bar_width = 0.5
    index = range(len(average))

    plt.bar(index, average['open_price'], bar_width, label='Average Open Price')
    plt.bar([i + bar_width for i in index], average['close_price'], bar_width, label='Average Close Price')

    plt.title('Opening and closing price average bar chart')
    plt.xlabel('Stock Code')
    plt.ylabel('Price')
    plt.xticks([i + bar_width / 2 for i in index], list(average.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64


def Total_trading_volume_bar_chart(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'volume']]
    total = data_to_use.groupby('stock_code').sum()


    plt.figure(figsize=(50, 25))
    bar_width = 0.5
    index = range(len(total))

    plt.bar(index, total['volume'], bar_width, label='Total trading Volume')

    plt.title('Total trading volume bar chart')
    plt.xlabel('Stock Code')
    plt.ylabel('Volume')
    plt.xticks([i for i in index], list(total.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64


def Bar_chart_of_the_highest_price_reached_by_each_stock(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'high_price']]
    highest = data_to_use.groupby('stock_code').max()


    plt.figure(figsize=(50, 25))
    bar_width = 0.5
    index = range(len(highest))

    plt.bar(index, highest['high_price'], bar_width, label='highest price')

    plt.title('Bar chart of the highest price reached by each stock')
    plt.xlabel('Stock Code')
    plt.ylabel('highest price')
    plt.xticks([i for i in index], list(highest.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64

def Bar_chart_of_the_lowest_price_reached_by_each_stock(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'low_price']]
    lowest = data_to_use.groupby('stock_code').min()

    plt.figure(figsize=(50, 25))
    bar_width = 0.5
    index = range(len(lowest))
    plt.bar(index, lowest['low_price'], bar_width, label='lowest price')

    plt.title('Bar chart of the lowest price reached by each stock')
    plt.xlabel('Stock Code')
    plt.ylabel('lowest price')
    plt.xticks([i for i in index], list(lowest.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64

def Bar_chart_of_the_compound_increase_or_decrease_of_each_stock_in_the_year(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    df['date'] = pd.to_datetime(df['date'])

    grouped = df.groupby('stock_code')

    # 计算每只股票的年初和年末价格
    start_prices = grouped.apply(lambda x: x.loc[x['date'].idxmin()]['close_price'])
    end_prices = grouped.apply(lambda x: x.loc[x['date'].idxmax()]['close_price'])

    compound_change = ((end_prices - start_prices) / start_prices) * 100
    plt.figure(figsize=(50, 25))
    bar_width = 0.5
    index = range(len(compound_change))
    plt.bar(index, compound_change, bar_width, label='compound change')

    plt.title('Bar chart of the compound increase or decrease of each stock in the year')
    plt.xlabel('Stock Code')
    plt.ylabel('compound change')
    plt.xticks([i for i in index], list(compound_change.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64

def A_scatter_plot_of_the_average_amplitude_of_each_stock(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'amplitude']]
    amplitude = data_to_use.groupby('stock_code').mean()

    plt.figure(figsize=(50, 25))

    import seaborn as sns

    sns.scatterplot(x='stock_code', y='amplitude', data=amplitude, s=100, color='red')
    plt.xlabel('Stock Code')
    plt.ylabel('Average Amplitude')
    plt.title('A Scatter Plot of the Average Amplitude of Each Stock')
    plt.xticks(rotation=90)
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64

def A_bar_chart_of_the_average_turnover_rate_of_each_stock(df):
    df.columns = ['stock_code', 'date', 'open_price', 'close_price', 'high_price', 'low_price',
                  'volume', 'change', 'amplitude', 'turnover']
    data_to_use = df[['stock_code', 'turnover']]
    average = data_to_use.groupby('stock_code').mean()

    plt.figure(figsize=(50, 25))
    bar_width = 0.5
    index = range(len(average))

    plt.bar(index, average['turnover'], bar_width, label='Average Turnover Rate')


    plt.title('A bar chart of the average turnover rate of each stock')
    plt.xlabel('Stock Code')
    plt.ylabel('Average Turnover Rate')
    plt.xticks([i for i in index], list(average.index))
    plt.legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    image_base64 = plot_to_base64()
    plt.close()
    return image_base64