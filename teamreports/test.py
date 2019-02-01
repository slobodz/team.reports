import asyncio
from aiohttp import ClientSession
import aiohttp
import requests as r
import json

a = []


def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post('https://team-services-uat.herokuapp.com/api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


token = post_token('test@kalorik.pl', 'Krakow123').json()['token']





async def post(url, data, headers, session):
    async with session.post(url, data=data, params=headers) as response:
        print(response)
        return await response.json()



# async def fetch(url, headers, session, prod):
#     async with session.get(url, params=headers) as response:
#         print(response.status)
#         a = await response.read()
#         return (prod, a)


async def test2(token):

    products = ['149006-LAGRANGE', 'testestest']
    url = 'https://team-services-uat.herokuapp.com/api/product/search'

    headers = {'Token':token, 'Content-Type': 'application/json'} 

    tasks = []


    async with ClientSession() as session:
        for prod in products:
            data = {'product_code':prod}
            #data = json.dumps(data)

            #task = asyncio.ensure_future(post(url, data, headers, session))
            a = await post(url, data, headers, session)
            #tasks.append(task)
        #a = await asyncio.gather(*tasks)

    return a





# loop = asyncio.get_event_loop()
# test = asyncio.ensure_future(test2(token))
# loop.run_until_complete(test)

test = test2(token)



#print(test)
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(token))
# loop.run_until_complete(future)

# future.result().__len__()
