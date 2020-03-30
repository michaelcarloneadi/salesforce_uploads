# Automating uploads from TSV to CSV
## REQUIREMENTS
1. Python 3
2. Pandas (pip3 install pandas)

## Background
This script takes the TSV from PFS and then outputs a cleaner version for upload to SFSC via Dataloader.  There are four modules that we use to make sure we can do this
1. clean_csv
2. helper
3. make_directories
4. pricingmap

## clean_csv.py
Import this module when you want to run it by itself and pass the following parameters:
* orders_imported : `--orders` : Boolean : True if you are trying to make CSVs of the other records, False if you cannot make the Order record link to other OMS records yet
* pricing run : `--pricing` : Boolean : Defaults to True unless passed.  Only pass if you have run pricing and removed Order Product files, else the script will fail.

When you run this via command line and not through a script, pass in the corresponding arguments above to set the parameter to `True`
## helper
A helper module that contains some functions that we use throughout the script
## make_directories
Makes all the directories that we expect of the script when it is walking through the process.  Note that you will want to run this first and then download all the TSVs into the respective TSV folder, then run clean_csv.py
## pricingmap
Reads the Order Product csv files and sums up the order pricing information off of the files.  This ACTIVELY EXCLUDES SR Order Types, something we need to change in the future

# How to use this script
1. Make sure you have Python3.  If you dont, run `brew install python` and then run `python3 --version`.  You can also try `python --version` if you have the path linked properly.  Make sure this returns version 3.\*.\* (code was written with 3.7.\*).  Additionally make sure you install pandas via `pip3 install pandas`
2. In the directory you are running the Python scripts in, go into your terminal and run `python3 make_directories.py` or, if you have it linked correctly, `python make_directories.py`.  Additionally, add all imported log files (success*.csv, etc) into the relevant file under `./imports/`
3. Download the data from SFTP into the proper folder (ex. February 2020 data goes into the `./February 2020/tsv` folder
4. Save customer import success csv files into `imported_customers` folder
5. When all is downloaded and saved, for the first run `python3 clean_csv.py`
6. Upload order records and save the success csv files in `uploaded_orders`
7. When upload is complete and files are saved, run `python3 clean_csv.py --orders`
8. Inspect and upload
Note: Files missing an ORDER__C linkage will be placed in a missing_orders directory for troubleshooting

# Troubleshooting
## Key Error
When you are cleaning, there are times when you run into a KeyError.  You can make changes to the columns via the following options when run via `python3 clean_csv.py [options]`
_Example_: `python3 clean_csv.py --orders -onum Order_External_Id__c`
* `-onum` Customer Order Number [ASC/ONT/OUT prefixed number] : DEFAULT Order_External_Id__c
* `-oid` Order ID : DEFAULT ID
* `-cemail` Customer email : DEFAULT EMAIL
* `-cid` Customer ID : DEFAULT ID
* `-p` Product identifier : DEFAFULT STOCKKEEPINGUNIT__C
* `-pid` Product ID : DEFAULT ID
* `-op` Line item product identifier : DEFAULT PRODUCT_SKU__C
* `-opid` Line item identifier : DEFAULT ID
* `shipor` Order that the shipment corresponds to : DEFAULT ORDER_EXTERNAL_ID__C
* `shipid` Shipment ID : DEFAULT ID
## Logging
There are logs under `./logs/` that you can use for troubleshooting.  When there are parsing or other errors, the row that errored out will be logged, as will the ID, if available, that was being parsed.


Let me know if you have any questions when running this
