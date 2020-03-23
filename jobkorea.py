import requests

from bs4 import BeautifulSoup

DOMAIN = 'http://www.jobkorea.co.kr'
URL = DOMAIN + '/recruit/joblist?menucode=duty&duty=1000100'


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'tplPagination newVer'})
    links = pagination.find_all('li')
    pages = []
    for link in links:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    titBx = html.find('div', {'class': 'titBx'})
    tplCo = html.find('td', {'class': 'tplCo'})
    p = titBx.find('p', {'class': 'etc'})
    title = titBx.find('a')['title']
    company = tplCo.find('a').string
    location = p.find_all('span', {'class': 'cell'})[2].string
    link = DOMAIN + titBx.find('a')['href']
    return {'title': title,
            'company': company,
            'location': location,
            'link': link}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping JobKorea: Page {page+1}')
        result = requests.get(f'{URL}#anchorGICnt_{page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        tplJobList = soup.find('div', {'class': 'tplJobList'})
        results = tplJobList.find_all('tr', {'class': 'devloopArea'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
