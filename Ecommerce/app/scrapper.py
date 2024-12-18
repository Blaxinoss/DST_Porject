import re
import requests
from bs4 import BeautifulSoup

def scrape_sigma(query):
    url = f"https://sigma-computer.com/search?search={query}&submit_search=&route=product%2Fsearch"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': 'product-layout col-lg-15 col-md-4 col-sm-6 col-xs-12'})
    results = []
    
    for product in products:
        title_element = product.find('a', {'title': True})
        price_element = product.find('span', {'class': 'price-new'})
        
        if title_element and price_element:
            title = title_element['title']
            price = price_element.text.strip()
            # Use regex to extract numbers only
            cleaned_price = re.sub(r'[^\d]', '', price)
            
            results.append({
                "title": title,
                "price": cleaned_price,
            })
    
    return results



def scrape_hardware(query):
    url = f'https://hardwaremarket.net/?s={query}&post_type=product'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    products = soup.find_all('div', {'class': 'product-element-bottom'})
    results = []
    
    for prod in products:
        title = prod.find('h3',{'class':'wd-entities-title'}).text.strip() 
        if query.lower() not in title.lower():
                continue
        priceparent = prod.find('span',{'class':'woocommerce-Price-amount amount'})
        price = priceparent.find('bdi').text.strip()

        
        results.append({
                "title": title,
                "price": price,
            })
    
    return results




def scrape_kimostore(query):
    url = f'https://kimostore.net/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    products = soup.find_all('div', {'class': 'product-item__info-inner'})
    results = []
    
    for prod in products:
        title = prod.find('a',{'product-item__title text--strong link'}).text.strip() 
        price = prod.find('span',{'class':'price'}).text.strip().replace('/\w+/ig','')
        
        results.append({
                "title": title,
                "price": price,
            })
    
    return results

