from bs4 import BeautifulSoup
import requests

url = "https://trychatgpt.ru"

response = requests.get(url)
print(response)