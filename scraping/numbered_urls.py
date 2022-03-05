import re
import csv

with open('restaurant_urls3.csv') as f:
    urls = [next(f) for _ in range(1050)]

urls_to_fix = []
for url in urls:
    if re.search(r'-\d+$', url):
        urls_to_fix.append(url.strip())

nf = open('urls_to_fix.csv', 'w')
with nf:
    write = csv.writer(nf)
    for url in urls_to_fix:
        write.writerow([url])