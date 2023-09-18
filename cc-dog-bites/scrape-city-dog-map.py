import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.chicagoparkdistrict.com/parks-facilities/dog-friendly-areas'

# send HTTP GET request to the URL
response = requests.get(url)

# check if request was successful
if response.status_code == 200:

    # parse HTML content using beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the section containing addresses
    address_spans = soup.find_all('span', class_='address-line1')

    # retrieve address text between spans
    address_list = [span.get_text() for span in address_spans]

    print(address_list)

    # find the secion containing zip codes
    zipcode_spans = soup.find_all('span', class_='postal-code')

    # retrieve zipcode text between spans
    zipcode_list = [span.get_text() for span in zipcode_spans]

    print(zipcode_list)

    # find section containing name of dog park
    name_links = soup.select("a[href*='parks-facilities']")

    # retrieve name href text
    name_list = [link.get_text() for link in name_links]

    print(name_list)

print(len(name_list))
print(len(address_list))
print(len(zipcode_list))

# clean up names list - manually
remove_list = ['Parks', 'Find a Park', 'Capital Projects', 'Park Renamings', 'Facilities', 'Facility Types',
               'Find a Facility', 'Pools', 'All Other Facilities', 'Parks & Facilities', '\n', 'Filter', ' Schedules']

clean_names_list = [i for i in name_list if i not in remove_list]

print(len(clean_names_list))
print(len(address_list))
print(len(zipcode_list))

# put it in a dict
dog_map_dict = {'dog_area_name': clean_names_list,
                'address': address_list,
                'zipcode': zipcode_list}

# put it into a pandas df and export as csv
df = pd.DataFrame(dog_map_dict)
df.to_csv('scraped_city_dog_map.csv')

# add city and state and format for census batch geocoder -- > geocode --> spotcheck --> put in flourish map!
