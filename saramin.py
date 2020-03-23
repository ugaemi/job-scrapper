import requests

from bs4 import BeautifulSoup

PAGE_COUNT = 40
DOMAIN = 'http://www.saramin.co.kr'
URL = DOMAIN + f'/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword=python&loc_mcd=101000&cat_key=40430,40426&recruitSort=relation&recruitPageCount={PAGE_COUNT}&inner_com_type=&company_cd=0,1,2,3,4,5,6,7,9'


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', {'class': 'pagination'})
    links = pagination.find_all('a')
    pages = []
    for link in links:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    area_job = html.find('div', {'class': 'area_job'})
    area_corp = html.find('div', {'class': 'area_corp'})
    job_condition = area_job.find('div', {'class': 'job_condition'})
    locations = job_condition.find_all('a')
    title = area_job.find('a')['title']
    company = area_corp.find('span').string
    location = ' '.join(list(map(lambda x: x.string, locations)))
    link = DOMAIN + area_job.find('a')['href']
    return {'title': title,
            'company': company,
            'location': location,
            'link': link}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping Saramin: Page {page+1}')
        result = requests.get(f'{URL}&recruitPage={page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all('div', {'class': 'item_recruit'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
