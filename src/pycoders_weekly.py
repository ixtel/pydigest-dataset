# -*- coding: utf-8 -*-
import csv
import glob
import os
import re
from html.parser import HTMLParser
from typing import Dict
from typing import List

from bs4 import BeautifulSoup

from src import get_issue_from_file

ISSUE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'PycodersWeekly'))


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_td_args():
    return [
        ('td', {'class': 'upperBodyContent', 'valign': 'top'}),
        ('td', {'class': 'mcnTextContent', 'valign': 'top',
                'style': "padding-top: 9px;padding-right: 18px;padding-bottom: 9px;"
                         "padding-left: 18px;mso-table-lspace: 0pt;"
                         "mso-table-rspace: 0pt;"
                         "-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"
                         "color: #606060;font-family: Helvetica;font-size: 15px;"
                         "line-height: 150%;text-align: left;"}),
        ('td', {
            'style': 'mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;'}),
        ('table', {
            'style': 'border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;',
            'class': 'mcnTextBlock'})

    ]


def parse_issue(content, link_args=None):
    data_links = []
    body = None
    if link_args is None:
        link_args = {"style": "color: #ED5E29;font-weight: normal;text-decoration: none;"}

    soup = BeautifulSoup(content, "lxml")

    for td_args in reversed(get_td_args()):
        elements = soup.findAll(*td_args)
        if elements is not None:
            for x in elements:
                if len(x.findAll('a', link_args)) > 5:
                    body = x
                    break
    else:
        body = soup

    links = body.findAll('a', link_args)

    miss_links = [
        'http://www.datadoghq.com/?utm_source=pycoders&utm_medium=newsletter&utm_content=sq&utm_campaign=devnewsletters',
        'http://launchbit.com/taz/574-6289-*|EMAIL_UID|*',
        'http://twitter.com/mgrouchy',
        'http://gazarojobs.theresumator.com/apply',
        'https://www.gittip.com/',
        'http://pythonjobshq.com',
        'https://www.neckbeardrepublic.com',
        'http://pycoders.com',

    ]
    # print(len(links), link_args)

    for href in links:
        if not href.has_attr('href'):
            continue
        link = href['href']
        if any([x in link for x in miss_links if x and link]):
            continue
        title = href.text
        try:
            raw_description = str(href.nextSibling.nextSibling).replace('<br/>', '').strip()
            if not raw_description:
                raw_description = str(href.nextSibling.nextSibling.nextSibling).replace('<br/>', '').strip()

            urls = re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              strip_tags(raw_description))
            if urls and urls[0]:
                if '(' in urls[0] and ')' in urls[0]:
                    raw_description = str(href.parent.parent.nextSibling.nextSibling.text)

            description = strip_tags(raw_description).strip().replace('  ', ' ')
            if "Pycoder's Weekly Issue" in description:
                continue

        except AttributeError as e:
            # print(link)
            continue
        else:
            data_links.append({
                'link': link,
                'title': title,
                'description': description
            })

    return data_links


#
#
# def main():
#     pass
#     # map(_get_block_item, _get_blocks)
#
#
#
# def download_issues():
#     path = os.path.join(ISSUE_FOLDER, 'issues.txt')
#     with open(path, 'r') as fio:
#         issues = [x.strip() for x in fio.readlines() if x]
#     for i, issue in enumerate(reversed(issues), start=1):
#         res = requests.get(issue)
#         print(i, issue)
#         issue_path = os.path.join(ISSUE_FOLDER, '%s.html' % i)
#         with open(issue_path, 'w') as fio:
#             fio.write(res.text)
#
#
# download_issues()



def parse_part() -> List[Dict[str, str]]:
    links = []
    folder = ISSUE_FOLDER
    params_link = [
        {"style": "color: #ED5E29;font-weight: normal;text-decoration: none;"},
        {"style": "font-family: Times;font-size: medium;font-weight: bold;color: #ED5E29;text-decoration: none;"},
        {"style": "text-decoration: none;color: #ED5E29;font-weight: normal;"},
        {
            "style": "color: #AAAAAA;font-weight: normal;text-decoration: none;word-wrap: break-word;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"},
    ]
    for x in glob.glob('%s/*.html' % folder):
        for params in params_link:
            issue_links = parse_issue(get_issue_from_file(x), params)
            if len(issue_links) > 5:
                links.extend(issue_links)
                break
    return links


if __name__ == '__main__':

    all_links = parse_part()

    with open('pycodersweekly.csv', 'w') as fio:
        fieldnames = all_links[0].keys()
        writer = csv.DictWriter(fio, fieldnames=fieldnames)
        headers = dict((n, n) for n in fieldnames)
        writer.writerow(headers)
        for x in all_links:
            writer.writerow(x)
