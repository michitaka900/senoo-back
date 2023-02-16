from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.eBay import get_results, get_details, get_auth_token, get_products
from core.shopify import get_latest_products, find_shopify_products, create_product, update_product, get_ebay_product
import json

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

    try:
        for item in products:
            id_list.append(item['variants'][0]['option1'])
    except:
        pass

    id_chunks = [id_list[i:i + 20] for i in range(0, len(id_list), 20)]
    for arr in id_chunks:
        id_strings = ','.join(arr)
        print(id_strings)
        try:
            items = get_products(id_strings)
            for item in items:
                if item['ListingStatus'] != 'Active':
                    for p in products:
                        ebay_id = p["variants"][0]["option1"]
                        if ebay_id == item['ItemID']:
                            out_of_stock.append(p)
        except:
            pass
    return Response(out_of_stock)


@api_view(['GET'])
def getUserAccessToken(request):
    response = get_auth_token()
    return Response(response.status_code)