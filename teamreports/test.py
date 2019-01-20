import asyncio
from aiohttp import ClientSession

a = []


async def fetch(url, headers, session):
    async with session.get(url, params=headers) as response:
        return await response.json()

async def run(r):
    url = 'https://team-services-uat.herokuapp.com/api/product'
    headers = {
             "Content-Type": "application/json",
             "Token": 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0Nzg1MTA2NCwiZXhwIjoxNTQ3ODU0NjY0fQ.eyJjb25maXJtIjoyfQ.yY2pHaQWVCxx-3Z2engIny0iVYFhvwzowUjRSCSfar8',
             }


    tasks = []

 # Fetch all responses within one Client session,
 # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
             headers['Page'] = i+1
             task = asyncio.ensure_future(fetch(url, headers, session))
             tasks.append(task)
    
        responses = await asyncio.gather(*tasks)
    return [product for sublist in responses for product in sublist]
 #lista.extend(responses)
 #return responses
    
     #print(responses)
     # you now have all response bodies in this variable



loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(21))
loop.run_until_complete(future)

future.result().__len__()
