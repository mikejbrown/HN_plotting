# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 00:32:50 2016

@author: Michael
"""

import pylab as plt
import matplotlib
from data_reader import read_data
from common import get_data_file_path, output_fig, time_points_for_variable

matplotlib.style.use('ggplot')

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

    # Histograms
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
        plt.legend(loc=(1.1, 0.2))
        plt.xlabel('%s' % var)
        plt.title('Cumulative frequency of %s score -- %s' % (var, cat))
        output_fig('%s-%s-histogram.png' % (var, cat),
                   save_figs, **plot_options)
        plt.clf()


def _do_plot(var, mask, title, save_figs, plot_options):
    """ A helper function to do a boxplot with errorbars for masked data. """
    title_fields = title.replace(r'($1 \sigma$ error bars)', '').split()[:2]
    fname = '-'.join(title_fields) + '-reduced-barplot-errorbar.png'
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
    plt.legend(loc=(1.1, 0.2))
    output_fig(fname, save_figs, **plot_options)

if __name__ == "__main__":
    DATA_FILE_PATH = get_data_file_path()

    SAVE_FIGS = True

    DATA = read_data(DATA_FILE_PATH)

    do_plots_for_variable('Taste', SAVE_FIGS, **DEFAULT_PLOT_OPTIONS)
    do_plots_for_variable('Overall_QOL', SAVE_FIGS, **DEFAULT_PLOT_OPTIONS)
