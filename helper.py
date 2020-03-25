'''
    Helper module for parsing through the PFS files
'''
import os

class OrderMap:
    def __init__(self, working_directory):
        self.orderField = 'ORDER_EXTERNAL_ID__C'
        self.idField = 'ID'
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_order_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Order Number
        '''
        import csv

        order_map = dict()
        for file in self.files:
            with open(os.path.join(self.wd, file)) as orderfile:
                dictrows = csv.DictReader(orderfile, delimiter=',')
                for row in dictrows:
                    if row[self.orderField] not in order_map.keys():
                        order_map[row[self.orderField]] = row[self.idField]
        return order_map

class CustomerMap:
    def __init__(self, working_directory):
        self.emailField = 'EMAIL'
        self.idField = 'ID'
        self.wd = working_directory
        _, _, self.files = next(os.walk(self.wd), (None, None, []))
    def get_customer_map(self):
        '''
            return <Dictionary> mapping between SFSC ID and Customer Email
        '''
        import csv

        customer_map = dict()
        for file in self.files:
            with open(os.path.join(self.wd, file)) as customerfile:
                dictrows = csv.DictReader(customerfile, delimiter=',')
                for row in dictrows:
                    if row[self.emailField] not in customer_map.keys():
                        customer_map[row[self.emailField]] = row[self.idField]
        return customer_map


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


def get_headers(filename):
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
        print('Error passing: %s' % e)
        # if that dont work, try the last row...
        if headers[1].split('\t')[-1].strip() == 'SR':
            print('Nevermind, found')
            order_type = '-Return'
        elif headers[1].split('\t')[-1].strip() == 'SO':
            print('Nevermind, found')
            order_type = '-Shipment'
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
    return os.path.join(d, 'tsv'), os.path.join(d, 'csv'), os.path.join(d, 'clean'), os.path.join(d, 'uploaded_orders')


def date_concat(dateString):
    '''
        param dateString <String> date from PFS file
        return <String> datetime in format YYYY-MM-DDT00:00:00Z
    '''
    return '%sT00:00:00.000Z' % dateString


def order_cleaner(order):
    '''
        param order <OrderedDict> dictionary that contains dirty order information to import
    '''
    order['Order_Date__c'] = date_concat(order['Order_Date__c'])
    order['Legacy_OMS__c'] = 'PFSweb'


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
        )}
    )


def shipment_cleaner(shipment):
    '''
        param shipment <OrderedDict> dictionary that contains dirty shipment information to import
    '''
    shipment['Actual_Shipment_Date__c'] = date_concat(shipment['Actual_Shipment_Date__c'])
    shipment.update({'TLA_Shipment_Provider_Carrier__c': shipment['Shipment_Provider_Carrier__c'][:3]})


def map__c(row, mapping, field):
    '''
        param row <OrderedDict> dictionary that contains the data with Order__c field
        param mapping <Dict> dictionary that has a mapping between two fields
        param field <String> what field we want to exchange
    '''
    if row[field] in mapping.keys():
        row[field] = mapping[row[field]]

def debug(filepath):
    with open(filepath) as f:
        rows = f.readlines()
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'testexport.csv'), 'w') as f:
        for ix in rows[:21]:
            f.write(ix)