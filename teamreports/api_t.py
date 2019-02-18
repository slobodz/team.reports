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
    """Merge dictionaries from list1 with dictionaries with list2 on product_code which is
        common key in all dictionaries. list1 must not be empty"""
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



async def fetch(url, session, headers=None):
    async with session.get(url, params=headers) as response:
        print(response)
        if(response.status == 200):
            return await response.json()


async def fetch_bytes(url, session, product_code):
    async with session.get(url) as response:
        print(response)       
        if(response.status == 200):
            photo_bytes = await response.read()
            return {PRODUCT_CODE: product_code, 'photo': photo_bytes}

async def post_for_product(url, session, product_json):
    async with session.post(url, json=product_json) as response:
        print(response)
        if(response.status == 200):
            return await response.json()
        elif(response.status == 404):
            return product_json



async def get_all_async(client_headers, how_many_pages):
    product_tasks = []
    stock_tasks = []
    price_tasks = []
    attachment_tasks = []

   
    async with ClientSession(headers=client_headers) as session:
        for page in range(how_many_pages):

            headers = {'Page': page + 1} #pages starts from 1 not 0

            product_task = asyncio.ensure_future(fetch(URL + 'api/products', headers=headers, session=session))
            product_tasks.append(product_task)
            
            stock_task = asyncio.ensure_future(fetch(URL + 'api/products/stock/aggregated', headers=headers, session=session))
            stock_tasks.append(stock_task)

            price_task = asyncio.ensure_future(fetch(URL + 'api/products/price/aggregated', headers=headers, session=session))
            price_tasks.append(price_task)

            attachment_task = asyncio.ensure_future(fetch(URL + 'api/products/attachment/aggregated', headers=headers, session=session))
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
    
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(#headers={"Token": token}
        ) as session:
        for photo in products_jpgs:
            #photo_task = asyncio.ensure_future(fetch_bytes(URL + 'api/product/attachment/image/' + photo['file_name'], session, photo[PRODUCT_CODE]))
            photo_task = asyncio.ensure_future(fetch_bytes(photo['tile_url'], session, photo[PRODUCT_CODE]))            
            photo_tasks.append(photo_task)

        photo_responses = await asyncio.gather(*photo_tasks)

    return [photo for photo in photo_responses if photo]




def get_all_products(token):
    try:
        page_headers = {"Content-Type": "application/json", "Token": token}
        page_info = r.get(URL + 'api/products/count', headers=page_headers).json()
        how_many_pages = math.ceil(page_info['total_count']/page_info['page_size'])

        client_headers = {
                        'Token': token,
                        'Content-Type': 'application/json'
                    }

        #get async all products, stocks, prices and att
        asyncio.set_event_loop(asyncio.new_event_loop()) #setup new loop and use it as active in the next line
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_all_async(client_headers, how_many_pages))
        loop.run_until_complete(future)

        product_list = future.result()[0]
        stock_list = future.result()[1]
        price_list = future.result()[2]
        attachment_list = future.result()[3]


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


        #take all products with have a photo (not null)
        product_jpgs = [{PRODUCT_CODE: product[PRODUCT_CODE], 'tile_url': product['tile_url']} for product in product_stock_price_att_list if product['tile_url']]

        #get photos async
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_all_photos_async(token, product_jpgs))
        loop.run_until_complete(future)

        photo_list = future.result()

        loop.close()


        #merge products+stocks+prices+att with photos
        product_stock_price_att_photo_list = merge_lists_of_dicts(product_stock_price_att_list, photo_list)
    
        return product_stock_price_att_photo_list
    except Exception as e:
        print(e)
        raise



async def get_selected_products_async(product_code_list, client_headers):
    products_ids = []
    product_tasks = []

    async with ClientSession(headers=client_headers) as session:
        for product_code in product_code_list:
            product_json = {PRODUCT_CODE: product_code}
            product_task = asyncio.ensure_future(post_for_product(URL + 'api/product/search/', session, product_json))
            product_tasks.append(product_task)               

        product_responses = await asyncio.gather(*product_tasks)

    for product in product_responses:
        if 'product_id' in product:
            products_ids.append(str(product['product_id'])) #change id to strings to use it later in url

    return (product_responses, products_ids)



async def get_selected_product_features_async(products_ids, client_headers):
    stock_tasks = []
    price_tasks = []
    attachment_tasks = []


    async with ClientSession(headers=client_headers) as session:
        for product_id in products_ids:
            stock_task = asyncio.ensure_future(fetch(URL + 'api/products/stock/aggregated/' + product_id, session=session))
            stock_tasks.append(stock_task)

            price_task = asyncio.ensure_future(fetch(URL + 'api/products/price/aggregated/' + product_id, session=session))
            price_tasks.append(price_task)            

            attachment_task = asyncio.ensure_future(fetch(URL + 'api/products/attachment/aggregated/' + product_id, session=session))
            attachment_tasks.append(attachment_task)

        stock_responses = asyncio.gather(*stock_tasks)
        price_responses = asyncio.gather(*price_tasks)
        attachment_responses = asyncio.gather(*attachment_tasks)
        all_resp = await asyncio.gather(stock_responses, price_responses, attachment_responses)

    stock_list = [stock for stock in all_resp[0] if stock]
    price_list = [price for price in all_resp[1] if price]
    attachment_list = [att for att in all_resp[2] if att]

    #take all products which have a photo (not null)
    products_jpgs = [{PRODUCT_CODE: att[PRODUCT_CODE], 'tile_url': att['tile_url']} for att in attachment_list if att['tile_url']]
    photo_tasks = []

    async with ClientSession(#headers={'Token': client_headers['Token']}
        ) as session:
        for photo in products_jpgs:
            # photo_task = asyncio.ensure_future(fetch_bytes(URL + 'api/product/attachment/image/' + photo['file_name'], session, photo[PRODUCT_CODE]))
            photo_task = asyncio.ensure_future(fetch_bytes(photo['tile_url'], session, photo[PRODUCT_CODE]))            
            photo_tasks.append(photo_task)

        photo_responses = await asyncio.gather(*photo_tasks)

    photo_list = [photo for photo in photo_responses if photo]

    return (stock_list, price_list, attachment_list, photo_list)




def get_selected_products(product_code_list, token):
    try:
        client_headers = {
                            'Token': token,
                            'Content-Type': 'application/json'
                        }


        #get async all products
        asyncio.set_event_loop(asyncio.new_event_loop()) #setup new loop and use it as active in the next line
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_selected_products_async(product_code_list, client_headers))
        loop.run_until_complete(future)

        product_list = future.result()[0]
        products_ids = future.result()[1]


        #get async all stocks, prices, att, photos
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_selected_product_features_async(products_ids, client_headers))
        loop.run_until_complete(future)

        stock_list = future.result()[0]
        price_list = future.result()[1]
        attachment_list = future.result()[2]
        photo_list = future.result()[3]

        loop.close() #close loop so the memory is released


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



