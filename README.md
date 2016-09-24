[![Code Climate](https://codeclimate.com/github/mikejbrown/HN_plotting/badges/gpa.svg)](https://codeclimate.com/github/mikejbrown/HN_plotting)
[![Test Coverage](https://codeclimate.com/github/mikejbrown/HN_plotting/badges/coverage.svg)](https://codeclimate.com/github/mikejbrown/HN_plotting/coverage)
[![Issue Count](https://codeclimate.com/github/mikejbrown/HN_plotting/badges/issue_count.svg)](https://codeclimate.com/github/mikejbrown/HN_plotting)
About
=====

Just some data munging and plotting for a little side project.

Copyright 2016 Michael J. Brown

Licensed under the MIT license (see the LICENSE file for more detail).

Requirements
============

- [Python 3](https://www.python.org/)
  - Tested with 3.5.2.
- [pandas](http://pandas.pydata.org/)
  - Tested with 0.18.0.
- [matplotlib](http://matplotlib.org/)
  - Tested with 1.5.1.

You may run the full analysis suite simply by using

```sh
$ ./run.sh
```

or, if you want to run in a python virtual environment which includes all of the dependencies,

```sh
$ ./run-in-venv.sh
```

Note: you may need to edit some paths in this script depending on your platform.

Note: the above commands assume that you want to use the synthetic data set.
If you have a real data set to process, you need to modify the procedure slightly.

* Make sure the output directories are clean (not strictly necessary, but helpful):
```sh
$ rm analysis/* images/*
```
* Run one or both scripts using the `--file` option:
```sh
$ python data_reader.py --file myfile.csv
$ python plotting.py --file myfile.csv
```

If you don't use either of the `--use-synthetic` or `--file` options, the data file
`Taste_and_QOL_data.csv` (which is not tracked by the repo) is used by default.
