import seaborn as sns

countries_NON_ANON = {
    'wenetDenmark': 'AAU',  # 'DK',
    'wenetIndia': 'AMRITA',  # 'IN',
    'wenetMexico': 'IPICYT',  # 'MX',
    'wenetChina': 'JLU',  # 'CN',
    'wenetUK': 'LSE',  #'UK'
    #'wenetUk': 'LSE',
    'wenetMongolia': 'NUM',  # 'MN',
    'wenetParaguay': 'UC',  # 'PY',
    'wenetItaly': 'UNITN',  # 'IT',
}

countries = {
    'wenetDenmark': 'UNI-DEN',  # 'DK',
    'wenetIndia': 'UNI-IND',  # 'IN',
    'wenetMexico': 'UNI-MEX',  # 'MX',
    'wenetChina': 'UNI-CHN',  # 'CN',
    'wenetUK': 'UNI-UK',  #'UK'
    #'wenetUk': 'LSE',
    'wenetMongolia': 'UNI-MON',  # 'MN',
    'wenetParaguay': 'UNI-PAR',  # 'PY',
    'wenetItaly': 'UNI-ITA',  # 'IT',
}

site_path = [
    "Site_Copenhagen_DK",
    "Site_Amrita_IN",
    "Site_Trento_IT",
    "Site_Jilin_CN",
    "Site_London_UK",
    "Site_Asuncion_PY",
    "Site_Ulan-Bator_MN",
    "Site_San-Luis-Potosi_MX",
]

# sns.color_palette("colorblind", 8)
sns.color_palette("Set2", 8)
col_palette = dict(zip(countries.values(), sns.color_palette("deep", 8)))

# palette_per_continent = OrderedDict({
#     # europe
#     'IT': col_palette[0],
#     'UK': col_palette[0],
#     "DK": col_palette[0],
#     # asia
#     "CN": col_palette[2],
#     "IN": col_palette[2],
#     'MN': col_palette[2],
#     # south-america
#     'MX': col_palette[7],
#     'PY': col_palette[7],
# })
