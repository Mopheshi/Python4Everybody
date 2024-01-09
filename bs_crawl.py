import ssl
import urllib.request

from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def crawl(url, count, position):
    names = list()

    while count > 0:
        # Fetching the HTML content from the given URL
        html = urllib.request.urlopen(url, context=ctx).read()
        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Finding all anchor tags in the parsed HTML
        tags = soup('a')
        # Selecting the tag based on the given position
        tag = tags[int(position)]

        # Fetching the href attribute from the selected tag
        tag.get('href', None)
        # Appending the content of the selected tag to the names list
        names.append(tag.contents[0])
        # Displaying the retrieved href attribute
        print(f"Retrieving: {tag.get('href', None)}")

        # Updating the URL to the next linked page
        url = tag.get('href', None)

        count -= 1

    return names[-1]  # returning the last element of the list "names"


url = input("Enter url: ")
count = int(input("Enter count: "))
position = input("Enter position: ")

print()

name = crawl(url, count, position)
print()
print(f"Name is {name}")
