import requests
import json
import math
import sqlite3
import os
from os import listdir
from os.path import isfile, join
import ast
import numpy as np
import matplotlib.pyplot as plt

#sends a request to StockX for popular sneakers, returns a list of # quantity with product UUID and a short product description
def get_stockX_popular(quantity):
    headers = {
    'accept': '*/*',
    'app-platform': 'ios',
    'app-name': 'StockX-iOS',
    'accept-language': 'en-US',
    'x-api-key': '99WtRZK6pS1Fqt8hXBfWq8BYQjErmwipa3a0hYxX',
    'user-agent': 'StockX/31379 CFNetwork/1206 Darwin/20.1.0',
    }

    listofProducts = []
    pages = math.ceil(quantity/40)
    page = 1
    while page!= pages+1:

        params = {
            'browseVerticals': 'sneakers',
            'country': 'US',
            'dataType': 'product',
            'filterVersion': '3',
            'order': 'DESC',
            'page': page,
            'sort': 'most-active',
            }

        response = requests.get('https://gateway.stockx.com/api/v3/browse', params=params, headers=headers)
        products = json.loads(response.text)["Products"]
        for product in products:
            listofProducts.append([product["uuid"],product["shortDescription"]])
        page += 1

    return (listofProducts[0:quantity])

#takes a StockX product UUID and returns a dictionary with relevent product sales information
def build_stockX_product(UUID):
    headers = {
    'accept': '*/*',
    'app-platform': 'ios',
    'app-name': 'StockX-iOS',
    'accept-language': 'en-US',
    'x-api-key': '99WtRZK6pS1Fqt8hXBfWq8BYQjErmwipa3a0hYxX',
    'user-agent': 'StockX/31379 CFNetwork/1206 Darwin/20.1.0',
    }

    params = (
        ('includes', 'market,360'),
        ('currency', 'USD'),
        ('country', 'US'),
    )
    response = requests.get('https://gateway.stockx.com/api/v2/products/'+UUID, headers=headers, params=params)
    response = json.loads(response.text)["Product"]
    childrenInfo = response["children"]
    childrenDictionary = {}
    for child in childrenInfo:
        childDict = {}
        childData = childrenInfo[child]
        market = childrenInfo[child]["market"]
        childDict["Lowest Ask"] = market["lowestAsk"]
        try:
            childDict["Total Asks"] = market["numberOfAsks"]
        except:
             childDict["Total Asks"] = 0
        childDict["Highest Bid"] = market["highestBid"]
        try:
            childDict["Total Bids"] = market["numberOfBids"]
        except:
            childDict["Total Bids"] = 0
        try:
            childDict["Total Sold"] = market["deadstockSold"]
        except:
            childDict["Total Sold"] = 0
        try:
            childDict["Average Sale Price"] = market["averageDeadstockPrice"]
        except:
            childDict["Average Sale Price"] = 0
        try:
            childDict["Market Cap"] = market["totalDollars"]
        except:
            childDict["Market Cap"] = 0
        childrenDictionary [childData["shoeSize"]] = childDict
    return childrenDictionary

#takes a product UUID and returns the StockX product link
def get_stockX_product_link(UUID):
    headers = {
    'accept': '*/*',
    'app-platform': 'ios',
    'app-name': 'StockX-iOS',
    'accept-language': 'en-US',
    'x-api-key': '99WtRZK6pS1Fqt8hXBfWq8BYQjErmwipa3a0hYxX',
    'user-agent': 'StockX/31379 CFNetwork/1206 Darwin/20.1.0',
    }

    params = (
        ('includes', 'market,360'),
        ('currency', 'USD'),
        ('country', 'US'),
    )
    response = requests.get('https://gateway.stockx.com/api/v2/products/'+UUID, headers=headers, params=params)
    response = json.loads(response.text)["Product"]
    marketInfo = response["market"]
    return ('https://stockx.com/'+response["urlKey"])

#sends a request to Goat for popular sneakers, returns a list of # quantity with product slug and a short product description
def get_Goat_popular(quantity):
    headers = {
    'user-agent': 'GOAT/2 CFNetwork/1331.0.7 Darwin/21.4.0',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    }

    listofProducts = []
    pages = math.ceil(quantity/20)
    page = 1
    while page!= pages+1:
        response = requests.get('https://ac.cnstrc.com/browse/group_id/sneakers?key=key_XT7bjdbvjgECO5d8&sort_by=relevance&sort_order=descending&&page={}'.format(page), headers=headers)
        products = json.loads(response.text)['response']['results']
        for product in products:
            listofProducts.append([product['data']['id'],product['data']['slug']])
        page += 1
    return (listofProducts[0:quantity])

#takes a Goat product slug and returns a dictionary with relevent product sales information
def build_goat_product(productTemplateId):
    headers = {
    'accept': 'application/json',
    'x-px-authorization': '3',
    'x-px-original-token': '3:be595f7a21be20e9873483838911212a57a708980dddce63cbb42f2c079092e8:WNPvpwygp6Blm23qTMGwZqOyEsip5VcqZqJsTtA2vXk0u0JkuMdPLn6hwKsNWkc93t1jEpDTbIfB6Lp0SuGJ4A==:1000:hG4DxQMasirdbDTjz9qRUt0HT3oygChpYmJOATdP9tHbFw9/alkHdujVI/f/6Y+DA8F/U6dlbkQmCW/XwbRCfh0FrmnWyRarfywYO51V5dLXpPkdKpz8qN9pCu/fTYsX2tiRWdltVzBkyDTYDYIoJGZZTRNDtYgk3KLgroIA3fTdRkLt6v/CfZVeWcRl3QJbwrj8ucOoiF4yYBsNVW98/A==',
    'cookie': '_sneakers_session=iDnCQ3zCGPUYFhqXfUWqS%2FwdGAtrpueQNPYWJtj5KQBb1JglhgtgcwSpeRRWtaoFGmUwPvEj2Oz0Ce4JAGI70lt9vXvmT043NbQREjTNgzKxuHObL5pqaKUbinVveT6Pkxagi10bVkoBVwV8rxqCEzDVvpYHqzLFcEXW7XDQEAGRmBCq3Tvlirjqo5fU%2B5AqIdFp2SgjMNnakilEWc4nNRHU0BX%2F3DF3glzemSMOWHG5C1W%2BZWhGo2WvgbZWNo8UgflDmq%2BNaSFDNCOYzQi%2FMcUUSjNsu6kW13pyfdfeXHPEv3CBAubUziO%2FsvN29Jvii5VXEdmf%2FxRhw1NjdIC9Fgfd27I6c3Ae1CNlRePTE9fUL4CCysQA%2BzwWOdubzacvuo4bgLnU8jMCWfUYNQ%3D%3D--tzqX8KGlpphsPT9d--CxSUstkAaJ41XCcPb4ETaQ%3D%3D',
    'cookie': '__cf_bm=.nZxjA3OHQmpjKSOM7QrmtWsj3IzWAe9tJ9bFhkuwM4-1650937450-0-AaiBJ020DMbjOgRDYiVRlH3tc7aBHIRkF5yTQktQkVeA4C71445dodei/cY6V7uwWw4DvYTHnNB1M7SstM8oDNQ=',
    'cookie': 'currency=USD',
    'if-none-match': 'W/"edf3e545f852cb02d18a73a0943ed2ab"',
    'user-agent': 'GOAT/2.51.1 (iPhone; iOS 15.4.1; Scale/3.00) Locale/en',
    'authorization': 'Token token="L27vE32-oBq9vtoMst9y"',
    'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'countryCode': 'US',
        'productTemplateId': productTemplateId,
    }

    response = requests.get('https://www.goat.com/api/v1/product_variants/buy_bar_data', params=params, headers=headers)
    itemData = {}
    for item in json.loads(response.text):
        #if item['shoeCondition'] == 'new_no_defects':
        try:
            itemData [item['sizeOption']['value']] = (item['lowestPriceCents']['amountUsdCents']/100)
        except:
            continue
        else:
            continue
    return itemData

#takes a product slug and returns the Goat product link
def get_Goat_product_link(slug):
    return ('https://goat.com/sneakers/'+slug)

#takes a link, runs it through the VigLink API, and then shortens it using bit.ly
def makeMoney(link):
    params = (
        ('u', link),
        ('key', 'a046c4a6cc7b2b4f1561c4d6979fb7e8'),
    )

    headers = {
        'Authorization': 'Bearer 53a911224f69dccf55b565a7329fc48c2325a2de',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://viglink.io/uri/anywhere/generate', params=params)
    response = json.loads(response.text)["anywhereUrl"]
    data = {"long_url": response, "domain": "bit.ly" }
    response2 = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=json.dumps(data))

    return(json.loads(response2.text)["id"])

#creates a database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#creates a database using StockX popular data
def build_StockX_popular_DB(data, cur, conn):
    cur.execute ("DROP TABLE IF EXISTS StockXPopular")
    cur.execute("CREATE TABLE IF NOT EXISTS StockXPopular (UUID TEXT, description TEXT, Link TEXT)")
    for i in data:
        link = makeMoney(get_stockX_product_link(i[0]))
        cur.execute("INSERT OR IGNORE INTO StockXPopular (UUID,description,Link) VALUES (?,?,?)",(i[0],i[1],link))
    conn.commit()

#creates a database using StockX product data
def build_StockX_product_DB(UUID,data,cur,conn):
    link = makeMoney(get_stockX_product_link(UUID))
    UUID = UUID.replace("-","")
    DataBaseName = 'StockX_product_'+UUID
    cur.execute("DROP TABLE IF EXISTS "+DataBaseName+"")
    cur.execute("CREATE TABLE IF NOT EXISTS " + DataBaseName +" (Size TEXT, LowestAsk INTEGER, TotalAsks INTEGER, HighestBid INTEGER, TotalBids INTEGER, TotalSold INTEGER, AVGSalePrice INTEGER, MarketCap INTEGER, Link TEXT)")
    for i in data:
        cur.execute("INSERT OR IGNORE INTO " + DataBaseName + " (Size,LowestAsk,TotalAsks,HighestBid,TotalBids,TotalSold,AVGSalePrice,MarketCap,Link) VALUES (?,?,?,?,?,?,?,?,?)",(i,data[i]['Lowest Ask'],data[i]['Total Asks'],data[i]['Highest Bid'],data[i]['Total Bids'],data[i]['Total Sold'],data[i]['Average Sale Price'],data[i]['Market Cap'],link))
    conn.commit()

#creates a database using Goat popular data
def build_Goat_popular_DB(data, cur, conn):
    cur.execute ("DROP TABLE IF EXISTS GoatPopular")
    cur.execute("CREATE TABLE IF NOT EXISTS GoatPopular (id TEXT, slug TEXT, Link TEXT)")
    for i in data:
        link = makeMoney(get_Goat_product_link(i[1]))
        cur.execute("INSERT OR IGNORE INTO GoatPopular (id,slug,Link) VALUES (?,?,?)",(i[0],i[1],link))
    conn.commit()

#creates a database using Goat product data
def build_Goat_product_DB(slug,data,cur,conn):
    link = makeMoney(get_Goat_product_link(slug))
    slug = slug.replace("-","")
    DataBaseName = 'Goat_product_'+slug
    cur.execute("DROP TABLE IF EXISTS "+DataBaseName+"")
    cur.execute("CREATE TABLE IF NOT EXISTS " + DataBaseName +" (Size TEXT, Price INTEGER, Link TEXT)")
    for i in data:
        cur.execute("INSERT OR IGNORE INTO " + DataBaseName + " (Size,Price,Link) VALUES (?,?,?)",(i,data[i],link))
    conn.commit()

#reads StockX popular products and creates a database for every popular product (1 at a time to comply with class 25 limit)
def read_StockX_popular_table(cur, conn):
    cur.execute("Select UUID from StockXPopular")
    UUIDList = []
    for item in cur:
        UUIDList.append(item[0])
    for UUID in UUIDList:
        build_StockX_product_DB(UUID,build_stockX_product(UUID),cur,conn)
        print ("Built Table for UUID " + UUID)

#reads Goat popular products and creates a database for every popular product (1 at a time to comply with class 25 limit)
def read_Goat_popular_table(cur, conn):
    cur.execute("Select slug from GoatPopular")
    slugList = []
    for item in cur:
        slugList.append(item[0])
    for slug in slugList:
        build_Goat_product_DB(slug,build_goat_product(slug),cur,conn)
        print ("Built Table for slug " + slug)

#gets average price per size of every product on StockX and Goat databases
def get_avg_price_all(cur,conn):
    cur.execute("Select UUID from StockXPopular")
    UUIDList = []
    for item in cur:
        UUIDList.append(item[0])

    cur.execute("Select slug from GoatPopular")
    slugList = []
    for item in cur:
        slugList.append(item[0])

    StockXDict = {}
    for UUID in UUIDList:
        UUID = UUID.replace("-","")
        DataBaseName = 'StockX_product_'+UUID
        cur.execute("SELECT Size,AVGSalePrice from "+DataBaseName+"")
        newList = []
        for item in cur:
            try:
                newList.append([float(item[0]),item[1]])
            except:
                continue
        for item in newList:
            if item[0] not in StockXDict.keys():
                StockXDict[item[0]] = []
            StockXDict[item[0]].append(item[1])

    GoatDict = {}
    for slug in slugList:
        slug = slug.replace("-","")
        DataBaseName = 'Goat_product_'+slug
        cur.execute("SELECT Size, Price from " + DataBaseName +"")
        newList = []
        for item in cur:
            newList.append([float(item[0]),item[1]])
        for item in newList:
            if item[0] not in GoatDict.keys():
                GoatDict[item[0]] = []
            GoatDict[item[0]].append(item[1])

    cloneDict = StockXDict

    for key in GoatDict.keys():
        if key not in cloneDict.keys():
            cloneDict[key] = GoatDict[key]
        else:
            for value in GoatDict[key]:
                cloneDict[key].append(value)

    finalAvgDict = {}

    for item in cloneDict:
        total = 0
        for value in cloneDict[item]:
            total += value
        finalAvgDict[item]= round(total/len(cloneDict[item]),2)

    f = open("avgSales.txt", "w")
    f.write(str(finalAvgDict))
    f.close()

#gets total number of bids per size for StockX products
def total_bids_by_size_StockX(cur,conn):
    cur.execute("Select UUID from StockXPopular")
    UUIDList = []
    for item in cur:
        UUIDList.append(item[0])

    StockXDict = {}
    for UUID in UUIDList:
        UUID = UUID.replace("-","")
        DataBaseName = 'StockX_product_'+UUID
        cur.execute("SELECT Size,TotalBids from "+DataBaseName+"")
        newList = []
        for item in cur:
            try:
                newList.append([float(item[0]),item[1]])
            except:
                continue
        for item in newList:
            if item[0] not in StockXDict.keys():
                StockXDict[item[0]] = []
            StockXDict[item[0]].append(item[1])

    finalBidsDict = {}

    for item in StockXDict:
        total = 0
        for value in StockXDict[item]:
            total += value
        finalBidsDict[item]= total

    f = open("bidsTotals.txt", "w")
    f.write(str(finalBidsDict))
    f.close()

#gets total number of pairs sold per size for StockX products
def total_sold_by_size_StockX(cur,conn):
    cur.execute("Select UUID from StockXPopular")
    UUIDList = []
    for item in cur:
        UUIDList.append(item[0])

    StockXDict = {}
    for UUID in UUIDList:
        UUID = UUID.replace("-","")
        DataBaseName = 'StockX_product_'+UUID
        cur.execute("SELECT Size,TotalSold from "+DataBaseName+"")
        newList = []
        for item in cur:
            try:
                newList.append([float(item[0]),item[1]])
            except:
                continue
        for item in newList:
            if item[0] not in StockXDict.keys():
                StockXDict[item[0]] = []
            StockXDict[item[0]].append(item[1])

    finalBidsDict = {}

    for item in StockXDict:
        total = 0
        for value in StockXDict[item]:
            total += value
        finalBidsDict[item]= total

    f = open("salesTotals.txt", "w")
    f.write(str(finalBidsDict))
    f.close()

#creates TXT files for visualization purposes for StockX products, uses join function
def create_StockX_product_TXT(cur,conn):
    cur.execute("Select UUID from StockXPopular")
    UUIDList = []
    for item in cur:
        UUIDList.append(item[0])

    StockXDict = {}
    for UUID in UUIDList:
        UUID = UUID.replace("-","")
        DataBaseName = 'StockX_product_'+UUID
        cur.execute("SELECT StockXPopular.description, "+DataBaseName+".Size, "+DataBaseName+".TotalSold,  "+DataBaseName+".Link  FROM StockXPopular JOIN "+DataBaseName+" ON StockXPopular.Link = "+DataBaseName+".Link")
        pricing = {}
        headers = {}
        for item in cur:
            pricing[item[1]] = item[2]
            headers["title"] = str(item[0]).replace("-"," ").title()
            headers["link"] = item[3]
        f = open(str(DataBaseName+"headers.txt"), "w")
        f.write(str(headers))
        f.close()
        f = open(str(DataBaseName+"data.txt"), "w")
        f.write(str(pricing))
        f.close()

#creates TXT files for visualization purposes for Goat products, uses join function
def create_Goat_product_TXT(cur,conn):
    cur.execute("Select slug from GoatPopular")
    slugList = []
    for item in cur:
        slugList.append(item[0])

    GoatDict = {}
    for slug in slugList:
        slug = slug.replace("-","")
        DataBaseName = 'Goat_product_'+slug
        cur.execute("SELECT GoatPopular.slug, "+DataBaseName+".Size, "+DataBaseName+".Price,  "+DataBaseName+".Link  FROM GoatPopular JOIN "+DataBaseName+" ON GoatPopular.Link = "+DataBaseName+".Link")
        pricing = {}
        headers = {}
        for item in cur:
            pricing[item[1]] = item[2]
            headers["title"] = str(item[0]).replace("-"," ").title()
            headers["link"] = item[3]
        f = open(str(DataBaseName+"headers.txt"), "w")
        f.write(str(headers))
        f.close()
        f = open(str(DataBaseName+"data.txt"), "w")
        f.write(str(pricing))
        f.close()

#visualizes all Goat TXT's
def visualize_Goat_TXTs():
    goatTXTheaders = []
    for x in os.listdir():
        if x.startswith("Goat") & x.endswith("headers.txt"):
            goatTXTheaders.append(x)
    for file in goatTXTheaders:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                headers = ast.literal_eval(line)
            f.close()
        file = file.replace("headers","data")
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                data = ast.literal_eval(line)
            f.close()
        floatedData = {}
        for item in data:
            itemKey = float(item)
            floatedData[itemKey] = int (data[item])
        file = file.replace("data","")
        sizes = list(floatedData.keys())
        prices = list(floatedData.values())
        fig = plt.figure(figsize =(15, 10))
        plt.bar(sizes, prices, color ='maroon', width = 0.4)
        plt.xticks(np.arange(len(sizes)))
        plt.xlim([3, 19])
        plt.xlabel("Size")
        plt.ylabel("Price (USD) $")
        plt.suptitle(headers["title"])
        plt.title(headers["link"])
        plt.savefig(file+'.png')
        plt.close()

#visualizes all StockX TXT's
def visualize_StockX_TXTs():
    stockXTXTheaders = []
    for x in os.listdir():
        if x.startswith("StockX") & x.endswith("headers.txt"):
            stockXTXTheaders.append(x)
    for file in stockXTXTheaders:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                headers = ast.literal_eval(line)
            f.close()
        file = file.replace("headers","data")
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                data = ast.literal_eval(line)
            f.close()
        floatedData = {}
        for item in data:
            try:
                itemKey = float(item)
                floatedData[itemKey] = int (data[item])
            except:
                continue
        file = file.replace("data","")
        sizes = list(floatedData.keys())
        prices = list(floatedData.values())
        fig = plt.figure(figsize =(15, 10))
        plt.bar(sizes, prices, color ='maroon', width = 0.2)
        plt.xticks(np.arange(len(sizes)))
        plt.xlim([3, 19])
        plt.xlabel("Size")
        plt.ylabel("Total Units Sold")
        plt.suptitle(headers["title"])
        plt.title(headers["link"])
        plt.savefig(file+'.png')
        plt.close()

#visualizes Average sales price data
def visualize_avg_price_all():
    with open('avgSales.txt') as f:
        lines = f.readlines()
        for line in lines:
            data = ast.literal_eval(line)
            f.close()
        sizes = list(data.keys())
        avg_sale_price = list(data.values())
        fig = plt.figure(figsize =(15, 10))
        plt.bar(sizes, avg_sale_price, color ='maroon', width = 0.4)
        plt.xticks(np.arange(len(sizes)))
        plt.xlim([3, 19])
        plt.xlabel("Size")
        plt.ylabel("Average Price $")
        plt.suptitle("Average Sale Price By Size Across Goat and StockX")
        plt.savefig('avgSales.png')

#visualizes total bids data
def visualize_total_bids_by_size_StockX():
    with open('bidsTotals.txt') as f:
        lines = f.readlines()
        for line in lines:
            data = ast.literal_eval(line)
            f.close()
        sizes = list(data.keys())
        avg_sale_price = list(data.values())
        fig = plt.figure(figsize =(15, 10))
        plt.bar(sizes, avg_sale_price, color ='maroon', width = 0.4)
        plt.xticks(np.arange(len(sizes)))
        plt.xlim([3, 19])
        plt.xlabel("Size")
        plt.ylabel("Total Bids")
        plt.suptitle("Total Bids By Size on StockX")
        plt.savefig('bidsTotals.png')

#visualizes total sales by size data
def visualize_sales_by_size_StockX():
    with open('salesTotals.txt') as f:
        lines = f.readlines()
        for line in lines:
            data = ast.literal_eval(line)
            f.close()
        sizes = list(data.keys())
        avg_sale_price = list(data.values())
        fig = plt.figure(figsize =(15, 10))
        plt.bar(sizes, avg_sale_price, color ='maroon', width = 0.4)
        plt.xticks(np.arange(len(sizes)))
        plt.xlim([3, 19])
        plt.xlabel("Size")
        plt.ylabel("Total Units Sold")
        plt.suptitle("Total Units Sold By Size on StockX")
        plt.savefig('salesTotals.png')

#initializes popular data for StockX and Goat
def initialize_popular_data():
    cur, conn = setUpDatabase("SneakerDatabase.db")
    stockXQuantity = input("How many items would you like to scrape from StockX? ")
    print ("Initializing StockX Popular Data")
    stockX_popular = get_stockX_popular(int(stockXQuantity))
    print ("StockX Popular Data Initialized!")
    print ("Building StockX Database ... this may take a while")
    build_StockX_popular_DB(stockX_popular, cur, conn)
    print ("StockX Database Built!")
    goatQuantity = input("How many items would you like to scrape from Goat? ")
    print ("Initializing Goat Popular Data")
    goat_popular = get_Goat_popular(int(goatQuantity))
    print("Goat Popular Data Initialized!")
    print ("Building Goat Database ... this may take a while")
    build_Goat_popular_DB(goat_popular, cur, conn)
    print ("Goat Database Built!")
    print ("")
    print ("")

#builds product databases for StockX and Goat Products
def refresh_SKU_data():
    cur, conn = setUpDatabase("SneakerDatabase.db")
    print ("Building StockX Product Data")
    read_StockX_popular_table(cur, conn)
    print ("All StockX Product Data Built")
    print ("Building Goat Product Data")
    read_Goat_popular_table(cur,conn)
    print ("All Goat Product Data Built")
    print ("")
    print ("")

def create_all_visuals():
    cur, conn = setUpDatabase("SneakerDatabase.db")
    get_avg_price_all(cur,conn)
    total_bids_by_size_StockX(cur,conn)
    total_sold_by_size_StockX(cur,conn)
    create_StockX_product_TXT(cur,conn)
    create_Goat_product_TXT(cur,conn)
    print ("Creating StockX Product Visualizations")
    visualize_StockX_TXTs()
    print ("StockX Product Visualizations Created")
    print ("Creating Goat Product Visualizations")
    visualize_Goat_TXTs()
    print ("Goat Product Visualizations Created")
    print ("Creating Average Price Visualization")
    visualize_avg_price_all()
    print ("Average Price Visualization Created")
    print ("Creating Bids by Size Visualization")
    visualize_total_bids_by_size_StockX()
    print ("Bids by Size Visualizatio Created")
    print ("Creating Sales by Size Visualization")
    visualize_sales_by_size_StockX()
    print ("Sales by Size Visualization Created")
    print ("")
    print ("")

def main():
    os.system('clear')
    print("Welcome to Sneaker Scraper!")
    print("___________________________")
    print("To refresh popular data, enter 1")
    print("To refresh SKU data for existing popular data, enter 2")
    print("To generate visuals using current SKU data, enter 3")
    print("If you have not ran Sneaker Scraper on your machine, and would like to do all of the above, enter 4")
    print("To quit, enter 5")

    decide = input("Input: ")

    if decide == "1":
        print ("Great! Let's refresh popular data for StockX and Goat!")
        initialize_popular_data()
        main()
    elif decide == "2":
        refresh_SKU_data()
        main()
    elif decide == "3":
        create_all_visuals()
        main()
    elif decide == "4":
        initialize_popular_data()
        refresh_SKU_data()
        create_all_visuals()
    elif decide == "5":
        quit()

main()
