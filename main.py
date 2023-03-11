import requests
from bs4 import BeautifulSoup

def url_next_page(markup, url_main):
    """Проверка на наличие следующей страницы."""
    soup = BeautifulSoup(markup, 'lxml')
    pagination = soup.find('div', class_='pagination').find_all('li')[-1]
    if pagination.find('a').get('class') == ['arrow']:
        return url_main + pagination.find('a').get('href')


def get_one_scrap(url, headers):
    """Парсинг одной страницы."""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    start_position = 1
    table_rows = soup.find('table', class_='problems').find_all('tr')[start_position:]
    one_scrap = []
    for table_row in table_rows:
        data = []
        row_cells = table_row.find_all('td')
        data.append(row_cells[0].find('a').text.strip())
        name_tags = row_cells[1].find_all('div')
        name = name_tags[0].find('a').text.strip()
        data.append(name)
        tags = [tag.text.strip() for tag in name_tags[1].find_all('a')]
        data.append(tags)
        complexity = None
        if row_cells[3].find('span'):  
            complexity = row_cells[3].find('span').text.strip()
        data.append(complexity)
        resolved = None
        if row_cells[4].find('a'):
            resolved = row_cells[4].find('a').text.strip()[1:]
        data.append(resolved)
        one_scrap.append(data)
    return one_scrap

def main():
    url = 'https://codeforces.com/problemset/page/86?order=BY_SOLVED_DESC'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    get_one_scrap(url, headers)


if __name__=='__main__':
    main()
