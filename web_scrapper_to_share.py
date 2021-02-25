"""

Author: Carlos Climent
Created on: 23/02/2021
Last update: 24/02/2021

"""

from bs4 import BeautifulSoup
import requests
import pandas as pd


cookies = {
    # fill this according to this post:
    # https://medium.com/better-programming/web-scraping-behind-authentication-with-python-be5f82eb85f0
}

headers = {
    # fill this according to this post:
    # https://medium.com/better-programming/web-scraping-behind-authentication-with-python-be5f82eb85f0
}


# Create a session object
s = requests.Session()


bu_dict = {
    0: 'Australia',
    1: 'California',
    2: 'Cologne',
    3: 'Essex',
    4: 'Michigan',
    5: 'Midlands',
    6: 'Munich',
    7: 'RoUK',
    8: 'Southern Europe'
}

list_accreditations = ['SME_table',
                       'Expert_table',
                       'Experienced_table',
                       'Proficient_table',
                       'Novice_table']


def get_employees(soup, skill):
    """

    :param soup:
    :param skill:
    :return:

    This function iterates through a skill on the skills matrix and returns a list of lists (nx4 matxix)
    being:
        n: the numbers of persons accredited with the skills, and
        4: the data corresponding to: employee name, business_unit, level of the skill and skill name

    """
    result = []

    #iterate through each skill level
    for accreditation_level in list_accreditations:

        employees_all = soup.find("div", {"id": accreditation_level}).find_all("td")

        accreditation = accreditation_level.replace("_table", "")

        #iterate through each BU
        for i in range(0, len(employees_all)):
            employees_bu = employees_all[i].find_all('a')
            bu = bu_dict[i]
            for j in range(0, len(employees_bu)):
                employee = employees_bu[j].text
                result.append([employee, bu, accreditation, skill])

    return result


def get_skill(soup):
    """
    :param soup:
    :return:

    Given the soup object, this function returns the skill being scrapped
    """

    return soup.find("div", {"class": "col-xs-8"}).text.replace('\n', "")


# Initialize the data frame as an empty data frame with 4 columns
df = pd.DataFrame(columns=[0, 1, 2, 3])


#Iterate through the skills number of skills
for i in range(1, 400):
    response = s.get(f'https://www.qrthehub.co.uk/skillsmatrix/skill/{i}/', headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.content, 'lxml')
    try:
        skill = get_skill(soup)
        results = get_employees(soup, skill)

        df = df.append(results)
    except:
        print(f"Exception on skill {i}")


df.columns = ["employee", "bu", "level", "skill"]

df.to_csv("skills_matrix.csv", index=False)




