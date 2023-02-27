from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
import os
import requests
import base64
import json
import urllib
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
DEV_ID = os.getenv('DEV_ID')
CERT_ID = os.getenv('CERT_ID')
RU_NAME = os.getenv('RU_NAME')
TOKEN = os.getenv('TOKEN')


def get_results(query):
    try:
        api = Finding(appid=API_KEY, config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': query})
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

def get_seller_items():
    try:
        api = Finding(appid=API_KEY, config_file=None)
        response = api.execute('findItemsAdvanced', {'sellerid': 'ace-collection'})
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def get_details(itemId):
    try:
        token = get_auth_token()
        api = Trading(appid=API_KEY, devid=DEV_ID, certid=CERT_ID,
                      iaf_token=token, config_file=None)
        response = api.execute('GetItem', {'ItemID': itemId})
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict()['Errors']['ErrorCode'])


def get_products(itemIds):
    try:
        token = get_auth_token()
        url = f'https://open.api.ebay.com/shopping?callname=GetMultipleItems&responseencoding=JSON&siteid=0&version=1119&includeselector=details&ItemID={itemIds}'
        headers = {
            "X-EBAY-API-IAF-TOKEN": token
        }
        response = requests.get(url, headers=headers)
        return response.json()['Item']

    except requests.exceptions.HTTPError as e:
        print (e.response.text)

def get_auth_code():
    res = requests.get('https://auth.ebay.com/oauth2/authorize?client_id=Yoshiyuk-nestshop-PRD-59c70a856-0aa7c56d&response_type=code&redirect_uri=Yoshiyuki_Matsu-Yoshiyuk-nestsh-zvueewlei&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly')
    return res


def get_auth_token():
    now = time.time()
    access_token = ""
    with open('./core/token.json', "r") as f:
        token_data = json.load(f)

    if token_data['expires_at'] > now:
        access_token = token_data['access_token']
    else:
        authHeaderData = API_KEY + ':' + CERT_ID
        encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))
        encodedAuthHeader = str(encodedAuthHeader)[
            2:len(str(encodedAuthHeader))-1]
        with open('./core/credentials.json', "r") as f:
            token_data = json.load(f)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encodedAuthHeader)
        }
        body = {
            "grant_type": "refresh_token",
            "refresh_token": token_data['refresh_token'],
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        data = urllib.parse.urlencode(body)
        tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"
        response = requests.post(tokenURL, headers=headers, data=data)
        access_token = response.json()['access_token']
        expires_at = now + 7150
        dict = {"access_token": access_token, "expires_at": expires_at}
        json_object = json.dumps(dict, indent=4)
        with open('./core/token.json', "w") as f:
            f.write(json_object)

    return access_token

# def get_auth_code():
#     now = time.time()
#     access_token = ""
#     token = open('/app/core/token.json', "w")
#     if token['expires_at'] > now:
#         access_token = token['access_token']
#     else:

#     code_decoded = urllib.parse.unquote(code)
#     AppSettings = {
#         'client_id': API_KEY,
#         'client_secret': CERT_ID,
#         'ruName': RU_NAME}

#     authHeaderData = AppSettings['client_id'] + \
#         ':' + AppSettings['client_secret']
#     encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))
#     encodedAuthHeader = str(encodedAuthHeader)[2:len(str(encodedAuthHeader))-1]

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": "Basic " + str(encodedAuthHeader)
#     }

#     body = {
#         "grant_type": "authorization_code",
#         "redirect_uri": AppSettings['ruName'],
#         "code": code_decoded
#     }
#     # print(code_decoded)

#     data = urllib.parse.urlencode(body)

#     tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"

#     response = requests.post(tokenURL, headers=headers, data=data)
#     return response.json()
