import make_directories
import clean_csv

# first we want to make subdirectories to download data to
# set this to False * AFTER * you make the directories
MAKE_DIR = True
if MAKE_DIR:
    make_directories.make_directories()

# set this to True * AFTER * you have downloaded the files from PFSWeb
DOWNLOADED = False
ORDER_RECORD_IMPORTED = False
if DOWNLOADED:
    clean_csv.clean(make_output=True, clean_data=True, orders_imported=ORDER_RECORD_IMPORTED)