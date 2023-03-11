import requests
from bs4 import BeautifulSoup

def url_next_page(soup, url_main):
    """Проверка на наличие следующей страницы."""
    pagination = soup.find('div', class_='pagination').find_all('li')[-1]
    if pagination.find('a').get('class') == ['arrow']:
        return url_main + pagination.find('a').get('href')


def get_one_scrap(url, headers):
    """Парсинг одной страницы."""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    start_position = 1
    table_rows = soup.find('table', class_='problems').find_all('tr')[start_position:]
    url_main = url.split('/problemset')[0]
    one_scrap = []
    for table_row in table_rows:
        data = []
        row_cells = table_row.find_all('td')
        number = row_cells[0].find('a').text.strip()
        href = url_main + row_cells[0].find('a').get('href')
        data.append(number)
        data.append(href)
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
    is_url_next_page = url_next_page(soup, url_main)
    return one_scrap, is_url_next_page


def scrap(url, headers):
    """Парсинг всех страниц."""
    is_url_next_page = url
    while is_url_next_page:
        one_scrap, is_url_next_page = get_one_scrap(is_url_next_page, headers)
        print(one_scrap[0], sep='\n')


def main():
    url = 'https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC'
    headers = {
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    scrap(url, headers)


if __name__=='__main__':
    main()
