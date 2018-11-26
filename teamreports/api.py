import requests as r
import math
import pandas as pd


URL = 'https://team-services-uat.herokuapp.com/'

def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post(URL + 'api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


def get_all_products(token, self_obj=None):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/count', headers=page_headers)#.json()
        if not page_info.ok:
            self_obj.token_expired()

        product_list = []
        for page in range(math.ceil(page_info['total_count']/page_info['page_size'])):        
            headers = {
                        "Content-Type": "application/json",
                        "Token": token,
                        "Page": str(page + 1)} #because loop starts from 0 but pages starts from 1
            
            chunk = r.get(URL + 'api/product', headers=headers).json()
            product_list.extend(chunk)

        products_df = pd.DataFrame.from_dict(product_list)
        return products_df
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise


def get_all_prices(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/price/count', headers=page_headers).json()

        price_list = []
        for page in range(math.ceil(page_info['total_count']/page_info['page_size'])):        
            headers = {
                        "Content-Type": "application/json",
                        "Token": token,
                        "Page": str(page + 1)} #because loop starts from 0 but pages starts from 1
            
            chunk = r.get(URL + 'api/product', headers=headers).json()
            price_list.extend(chunk)

        prices_df = pd.DataFrame.from_dict(price_list)
        return prices_df
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise

import gui #import LoginForm