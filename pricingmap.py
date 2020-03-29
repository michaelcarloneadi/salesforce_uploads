import os, csv


def make_dir(working_directory):
    if not os.path.exists(os.path.join(working_directory, 'pricing')):
        os.mkdir(os.path.join(working_directory, 'pricing'))
    pricing_directory = os.path.join(working_directory, 'pricing')

    return pricing_directory

def check_module():
    import importlib.util
    if not importlib.util.find_spec('pandas'):
        print("You need to import pandas to create the pricing aggregation.  Please do so via")
        print(">>      pip3 pandas")
        print("or through sudo if you encounter an error")
        return False
    else:
        return True

def create_pricing(working_directory):
    if check_module():
        import pandas
        import glob
        pricing_directory = make_dir(working_directory)
        pricingcolumns = [
            'Order__c'
            ,'Net_Price__c'
            ,'Base_Price__c'
            ,'Gross_Price__c'
            ,'Tax__c'
            ,'Product_Disc_Gross_Price__c'
        ]

        dataframe = pandas.concat([pandas.read_csv(f, encoding='ISO-8859-1', sep = '\t', thousands=',') for f in glob.glob(os.path.join(working_directory, 'tsv', '*OrderProduct*'))], ignore_index=True)
        staging = dataframe[dataframe["PFS Order Type"] == "SO"].copy()
        pricingdf = staging[pricingcolumns].copy()
        staging[pricingcolumns].to_csv(os.path.join(pricing_directory, 'order_product_pricing_raw.csv'), quotechar='"', quoting=csv.QUOTE_ALL)
        pricingdf.fillna('0').groupby(['Order__c']).agg({
            pricingcolumns[1]: 'sum'
            ,pricingcolumns[2]: 'sum'
            ,pricingcolumns[3]: 'sum'
            ,pricingcolumns[4]: 'sum'
            ,pricingcolumns[5]: 'sum'
        }).round(2).to_csv(os.path.join(pricing_directory, 'order_product_pricing.csv'), quotechar='"', quoting=csv.QUOTE_ALL)

        return os.path.join(pricing_directory, 'order_product_pricing.csv')

def return_pricing(pricingfile):
    pricedict = dict()
    with open(pricingfile, encoding='ISO-8859-1') as f:
        prices = csv.DictReader(f, delimiter=',')
        for price in prices:
            pricedict[price['Order__c']] = {
                'Base_Price__c': price['Base_Price__c']
                ,'Net_Price__c': price['Net_Price__c']
                ,'Gross_Price__c': price['Gross_Price__c']
                ,'Tax__c': price['Tax__c']
                ,'Product_Disc_Gross_Price__c': price['Product_Disc_Gross_Price__c']
            }
    return pricedict

if __name__ == '__main__':
    wd = '/Users/michaelcarlone/PycharmProjects/salesforce_uploads/December 2019'
    create_pricing(wd)