import re

fh = open("files/actual.txt", "r")
number = numbers = []

for line in fh:
    number.extend(re.findall('[0-9]+', line))
    numbers = [int(num) for num in number]

print(sum(numbers))
