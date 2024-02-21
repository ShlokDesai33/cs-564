
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


users, items_data, bids_data, itemCategories_data = set(), [], [], []

def clear_output(filename):
    with open(filename, 'w') as f:
        f.write("") #Creates empty files if previous already exists

def write_output(filename, data):
    with open(filename, 'a') as f:
        for content in data:
            f.write('|'.join(map(str, content)) + '\n')

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""

def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']
        
        # Users is set to prevent duplicate between bidders and sellers

        # Item_ID, User_Id, name, Current Price, Buy Price, 
        # First_Bid, Number_of_Bids, Started, Ends, Description
        for item in items:
            item_id = item['ItemID']
            seller = item['Seller']
            seller_id = seller['UserID']
            
            escaped_seller_id = seller_id.strip().replace('"', '""')
            trimmed_and_quoted_seller_id = f'"{escaped_seller_id}"'

            escaped_location=item.get('Location', "NULL").strip().replace('"', '""')
            trimmed_and_quoted_location=f'"{escaped_location}"'

            escaped_country=item.get('Country', "NULL").strip().replace('"', '""')
            trimmed_and_quoted_country=f'"{escaped_country}"'

            escaped_item_name=item['Name'].strip().replace('"', '""')
            trimmed_and_quoted_item_name=f'"{escaped_item_name}"'

            if 'Description' in item:
                if item['Description']:
                        descrip = item.get('Description', "NULL")
                else:
                        descrip = "NULL"
            else: 
                descrip = "NULL"
            
            escaped_item_description=descrip.strip().replace('"', '""')
            trimmed_and_quoted_item_description=f'"{escaped_item_description}"'

            # Users is a Set to prevent Duplicatse. ID,Rating, Country, Location. Adding Seller
            users.add((trimmed_and_quoted_seller_id, seller.get('Rating'), trimmed_and_quoted_location, trimmed_and_quoted_country))
            
            if 'Buy_Price' in item:
                        buy_price = transformDollar(item['Buy_Price']) 
            else: 
                        buy_price = "NULL"

            # ItemID, User_id, time, amount (0 to Multiple Bids possible for item)
            if item.get('Bids') is not None:
                for bidDetail in item['Bids']:
                    bid = bidDetail['Bid']  
                    bidder = bid['Bidder']
                    bidder_id = bidder['UserID']
                    
                   
                    escaped_bidder_id = bidder_id.strip().replace('"', '""')
                    trimmed_and_quoted_bidder_id = f'"{escaped_bidder_id}"'

                    escaped_bidder_location=bidder.get('Location', "NULL").strip().replace('"', '""')
                    trimmed_and_quoted_bidder_location=f'"{escaped_bidder_location}"'

                    escaped_bidder_country=bidder.get('Country', "NULL").strip().replace('"', '""')
                    trimmed_and_quoted_bidder_country=f'"{escaped_bidder_country}"'


                    # Users is a Set to prevent Duplicatse. ID,Rating, Country, Location. Adding Bidder
                    users.add((trimmed_and_quoted_bidder_id, bidder.get('Rating'), trimmed_and_quoted_bidder_location, trimmed_and_quoted_country))
                    
                    
                    bids_data.append((item_id, trimmed_and_quoted_bidder_id, transformDttm(bid['Time']), transformDollar(bid['Amount'])))

            items_data.append((item_id, trimmed_and_quoted_seller_id, trimmed_and_quoted_item_name, transformDollar(item['Currently']),
                               buy_price, transformDollar(item['First_Bid']),
                               item['Number_of_Bids'], transformDttm(item['Started']), transformDttm(item['Ends']),
                              trimmed_and_quoted_item_description))
            
            # item_id,category
            for category in item['Category']:
                escaped_category = category.strip().replace('"', '""')
                trimmed_and_quoted_category = f'"{escaped_category}"'
                itemCategories_data.append((item_id, trimmed_and_quoted_category))
            
            
            

        

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print ('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    
    clear_output('items.dat')
    clear_output('bids.dat')
    clear_output('itemCategories.dat')
    clear_output('users.dat')
    # loops over all .json files in the argument
    i =0 
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing ", f)

    #Output
    write_output('items.dat', items_data)
    write_output('bids.dat', bids_data)
    write_output('itemCategories.dat', itemCategories_data)
    write_output('users.dat', users)

if __name__ == '__main__':
    main(sys.argv)
