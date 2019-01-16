
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import utils
from plot_util import plot_ci


def plot_proportion_ci(freq_list, freq_labels, title, ylabel='Proportion', ax=None):
    p, ci = [], []
    for freq in freq_list:
        x, n = freq
        prop, ci_low, ci_high = utils.proportion_ci(x, n)
        p.append(prop)
        ci.append([ci_low, ci_high])
    if ax is None:
        fig1, ax1 = plt.subplots()
    else:
        ax1 = ax
    ax1.set_ylim([-0.25, 1.25])
    plot_ci(p, ci, title=title, labels=freq_labels, ylabel=ylabel, ax=ax1)



def aggregate_resistance_levels(df, vn):
    dec = df[vn].apply(lambda x: 'nan' if np.isnan(x) else utils.resistance_decoding[x])
    dec_vc = dec.value_counts()
    res = {k: dec_vc[k] if k in dec_vc.index else 0 for k in (utils.resistance_level_names + ['nan'])}
    return res['S'], res['I'], res['R']


df = pd.read_csv('../data/aggregate_dataset.csv')


if False:
    # Analyse drug resistance trends over time
    # Split data by species, bacteria and drug

    df_sub = df[(df['Pos_control'] == 0) & (df['Neg_control'] == 0)]
    for species_name in ('HUMAN', 'PIG'):
        for bacteria_name in ('E.coli', 'Klebsiella'):
            no_of_subplot_rows = 4
            fig, axs = plt.subplots(2, no_of_subplot_rows)
            fig.set_size_inches(20, 10)
            for ax_i, dn in enumerate(utils.drug_names):
                freqs_to_plot, freq_labels = [], []
                for time_i in range(1, 5):
                    vn = utils.var_name(species_name, bacteria_name, dn, time_i)
                    s, i, r = aggregate_resistance_levels(df_sub, vn)
                    x = i + r
                    n = s + i + r
                    ylabel = '(I+R)/(S+I+R)'
                    freqs_to_plot.append((x, n))
                    freq_labels.append('t' + str(time_i))

                title = '{0} {1} {2}'.format(species_name, bacteria_name, dn)
                ax = axs[ax_i//no_of_subplot_rows, ax_i % no_of_subplot_rows]
                plot_proportion_ci(freqs_to_plot, freq_labels, title, ylabel=ylabel, ax=ax)


if True:
    # Compare resistance to different drugs
    # Split data by species, bacteria, time step = t1

    df_sub = df[(df['Pos_control'] == 0) & (df['Neg_control'] == 0)]
    no_of_subplot_rows = 2
    fig, axs = plt.subplots(2, no_of_subplot_rows)
    fig.set_size_inches(20, 10)
    for sn_i, species_name in enumerate(('HUMAN', 'PIG')):
        for bn_i, bacteria_name in enumerate(('E.coli', 'Klebsiella')):
            ax_i = 2*sn_i + bn_i
            time_i = 1
            freqs_to_plot, freq_labels = [], []
            for dn in utils.drug_names:
                vn = utils.var_name(species_name, bacteria_name, dn, time_i)
                s, i, r = aggregate_resistance_levels(df_sub, vn)
                x = i + r
                n = s + i + r
                ylabel = '(I+R)/(S+I+R)'
                freqs_to_plot.append((x, n))
                freq_labels.append(dn)

            title = '{0} {1} t{2}'.format(species_name, bacteria_name, time_i)
            ax = axs[ax_i//no_of_subplot_rows, ax_i % no_of_subplot_rows]
            plot_proportion_ci(freqs_to_plot, freq_labels, title, ylabel=ylabel, ax=ax)


if False:
    # Compare drug resistance in the two sites
    # Split data by species, bacteria, drug and time step

    df_sub = df[(df['Pos_control'] == 0) & (df['Neg_control'] == 0)]
    df_sub_kam = df_sub[df_sub['Site'] == utils.site_encoding['KAMPALA']]
    df_sub_mub = df_sub[df_sub['Site'] == utils.site_encoding['MUBENDE']]
    df_sub = [df_sub_kam, df_sub_mub]
    for species_name in ('HUMAN', 'PIG'):
        for bacteria_name in ('E.coli', 'Klebsiella'):
            no_of_subplot_rows = 4
            fig, axs = plt.subplots(2, no_of_subplot_rows)
            fig.set_size_inches(20, 10)
            for dn_i, dn in enumerate(utils.drug_names):
                freqs_to_plot, freq_labels = [], []
                for time_i in range(1, 5):
                    for site_i in range(0, 2):
                        vn = utils.var_name(species_name, bacteria_name, dn, time_i)
                        s, i, r = aggregate_resistance_levels(df_sub[site_i], vn)
                        x = i + r
                        n = s + i + r
                        ylabel = '(I+R)/(S+I+R)'
                        freqs_to_plot.append((x, n))
                        freq_labels.append(utils.site_decoding[site_i] + ' t' + str(time_i))

                title = '{0} {1} {2}'.format(species_name, bacteria_name, dn)
                ax = axs[dn_i // no_of_subplot_rows, dn_i % no_of_subplot_rows]
                plot_proportion_ci(freqs_to_plot, freq_labels, title, ylabel=ylabel, ax=ax)


print('Showing plots')
plt.show()
