
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_ci(p, ci, title='No title', labels=None, ylabel='Proportion', ax=None):
    x = list()
    for p_i, ci_i in zip(p, ci):
        ci_i_low = ci_i[0]
        z_se = p_i - ci_i_low
        x.append([p_i-z_se*2, p_i+z_se*2])

    if ax is None:
        fig1, ax1 = plt.subplots()
    else:
        ax1 = ax
    ax1.set_title(title)
    ax1.set_ylabel(ylabel)
    ax1.boxplot(x, labels=labels, showfliers=False, showbox=True, whis=False, showcaps=False)


if __name__ == '__main__':
    p = [4, 5]
    ci = [[3.75, 4.25], [4.75, 5.25]]
    plot_ci(p, ci, title='Test run')
    plt.show()
