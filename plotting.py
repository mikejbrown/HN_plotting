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


if __name__ == "__main__":
    data_file_path = "Taste_and_QOL_data.csv"
    save_figs = True

    data = read_data(data_file_path)

    cols = time_points_for_variable('Taste')

    #print(data[cols].groupby('Category').describe())
    for cat in data.Category.values.sort_values().unique():
        odata = data[data.Category==cat][cols]
        odata.columns = ["Baseline", "Wk 2", "Wk 4", "Wk 6", "FU 1", "FU 3", "FU 6", "FU 12"]
        plt.figure()
        odata.boxplot()
        plt.title('Taste -- %s' % cat)
        output_fig('boxplot-taste-%s.png'%cat, save_figs)

    cols.insert(0, 'Category')
    gb = data[cols].groupby('Category')
    means = gb.mean()
    means.columns = ["Baseline", "Wk 2", "Wk 4", "Wk 6", "FU 1", "FU 3", "FU 6", "FU 12"]
    means = means
    errors = gb.std()
    errors.columns = ["Baseline", "Wk 2", "Wk 4", "Wk 6", "FU 1", "FU 3", "FU 6", "FU 12"]
    errors = errors
    fig, ax = plt.subplots()
    means.plot.bar(yerr=errors, ax=ax)
    plt.legend(loc=(1.1,0.2))
    output_fig('barplot-errorbar.png', save_figs)