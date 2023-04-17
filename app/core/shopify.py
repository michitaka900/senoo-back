import datetime, os, io, json, requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BASE_URL = os.getenv('SHOPIFY_BASE_URL')

# os.chdir(r'')
# path = 'images/'

def getPreviousMonth():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=10)
    week_ago = week_ago.strftime('%Y-%m/%d')
    year = int(week_ago.split('-')[0])
    month = int(week_ago.split('-')[1].split('/')[0])
    day = int(week_ago.split('/')[1])
    first_day_of_previous_month = datetime.datetime(
        year, month, day, 0, 0).isoformat() + '+09:00'

    return first_day_of_previous_month

def get_latest_products():
    previous_month = getPreviousMonth()
    fields = ['id', 'title', 'created_at', 'updated_at',
              'status', 'variants', 'image', 'images', 'vendor']
    url = f'{BASE_URL}/products.json?limit=250&fields={",".join(fields)}&created_at_min={previous_month}'
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    r = requests.get(url, headers=headers)
    products = r.json()['products']

    return products


def find_shopify_products(qs):
    vendor = qs
    fields = ['id', 'handle', 'created_at', 'updated_at',
              'status', 'variants', 'image', 'images', 'vendor']
    url = f'{BASE_URL}/products.json?limit=250&fields={",".join(fields)}&vendor={vendor}'
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    r = requests.get(url, headers=headers)
    products = r.json()['products']
    return products


def add_images(id, imgUrl):
    url = f'{BASE_URL}/products/{id}/images.json'
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    payload = {
        "image": {
            "src": imgUrl,

        }
    }
    payload = json.dumps(payload)
    requests.post(url, headers=headers, data=payload)


def create_product(data):
    url = f'{BASE_URL}/products.json'
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    payload = {
        "product": {
            "title": data['title'],
            "body_html": data['description'],
            "vendor": data['vendor'],
            "product_type": "eBay",
            "status": "draft",
            "tags": data["tags"],
            "variants": [{
                "price": data['price'],
                "sku": data['title'],
                "inventory_quantity": data['stocks'],
                'inventory_management': 'shopify',
                "barcode": data['itemId'] + "," + data['itemUrl'],
            }]
        }
    }
    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload)
    inventory_id = response.json()['product']['variants'][0]['inventory_item_id']
    requests.post(url=f'{BASE_URL}/inventory_levels/connect.json', headers=headers,
                  data={"location_id": 58034028696, "inventory_item_id": inventory_id})
    id = response.json()['product']['id']
    for idx, url in enumerate(data['images']):
        img_id = url.split('/z/')[1].split('/$')[0]
        img_url = 'https://i.ebayimg.com/images/g/' + img_id +  '/s-l1600.jpg'
        add_images(id, img_url)
        # download_image(img_url, data['title']+str(idx))
    return response


def update_product(data):
    url = f"{BASE_URL}/products/{data['id']}.json"
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    payload = {
        "product": {
            "id": data['id'],
            'status': data['status'],
            "variants": [{
                "barcode": data['barcode'],
                "sku": data['sku'],
                "price": data['price'],
                'inventory_management': 'shopify',
            }]
        }
    }
    requests.put(url, headers=headers, data=payload)
    url = f"{BASE_URL}/inventory_levels/set.json"
    payload = {
        "location_id": 58034028696,
        "inventory_item_id": data['inventory_id'],
        "available": data['inventory']
    }
    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload)
    return response


def get_ebay_product():
    url = f"{BASE_URL}/products.json?product_type=eBay&status=draft&limit=250&fields=id,title,status,variants,quantity"
    headers = {'Content-Type': 'application/json',
               'X-Shopify-Access-Token': ACCESS_TOKEN}
    has_next = True
    data_list = []

    while has_next:
        response = requests.get(url, headers=headers)
        data = response.json()['products']
        data_list.extend(data)
        try:
            link_header = response.headers['Link']
            if (link_header.find('next') > 0 and link_header.find('previous') > 0):
                url = link_header.split(', <')[1].split('>')[0]
            elif link_header.find('next') > 0:
                url = link_header.replace('<', '').split('>')[0]
            else:
                has_next = False
        except:
            has_next = False
    return data_list


# def download_image(url, file_name):
#     try:
#         image_content = requests.get(url).content
#         image_file = io.BytesIO(image_content)
#         image = Image.open(image_file).convert('RGB')
#         file_path = path + file_name + '.jpg'
#         with open(file_path, "wb") as f:
#             image.save(f, "JPEG")
#     except Exception as e:
#         print('Failed: ', e)
