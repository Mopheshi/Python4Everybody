import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

url = input("Enter url: ")
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all the anchor tags
tags = soup('a')
for tag in tags:
    print(tag.get('href', None))  # Retrieves the link(s) (href) contained in the page
    print(tag.getText('href', None))  # Get all child strings of this PageElement, concatenated using the given separator.
