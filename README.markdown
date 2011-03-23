Whipcar Price Prediction Model
==============================

There are two main components here, a set of Python tools for predicting with various algorithms and plotting features against monthly rate. There is also a PHP library which is a cut down implementation of the best of breed algorithm implemented in the Python implementation.

Setup
-----

The scripts expect to find input CSV files in a directory called `data` at the root of the project. These CSV files should be formatted the same as the original files provided. They are not included in this distribution so you will need to create the directory and add a file. The scripts also expect a directory called `images` at the root of the project to place generated jitter plots.

Python Implementation
---------------------

There are two runnable files in the Python implementation `jitter.py` that generates the jitter plots and `test.py` that tests the algorithms.

### Creating new jitter plots

### Creating new algorithms


PHP Implementation
------------------

There is only one runnable file in the PHP implementation `test.php` that tests the single algorithm implemented in PHP.