from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
import os, requests, base64, json, urllib


API_KEY = os.environ.get('API_KEY')
DEV_ID = os.environ.get('DEV_ID')
CERT_ID = os.environ.get('CERT_ID')
RU_NAME = os.environ.get('RU_NAME')
TOKEN = os.environ.get('TOKEN')


def get_results(query):
    try:
        api = Finding(appid=API_KEY, config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': query})
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def get_details(itemId):
    try:
        token = get_auth_token()
        print(token)
        api = Trading(iaf_token=token, config_file=None)
        response = api.execute('GetItem', {'ItemID': itemId})
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict()['Errors']['ErrorCode'])


def get_auth_code():
    res = requests.get('https://auth.ebay.com/oauth2/authorize?client_id=Yoshiyuk-nestshop-PRD-59c70a856-0aa7c56d&response_type=code&redirect_uri=Yoshiyuki_Matsu-Yoshiyuk-nestsh-zvueewlei&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly')
    return res


def get_auth_token():

    code = "v%5E1.1%23i%5E1%23I%5E3%23p%5E3%23f%5E0%23r%5E1%23t%5EUl41Xzc6REVDMkJBMzA5QTcwMjdFRTU0OTExRjAzMUNFOEQ1QTVfMF8xI0VeMjYw"
    code_decoded = urllib.parse.unquote(code)
    AppSettings = {
        'client_id': API_KEY,
        'client_secret': CERT_ID,
        'ruName': RU_NAME}

    authHeaderData = AppSettings['client_id'] + \
        ':' + AppSettings['client_secret']
    encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))
    encodedAuthHeader = str(encodedAuthHeader)[2:len(str(encodedAuthHeader))-1]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + str(encodedAuthHeader)
    }

    body = {
        "grant_type": "authorization_code",
        "redirect_uri": AppSettings['ruName'],
        "code": code_decoded
    }
    # print(code_decoded)

    data = urllib.parse.urlencode(body)

    tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"

    response = requests.post(tokenURL, headers=headers, data=data)
    return response.json()
