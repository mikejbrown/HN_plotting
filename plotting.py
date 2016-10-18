# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 00:32:50 2016

@author: Michael
"""

import pylab as plt
import matplotlib
import pandas as pd
from scipy.stats.mstats import mode

from data_reader import read_data
from common import get_data_file_path, output_fig, time_points_for_variable

matplotlib.style.use('ggplot')
matplotlib.rc('figure', figsize=[9, 4])
matplotlib.rc('font', size=16)

DEFAULT_PLOT_OPTIONS = {'dpi': 128, 'bbox_inches': 'tight'}


def do_plots_for_variable(var, save_figs, **plot_options):
    """ Make a set of plots for the data on variable var. """
    cols = time_points_for_variable(var)
    time_point_labels = ["Baseline",
                         "Wk 2",
                         "Wk 4",
                         "Wk 6",
                         "FU 1",
                         "FU 3",
                         "FU 6",
                         "FU 12"]

    # Boxplots for each category
    plt.figure()
    for cat in DATA.Category.values.sort_values().unique():
        cdata = DATA[DATA.Category == cat][cols]
        cdata.columns = time_point_labels
        cdata.boxplot()
        plt.title('%s -- %s' % (var, cat))
        output_fig('%s-%s-boxplot.png' % (var, cat), save_figs, **plot_options)
        plt.clf()

    # Bar plots with error bars
    cols2 = cols.copy()
    cols2.insert(0, 'Category')

    mask = DATA.Patient > 0  # trivial mask
    title = r'%s ($1 \sigma$ error bars)' % var
    _do_plot(var, mask, title, save_figs, plot_options)

    mask = DATA.Chemo == 'No chemo'
    title = r'%s no chemo ($1 \sigma$ error bars)' % var
    _do_plot(var, mask, title, save_figs, plot_options)

    mask = DATA.Chemo == 'Chemo'
    title = r'%s chemo ($1 \sigma$ error bars)' % var
    _do_plot(var, mask, title, save_figs, plot_options)

    mask = DATA.Modality == '3D'
    title = r'%s 3D ($1 \sigma$ error bars)' % var
    _do_plot(var, mask, title, save_figs, plot_options)

    mask = DATA.Modality == 'IMRT'
    title = r'%s IMRT ($1 \sigma$ error bars)' % var
    _do_plot(var, mask, title, save_figs, plot_options)

    idx = ((DATA.Category == 'Oral') |
           (DATA.Category == 'Oropharynx') |
           (DATA.Category == 'Larynx'))
    cols.insert(0, 'Category')
    grouped_nochemo_data = DATA[DATA.Chemo == 'No chemo'][idx][cols].groupby('Category')
    grouped_chemo_data = DATA[DATA.Chemo == 'Chemo'][idx][cols].groupby('Category')

    means_nochemo = grouped_nochemo_data.mean()
    means_chemo = grouped_chemo_data.mean()
    means_nochemo.columns = time_point_labels
    means_chemo.columns = time_point_labels
    means_nochemo = means_nochemo.loc[['Oral', 'Oropharynx', 'Larynx']]
    means_chemo = means_chemo.loc[['Oral', 'Oropharynx', 'Larynx']]

    fname = '%s-oral-chemo-vs-nochemo-mean-reduced-lineplot.png' % var
    plt.figure()
    data = pd.DataFrame({'no chemo': means_nochemo.loc['Oral'],
                         'chemo': means_chemo.loc['Oral']})
    data.plot()
    plt.title('%s Oral mean - chemo vs no chemo' % var)
    plt.axis([0, len(time_point_labels)-1, -1, 101])
    plt.legend(loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

    fname = '%s-oropharynx-chemo-vs-nochemo-mean-reduced-lineplot.png' % var
    plt.figure()
    data = pd.DataFrame({'no chemo': means_nochemo.loc['Oropharynx'],
                         'chemo': means_chemo.loc['Oropharynx']})
    data.plot()
    plt.title('%s Oropharynx mean - chemo vs no chemo' % var)
    plt.axis([0, len(time_point_labels)-1, -1, 101])
    plt.legend(loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

    fname = '%s-larynx-chemo-vs-nochemo-mean-reduced-lineplot.png' % var
    plt.figure()
    data = pd.DataFrame({'no chemo': means_nochemo.loc['Larynx'],
                         'chemo': means_chemo.loc['Larynx']})
    data.plot()
    plt.title('%s Larynx mean - chemo vs no chemo' % var)
    plt.axis([0, len(time_point_labels)-1, -1, 101])
    plt.legend(loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

    # Histograms
    cols = time_points_for_variable(var)
    cols_data = DATA[cols]
    cols_data.columns = time_point_labels
    plt.figure()
    cols_data.plot.hist(stacked=True, cumulative=True)
    plt.legend(loc=(1.1, 0.2))
    plt.xlabel('%s' % var)
    plt.title('Cumulative frequency of %s score' % var)
    output_fig('%s-histogram.png' % var, save_figs, **plot_options)

    plt.figure()
    for cat in DATA.Category.values.sort_values().unique():
        cols_data = DATA[DATA.Category == cat][cols]
        cols_data.columns = time_point_labels
        cols_data.plot.hist(stacked=True, cumulative=True)
        plt.legend(loc=(1.1, -0.1))
        plt.xlabel('%s' % var)
        plt.title('Cumulative frequency of %s score -- %s' % (var, cat))
        output_fig('%s-%s-histogram.png' % (var, cat),
                   save_figs, **plot_options)
        plt.clf()


def _do_plot(var, mask, title, save_figs, plot_options):
    """ A helper function to do a boxplot with errorbars for masked data. """
    title_fields = title.replace(r'($1 \sigma$ error bars)', '').split()[:2]
    fname = '-'.join(title_fields) + '-reduced-barplot-errorbar.png'
    spread = .5
    cols = time_points_for_variable(var)
    cols.insert(0, 'Category')

    time_point_labels = ["Baseline",
                         "Wk 2",
                         "Wk 4",
                         "Wk 6",
                         "FU 1",
                         "FU 3",
                         "FU 6",
                         "FU 12"]
    idx = ((DATA.Category == 'Oral') |
           (DATA.Category == 'Oropharynx') |
           (DATA.Category == 'Larynx'))

    grouped_data = DATA[mask][idx][cols].groupby('Category')

    means = grouped_data.mean()
    means.columns = time_point_labels
    means = means.loc[['Oral', 'Oropharynx', 'Larynx']]

    errors = grouped_data.std()
    errors.columns = time_point_labels
    errors = errors.loc[['Oral', 'Oropharynx', 'Larynx']]

    _, axes = plt.subplots()
    means.plot.bar(yerr=errors, ax=axes)
    plt.title(title)
    plt.legend(loc=(1.1, -0.1))
    output_fig(fname, save_figs, **plot_options)

    fname = '-'.join(title_fields) + '-mean-reduced-lineplot.png'
    plt.figure()
    means.loc['Oral']=means.loc['Oral']-spread
    means.loc['Oropharynx']=means.loc['Oropharynx']+0
    means.loc['Larynx']=means.loc['Larynx']+spread
    means.T.plot(style=['r-', 'g-', 'b-'])
    plt.title(title.replace(r'($1 \sigma$ error bars)', '') + ' mean')
    plt.axis([0, len(time_point_labels)-1, -1, 101])
    plt.legend(['Oral', 'Oropharynx', 'Larynx'], loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

    fname = '-'.join(title_fields) + '-mode-reduced-lineplot.png'
    plt.figure()
    gp_data = grouped_data.agg(lambda x: mode(x)[0][0])
    gp_data = gp_data.loc[['Oral', 'Oropharynx', 'Larynx']]
    gp_data.columns = time_point_labels
    gp_data.loc['Oral']=gp_data.loc['Oral']-spread
    gp_data.loc['Oropharynx']=gp_data.loc['Oropharynx']+0
    gp_data.loc['Larynx']=gp_data.loc['Larynx']+spread
    gp_data = gp_data.T
    gp_data.plot(style=['r-', 'g-', 'b-'])
    plt.title(title.replace(r'($1 \sigma$ error bars)', '') + ' mode')
    plt.axis([0, len(time_point_labels)-1, -1, 101])
    plt.legend(['Oral', 'Oropharynx', 'Larynx'], loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

if __name__ == "__main__":
    DATA_FILE_PATH = get_data_file_path()

    SAVE_FIGS = True

    DATA = read_data(DATA_FILE_PATH)

    do_plots_for_variable('Taste', SAVE_FIGS, **DEFAULT_PLOT_OPTIONS)
    do_plots_for_variable('Overall_QOL', SAVE_FIGS, **DEFAULT_PLOT_OPTIONS)
