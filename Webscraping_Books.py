import requests
from bs4 import BeautifulSoup

soup = []
# Gets all 1000 books
try: 
    for number in range(1,50):
        url = f'http://books.toscrape.com/catalogue/page-{number}.html'

        html = requests.get(url).text

        soup.append(BeautifulSoup(html,"html.parser"))
except:
    print("No soup today :( ")

# Gets all 1000 books
book_list = []

try:
    for i in soup:

        # Creates list of each book's html code
        items_list = i.find_all('article')

        for item in items_list:

            # Checks to see if the item is in stock before adding it to the list
            item_contents = item.find('p',attrs = {"class": "instock availability"}).contents
            item_contents_clean = item_contents[2].splitlines()
            available = item_contents_clean[2].lstrip()

            if available != 'In stock':
                continue
            else:
                # Create a dictionary to add to the book list if the book is in stock
                book_info = {}
                book_info["title"] = item.find("h3").find("a").attrs["title"]
                book_info["price"] = item.find('p', attrs = {'class': 'price_color'}).text[1:]
                book_info["rating"] = item.find('p').attrs['class'][1]
                book_list.append(book_info)
except:
    print("No soup  today :( ")

print(book_list[0:50])

# Writes a CSV file and saves it to your current working directory
with open('BS4_books_list.csv','wt',encoding='utf-8') as books:
    for i in book_list:
        books.write(str(i)+";")