import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import countries, col_palette, site_path
from utils import load_datasets


def plot_td(df, tag):
    td_counts = (df#[df['expired'].isna() & df['answertimestamp'].notna()] # exclude expired and exclude the one without answertimestamp
                 .groupby(['experimentid', 'userid'])
                 .answertimestamp
                 .count()
                 .reset_index()
                 .rename(columns={'answertimestamp': 'count'}))

    td_counts.to_csv(os.path.join(figures_path, f'td_{"_".join(tag.lower().split(" "))}.csv'), index=False)

    fig, ax = plt.subplots(figsize=(7, 5))

    ax = sns.boxplot(ax=ax,
                     data=td_counts, y="experimentid", x="count",
                     hue="experimentid",
                     order=list(countries.values()),
                     palette=col_palette,
                     whis=[0, 100], width=.6
                     )
    sns.stripplot(td_counts, ax=ax, x="count", y="experimentid", size=4, color=".3")

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel="", xlabel=f"number of time diaries per participant")
    sns.despine(ax=ax, trim=True, left=True)

    #plt.tight_layout()
    plt.savefig(
        os.path.join(figures_path, f'td_{"_".join(tag.lower().split(" "))}.pdf'),
        bbox_inches='tight')


def plot_activity_per_hour(activity_id, activity_label, td, legend=True):
    td[td.A3 == activity_id].to_csv(f'figures/td/td_answer_hour_{activity_label.lower()}.csv', index=False)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.despine(fig)
    g = sns.lineplot(data=td[td.A3 == activity_id],
                     x='time',
                     y='proportion',
                     palette=col_palette,
                     hue_order=list(countries.values()),
                     hue='experimentid',
                     legend=legend)
    if legend == True:
        sns.move_legend(ax, "lower center",
                        bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=False, )
        g.get_legend().set_title("")
    ax.set_xticks(['00:00', '05:00', '10:00', '15:00', '20:00'])
    ax.grid(False)
    ax.set(ylabel='% of diaries', xlabel='hour of the day')
    plt.tight_layout()
    plt.savefig(f'figures/td/td_answer_hour_{activity_label.lower()}.pdf',
                bbox_inches='tight')


def activities_distribution_per_hour(df):
    td = df.copy()
    td = td[td['tag'] == 'Time Diaries']
    td['instancetimestamp'] = td['instancetimestamp'].dt.floor('s')
    td['instancetimestamp'] = td['instancetimestamp'].dt.round('30min')
    td['time'] = td['instancetimestamp'].dt.strftime('%H:%M')
    td = (td.groupby(['experimentid', 'time'])['A3']
          .value_counts(normalize=True, dropna=True)
          .reset_index())
    td['proportion'] *= 100

    plot_activity_per_hour(activity_id=1, activity_label='Sleeping', td=td, legend=False)
    plot_activity_per_hour(activity_id=5, activity_label='Study', td=td, legend=False)
    plot_activity_per_hour(activity_id=2, activity_label='Eating', td=td, legend=True)


def get_food(df, columns):
    # questions about food are multichoice
    food = (df[columns + ['experimentid', 'userid', 'instancetimestamp']]
            .melt(value_vars=columns,
                  id_vars=['experimentid', 'userid', 'instancetimestamp']))

    list_per_country = (food
                        .groupby(['experimentid', 'variable'])['value']
                        .sum()
                        .reset_index()
                        .sort_values(['experimentid', 'value'], ascending=False))

    # compute ranking position of each food item per country
    list_per_country.loc[:, 'ord'] = (list_per_country
                                      .sort_values(['experimentid', 'value'],
                                                   ascending=False)
                                      .groupby(['experimentid'])
                                      .cumcount())
    pivot_top_per_country = pd.pivot(list_per_country, columns='experimentid',
                                     index='variable', values='ord')

    to_plot = pivot_top_per_country[list(countries.values())]  # reorder countries
    # take top selected food in at least one country
    top_k = 3
    to_plot = to_plot.loc[(to_plot < top_k).any(axis=1)]
    to_plot = to_plot + 1  # start ranking from 1
    return to_plot


def plot_parallel_plot_food(to_plot, figname):
    col_food_to_string = {
        'A3c_1': 'Bread, breakfast cereals',
        # 'Bread, steamed buns and/or breakfast cereals',
        'A3c_12': 'Water',
        'A3c_14': 'Coffee/tea or similar ',
        'A3c_2': 'Rice, potatoes, etc.',
        # Rice, potatoes, beans, pasta, noodles, dumplings, etc.'
        'A3c_20': 'Other food',
        'A3c_3': 'Vegetables',
        'A3c_4': 'Fruits',
        'A3c_7': 'Processed meat',  # 'Processed meat (ham, bacon, sausages)',
        'A3c_8': 'Dairy products',
        # 'Dairy products (Plain or low-fat milk, yoghurt, cheese)'
        # ===============
        'A6c_1': 'Confectionery',
        'A6c_2': 'Cookies, cakes, and pastries',
        'A6c_10': 'Rice, potatoes,...',
        'A6c_12': 'Fruits',
        'A6c_18': 'Water',
        'A6c_20': 'Coffee/tea',
        'A6c_21': 'Others non-alcoholic drink'
    }

    to_plot.reset_index().replace(col_food_to_string).to_csv(f'figures/td/{figname}.csv', index=False)
    # Create parallel plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # Vertical lines for the years
    # plt.axvline(x=years[0], color='black', linestyle='--', linewidth=1) # 1952
    # plt.axvline(x=years[1], color='black', linestyle='--', linewidth=1) # 1957
    g = sns.lineplot(data=to_plot.transpose(),
                     # hue_order=list(countries.values()),
                     sort=False,
                     dashes=False,
                     markers=True,
                     markersize=8,
                     legend=False)
    sns.despine(fig, left=True, bottom=True)
    # ax.yaxis.grid(False)
    ax.invert_yaxis()
    # np.concatenate((np.arange(1,top_k+1),np.arange(top_k+2, to_plot.max(None) + 1, 2)))
    uniques = list()
    for c in to_plot.columns:
        uniques.extend(list(to_plot[c].unique()))
    ax.set_yticks(list(set(uniques)))

    last_country = list(countries.values())[-1]

    for food_id in to_plot.index:
        y_position = to_plot.loc[food_id, last_country] + 0.2
        x_position = len(to_plot.columns) - 1 + 0.22
        plt.text(x_position,  # x-axis position
                 y_position,  # y-axis position
                 col_food_to_string[food_id],  # Text
                 fontsize=10,  # Text size
                 color='black',  # Text color
                 )
    g.set(xlabel=None, ylabel='ranking position')
    g.set_xlim(right=len(countries.values()) - 1 + 0.05)
    g.xaxis.tick_top()
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(f'figures/td/{figname}.pdf', bbox_inches='tight')


def mood_distribution_per_hour(mood_df):
    mood_df = mood_df[mood_df['A6a'].notna()]
    mood_df['instancetimestamp'] = mood_df['instancetimestamp'].dt.floor('s')
    mood_df['instancetimestamp'] = mood_df['instancetimestamp'].dt.round('30min')
    mood_df['time'] = mood_df['instancetimestamp'].dt.strftime('%H:%M')

    positive_mood = mood_df.copy()
    positive_mood['A6a'] = positive_mood['A6a'].replace({1: 1, 2: 1})
    positive_mood = (positive_mood.groupby(['experimentid', 'time'])['A6a']
                     .value_counts(normalize=True, dropna=True)
                     .reset_index())
    positive_mood['proportion'] *= 100

    # =========== plot ===============
    positive_mood[positive_mood['A6a'] == 1].to_csv('figures/td/td_answer_hour_mood.csv', index=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.despine(fig)
    g = sns.lineplot(data=positive_mood[positive_mood['A6a'] == 1],
                     x='time',
                     y='proportion',
                     palette=col_palette,
                     hue_order=list(countries.values()),
                     hue='experimentid',
                     legend=True)

    g.get_legend().set_title("")
    h, l = g.get_legend_handles_labels()
    g.legend_.remove()
    g.legend(h, l, ncol=2)
    ax.set_xticks(['00:00', '05:00', '10:00', '15:00', '20:00'])
    ax.set_ylim(0, 100)
    ax.grid(False)
    ax.set(ylabel='% of diaries', xlabel='hour of the day')
    plt.tight_layout()
    plt.savefig(f'figures/td/td_answer_hour_mood.pdf', bbox_inches='tight')


def plot_hist_mood_in_location(to_plot, location):
    to_plot.to_csv(f'figures/td/td_mood_distribution_country_{location}.csv', index=False)
    fig, ax = plt.subplots(figsize=(8, 6))

    # Use Seaborn color palette for consistent colors
    colors = sns.color_palette("viridis", n_colors=len(to_plot.columns))

    # Bottom tracker for stacking
    bottom = pd.Series([0] * len(to_plot), index=to_plot.index)

    # Plot each subcategory as a segment of the stacked bar
    for i, col in enumerate(
            ['very bad', 'fairly bad', 'neutral', 'fairly good', 'very good']):
        ax.bar(to_plot.index, to_plot[col], bottom=bottom, color=colors[i], label=col)
        # Update the bottom to stack the next subcategory on top
        bottom += to_plot[col]

    handles, labels = plt.gca().get_legend_handles_labels()
    order = [4, 3, 2, 1, 0]
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])

    sns.despine(fig, bottom=True, left=True)
    plt.xticks(rotation=35)
    ax.set(ylabel='% of mood reports', xlabel='')
    ax.grid(False)

    sns.move_legend(ax, "lower center",
                    bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=False, )
    plt.tight_layout()
    plt.savefig(f'figures/td/td_mood_distribution_country_{location}.pdf',
                bbox_inches='tight')


def mood_in_locations(mood_dist):
    HOME = [1, 2, 3]
    UNIVERSITY = [5, 6, 7, 8]
    mood_dist = mood_dist[mood_dist['A4'].isin(HOME + UNIVERSITY)]
    mood_dist['A4'] = mood_dist['A4'].astype(str).replace(
        {str(h): 'home' for h in HOME})
    mood_dist['A4'] = mood_dist['A4'].astype(str).replace(
        {str(u): 'uni' for u in UNIVERSITY})
    mood_dist['A6a'] = mood_dist['A6a'].astype(str).replace(
        {'5': 'very bad',
         '4': 'fairly bad',
         '3': 'neutral',
         '2': 'fairly good',
         '1': 'very good'})

    to_plot = (mood_dist
               .groupby(['experimentid', 'A4'])['A6a']
               .value_counts(normalize=True, dropna=True)
               .reset_index())

    to_plot = to_plot.pivot(index=['experimentid', 'A4'],
                            columns='A6a', values='proportion')
    to_plot = to_plot[list(to_plot.columns[::-1])]

    to_plot.columns.name = None

    for location in ['home', 'uni']:
        location_to_plot = to_plot.reset_index(level=1)
        location_to_plot = location_to_plot[location_to_plot['A4'] == location]
        location_to_plot.drop(columns='A4', inplace=True)
        location_to_plot = location_to_plot.reindex(index=countries.values())
        location_to_plot = location_to_plot.fillna(0)
        plot_hist_mood_in_location(location_to_plot, location)


def main():
    df = load_datasets(base_path, site_path, sensor_path)

    # BOXPLOT DISTRIBUTION OF USERS BASED ON NUMBER OF TIME DIARIES ANSWERED
    # for t in df.tag.unique():
    #    plot_td(df[df.tag == t], t)
    plot_td(df.copy(), 'all')

    # LINEPLOT DISTRIBUTION ACTIVITIES PER HOUR
    activities_distribution_per_hour(df.copy())

    # FOOD RANKING
    to_plot = get_food(df[df['tag'] == 'Time Diaries'].copy(),
                       columns=[f'A3c_{i}' for i in range(1, 21)])
    plot_parallel_plot_food(to_plot, figname='td_food_ranking')

    to_plot = get_food(df[df['tag'] == 'Snack Questions'].copy(),
                       columns=[c for c in df.columns if 'A6c' in c])
    plot_parallel_plot_food(to_plot, figname='snack_ranking')

    mood_distribution_per_hour(
       df[['userid', 'experimentid', 'instancetimestamp', 'A6a']].copy())

    mood_in_locations(df[['experimentid', 'instancetimestamp', 'A6a', 'A4']].copy())


if __name__ == '__main__':
    figures_path = 'figures/td'
    os.makedirs('figures/td', exist_ok=True)

    base_path = './data/'
    sensor_path = 'Diachronic-Interactions/timediaries.parquet'

    sns.set_theme(style="whitegrid", font_scale=1.5)

    main()

    #df = load_datasets(base_path, site_path, sensor_path)

    print('Done!')
