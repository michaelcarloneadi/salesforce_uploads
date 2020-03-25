# Automating uploads from TSV to CSV
This script takes the TSV from PFS and then outputs a cleaner version for upload to SFSC via Dataloader.  There are three modules that we use to make sure we can do this
1. clean_csv
2. helper
3. make_directories

## clean_csv.py
Import this module when you want to run it by itself and pass the following parameters:
* make_output : `--output` : Boolean : True if you want to output the TSV into CSV format and False if you just want to read it
* clean_data : `--clean` : Boolean : True if you want to clean the CSV into a format expected of SFSC, False if not
* orders_imported : `--orders` : Boolean : True if you are trying to make CSVs of the other records, False if you cannot make the Order record link to other OMS records yet

When you run this via command line and not through a script, pass in the corresponding arguments above to set the parameter to `True`
## helper
A helper module that contains some functions that we use throughout the script
## make_directories
Makes all the directories that we expect of the script when it is walking through the process.  Note that you will want to run this first and then download all the TSVs into the respective TSV folder, then run clean_csv.py

# How to use this script
1. Make sure you have Python3.  If you dont, run `brew install python` and then run `python3 --version`.  You can also try `python --version` if you have the path linked properly.  Make sure this returns version 3.\*.\* (code was written with 3.7.\*)
2. In the directory you are running the Python scripts in, go into your terminal and run `python3 make_directories.py` or, if you have it linked correctly, `python make_directories.py`
3. Download the data from SFTP into the proper folder (ex. February 2020 data goes into the `./February 2020/tsv` folder
4. Save customer import success csv files into `imported_customers` folder
5. When all is downloaded and saved, for the first run `python3 clean_csv.py --output --clean`
6. Upload order records and save the success csv files in `uploaded_orders`
7. When upload is complete and files are saved, run `python3 clean_csv.py --output --clean --orders`
8. Inspect and upload

Let me know if you have any questions when running this
