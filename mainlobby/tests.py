import json 

with open('json_data.json', encoding='utf-8') as json_file:
    dicts = json.load(json_file)
price0 = float(dicts['price0']) * 100
price1 = float(dicts['price1']) * 100
price2 = float(dicts['price2']) * 100
price1 = int(price1)
PRODUCTS_STRIPE_NOW_PRICE = {
'product_regular': price0,
'product_pro': price1,
'product_platinum': price2,
}

print(PRODUCTS_STRIPE_NOW_PRICE)