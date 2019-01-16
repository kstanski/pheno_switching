
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import utils


df = pd.read_csv('../data/aggregate_dataset.csv')

#df_sub = df[(df['Pos_control'] == 0) & (df['Neg_control'] == 0)]

fig, axs = plt.subplots(2, 2)
fig.set_size_inches(15, 15)
for ax_idx, time_i in enumerate(range(1,5)):
    ax = axs[ax_idx // 2, ax_idx % 2]
    ax.hist(df['PCT_t' + str(time_i)], bins=10)
    ax.set_title('Time step t' + str(time_i))
    ax.set_ylabel('counts')
    ax.set_xlabel('PCT result')

print('Showing plots')
plt.show()
