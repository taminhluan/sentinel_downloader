# importing the requests library 
import requests
import wget
from clint.textui import progress
import os
from config import username, password

# Step 1: Login
session = requests.Session()
login_url = "https://scihub.copernicus.eu/dhus//login"
login_response = session.post(url = login_url, data = { 'login_username': username, 'login_password': password})

# Step 2: Get data
boundary = "107.3309326171875 10.504015637704898,109.017333984375 10.504015637704898,109.017333984375 11.662996112308047,107.3309326171875 11.662996112308047,107.3309326171875 10.504015637704898"
ingestion_date = "2020-01-01T00:00:00.000Z TO 2020-06-22T23:59:59.999Z%20"
offset = 0
limit = 150
url = f"https://scihub.copernicus.eu/dhus/api/stub/products?filter=(%20footprint:%22Intersects(POLYGON(({boundary})))%22%20)%20AND%20(%20ingestionDate:[{ingestion_date}]%20)%20AND%20(%20%20(platformname:Sentinel-2 AND producttype:S2MSI2A))&offset={offset}&limit={limit}&sortedby=ingestiondate&order=desc"
# cookie = "TWIKISID=9e65104c741a09057f106f97e628bba7; accept_cookies=1; dhusAuth=01013aca5f95094d20292c93371173a3; dhusIntegrity=4d07349e87d7de09c3470fa0b87c925da5d2895e; JSESSIONID=2B24E61A5413E8F6F598AC759B22A389"
# sending get request and saving the response as response object 
r = session.get(url = url) 
# extracting data in json format 
data = r.json() 
# print data
print(data)

# print product uuid
for product in data["products"]:
    product_uuid = product["uuid"]
    download_link = f"https://scihub.copernicus.eu/dhus/odata/v1/Products('{product_uuid}')/$value"
    
    print(f"Downloading {product_uuid}")
    folder = '/media/luantm/a7293494-83da-45a8-903f-93d5148f3c5f/sentinel_data'
    # Step 2.1 Check exist
    if f"{product_uuid}.zip" in os.listdir(f"{folder}"):
        print(f"Skip file {product_uuid}.zip")
        continue

    # download
    #   method 1
    # wget.download(download_link, f'{product_uuid}.zip')
    #   method 2
    # os.system(f"wget --http-user={username} --http-password={password} '{download_link}' -O 'data/{product_uuid}.zip'")
    #   method 3
    r = session.get(url = download_link, stream=True )
    
    with open(f'{folder}/{product_uuid}.zip', 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

    print(f"Download successfully {product_uuid}.zip")
