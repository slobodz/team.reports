import requests as r
import math
from PIL import Image
from io import BytesIO
from teamreports import app_config

URL = app_config.URL
PRODUCT_CODE = 'product_code'

def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post(URL + 'api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


def merge_lists_of_dicts(list1, list2):
    merged_list = []
    for id_list1, one_dict_list1 in enumerate(list1):
        is_key_in_list2 = False
        for id_list2, one_dict_list2 in enumerate(list2):
            if one_dict_list1[PRODUCT_CODE] == one_dict_list2[PRODUCT_CODE]:
                a = {**one_dict_list1, **one_dict_list2} 
                merged_list.append(a)
                list2.pop(id_list2)
                is_key_in_list2 = True
                break
        if not is_key_in_list2:
            merged_list.append(one_dict_list1)


    return merged_list


def get_all_products(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/count', headers=page_headers).json()

        product_list = []
        stock_list = []
        price_list = []
        attachment_list = []
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

            attachment_chunk = r.get(URL + 'api/product/attachment', headers=headers)
            attachment_list.extend(attachment_chunk.json())

        #merge products with stocks
        product_stock_list = merge_lists_of_dicts(product_list, stock_list)

        #merge products+stocks with prices
        product_stock_price_list = merge_lists_of_dicts(product_stock_list, price_list)

        #merge products+stocks+prices with metadeta attachment
        product_stock_price_att_list = merge_lists_of_dicts(product_stock_price_list, attachment_list)

        #merge products+stocks+prices+att with photos
        for id_prod, product in enumerate(product_stock_price_att_list):
            if product['file_name']:
                photo = r.get(URL + 'api/product/attachment/image/' + product['file_name'], headers={"Token": token})
                if(photo.ok):
                    product_stock_price_att_list[id_prod]['photo'] = photo.content
                
        return product_stock_price_att_list
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise




def get_selected_products(product_code_list, token):
    try:
        product_list = []
        stock_list = []
        price_list = []
        attachment_list = []
        photo_list = []        
        headers = {
                    "Content-Type": "application/json",
                    "Token": token
                }
   

        for product_code in product_code_list:
            product_single = r.get(URL + 'api/product/search', headers={
                                                                        "Content-Type": "application/json",
                                                                        "Token": token,
                                                                        "Productcode": product_code
                                                                    })
            if product_single.ok:
                product_list.append(product_single.json())
                product_id = str(product_single.json()['product_id'])

                stock_single = r.get(URL + 'api/product/stock/' + product_id, headers=headers)
                if stock_single.ok:       
                    stock_list.append(stock_single.json())

                price_single = r.get(URL + 'api/product/price/' + product_id, headers=headers)
                if price_single.ok:
                    price_list.append(price_single.json())

                att_single = r.get(URL + 'api/product/attachment/' + product_id, headers=headers)
                if att_single.ok:
                    attachment_list.append(att_single.json())
                    photo = r.get(URL + 'api/product/attachment/image/' + att_single.json()['file_name'], headers={"Token": token})
                    if photo.ok:
                        photo_list.append({PRODUCT_CODE: product_code, 'photo': photo.content})
            else:
                product_list.append({PRODUCT_CODE:product_code}) #append dict with product_code only so the rest attributes will be marked as not found


        #merge products with stocks
        if not stock_list:
            product_stock_list = product_list
        else:
            product_stock_list = merge_lists_of_dicts(product_list, stock_list)


        #merge products+stocks with prices
        if not price_list:
            product_stock_price_list = product_stock_list
        else:        
            product_stock_price_list = merge_lists_of_dicts(product_stock_list, price_list)


        #merge products+stocks+prices with metadeta attachment
        if not attachment_list:
            product_stock_price_att_list = product_stock_price_list
        else:        
            product_stock_price_att_list = merge_lists_of_dicts(product_stock_price_list, attachment_list)


        #merge products+stocks+prices+att with photo
        if not photo_list:
            product_stock_price_att_photo_list = product_stock_price_att_list
        else:        
            product_stock_price_att_photo_list = merge_lists_of_dicts(product_stock_price_att_list, photo_list)            


                        
        return product_stock_price_att_photo_list
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'
        raise
