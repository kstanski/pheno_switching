
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 200)

from utils import var_name, build_encoding


df = pd.read_csv('../data/PHENOSWICTHING.csv')

# Check head of the table
print()
print('Original file')
print(df.head())

# Check consistency SAMPLING.POINT vs time_point (issue with KLAKIR071)
df['Time_point'] = df['CASE_ID3'].apply(lambda case_id: int(case_id[-1]))
rows = list()
for i, row in df.iterrows():
    if row['Time_point'] != row['SAMPLING.POINT']:
        rows.append(row)
time_point_vs_sampling_point_mismatch = pd.DataFrame(rows)
time_point_vs_sampling_point_mismatch.to_csv('../data/time_point_vs_sampling_point_mismatch.csv', encoding='utf-8')

# Clean data
df['Species'] = df['Species'].apply(lambda s: 'PIG' if s == 'pig' else s)

# Aggregate data
    # Build DataFrame
case_pig_ids = sorted(df[(df['TYPE'] == 'CASE') | (df['TYPE'] == 'PIG')]['CASE_ID3'].apply(lambda case_id: case_id[:-1]).unique())
pos_ids = sorted(df[df['TYPE'] == 'POS CONTROL']['CASE_ID3'].apply(lambda ctr_id: ctr_id[:-1] + '_P').unique())
neg_ids = sorted(df[df['TYPE'] == 'NEG CONTROL']['CASE_ID3'].apply(lambda ctr_id: ctr_id[:-1] + '_N').unique())
df_agr = pd.DataFrame({'ID': case_pig_ids + pos_ids + neg_ids})

colnames = ['Site', 'Pos_control', 'Neg_control']
for time_i in range(1, 5):
    colnames.append('PCT_t' + str(time_i))
for bacteria in df['Bacteria'].unique():
    for drug in df['variable'].unique():
        for species in df['Species'].unique():
            for time_i in range(1, 5):
                colnames.append(var_name(species, bacteria, drug, time_i))

for colname in colnames:
    df_agr[colname] = np.nan

df_agr.set_index('ID', inplace=True)

    # Fill DataFrame
site_encoding = build_encoding(['KAMPALA', 'MUBENDE'])
resistance_encoding = build_encoding(['S', 'I', 'R'])

for i, row in df.iterrows():
    pre_ID = row['CASE_ID3'][:-1]

    is_pos_neg_control = row['TYPE']
    if is_pos_neg_control == 'POS CONTROL':
        ID = pre_ID + '_P'
        df_agr.loc[ID, 'Pos_control'] = 1
        df_agr.loc[ID, 'Neg_control'] = 0
    elif is_pos_neg_control == 'NEG CONTROL':
        ID = pre_ID + '_N'
        df_agr.loc[ID, 'Pos_control'] = 0
        df_agr.loc[ID, 'Neg_control'] = 1
    else:
        ID = pre_ID
        df_agr.loc[ID, 'Pos_control'] = 0
        df_agr.loc[ID, 'Neg_control'] = 0

    df_agr.loc[ID, 'Site'] = site_encoding[row['SITE']]
    time_point = row['SAMPLING.POINT']
    pct = row['Res_pct']
    df_agr.loc[ID, 'PCT_t' + str(time_point)] = pct

    species = row['Species']
    bacteria = row['Bacteria']
    drug = row['variable']
    resistance_val = resistance_encoding[row['value']]
    df_agr.loc[ID, var_name(species, bacteria, drug, time_point)] = resistance_val

df_agr.to_csv('../data/aggregate_dataset.csv', encoding='utf-8')
