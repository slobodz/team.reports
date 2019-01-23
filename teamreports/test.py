import asyncio
from aiohttp import ClientSession
import requests as r

a = []


def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post('https://team-services-uat.herokuapp.com/api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


token = post_token('test@kalorik.pl', 'Krakow123').json()['token']









async def fetch(url, headers, session, prod):
    async with session.get(url, params=headers) as response:
        print(response.status)
        a = await response.read()
        return (prod, a)


async def test1(token, images):

    images = [('CM1006POD-KALORIK', 'CM1006POD-KALORIK.jpg'), ('AC2F14.0-IN', 'AC2F14.0-IN.jpg')]
    url = 'https://team-services-uat.herokuapp.com/api/product/attachment/image/'

    headers = {'Token':token}

    tasks = []

    async with ClientSession() as session:
        for image in images:
            task = asyncio.ensure_future(fetch(url + image[1], headers, session, image[0]))
            tasks.append(task)
        a = await asyncio.gather(*tasks)

    return a


loop = asyncio.get_event_loop()
test = asyncio.ensure_future(test1(token))
loop.run_until_complete(test)





print(test)
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(token))
# loop.run_until_complete(future)

# future.result().__len__()
