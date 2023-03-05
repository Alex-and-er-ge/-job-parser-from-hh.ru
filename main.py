import requests
from bs4 import BeautifulSoup

URL = 'https://hh.ru/search/vacancy'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
KEYWORDS = ['python']

def parse_hh_page(page):
    """Parse a single page of job listings"""
    vacancies = []
    response = requests.get(page, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    vacancy_items = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for item in vacancy_items:
        vacancy = {}
        # Get the vacancy title and link
        title = item.find('a', {'class': 'bloko-link'})
        vacancy['title'] = title.text.strip()
        vacancy['link'] = title['href']
        # Check if the vacancy contains the keywords
        if any(keyword in vacancy['title'].lower() for keyword in KEYWORDS):
            vacancies.append(vacancy)

    return vacancies

def parse_hh(keyword):
    """Parse job listings from hh.ru"""
    vacancies = []
    page = 0
    while True:
        # Construct the URL with search parameters
        params = {'text': keyword, 'page': page}
        response = requests.get(URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Stop parsing if there are no more job listings
        if 'Ничего не найдено' in str(soup):
            break

        # Parse job listings on the page
        vacancies += parse_hh_page(response.url)

        # Move to the next page
        page += 1

    return vacancies

if __name__ == '__main__':
    # Search for job listings with the keyword 'python'
    vacancies = parse_hh('python')
    for vacancy in vacancies:
        print(vacancy['title'], vacancy['link'])
