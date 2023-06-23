from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

URL = "https://precollege.usc.edu/online-programs/"
root = requests.get(URL, headers = {'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(root.text, 'html.parser')

urls = []
container = soup.find('div', attrs = {'class', 'entry-content'})
for link in container.find_all('a'):
    l = link.get('href')
    urls.append(l)

USC_programs = []
names = []
tuitions = []
app_fee = []
descriptions = []
eligibility = []
dates = []
app_date = []

for url in urls[1:]:
    each_program = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
    program_soup = BeautifulSoup(each_program.text, 'html.parser')
    program_name = program_soup.find('h1').text
    names.append(program_name)
    
    program_summary= program_soup.find('div', {'class', 'summary'})
    program_summary_list = program_summary.find_all('p')
    program_tuition = program_summary_list[len(program_summary_list)-1]
    program_tuition_str = str(program_tuition)
    num = re.findall('\d+', program_tuition_str)
    
    app_fee.append(num[2])
    tuitions.append(num[1])

    program_summary_list2 = program_summary.select('p')
    program_start_date = program_summary_list2[0].text
    program_eligibility = program_summary_list2[len(program_summary_list)-2].text
    eligibility.append(program_eligibility)
    dates.append(program_start_date)

    program_overview = program_soup.find("section", {"class" : "fc__program"})
    program_content = program_overview.find('div', {'class' : 'content'})
    program_description = ''
    
    for p in program_content.select('p:not(:has(*))'):
        if 'Upon completing' not in p.text:
            program_description += p.text
            program_description += " "
    descriptions.append(program_description)

    program_app_date_str = ''
    for i in program_soup.find_all('td', attrs={'class' : 'column-2'}):
        program_app_date_str += i.text + '; '


    app_date.append(program_app_date_str)

    USC_programs.append([program_name, program_description, num[2], program_app_date_str, num[1], program_start_date, program_eligibility, url])

df = pd.DataFrame(USC_programs, columns=['course_title', 'course_description', 'app_fee', 'app_date', 'tuition', 'start_date', 'eligibility_requirements', 'link'])  
df.to_csv('USC_Programs.csv')


