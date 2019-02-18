import requests as r
import math
from PIL import Image
from io import BytesIO
from teamreports import app_config
import asyncio
from aiohttp import ClientSession

class ApiClient:

    def __init__(self, email, password):
        self.token_call = self.post_token(email, password)
        if self.token_call.ok:
            self.headers_token = {'Token': self.token_call.json()['token']}
            self.headers_contenttype_token = {'Content-Type': 'application/json', 'Token': self.token_call.json()['token']}

    
    def post_token(self, email, password):
        """Send credentials to get token"""

        headers = {"Username": email, "Password": password}
        return r.post(app_config.URL + 'api/auth/', headers=headers)


    def merge_lists_of_dicts(self, list1, list2):
        """Merge dictionaries from list1 with dictionaries with list2 on product_code which is
            common key in all dictionaries. list1 must not be empty"""

        try:
            merged_list = []
            if list1:
                for id_list1, one_dict_list1 in enumerate(list1):
                    is_key_in_list2 = False
                    for id_list2, one_dict_list2 in enumerate(list2):
                        if one_dict_list1['product_code'] == one_dict_list2['product_code']:
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



    async def fetch(self, url, session, headers=None):
        async with session.get(url, params=headers) as response:
            if(response.status == 200):
                return await response.json()
            else:
                print(response)

    async def fetch_bytes(self, url, session, product_code, headers=None):
        async with session.get(url, params=headers) as response:      
            if(response.status == 200):
                photo_bytes = await response.read()
                return {'product_code': product_code, 'image': photo_bytes}
            else:
                print(response)

    async def post_for_product(self, url, session, product_json, headers=None):
        async with session.post(url, json=product_json, params=headers) as response:
            if(response.status == 200):
                return await response.json()
            elif(response.status == 404):
                return product_json
            else:
                print(response)

    def get_all_products(self):
        try:
            #get async all products, stocks, prices and att
            asyncio.set_event_loop(asyncio.new_event_loop()) #setup new loop and use it as active in the next line
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_all_async())
            loop.run_until_complete(future)

            product_list = future.result()['products']
            stock_list = future.result()['stocks']
            price_list = future.result()['prices']
            attachment_list = future.result()['attachments']


            #merge products with stocks
            if not stock_list:
                product_stock_list = product_list
            else:
                product_stock_list = self.merge_lists_of_dicts(product_list, stock_list)


            #merge products+stocks with prices
            if not price_list:
                product_stock_price_list = product_stock_list
            else:        
                product_stock_price_list = self.merge_lists_of_dicts(product_stock_list, price_list)


            #merge products+stocks+prices with metadeta attachment
            if not attachment_list:
                product_stock_price_att_list = product_stock_price_list
            else:        
                product_stock_price_att_list = self.merge_lists_of_dicts(product_stock_price_list, attachment_list)


            #take all products with have a photo (not null)
            product_jpgs = [{'product_code': product['product_code'], 'tile_url': product['tile_url']} for product in product_stock_price_att_list if product['tile_url']]

            #get photos async
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_all_images_async(product_jpgs))
            loop.run_until_complete(future)

            image_list = future.result()

            loop.close()


            #merge products+stocks+prices+att with photos
            product_stock_price_att_image_list = self.merge_lists_of_dicts(product_stock_price_att_list, image_list)
        
            return product_stock_price_att_image_list
        except Exception as e:
            print(e)
            raise



    async def get_all_async(self):
        product_tasks = []
        stock_tasks = []
        price_tasks = []
        attachment_tasks = []

        page_info = r.get(app_config.URL + 'api/products/count', headers=self.headers_contenttype_token).json()
        how_many_pages = math.ceil(page_info['total_count']/page_info['page_size'])

    
        async with ClientSession(headers=self.headers_contenttype_token) as session:
            for page in range(how_many_pages):

                headers = {'Page': page + 1} #pages starts from 1 not 0

                product_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products', headers=headers, session=session))
                product_tasks.append(product_task)
                
                stock_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/stock/aggregated', headers=headers, session=session))
                stock_tasks.append(stock_task)

                price_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/price/aggregated', headers=headers, session=session))
                price_tasks.append(price_task)

                attachment_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/attachment/aggregated', headers=headers, session=session))
                attachment_tasks.append(attachment_task)

            product_responses = asyncio.gather(*product_tasks)
            stock_responses = asyncio.gather(*stock_tasks)
            price_responses = asyncio.gather(*price_tasks)
            attachment_responses = asyncio.gather(*attachment_tasks)
            all_resp = await asyncio.gather(product_responses, stock_responses, price_responses, attachment_responses)

        return  {
                    'products': [product for sublist in all_resp[0] if sublist is not None for product in sublist],
                    'stocks': [stock for sublist in all_resp[1] if sublist is not None for stock in sublist if sublist is not None],
                    'prices': [price for sublist in all_resp[2] if sublist is not None for price in sublist if sublist is not None],
                    'attachments': [attachment for sublist in all_resp[3] if sublist is not None for attachment in sublist if sublist is not None]
                }


    async def get_all_images_async(self, products_jpgs):

        image_tasks = []
        
        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with ClientSession() as session:
            for image in products_jpgs:
                image_task = asyncio.ensure_future(self.fetch_bytes(image['tile_url'], session, image['product_code']))
                image_tasks.append(image_task)

            image_responses = await asyncio.gather(*image_tasks)

        return [image for image in image_responses if image]


    async def get_selected_products_async(self, product_code_list):
        products_ids = []
        product_tasks = []

        async with ClientSession(headers=self.headers_contenttype_token) as session:
            for product_code in product_code_list:
                product_json = {'product_code': product_code}
                product_task = asyncio.ensure_future(self.post_for_product(app_config.URL + 'api/product/search/', session, product_json))
                product_tasks.append(product_task)               

            product_responses = await asyncio.gather(*product_tasks)

        for product in product_responses:
            if 'product_id' in product:
                products_ids.append(str(product['product_id'])) #change id to strings to use it later in url

        return {
                    'products': product_responses,
                    'products_ids': products_ids
            }



    async def get_selected_product_features_async(self, products_ids):
        stock_tasks = []
        price_tasks = []
        attachment_tasks = []


        async with ClientSession(headers=self.headers_contenttype_token) as session:
            for product_id in products_ids:
                stock_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/stock/aggregated/' + product_id, session=session))
                stock_tasks.append(stock_task)

                price_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/price/aggregated/' + product_id, session=session))
                price_tasks.append(price_task)            

                attachment_task = asyncio.ensure_future(self.fetch(app_config.URL + 'api/products/attachment/aggregated/' + product_id, session=session))
                attachment_tasks.append(attachment_task)

            stock_responses = asyncio.gather(*stock_tasks)
            price_responses = asyncio.gather(*price_tasks)
            attachment_responses = asyncio.gather(*attachment_tasks)
            all_resp = await asyncio.gather(stock_responses, price_responses, attachment_responses)

        stock_list = [stock for stock in all_resp[0] if stock]
        price_list = [price for price in all_resp[1] if price]
        attachment_list = [att for att in all_resp[2] if att]

        #take all products which have a image (not null)
        products_jpgs = [{'product_code': att['product_code'], 'tile_url': att['tile_url']} for att in attachment_list if att['tile_url']]
        image_tasks = []

        async with ClientSession() as session:
            for image in products_jpgs:
                image_task = asyncio.ensure_future(self.fetch_bytes(image['tile_url'], session, image['product_code']))            
                image_tasks.append(image_task)

            image_responses = await asyncio.gather(*image_tasks)

        image_list = [image for image in image_responses if image]

        return {
                    'stocks': stock_list,
                    'prices': price_list,
                    'attachments': attachment_list,
                    'images': image_list
            }

    def get_selected_products(self, product_code_list):
        try:

            #get async all products
            asyncio.set_event_loop(asyncio.new_event_loop()) #setup new loop and use it as active in the next line
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_selected_products_async(product_code_list))
            loop.run_until_complete(future)

            product_list = future.result()['products']
            products_ids = future.result()['products_ids']


            #get async all stocks, prices, att, images
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.get_selected_product_features_async(products_ids))
            loop.run_until_complete(future)

            stock_list = future.result()['stocks']
            price_list = future.result()['prices']
            attachment_list = future.result()['attachments']
            image_list = future.result()['images']

            loop.close() #close loop so the memory is released


            #merge products with stocks
            if not stock_list:
                product_stock_list = product_list
            else:
                product_stock_list = self.merge_lists_of_dicts(product_list, stock_list)


            #merge products+stocks with prices
            if not price_list:
                product_stock_price_list = product_stock_list
            else:        
                product_stock_price_list = self.merge_lists_of_dicts(product_stock_list, price_list)


            #merge products+stocks+prices with metadeta attachment
            if not attachment_list:
                product_stock_price_att_list = product_stock_price_list
            else:        
                product_stock_price_att_list = self.merge_lists_of_dicts(product_stock_price_list, attachment_list)


            #merge products+stocks+prices+att with image
            if not image_list:
                product_stock_price_att_image_list = product_stock_price_att_list
            else:        
                product_stock_price_att_image_list = self.merge_lists_of_dicts(product_stock_price_att_list, image_list)            


                            
            return product_stock_price_att_image_list
        except Exception as e:
            print(e)
            raise

