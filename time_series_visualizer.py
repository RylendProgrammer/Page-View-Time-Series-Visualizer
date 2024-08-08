import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
#df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)
print(df.head())

# Clean data
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)
filtered_df = df[(df['value'] > lower_bound) & (df['value'] < upper_bound)]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(filtered_df.index, filtered_df['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = filtered_df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    fig = df_bar.plot(kind='bar', figsize=(10, 8), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.title('Average Daily Page Views per Month')
    plt.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()