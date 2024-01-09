import xml.etree.ElementTree as ET

data = '''
    <stuff>
        <users>
            <user x='2'>
                <id>001</id>
                <name>Chuck</name>
            </user>
            
            <user x='7'>
                <id>009</id>
                <name>Severance</name>                
            </user>
        </users>
    </stuff>
'''

stuff = ET.fromstring(data)
users = stuff.findall('users/user')
print(f'There are {len(users)} users available.\n')

for user in users:
    print('Name:', user.find('name').text)
    print('ID:', user.find('id').text)
    print('Attribute:', user.get('x'))
    print()
