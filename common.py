# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:02:49 2016

@author: Michael
"""

import pandas as pd
import numpy as np
import pylab as plt


def get_data_file_path():
    """ Returns the data file path after parsing command line arguments. """
    import argparse
    parse = argparse.ArgumentParser()
    group = parse.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Path to data file to use")
    group.add_argument("-s", "--use-synthetic", action="store_true",
                       help="Use synthetic data")
    args = parse.parse_args()

    if args.use_synthetic:
        print("Using synthetic data")
        DATA_FILE_PATH = "data/synthetic-data.csv"
    if args.file:
        DATA_FILE_PATH = args.file
    else:
        DATA_FILE_PATH = "Taste_and_QOL_data.csv"

    return DATA_FILE_PATH


def output_analysis(results, name, save_analysis, base_path="analysis"):
    """ If save_analysis == True, saves the analysis results as a file of name
    'base_path/name'.
    If save_analysis == False, prints the results to the stdout."""
    if save_analysis:
        fname = __mk_dir_if_needed(name, base_path)
        with open(fname, 'w') as file:
            file.write(results)
    else:
        print(results)


def output_fig(name, save_figs, base_path="images", **kwargs):
    """ If save_figs == True, saves the figure as a file of name 'base_path/name'.
    If save_figs == False, display the figure interactively instead.
    kwargs are passed onto matplotlib.pyplot.savefig unmodified"""
    if save_figs:
        fname = __mk_dir_if_needed(name, base_path)
        try:
            print("Saving image %s" % fname)
            plt.savefig(fname, **kwargs)
        except:
            raise RuntimeError("Could not save image {0}".format(fname))
    else:
        plt.show()


def time_points_for_variable(variable):
    """ Returns a list of column names for the time points of a variable. """
    time_points = ['_B', '_W2', '_W4', '_W6', '_FU1', '_FU3', '_FU6', '_FU12']
    return [variable + tp for tp in time_points]


def __mk_dir_if_needed(name, base_path):
    """ Helper function that makes a dir for file saving if needed.
    Returns the fully qualified filename. """
    import os
    fname = os.path.realpath(os.path.join(base_path, name))
    dname = os.path.dirname(fname)
    if not (os.path.exists(dname) and os.path.isdir(dname)):
        os.mkdir(dname)
    return fname
