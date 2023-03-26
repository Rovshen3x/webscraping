import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def scraper():
        url = 'https://www.nautimarket-europe.com/en/Electronic-Instruments-Compasses-Binoculares-Antennae?page='   
        product_data = []
        p = 0
        while(True):
            p = p + 1
            page = requests.get(f"{url}{p}")
            tree = BeautifulSoup(page.content, "html.parser")
            time.sleep(2)
            lis=tree.find("div", class_="main").find("div", class_="products").find('ol').find_all('li')

            for li in range(0,len(lis)):
                tag = lis[li]
                product={}
                
                try:
                    product['link'] = 'https://www.nautimarket-europe.com' + tag.select_one('.name > a').get('href')
                except:
                    product['link'] = ''

                try:
                    product['title'] = tag.select_one('.name > a').text
                except:
                    product['title'] = ''  

                try:
                    product['imageURL'] = tag.find('img').get('src')
                except:
                    product['imageURL'] = ''

                try:
                    product['price'] = tag.select_one('.price span').get('data-design-currency-amount')
                except:
                    product['price'] = ''

                try:
                    product['description'] = tag.select_one('.description').text
                except:
                    product['description'] = ''                
    
                product_data.append(product)
                
            print(f"page_number: {p} | products_count: {len(product_data)}")

            next_page=tree.find("div", class_="paging").findAll(text='Next')
            if not next_page:
                break 
            
        df = pd.DataFrame([t for t in product_data ])
        out_filename = "/Users/mac/Documents/Output_data.csv"
        df.to_csv(out_filename, index=False)

scraper()
