import requests as r
import math


URL = 'https://team-services-uat.herokuapp.com/'
PRODUCT_CODE = 'product_code'

def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post(URL + 'api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


def get_all_products(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/count', headers=page_headers).json()

        product_list = []
        stock_list = []
        price_list = []
        for page in range(math.ceil(page_info['total_count']/page_info['page_size'])):
            headers = {
                        "Content-Type": "application/json",
                        "Token": token,
                        "Page": str(page + 1)} #because loop starts from 0 but pages starts from 1
            
            product_chunk = r.get(URL + 'api/product', headers=headers)
            product_list.extend(product_chunk.json())

            stock_chunk = r.get(URL + 'api/product/stock', headers=headers)
            stock_list.extend(stock_chunk.json())

            price_chunk = r.get(URL + 'api/product/price', headers=headers)
            price_list.extend(price_chunk.json())

        product_stock_list = []
        product_stock_price_list = []

        #merge products with stocks
        for id_prod, one_product in enumerate(product_list):
            for id_stock, one_stock in enumerate(stock_list):
                if one_product[PRODUCT_CODE] == one_stock[PRODUCT_CODE]:
                    a = {**one_product, **one_stock} 
                    product_stock_list.append(a)
                    stock_list.pop(id_stock)
                    product_list.pop(id_prod)
                    break

        for remaining in product_list:
            product_stock_list.append(remaining)

        #merge products+stocks with stocks
        for id_prod, one_product in enumerate(product_stock_list):
            for id_price, one_price in enumerate(price_list):
                if one_product[PRODUCT_CODE] == one_price[PRODUCT_CODE]:
                    a = {**one_product, **one_price} 
                    product_stock_price_list.append(a)
                    price_list.pop(id_price)
                    product_stock_list.pop(id_prod)
                    break

        for remaining in product_stock_list:
            product_stock_price_list.append(remaining)

                        
        return product_stock_price_list
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise



a = get_all_products('eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0MzQ0NDQzMCwiZXhwIjoxNTQzNDQ4MDMwfQ.eyJjb25maXJtIjozfQ.U7ib244vfbrEMnYrUyrALqRc5wkmZtx_gjlTzzSYSVU')

print(a)
# def get_all_prices(token):
#     try:
#         page_headers = {"Content-Type": "application/json", "Token": token}
#         page_info = r.get(URL + 'api/product/price/count', headers=page_headers).json()

#         price_list = []
#         for page in range(math.ceil(page_info['total_count']/page_info['page_size'])):        
#             headers = {
#                         "Content-Type": "application/json",
#                         "Token": token,
#                         "Page": str(page + 1)} #because loop starts from 0 but pages starts from 1
            
#             chunk = r.get(URL + 'api/product', headers=headers).json()
#             price_list.extend(chunk)

#         prices_df = pd.DataFrame.from_dict(price_list)
#         return prices_df
#     except r.exceptions.ConnectionError as e:
#         return 'Cannot connect to the server'
#         raise

# import gui #import LoginForm