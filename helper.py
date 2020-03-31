'''
    Helper module for parsing through the PFS files
'''
import os, time, datetime, csv

class OrderMap:
    def __init__(self, working_directory, ordernumber, orderid):
        self.orderField = 'ORDER_EXTERNAL_ID__C' if not ordernumber else ordernumber
        self.idField = 'ID' if not orderid else orderid
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_order_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Order Number
        '''
        order_map = dict()
        for file in self.files:
            if file[-4:] == '.csv' and 'success' in file:
                with open(os.path.join(self.wd, file), encoding='ISO-8859-1') as orderfile:
                    dictrows = csv.DictReader(orderfile, delimiter=',')
                    for row in dictrows:
                        if row[self.orderField] not in order_map.keys():
                            order_map[row[self.orderField]] = row[self.idField]
        return order_map


class LineItemMap:
    def __init__(self, working_directory, orderproduct, opid):
        self.lineField = 'PRODUCT_SKU__C' if not orderproduct else orderproduct
        self.idField = 'ID' if not opid else opid
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_lineitem_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Order Number
        '''
        lineitem = dict()
        for file in self.files:
            if file[-4:] == '.csv' and 'success' in file:
                with open(os.path.join(self.wd, file), encoding='ISO-8859-1') as orderfile:
                    dictrows = csv.DictReader(orderfile, delimiter=',')
                    for row in dictrows:
                        if row[self.lineField] not in lineitem.keys():
                            lineitem[row[self.lineField]] = row[self.idField]
        return lineitem


class CustomerMap:
    def __init__(self, working_directory, customeremail, customerid):
        self.emailField = 'EMAIL' if not customeremail else customeremail
        self.idField = 'ID' if not customerid else customerid
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_customer_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Customer Email
        '''
        customer_map = dict()
        for file in self.files:
            if file[-4:] == '.csv' and 'success' in file:
                with open(os.path.join(self.wd, file), encoding='ISO-8859-1') as customerfile:
                    dictrows = csv.DictReader(customerfile, delimiter=',')
                    for row in dictrows:
                        if row[self.emailField] not in customer_map.keys():
                            customer_map[row[self.emailField].lower()] = row[self.idField]
        return customer_map


class ProductMap:
    def __init__(self, working_directory, product, productid):
        self.productField = 'STOCKKEEPINGUNIT__C' if not product else product
        self.idField = 'ID' if not productid else productid
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_product_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Customer Email
        '''
        product_map = dict()
        for file in self.files:
            if file[-4:] == '.csv' and 'success' in file:
                with open(os.path.join(self.wd, file), encoding='ISO-8859-1') as productfile:
                    dictrows = csv.DictReader(productfile, delimiter=',')
                    for row in dictrows:
                        if row[self.productField] not in product_map.keys():
                            product_map[row[self.productField].lower()] = row[self.idField]
        return product_map


class ShipmentMap:
    def __init__(self, working_directory, shipmentorder, shipmentid):
        self.shipmentorderField = 'ORDER_EXTERNAL_ID__C' if not shipmentorder else shipmentorder
        self.idField = 'ID' if not shipmentid else shipmentid
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_shipment_map(self):
        '''
            return <Dictionary> mapping SFSC ID and Order
        '''
        shipment_map = dict()
        for file in self.files:
            if file[-4:] == '.csv' and 'success' in file:
                with open(os.path.join(self.wd, file), encoding='ISO-8859-1') as shipmentfile:
                    dictrows = csv.DictReader(shipmentfile, delimiter=',')
                    for row in dictrows:
                        if row[self.shipmentorderField] not in shipment_map.keys():
                            shipment_map[row[self.shipmentorderField]] = row[self.idField]
        return shipment_map


class Logger:
    def __init__(self, verbose):
        self.verbose = verbose
        self.log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        self.log_name = 'runlog-%s%s.log' % (datetime.datetime.now().strftime('%Y%m%d'), int(time.time()))
        self.log_message = ''

    def write(self, message):
        self.log_message = '%s :: %s\n' % (datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S.%s'), message)
        self.out(self.log_message)
        if self.verbose:
            print(self.log_message)

    def out(self, message):
        with open(os.path.join(self.log_dir, self.log_name), 'a') as f:
            f.write(message)


def chooser(filename):
    '''
        param filename <String> name of the file we are cleaning
        return <Integer> type of file passed in
    '''
    choice = 0
    if 'Product' in filename:
        if 'Order' in filename:
            choice = 1
        elif 'Shipment' in filename:
            choice = 2
    else:
        if 'Order' in filename:
            choice = 3
        elif 'Payment' in filename:
            choice = 4
        elif 'Shipment' in filename:
            choice = 5
    return choice


def get_headers(filename, log=None):
    '''
        param filename <String> name of the file we want to grab headers from
        return <String>, <String []> pfs order type and string list of headers in the file
    '''
    order_type = ''
    with open(filename, encoding='ISO-8859-1') as tsvheaders:
        headers = tsvheaders.readlines()
    header = headers[0].split('\t')
    try:
        if [ih.strip() for ih in headers[1].split('\t')][header.index('PFS Order Type')] == 'SR':
            order_type = '-Return'
        elif [ih.strip() for ih in headers[1].split('\t')][header.index('PFS Order Type')] == 'SO':
            order_type = '-Shipment'
    except Exception as e:
        log.write('Error passing: %s' % e) if log else print('Error passing: %s' % e)
        # if that dont work, try the last row...
        if headers[1].split('\t')[-1].strip() == 'SR':
            order_type = '-Return'
            log.write('Found on retry %s' % order_type) if log else print('Found on retry %s' % order_type)
        elif headers[1].split('\t')[-1].strip() == 'SO':
            order_type = '-Shipment'
            log.write('Found on retry %s' % order_type) if log else print('Found on retry %s' % order_type)

        else:
            pass
    return order_type, [h.strip() for h in header]


def get_paths(directory_path, clean_directory):
    '''
        param directory_path <String> main directory where we are running the script from
        param clean_directory <String> the directory where we are cleaning files
        return <String>, String>, <String> filepaths of the different folders in the clean directory
    '''
    d = os.path.join(directory_path, clean_directory)
    return os.path.join(d, 'tsv'), os.path.join(d, 'csv'), os.path.join(d, 'clean')


def get_brand(order_external_id):
    ordernumbrand = order_external_id[:3]
    if ordernumbrand == 'ASC':
        return 'asics'
    elif ordernumbrand == 'ONT':
        return 'onitsukatiger'
    elif ordernumbrand == 'OUT':
        return 'outlet'
    else:
        return ''

def get_carrier():
    carriers = dict()
    DPD = 'a041U00000BLNikQAH'
    FedEx = 'a041U00000BLNifQAH'
    UPS = 'a041U00000BLNipQAH'
    USPS = 'a041U00000OnqHcQAJ'

    carriers = {
        'USPS': USPS
        ,'usps': USPS
        ,'Usps': USPS
        ,'DPD': DPD
        ,'Dpd': DPD
        ,'dpd': DPD
        ,'UPS': UPS
        ,'Ups': UPS
        ,'ups': UPS
        ,'FedEx': FedEx
        ,'FEDEX': FedEx
        ,'Fedex': FedEx
        ,'fedex': FedEx
    }
    return carriers

def map_carriers(tla_carrier):
    c = get_carrier()
    if not tla_carrier or tla_carrier == '':
        return ''
    else:
        return c[tla_carrier]


def date_concat(dateString):
    '''
        param dateString <String> date from PFS file
        return <String> datetime in format YYYY-MM-DDT00:00:00Z
    '''
    return '%sT00:00:00.000Z' % dateString


def order_cleaner(order, prices, ordernum):
    '''
        param order <OrderedDict> dictionary that contains dirty order information to import
    '''
    order['Order_Date__c'] = date_concat(order['Order_Date__c'])
    order['Legacy_OMS__c'] = 'PFSweb'
    order['AccountId__c'] = order['Email__c'].lower()


    order['Brand__c'] = get_brand(order[ordernum])

    try:
        priceinfo = prices[order[ordernum]]
        order['Merchandize_Gross_Price__c'] = priceinfo['Base_Price__c']
        order['Total_Tax__c'] = priceinfo['Tax__c']
        order['Adj_Merchandize_GrossPrice__c'] = priceinfo['Net_Price__c']
        order['Total_Gross_Price__c'] = priceinfo['Net_Price__c']
        order['Order_Total_Discount__c'] = str(
            (float(order['Order_Discount__c']) if order['Order_discount__c'] else 0.00) + (float(priceinfo['Product_Disc_Gross_Price__c']))
                )
        try:
            customer_ship_name = order['Ship_to_Last_Name__c'].split(' ')
            customer_bill_name = order['Bill_To_Last_Name__c'].split(' ')
            order['Ship_to_First_Name__c'] = customer_ship_name[0]
            order['Ship_to_Last_Name__c'] = ' '.join(customer_ship_name[1:])
            order['Bill_To_First_Name__c'] = customer_bill_name[0]
            order['Bill_To_Last_Name__c'] = ' '.join(customer_bill_name[1:])
        except Exception as e:
            raise(e)
    except Exception as err:
        if order['PFS Order Type'] == 'SR':
            pass
        else:
            raise(err)


def payment_cleaner(payment):
    '''
        param payment <OrderedDict> dictionary that contains dirty payment information to import
    '''
    cc_number = 'creditCardNumber*******************'
    payment.update(
        {'Custom_Field_1__c': '%s;creditCardExpirationMonth%s;creditCardExpirationYear%s;creditCardType%s' % (
            cc_number
            , payment['creditCardExpirationMonth']
            , payment['creditCardExpirationYear']
            , 'Mastercard' if payment['creditCardType'] == 'Master Card' else payment['creditCardType']
        )
         ,'Order_External_Id__c': payment['Order__c']
     }
    )

def order_product_cleaner(lineitem):
    lineitem['Product__c'] = lineitem['Product_Code__c']
    lineitem.update(
        {'Product_External_ID__c': lineitem['Product_Code__c']
         ,'Order_External_ID__c': lineitem['Order__c']
    }
    )


def shipment_product_cleaner(shipitem):
    shipitem['OrderProduct__c'] = shipitem['Product_SKU__c']
    shipitem['Shipment__c'] = shipitem['Order__c']
    shipitem.update(
        {'Product_External_ID__c': shipitem['Product_SKU__c']
         ,'Order_External_Id__c': shipitem['Order__c']
     }
    )

def shipment_cleaner(shipment):
    '''
        param shipment <OrderedDict> dictionary that contains dirty shipment information to import
    '''
    shipment['Actual_Shipment_Date__c'] = date_concat(shipment['Actual_Shipment_Date__c'])
    shipment.update({'TLA_Shipment_Provider_Carrier__c': shipment['Shipment_Provider_Carrier__c'][:3]
                     ,'Order_External_ID__c': shipment['Order__c']
     }
    )
    shipment['Shipment_Provider_Carrier__c'] = map_carriers(shipment['TLA_Shipment_Provider_Carrier__c'])


def map__c(row, mapping, field):
    '''
        param row <OrderedDict> dictionary that contains the data with Order__c field
        param mapping <Dict> dictionary that has a mapping between two fields
        param field <String> what field we want to exchange
    '''
    if row[field] in mapping.keys():
        row[field] = mapping[row[field]]
    else:
        row[field] = ''

def write_file(pathway, filename, header, orders):
    log_dir = os.path.join(pathway, 'missing-orders')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    with open(os.path.join(log_dir, filename), 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for order in orders:
            writer.writerow(v for k, v in order.items())


def debug(filepath):
    with open(filepath) as f:
        rows = f.readlines()
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'testexport.csv'), 'w') as f:
        for ix in rows[:21]:
            f.write(ix)