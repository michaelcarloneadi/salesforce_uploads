import os

def make_directories():
    directories = ['February 2020', 'January 2020', 'December 2019', 'November 2019', 'October 2019', 'September 2019'
                    , 'August 2019', 'July 2019', 'June 2019', 'May 2019', 'April 2019', 'March 2019', 'February 2019'
                    , 'January 2019']
    sub_directories = ['uploaded_orders', 'clean', 'csv', 'tsv']


    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    print('Current directory where we will be working: %s' % dir_path)

    for directory in directories:
        if directory in directories:
            os.mkdir(os.path.join(dir_path, directory))
            for sd in sub_directories:
                os.mkdir(os.path.join(dir_path, directory, sd))
        else:
            print('We already have this directory: %s' % directory)