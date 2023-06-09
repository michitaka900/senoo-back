from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.eBay import get_results, get_details, get_auth_token, get_products, get_seller_items
from core.shopify import get_latest_products, find_shopify_products, create_product, update_product, get_ebay_product
from dotenv import load_dotenv
import os, requests

load_dotenv()

@api_view(['GET'])
def getProductData(request):
    data = get_latest_products()
    return Response(data)


@api_view(['GET'])
def findShopifyItems(request):
    qs = request.GET.get('vendor', '')
    if qs:
        data = find_shopify_products(qs)
        return Response(data)
    else:
        pass


@api_view(['GET'])
def getEbayItems(request):
    qs = request.GET.get('q', '')
    if qs:
        data = get_results(qs)
        return Response(data)
    else:
        pass


@api_view(['GET'])
def getEbaySpecificItem(request):
    itemId = request.GET.get('id', '')
    if itemId:
        data = get_details(itemId)
        return Response(data)
    else:
        pass


@api_view(['POST'])
def createShopifyProduct(request):
    data = request.data
    response = create_product(data)

    return Response(response.status_code)


@api_view(['PUT'])
def updateInventory(request):
    data = request.data
    response = update_product(data)

    return Response(response.status_code)


@api_view(['GET'])
def checkInventory(request):
    out_of_stock = []
    id_list = []
    products = get_ebay_product()
    for item in products:
        try:
            if item['variants'][0]['barcode']:
                id_list.append(item['variants'][0]['barcode'].split(',')[0])
        except:
            pass
    id_chunks = [id_list[i:i + 20] for i in range(0, len(id_list), 20)]
    for arr in id_chunks:
        id_strings = ','.join(arr)
        try:
            items = get_products(id_strings)
            for item in items:
                if item['ListingStatus'] == 'Active':
                    for p in products:
                        if p["variants"][0]["barcode"]:
                            ebay_id = p["variants"][0]["barcode"].split(',')[0]
                            if ebay_id == item['ItemID']:
                                out_of_stock.append(p)
        except:
            pass
    return Response(out_of_stock)


@api_view(['GET'])
def getUserAccessToken(request):
    response = get_auth_token()
    return Response(response.status_code)


@api_view(['GET'])
def getSellerItems(request):
    response = get_seller_items()
    return Response(response)

@api_view(['POST'])
def login_user(request):
    data = request.data.get("data", None)
    print(data)
    if check_credentials(data):
        return Response({"token": "UcT6Y2LgZXWy5ks8YTtE"})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def check_credentials(data):
    LOGIN_ID = os.environ.get('LOGIN_ID')
    LOGIN_PW = os.environ.get('LOGIN_PW')
    if data['id'] == LOGIN_ID and data['pw'] == LOGIN_PW:
        return True
    else:
        return False

@api_view(['GET'])
def get_exchange_rate(request):
    qs = request.GET.get('code', '')
    res = requests.get(f'https://api.exchangerate.host/latest?base=JPY&symbols={qs}')
    rate = res.json()["rates"]
    return Response({"data": rate})