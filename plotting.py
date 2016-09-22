# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 00:32:50 2016

@author: Michael
"""

import pandas as pd
import numpy as np
import pylab as plt
import matplotlib
matplotlib.style.use('ggplot')

from data_reader import read_data, time_points_for_variable

default_plot_options = {'dpi': 128, 'bbox_inches': 'tight'}

def output_fig(name, save_figs, base_path="images", **kwargs):
    """ If save_figs == True, saves the figure as a file of name 'base_path/name'.
    If save_figs == False, display the figure interactively instead.
    kwargs are passed onto matplotlib.pyplot.savefig unmodified"""
    if save_figs:
        import os
        fname = os.path.realpath(os.path.join(base_path, name))
        dname = os.path.dirname(fname)
        if not (os.path.exists(dname) and os.path.isdir(dname)):
            os.mkdir(dname)
        try:
            plt.savefig(fname, **kwargs)
        except:
            raise RuntimeError("Could not save image {0}".format(fname))
    else:
        plt.show()


def do_plots_for_variable(var):
    """ """
    cols = time_points_for_variable(var)
    time_point_labels = ["Baseline", "Wk 2", "Wk 4", "Wk 6", "FU 1", "FU 3", "FU 6", "FU 12"]

    ## Boxplots for each category
    for cat in data.Category.values.sort_values().unique():
        cdata = data[data.Category==cat][cols]
        cdata.columns = time_point_labels
        plt.figure()
        cdata.boxplot()
        plt.title('%s -- %s' % (var,cat))
        output_fig('%s-%s-boxplot.png'%(var,cat), save_figs, **default_plot_options)

    ## Bar plots with error bars
    cols2 = cols.copy()
    cols2.insert(0, 'Category')
    gb = data[cols2].groupby('Category')
    means = gb.mean()
    means.columns = time_point_labels
    means = means
    errors = gb.std()
    errors.columns = time_point_labels
    errors = errors
    fig, ax = plt.subplots()
    means.plot.bar(yerr=errors, ax=ax)
    plt.title('%s ($1 \sigma$ error bars)'%var)
    plt.legend(loc=(1.1,0.2))
    output_fig('%s-barplot-errorbar.png'%var, save_figs, **default_plot_options)

    ## Histograms
    dc = data[cols]
    dc.columns = time_point_labels
    plt.figure()
    dc.plot.hist(stacked=True, cumulative=True)
    plt.legend(loc=(1.1,0.2))
    plt.xlabel('%s'%var)
    plt.title('Cumulative frequency of %s score'%var)
    output_fig('%s-histogram.png'%var, save_figs, **default_plot_options)

    for cat in data.Category.values.sort_values().unique():
        dc = data[data.Category==cat][cols]
        dc.columns = time_point_labels
        plt.figure()
        dc.plot.hist(stacked=True, cumulative=True)
        plt.legend(loc=(1.1,0.2))
        plt.xlabel('%s'%var)
        plt.title('Cumulative frequency of %s score -- %s' % (var,cat))
        output_fig('%s-%s-histogram.png' % (var,cat), save_figs, **default_plot_options)

if __name__ == "__main__":
    data_file_path = "Taste_and_QOL_data.csv"
    save_figs = True

    data = read_data(data_file_path)

    do_plots_for_variable('Taste')
    do_plots_for_variable('Overall_QOL')
