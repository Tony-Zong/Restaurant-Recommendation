import csv


def clean_urls(csv_file):
    urls = set()
    with open(csv_file, 'r') as f:
        for url in csv.reader(f):
            if '?' and 'http' not in url:
                urls.add(url[0])
    return urls

def csv(urls, destination):
    csv_write = open(destination, 'w')
    writer = csv.writer(csv_write)
        for url in urls:
            write.writerow([url])
