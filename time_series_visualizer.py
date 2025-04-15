import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar e limpar dados
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')
# Filtrando os dados para remover os 2.5% superiores e inferiores
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Copiar o dataframe para segurança
    df_line = df.copy()

    # Criar figura e plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar e retornar a figura
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Preparar dados
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupar e pivotar
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    # Corrigir a ordem dos meses
    df_grouped = df_grouped[['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 'December']]

    # Criar gráfico
    fig = df_grouped.plot(kind='bar', figsize=(15, 7)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Preparar dados
    df_box = df.copy().reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Criar gráficos
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Diagrama por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Diagrama por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()
    fig.savefig('box_plot.png')
    return fig