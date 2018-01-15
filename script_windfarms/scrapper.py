import csv
import requests
from bs4 import BeautifulSoup

r = requests.post('https://www.thewindpower.net/windfarms_list_en.php', {
    'action': 'submit',
    "pays": 'FR'
})

soup = BeautifulSoup(r.content, "html.parser")
soup.prettify()
links = [
    a['href'] for a in soup.findAll('a', {"class": "lien_standard_tab"})
]
links = [
    'https://www.thewindpower.net/{}'.format(a) for a in links
]

print('{} links to scrap'.format(len(links)))

data = []
for l in links:
    print('Scrapping {}'.format(l))
    r = requests.get(l)
    soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")
    puces = [
        p.getText() for p in soup.findAll('li', {'class': "puce_texte"})
    ]
    retained_elements = [
        x for x in puces if any(word in x for word in [
            'Longitude', 'Latitude', 'Total nominal power', 'Wind farm name'
        ])
    ]
    content = {}
    for element in retained_elements:
        key, value = element.split(':')
        content[key] = value

    data.append(content)
    print('Scrapping done')

with open('database.csv', 'w', encoding='utf-8') as f:
    dict_writer = csv.DictWriter(f, data[0].keys(), delimiter =';')
    dict_writer.writeheader()
    dict_writer.writerows(data)
