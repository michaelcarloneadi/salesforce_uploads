import os

def make_directories():
    directories = ['February 2020'
                    , 'January 2020'
                    , 'December 2019'
                    , 'November 2019'
                    , 'October 2019'
                    , 'September 2019'
                    , 'August 2019'
                    , 'July 2019'
                    , 'June 2019'
                    , 'May 2019'
                    , 'April 2019'
                    , 'March 2019'
                    , 'February 2019'
                    , 'January 2019'
               ]
    sub_directories = ['clean', 'csv', 'tsv']
    imports = ['imported_customers', 'imported_orders', 'imported_products', 'imported_orderproducts']
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    current_directories = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

    if not os.path.exists(os.path.join(dir_path, 'imports')):
        os.mkdir('imports')

    import_directories = [d for d in os.listdir(os.path.join(dir_path, 'imports')) if os.path.isdir(os.path.join(dir_path, 'imports', d))]
    for import_folder in imports:
        if import_folder not in import_directories:
            os.mkdir(os.path.join(dir_path, 'imports', import_folder))
        else:
            print('We already have this directory: %s' % import_folder)

    print('Current directory where we will be working: %s' % dir_path)

    for directory in directories:
        if directory not in current_directories:
            os.mkdir(os.path.join(dir_path, directory))
            for sd in sub_directories:
                os.mkdir(os.path.join(dir_path, directory, sd))
        else:
            print('We already have this directory: %s' % directory)

if __name__ == '__main__':
    make_directories()