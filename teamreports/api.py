import requests as r
import math

URL = 'https://team-services-uat.herokuapp.com/'

def post_token(email, password):
    try:
        headers = {"Username": email, "Password": password}
        return r.post(URL + 'api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


def get_products(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/count', headers=page_headers).json()

        product_list = []
        for page in range(math.ceil(page_info['total_count']/page_info['page_size'])):        
            headers = {
                        "Content-Type": "application/json",
                        "Token": token,
                        "Page": str(page + 1)} #because loop starts from 0 but pages starts from 1
            
            chunk = r.get(URL + 'api/product', headers=headers).json()
            product_list.extend(chunk)

        return product_list
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise




post_token('test@kalorik.pl', 'test')