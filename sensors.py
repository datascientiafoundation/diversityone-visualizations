import glob
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config import site_path, countries, col_palette


base_path = './data/'
sensor_path = 'Sensors'

def upsample_data(n_users, site):
    # upsample to create missing 30min timeslots if necessary
    min_date = n_users['date'].min()
    max_date = n_users['date'].max()
    expected_n_of_timeslots = len(pd.date_range(min_date, max_date, freq='30min'))
    actual_n_of_timeslots = len(n_users['date'])
    if expected_n_of_timeslots > actual_n_of_timeslots:
        # add exception for amrita, missing timeslots at the end
        if 'amrita' in site.lower():
            print('skip amrita')
            return n_users
        print('before ', min_date, max_date,
              ' -- ', max_date - min_date,
              ' -- actual ', actual_n_of_timeslots,
              ' -- expected ', expected_n_of_timeslots)
        upsampled = n_users.set_index('date')['userid'].resample(
            '30min').asfreq().reset_index()
        print(set(upsampled['date'].unique()) - set(n_users['date'].unique()))
        n_users = n_users.merge(upsampled['date'], on='date', how='outer')
        print('before ', min_date, max_date, ' -- upsample ', len(n_users))
        # print(upsampled.index.min(), upsampled.index.max(), ' -- ', upsampled.index.max() -
        # upsampled.index.min(), ' -- ', len(upsampled))
    elif expected_n_of_timeslots < actual_n_of_timeslots:
        raise ValueError()
    elif expected_n_of_timeslots == actual_n_of_timeslots:
        print('upsample OK')
    else:
        raise ValueError()
    return n_users


def process_one_country(site):
    data = []
    sensor_stats = glob.glob(
        str(os.path.join(base_path, site, sensor_path, '*/*30min.csv')))
    for s in sensor_stats:
        df = pd.read_csv(s)
        df['sensor'] = os.path.basename(s).split('_')[0]
        data.append(df)

    all_df = pd.concat(data)
    all_df.experimentid = all_df.experimentid.replace(countries)
    df = all_df.melt(id_vars=['experimentid', 'userid', 'sensor'],
                     var_name='date',
                     value_name='n_rows')
    print(f"{site} min date {df['date'].min()} "
          f"max date {df['date'].max()}, "
          f"n_days {pd.to_datetime(df['date'].max()) - pd.to_datetime(df['date'].min())}"
          )
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date
    n_users = (df[df['n_rows'] > 0].groupby(['experimentid', 'day'])[
                   'userid'].nunique() / df['userid'].nunique()).reset_index()
    # n_users = upsample_data(n_users, site)
    n_users = n_users.sort_values(by='day')
    n_users['timeslot'] = list(range(1, len(n_users) + 1))
    return n_users


def droppout():
    all_users_all_counties = []
    for site in site_path:
        site_n_users = process_one_country(site)
        all_users_all_counties.append(site_n_users)

    df = pd.concat(all_users_all_counties)

    to_plot = df[df['timeslot'] <= 25].copy()
    to_plot['userid'] = to_plot['userid'] * 100

    to_plot[['experimentid', 'userid', 'timeslot']].to_csv(os.path.join(figures_path, 'dropout.csv'), index=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    g = sns.lineplot(data=to_plot.sort_values(by='experimentid'),
                     x='timeslot',
                     y='userid',
                     hue_order=list(countries.values()),
                     hue='experimentid',
                     palette=col_palette)
    g.set(xlabel="day of the experiment", ylabel="% of users")
    g.axes.set_ylim(0)
    g.axes.set_xlim(1)
    sns.despine(fig, bottom=True, left=True)
    ax.grid(axis='x')
    sns.move_legend(ax, "lower center",
                    bbox_to_anchor=(.45, 1), ncol=3, title=None, frameon=False, )
    #g.get_legend().set_title("")
    #h, l = g.get_legend_handles_labels()
    #g.legend_.remove()
    #g.legend(h, l, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_path, 'dropout.pdf'), bbox_inches='tight')


def applications():
    apps_count = pd.read_csv('data/apps_count.csv')

    app_to_remove = ['it.unitn.disi.witmee.sensorlog']
    top_per_country = apps_count.reset_index()
    top_per_country = top_per_country[
        ~top_per_country['applicationname'].isin(app_to_remove)]

    top_per_country.experimentid = top_per_country.experimentid.replace(countries)
    top_per_country.loc[:, 'ord'] = top_per_country.groupby(
        ['experimentid']).cumcount() + 1
    top_per_country.head()
    paper_table = (top_per_country
    .groupby(['experimentid'])
    .head(5)
    .sort_values(by=['experimentid', 'ord'])
    .pivot(index='ord', columns='experimentid', values='applicationname')[
        countries.values()])

    paper_table = paper_table.replace({
        'com.facebook.orca': 'Facebook Messenger',
        'com.google.android.youtube': 'Youtube',
        'com.spotify.music': 'Spotify',
        'com.google.android.apps.maps': 'Google Maps',
        'com.whatsapp': 'Whatsapp',
        'com.facebook.katana': 'Facebook',
        'com.google.android.gm': 'Google Gmail',
        'com.google.android.googlequicksearchbox': 'Google quick search box',
        'com.tencent.mm': 'WeChat',
        'com.tencent.mobileqq': 'QQ - Tencent',
        ' com.taobao.taobao': 'Tabao',
        'tv.danmaku.bili': 'Bilibili',
        'com.taobao.taobao': 'Taobao',
        'com.android.mms': 'Google Messages',
        'com.android.chrome': 'Google Chrome',
        'com.android.settings': 'Android settings',
        'com.android.vending': 'Google Play Store',
        'com.instagram.android': 'Instagram'
    })
    print('\n\n\n ============================')
    print(paper_table.T.reset_index().to_latex(index=False))


def load_application_datasets():
    base_path = './data/application/'
    repository_sensor_path = 'Sensors/App-usage/applicationevent.parquet'
    sites = ["Site_Copenhagen_DK",
             "Site_Amrita_IN",
             "Site_Trento_IT",
             "Site_Jilin_CN",
             "Site_London_UK",
             "Site_Asuncion_PY",
             "Site_Ulan-Bator_MN",
             "Site_San-Luis-Potosi_MX"
             ]

    data = []
    for site in sites:
        print(f'loading {site}...')
        df = pd.read_parquet(os.path.join(base_path, site, repository_sensor_path))
        count_user_per_app = (df
                              .groupby(['experimentid', 'applicationname'])[
                                  'userid']
                              .nunique()
                              .sort_values(ascending=False))
        data.append(count_user_per_app)

    df = pd.concat(data)
    df.to_csv('data/apps_count.csv')
    return df


if __name__ == '__main__':
    figures_path= 'figures/sensors'
    os.makedirs(figures_path, exist_ok=True)

    sns.set_theme(style="whitegrid", font_scale=1.5)

    droppout()

    # load_application_datasets()  # just need to be run once
    applications()

    print('Done!')
