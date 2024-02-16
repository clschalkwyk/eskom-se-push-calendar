import requests
from dotenv import load_dotenv
import os
from tabulate import tabulate
# Load config vars
load_dotenv()

# load env and setup headers for autnentication
LICENSE_KEY=os.getenv('LICENSE_KEY')
LOCATION_OUTFILE='locations_found.json'

headers={
    'token': LICENSE_KEY
}

# Find your location ID on EskomSePush
def search_location(name):
    url =f"https://developer.sepush.co.za/business/2.0/areas_search?text={name}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(LOCATION_OUTFILE, 'w') as fp:
            fp.write(res.text)
            print('Locations Found:')
            try:
                tbl_headers = ['Region', 'Name', 'Id']
                found = []
                locations = res.json()['areas']
                for location in locations:
                    found.append([
                        location.get('region', ''),
                        location.get('name', ''),
                        location.get('id', ''),
                    ])

                print(tabulate(found, headers=tbl_headers, tablefmt='grid'))

            except Exception as e:
                print(f"Unable to list locations found:{e}")


# bearing in mind the rate limiting, dont run this too much
if __name__ == '__main__':
    search_text = input('Please enter your nearest location to search for:')
    search_location(search_text)
