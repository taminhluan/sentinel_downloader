# importing the requests library 
import requests
import wget
from clint.textui import progress
import os

url = "https://scihub.copernicus.eu/dhus/api/stub/products?filter=(%20footprint:%22Intersects(POLYGON((105.71566693217734%2020.96060509319706,105.85788794426517%2020.96060509319706,105.85788794426517%2021.075662534958127,105.71566693217734%2021.075662534958127,105.71566693217734%2020.96060509319706)))%22%20)%20AND%20(%20ingestionDate:[2020-01-01T00:00:00.000Z%20TO%202020-06-22T23:59:59.999Z%20]%20)%20AND%20(%20%20(platformname:Sentinel-2))&offset=0&limit=25&sortedby=ingestiondate&order=desc"
cookie = "TWIKISID=9e65104c741a09057f106f97e628bba7; accept_cookies=1; dhusAuth=01013aca5f95094d20292c93371173a3; dhusIntegrity=4d07349e87d7de09c3470fa0b87c925da5d2895e; JSESSIONID=2B24E61A5413E8F6F598AC759B22A389"

# sending get request and saving the response as response object 
r = requests.get(url = url, headers={"cookie": cookie}) 
  
# extracting data in json format 
data = r.json() 

# print data
# print(data)

# print product uuid
for product in data["products"]:
    product_uuid = product["uuid"]
    download_link = f"https://scihub.copernicus.eu/dhus/odata/v1/Products('{product_uuid}')/$value"
    
    print(f"Downloading {product_uuid}")
    
    # Check exist
    if f"{product_uuid}.zip" in os.listdir():
        print(f"Skip file ${product_uuid}.zip")
        continue

    # download
    r = requests.get(url = download_link, headers={"cookie": cookie}, stream=True )
    with open(f'{product_uuid}.zip', 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

    print(f"Download successfully {product_uuid}.zip")
