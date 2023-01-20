from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from core.eBay import get_results, get_details, get_auth_token, get_auth_code
from .serializers import ProductSerializer, ImageSerializer
from .models import Product, Image



@api_view(['GET'])
def getProductData(request):
    products = Product.objects.filter(status='active')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getEbayItems(request):
    qs = request.GET.get('q', '')
    if qs:
        data = get_results(qs)
        return Response(data)
    else:
        pass

@api_view(['GET'])
def getUserAccessToken(request):
    response = get_auth_token()
    print(response)
    return Response(response)
    # response['access_token'] #access keys as required
    # response['error_description'] #if errors


@api_view(['GET'])
def getEbaySpecificItem(request):
    itemId = request.GET.get('id', '')
    # response = get_auth_token()
    # token = response['access_token']
    if itemId:
        data = get_details(itemId)
        return Response(data)
    else:
        pass

@api_view(['GET'])
def updateDB(request):
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    BASE_URL = os.environ.get('SHOPIFY_BASE_URL')
    fields = ['id', 'handle', 'created_at', 'updated_at',
              'status', 'variants', 'image', 'images']
    url = f'{BASE_URL}/products.json?limit=250&fields={",".join(fields)}'
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}

    has_next_page = True
    iter = 0
    while has_next_page:
        iter += 1
        print(iter)
        r = requests.get(url, headers=headers)
        products = r.json()['products']
        for item in products:
            p = Product(
                id=item['id'],
                handle=item['handle'],
                created_at=item['created_at'],
                updated_at=item['updated_at'],
                status=item['status'],
                price=item['variants'][0]['price'],
                sku=item['variants'][0]['sku'],
                inventory_item_id=item['variants'][0]['inventory_item_id']
            )
            p.save()

            images = item['images']
            for image in images:
                i = Image(
                    id=image['id'],
                    src=image['src'],
                    position=image['position'],
                    width=image['width'],
                    height=image['height'],
                    product=p
                )
                i.save()
        if iter == 1:
            url = r.headers['Link'].replace('<','').split('>')[0]
        else:
            try:
                url = r.headers['Link'].split(', <')[1].split('>')[0]
            except:
                has_next_page = False
    return Response({})
