import requests as r
import math
from PIL import Image
from io import BytesIO
from teamreports import app_config
import asyncio
from aiohttp import ClientSession

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
    """Merge list of dictionaries from list1 with dictionaries with list2 on product_code which is
        common key in all dictionaries. list1 should not be empty"""
    try:
        merged_list = []
        if list1:
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
        else:
            return list2
    except Exception as e:
        print(e)



async def fetch(url, headers, session):
    async with session.get(url, params=headers) as response:
        print(response)
        if(response.reason == 'OK'):
            return await response.json()
        else:
            print(response)

async def fetch_bytes(url, headers, session, product_code):
    async with session.get(url, params=headers) as response:
        print(response)       
        if(response.reason == 'OK'):
            photo_bytes = await response.read()
            return {PRODUCT_CODE: product_code, 'photo': photo_bytes}


async def get_all_async(headers_for_all):
    product_tasks = []
    stock_tasks = []
    price_tasks = []
    attachment_tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for headers in headers_for_all:
            product_task = asyncio.ensure_future(fetch(URL + 'api/product', headers, session))
            product_tasks.append(product_task)
            
            stock_task = asyncio.ensure_future(fetch(URL + 'api/product/stock', headers, session))
            stock_tasks.append(stock_task)

            price_task = asyncio.ensure_future(fetch(URL + 'api/product/price', headers, session))
            price_tasks.append(price_task)

            attachment_task = asyncio.ensure_future(fetch(URL + 'api/product/attachment', headers, session))
            attachment_tasks.append(attachment_task)

        product_responses = asyncio.gather(*product_tasks)
        stock_responses = asyncio.gather(*stock_tasks)
        price_responses = asyncio.gather(*price_tasks)
        attachment_responses = asyncio.gather(*attachment_tasks)
        all_resp = await asyncio.gather(product_responses, stock_responses, price_responses, attachment_responses)

    return (
            [product for sublist in all_resp[0] if sublist is not None for product in sublist],
            [stock for sublist in all_resp[1] if sublist is not None for stock in sublist if sublist is not None],
            [price for sublist in all_resp[2] if sublist is not None for price in sublist if sublist is not None],
            [attachment for sublist in all_resp[3] if sublist is not None for attachment in sublist if sublist is not None]
        )


async def get_all_photos_async(token, products_jpgs):

    photo_tasks = []
    headers = {"Token": token}

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for product in products_jpgs:
            photo_task = asyncio.ensure_future(fetch_bytes(URL + 'api/product/attachment/image/' + product['file_name'], headers, session, product[PRODUCT_CODE]))
            photo_tasks.append(photo_task)

        photo_responses = await asyncio.gather(*photo_tasks)

    return [photo_data for photo_data in photo_responses if photo_data is not None]




def get_all_products(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/product/count', headers=page_headers).json()
        how_many_pages = math.ceil(page_info['total_count']/page_info['page_size'])
        headers_for_all = [{
                            "Content-Type": "application/json",
                            "Token": token,
                            "Page": str(i + 1)} #because loop starts from 0 but pages starts from 1
                            for i in range(how_many_pages)]

        #get async all products, stocks, prices and att
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_all_async(headers_for_all))
        loop.run_until_complete(future)

        product_list = future.result()[0]
        stock_list = future.result()[1]
        price_list = future.result()[2]
        attachment_list = future.result()[3]

        loop.close()


        #merge products with stocks
        product_stock_list = merge_lists_of_dicts(product_list, stock_list)

        #merge products+stocks with prices
        product_stock_price_list = merge_lists_of_dicts(product_stock_list, price_list)

        #merge products+stocks+prices with metadeta attachment
        product_stock_price_att_list = merge_lists_of_dicts(product_stock_price_list, attachment_list)

        #take all products with have a photo (not null)
        product_jpgs = [{PRODUCT_CODE: product[PRODUCT_CODE], 'file_name': product['file_name']} for product in product_stock_price_att_list if product['file_name']]

        #get photos async
        loop1 = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_all_photos_async(token, product_jpgs))
        loop1.run_until_complete(future)

        photo_list = future.result()


        #merge products+stocks+prices+att with photos
        product_stock_price_att_photo_list = merge_lists_of_dicts(product_stock_price_att_list, photo_list)
    
        return product_stock_price_att_photo_list
    except Exception as e:
        print(e)
        raise



async def get_selected_products_async(headers_for_selected):
    products_ids = []
    product_tasks = []

    async with ClientSession() as session:
        for headers in headers_for_selected:
            product_task = asyncio.ensure_future(fetch(URL + 'api/product/search', headers, session))
            product_tasks.append(product_task)               

        product_responses = await asyncio.gather(*product_tasks)

    product_list = [product for product in product_responses if product]
    for product in product_list:
        if product:
            products_ids.append(str(product['product_id'])) #change id to strings to use it later in url



    return (product_list, products_ids)



async def get_selected_product_features_async(products_ids, headers):
    stock_tasks = []
    price_tasks = []
    attachment_tasks = []


    async with ClientSession() as session:
        for product_id in products_ids:
            stock_task = asyncio.ensure_future(fetch(URL + 'api/product/stock/' + product_id, headers, session))
            stock_tasks.append(stock_task)

            price_task = asyncio.ensure_future(fetch(URL + 'api/product/price/' + product_id, headers, session))
            price_tasks.append(price_task)            

            attachment_task = asyncio.ensure_future(fetch(URL + 'api/product/attachment/' + product_id, headers, session))
            attachment_tasks.append(attachment_task)

        stock_responses = asyncio.gather(*stock_tasks)
        price_responses = asyncio.gather(*price_tasks)
        attachment_responses = asyncio.gather(*attachment_tasks)
        all_resp = await asyncio.gather(stock_responses, price_responses, attachment_responses)

    stock_list = all_resp[0]
    price_list = all_resp[1]
    attachment_list = all_resp[2]        

    #take all products which have a photo (not null)
    product_jpgs = [{PRODUCT_CODE: att[PRODUCT_CODE], 'file_name': att['file_name']} for att in attachment_list if att['file_name']]
    photo_headers = {'Token': headers['Token']}
    photo_tasks = []

    async with ClientSession() as session:
        for photo in product_jpgs:
            photo_task = asyncio.ensure_future(fetch_bytes(URL + 'api/product/attachment/image/' + photo['file_name'], photo_headers, session, photo[PRODUCT_CODE]))
            photo_tasks.append(photo_task)

        photo_responses = await asyncio.gather(*photo_tasks)



    return (stock_list, price_list, attachment_list, photo_responses)




def get_selected_products(product_code_list, token):
    try:
        product_list = []
        stock_list = []
        price_list = []
        attachment_list = []
        photo_list = []        
        headers_for_selected = [{
                                "Content-Type": "application/json",
                                "Token": token,
                                "Productcode": product_code} for product_code in product_code_list]
   

        #get async all products
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_selected_products_async(headers_for_selected))
        loop.run_until_complete(future)

        product_list = future.result()[0]
        

        products_ids = future.result()[1]



        headers_for_product_features = {
                                        "Content-Type": "application/json",
                                        "Token": token
                                    }

        #get async all stocks, prices, att, photos
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_selected_product_features_async(products_ids, headers_for_product_features))
        loop.run_until_complete(future)

        stock_list = future.result()[0]
        price_list = future.result()[1]
        attachment_list = future.result()[2]
        photo_list = future.result()[3]



        #loop.close()


        # for product_code in product_code_list:
        #     product_single = r.get(URL + 'api/product/search', headers={
        #                                                                 "Content-Type": "application/json",
        #                                                                 "Token": token,
        #                                                                 "Productcode": product_code
        #                                                             })
        #     if product_single.ok:
        #         product_list.append(product_single.json())
        #         product_id = str(product_single.json()['product_id'])

        #         stock_single = r.get(URL + 'api/product/stock/' + product_id, headers=headers)
        #         if stock_single.ok:       
        #             stock_list.append(stock_single.json())

        #         price_single = r.get(URL + 'api/product/price/' + product_id, headers=headers)
        #         if price_single.ok:
        #             price_list.append(price_single.json())

        #         att_single = r.get(URL + 'api/product/attachment/' + product_id, headers=headers)
        #         if att_single.ok:
        #             attachment_list.append(att_single.json())
        #             photo = r.get(URL + 'api/product/attachment/image/' + att_single.json()['file_name'], headers={"Token": token})
        #             if photo.ok:
        #                 photo_list.append({PRODUCT_CODE: product_code, 'photo': photo.content})
        #     else:
        #         product_list.append({PRODUCT_CODE:product_code}) #append dict with product_code only so the rest attributes will be marked as not found


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
    except Exception as e:
        print(e)
        raise



