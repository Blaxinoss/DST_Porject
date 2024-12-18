import re
import requests
from bs4 import BeautifulSoup
import json
import os
from app.test import dataNeeded






predicted_dollar_price = dataNeeded if dataNeeded else None

def clean_price(price_str):
    # Remove Arabic text or other non-numeric descriptions
    cleaned_text = re.sub(r'[^\d,.]', '', price_str)
    
    # Replace commas with empty string to unify the format
    cleaned_text = cleaned_text.replace(',', '')
    
    cleaned_text = cleaned_text.rstrip('L.E')  
    
    # Convert to float
    try:
        price_value = float(cleaned_text)
    except ValueError:
        price_value = 0  # Default if conversion fails

    return price_value


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
            
            
            # Clean price to extract numeric value
            cleaned_price = re.sub(r'[^\d]', '', price)
            egp_price = int(cleaned_price) if cleaned_price.isdigit() else 0
            
            # Convert EGP to USD using the predicted dollar price
            usd_price = round(egp_price / predicted_dollar_price, 2) if predicted_dollar_price else "N/A"
            
            results.append({
                "title": title,
                "price_egp": egp_price,
                "price_usd": usd_price,
            })
    
    return results


def scrape_hardware(query):
    url = f'https://hardwaremarket.net/?s={query}&post_type=product'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': 'product-element-bottom'})
    results = []
    
    for prod in products:
        title = prod.find('h3', {'class': 'wd-entities-title'}).text.strip() 
        if query.lower() not in title.lower():
            continue
        priceparent = prod.find('span', {'class': 'woocommerce-Price-amount amount'})
        price = priceparent.find('bdi').text.strip()
        
        # Clean price to extract numeric value
        egp_price = clean_price(price)
        
        # Convert EGP to USD using the predicted dollar price
        usd_price = round(egp_price / predicted_dollar_price, 4) if predicted_dollar_price else "N/A"
        usd_price = round(usd_price*1000,2)
        results.append({
            "title": title,
            "price_egp": egp_price,
            "price_usd": usd_price,
        })
    
    return results


def scrape_kimostore(query):
    url = f'https://kimostore.net/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': 'product-item__info-inner'})
    results = []
    
    for prod in products:
        title = prod.find('a', {'product-item__title text--strong link'}).text.strip()
        price = prod.find('span', {'class': 'price'}).text.strip()
        
        egp_price = clean_price(price)

        
        # Convert EGP to USD using the predicted dollar price
        usd_price = round(egp_price / predicted_dollar_price, 2) if predicted_dollar_price else "N/A"
        
        results.append({
            "title": title,
            "price_egp": egp_price,
            "price_usd": usd_price,
        })
    
    return results