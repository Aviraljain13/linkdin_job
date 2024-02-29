from bs4 import BeautifulSoup
import requests
import json

# f_JT = job type full time for multiple add C before every job type
# f_E = job experience 1,2,3,4 indexes for each job experience
# location = geo location

def start(job_name,loc,job_type,job_exp,page_num,job_loc,gen):
    
    j_loc=''
    gene=''
    # job location
    if job_loc!='' and job_loc!=None:
        if 'rem' in job_loc.lower():
            j_loc+='2,'
        if 'site' in job_loc.lower():
            j_loc+='1,'
        if 'hybrid' in job_loc.lower():
            j_loc+='3,'
        if j_loc[-1][0]==',':
            u_job_loc=j_loc[:-1]+''
            j_loc=u_job_loc
            print(j_loc)
    # when generated
    if gen!='' and gen!=None:
        if '24' in gen.lower():
            gene='r86400'
        if 'past week' in gen.lower():
            gene='r604800'
        if 'past month' in gen.lower():
            gene='r2592000,'
        
    # job type
    type=''
    if job_type!=None:
        if 'full' in job_type.lower():
            type+='F,'
        if 'part' in job_type.lower():
            type+='P,'
        if 'contract' in job_type.lower():
            type+='C,'
        if 'temp' in job_type.lower():
            type+='T,'
        if 'volunteer' in job_type.lower():
            type+='V'
        if type[:-1]==',':
            u_type=type[:-1]+''
            type=u_type
    # job exp
    exp=''
    if job_exp!=None:
        if 'intern' in job_exp.lower():
            exp+='1,'
        if 'entry' in job_exp.lower():
            exp+='2,'
        if 'associate' in job_exp.lower():
            exp+='3,'
        if 'mid senior' in job_exp.lower():
            exp+='4,'
        if 'director' in job_exp.lower():
            exp+='5'
        if exp[:-1]==',':
            u_exp=exp[:-1]+''
            exp=u_exp
    
    if page_num==None:
        page_num=0
    if page_num/5==(page_num//5):
        url=requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_name}&location={loc}&trk=public_jobs_jobs-search-bar_search-submi&f_TPR={gene}&f_JT={type}&f_E={exp}&f_WT={j_loc}&start={str(25*(page_num//5))}', headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'})
    else:
        url=requests.get(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_name}&location={loc}&trk=public_jobs_jobs-search-bar_search-submi&f_TPR={gene}&f_JT={type}&f_E={exp}&&f_WT={j_loc}&start={str(25*((page_num-1)//5))}', headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'})
    
    print(get_job(url))
    return get_job(url)


def job_data(loc,page):
    a=''
    if 'spain' in loc.lower():
        url=requests.get(f'https://www.infojobs.net/webapp/offers/search?keyword=&segmentId=&page={str(page)}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&sinceDate=_24_HOURS', headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'})
        a=json.loads(url.text)
    elif 'italy' in loc.lower():
        url=requests.get(f'https://www.infojobs.net/webapp/offers/search?keyword=&segmentId=&page={str(page)}&sortBy=PUBLICATION_DATE&onlyForeignCountry=false&sinceDate=_24_HOURS', headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'})
        a=json.loads(url.text)
    if a =='' or a==None:
        return None
    else:
        return a['offers']



def get_job(url):
    job_data=[]
    if url.status_code==200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(url.text, 'html.parser')
        div=soup.find_all('div',class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        for i in div:
            job={    
            'job_title':i.find('h3',class_='base-search-card__title').text.strip(), 
            'url':i.find('a')['href'],
            'company':i.find('a',class_='hidden-nested-link').text.strip(),
            'when_generated':i.find('time').text.strip(),
            'location':i.find('span',class_='job-search-card__location').text.strip(),
            'image':i.find('img')['data-delayed-url'].replace('amp;','')
            }
            job_data.append(job)
        print(len(job_data))
        return job_data
    else:
        return None