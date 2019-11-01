from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# Webpage we're scraping
base_url = "https://hattiesburg.craigslist.org/search/sss?query=cars&sort=rel"

# Send get http request
page = requests.get(base_url)


if page.status_code == requests.codes.ok:

    # Get the whole page.
  bs = BeautifulSoup(page.text, 'lxml')

# Get all listings on this page
listings = bs.find('div', class_='content').find('ul', class_='rows').find_all('li')

# Hold the data
data = {
        'Name': [],
        'Price': [],
        'Date': [],
        }


# 
for listing in listings:

  name = listing.find('a', class_='result-title hdrlnk').text
  if name:
    data['Name'].append(name)
  else:
    data['Name'].append('none')

  price = listing.find('span', class_='result-price').text
  if price:
    data['Price'].append(price)
  else:
    data['Price'].append('none')

  date = listing.find('time', class_='result-date').text
  if date:
    data['Date'].append(date)
  else:
    data['Date'].append('none')



# Store data to csv with pandas
df = pd.DataFrame(data, columns=['Name','Price','Date']) # taking in a dict or multi dimensional array. dict keys match with columns param

# change the range from 0-9, to 1-10. df.index is a range
df.index = df.index + 1
print(df)
df.to_csv('craigslist_cars_file.csv', sep=',', index=False, encoding='utf-8')

