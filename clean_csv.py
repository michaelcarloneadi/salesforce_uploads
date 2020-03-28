import csv
import os
import helper
from collections import OrderedDict

import argparse

def clean(make_output, clean_data, orders_imported, verbose, ordernum, orderid, email, customerid, product, productid, lineitem, lineid):
    '''
        param make_output <Boolean> output the data to different files, ie move from tsv to csv
        param clean_data <Boolean> clean the data and apply the proper fields we expect
        param orders_imported <Boolean> if the order record has been imported, flip to true so that
                                        we can create the linkage between order : record
    '''
    # field names for swapping down below
    ORDERC = 'Order__c'
    ACCOUNTC = 'AccountId__c'
    PRODUCTC = 'Product__c'
    LINEITEMC = 'OrderProduct__c'

    # make logs
    logs = helper.Logger(verbose)

    # the actual good stuff
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    logs.write("Current file directory :: %s" % dir_path)
    directories = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    print("Please choose a directory")
    for ix, dir in enumerate(directories):
        print(ix, dir)
    directoryindex = int(input(">> "))

    row = None
    if directoryindex < len(directories):
        # get the directory that we want to clean/run through
        clean_directory = directories[directoryindex]
        # retrieve root, dirs, and files from walk, retain only filenames
        _, _, filenames = next(os.walk(os.path.join(dir_path, clean_directory, 'tsv')), (None, None, []))

        # for each file, let's clean out the tsvs and export to csv
        for filename in filenames:
            logs.write('Reading %s' % filename)
            if filename[0] == '.' or filename[0] == '_':
                logs.write('Skipping, invalid file %s' % filename)
            else:
                filetype = helper.chooser(filename)
                # directory to read from, read to, and clean to
                p_in, p_out, p_clean = helper.get_paths(dir_path, clean_directory)
                # generate the order map
                order_path = os.path.join(dir_path, 'imports', 'imported_orders')
                ordermap = helper.OrderMap(order_path, ordernum, orderid)
                ordermapping = ordermap.get_order_map()
                # add a place to get customer mappings too
                customer_directory = os.path.join(dir_path, 'imports', 'imported_customers')
                customermap = helper.CustomerMap(customer_directory, email, customerid)
                customermapping = customermap.get_customer_map()
                # and product mappings
                product_directory = os.path.join(dir_path, 'imports', 'imported_products')
                productmap = helper.ProductMap(product_directory, product, productid)
                productmapping = productmap.get_product_map()
                # and finally order products
                lineitem_directory = os.path.join(dir_path, 'imports', 'imported_orderproducts')
                linemap = helper.LineItemMap(lineitem_directory, lineitem, lineid)
                lineitemmapping = linemap.get_lineitem_map()


                # get headers
                order_type, header = helper.get_headers(os.path.join(p_in, filename), logs)

                # need to handle this encoding because we have weird bytes
                with open(os.path.join(p_in, filename), encoding='ISO-8859-1') as tsvfile:
                    reader = csv.DictReader(tsvfile, delimiter='\t') # use a DictReader to preserve header names
                    if make_output:
                        # backup the stuff from tsv to csv
                        out_filename = '%s%s.csv' % (filename.split('.')[0], order_type)
                        with open(os.path.join(p_out, out_filename), 'w') as csvfile:
                            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                            try:
                                csvwriter.writerow(header)
                                for row in reader:
                                    csvwriter.writerow(v for k, v in row.items())
                            except Exception as e:
                                logs.write(row) if row else logs.write('Exception !!')
                                logs.write(e)
                                break
                if clean_data:
                    logs.write('cleaning %s' % filename)
                    # make a new list for objects that dont have  record
                    missingorders = []
                    missing_filename = '%s%s-Clean.csv' % (filename.split('.')[0], '_MissingOrderLink')
                    with open(os.path.join(p_in, filename), encoding='ISO-8859-1') as tsvfile:
                        clean_reader = csv.DictReader(tsvfile, delimiter='\t')  # and one for the clean file
                        if make_output:
                            # and create a new clean file for this
                            clean_filename = '%s%s-Clean.csv' % (filename.split('.')[0], order_type)
                            with open(os.path.join(p_clean, clean_filename), 'w') as cleanfile:
                                cleanwriter = csv.writer(cleanfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                                try:
                                    cleanwriter.writerow(header)
                                    for crow in clean_reader:
                                        if filetype == 3:
                                            helper.order_cleaner(crow)
                                            helper.map__c(crow, customermapping, ACCOUNTC, logs)
                                            cleanwriter.writerow(v for k, v in crow.items())
                                        if orders_imported and filetype != 3:
                                            if filetype == 1: # order product
                                                helper.order_product_cleaner(crow)
                                                helper.map__c(crow, ordermapping, ORDERC, logs)
                                                helper.map__c(crow, productmapping, PRODUCTC, logs)
                                            elif filetype == 2: # shipment product
                                                helper.map__c(crow, ordermapping, ORDERC, logs)
                                                helper.map__c(crow, lineitemmapping, LINEITEMC, logs)
                                            elif filetype == 4: # payment
                                                helper.payment_cleaner(crow)
                                                helper.map__c(crow, ordermapping, ORDERC, logs)
                                            elif filetype == 5: # shipment
                                                helper.shipment_cleaner(crow)
                                                helper.map__c(crow, ordermapping, ORDERC, logs)
                                            if crow[ORDERC] == '':
                                                missingorders.append(crow)
                                            else:
                                                cleanwriter.writerow(v for k, v in crow.items())
                                    helper.write_file(os.path.join(dir_path, clean_directory), missing_filename, header, missingorders)
                                except Exception as e:
                                    logs.write(crow) if crow else logs.write('Exception !!')
                                    logs.write(e)
                                    raise(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to clean data that we received from PFS.')
    parser.add_argument('--output', help='output the data to different files', action='store_false')
    parser.add_argument('--clean', help='clean the data for SFSC', action='store_false')
    parser.add_argument('--orders'
                        , help='order records are imported, mapping file can be made, and we can create the link'
                        , action='store_true')
    parser.add_argument('--verbose', action='store_true')
    # lets add the column names here, since the CSVs are weird
    # order columns
    parser.add_argument('-onum', default='ORDER_EXTERNAL_ID__C')
    parser.add_argument('-oid', default='ID')
    # customer columns
    parser.add_argument('-cemail', default='EMAIL')
    parser.add_argument('-cid', default='ID')
    # product columns
    parser.add_argument('-p', default='STOCKKEEPINGUNIT__C')
    parser.add_argument('-pid', default='ID')
    # line item columns
    parser.add_argument('-op', default='PRODUCT_SKU__C')
    parser.add_argument('-opid', default='ID')


    args = parser.parse_args()
    print('Output orders: %s' % args.output)
    print('Clean files for SFSC: %s' % args.clean)
    print('Orders are imported: %s' % args.orders)

    print('order definitions :: order=%s ; orderid=%s' % (args.onum, args.oid))
    print('customer definitions :: order=%s ; orderid=%s' % (args.cemail, args.cid))
    print('product definitions :: order=%s ; orderid=%s' % (args.p, args.pid))
    print('order product definitions :: order=%s ; orderid=%s' % (args.op, args.opid))

    clean(args.output, args.clean, args.orders, args.verbose, args.onum, args.oid, args.cemail, args.cid, args.p, args.pid, args.op, args.opid)