import ssl
import urllib.request
import xml.etree.ElementTree as ET

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter url: ")
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)

data = uh.read()
tree = ET.fromstring(data)
counts = tree.findall('.//count')
# comments = tree.findall('comments/comment')
total = 0

for count in counts:
    total += int(count.text)

# This approach works fine as well...
# for count in comments:
#     total += int(count.find('count').text)

print(f'Count: {total}')
