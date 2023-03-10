import requests
from bs4 import BeautifulSoup


def get_one_scrap(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    start_position = 1
    table_rows = soup.find('table', class_='problems').find_all('tr')[start_position:]
    one_scrap = []
    for table_row in table_rows:
        row_cells = table_row.find_all('td')
        data = []
        data.append(row_cells[0].find('a').text.strip())
        name_tags = row_cells[1].find_all('div')
        name = name_tags[0].find('a').text.strip()
        tags = [tag.text.strip() for tag in name_tags[1].find_all('a')]
        data.append(name)
        data.append(tags)
        data.append(row_cells[3].find('span').text.strip())
        data.append(row_cells[4].find('a').text.strip()[1:])
        one_scrap.append(data)
    return one_scrap

def main():
    url = 'https://codeforces.com/problemset?order=BY_SOLVED_DESC'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    print(*get_one_scrap(url, headers), sep='\n')


if __name__=='__main__':
    main()
