from aiohttp import ClientSession
import requests as r

def post_token(email, password):
    """Send credentials to get token"""
    try:
        headers = {"Username": email, "Password": password}
        return r.post('https://team-services-uat.herokuapp.com/api/auth/', headers=headers)
    except r.exceptions.ConnectionError as e:
        return 'Cannot connect to the server'


token = post_token('test@kalorik.pl', 'Krakow123').json()['token']



# def a(token):

#     url = 'https://team-services-uat.herokuapp.com/api/product/search/'
#     payload = {'product_code': '149006-LAGRANGE'}


#     async with ClientSession() as session:
#         async with session.post(url, data=payload) as resp:
#             params = await resp.json()



# a(token)
        
#     # async with session.get('https://api.weibo.com/2/users/show.json', params=params) as resp:
#     #     info = await resp.json()
#     # o = await Oauth.find('weibo-' + info['idstr'])
#     # if not o:
#     #     return 'redirect:/bootstrap/register?oid=weibo-%s&name=%s&image=%s' % (info['idstr'], info['name'], info['avatar_large'])
#     # user = await User.find(o.user_id)
#     # if not user:
#     #     return 'oauth user was deleted.'
#     # return user.signin(web.HTTPFound('/'))




def oauth2(code):
    url = 'https://api.weibo.com/oauth2/access_token'
    payload = {
        'client_id': '366603916',
        'client_secret': 'b418efbd77094585d0a7f9ccac98a706',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://www.qiangtaoli.com'
    }
    with ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            params = await resp.json()
        async with session.get('https://api.weibo.com/2/users/show.json', params=params) as resp:
            info = await resp.json()
        o = await Oauth.find('weibo-' + info['idstr'])
        if not o:
            return 'redirect:/bootstrap/register?oid=weibo-%s&name=%s&image=%s' % (info['idstr'], info['name'], info['avatar_large'])
        user = await User.find(o.user_id)
        if not user:
            return 'oauth user was deleted.'
        return user.signin(web.HTTPFound('/'))


oauth2('test')