# -*- encoding: utf-8 -*-
import csv
import glob
import os
import shutil
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from src import get_issue_from_file

ISSUE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'ImportPython'))


def getlist1(list1):
    if type(list1) != list:
        return list1
    return list1[0] if list1 else ''


def gen_inbox():
    folder = '/home/warmonger/Downloads/Pythonweekly/importpython.com/newsletter/no'
    new_folder = os.path.join(ISSUE_FOLDER, 'part3')
    for x in glob.glob('%s/*/*.html' % folder):
        try:
            new_path = os.path.join(new_folder, "%s.html" % x.split('/')[-2])
            shutil.copy(x, new_path)
            # parse_issue(get_issue_from_file(x))
        except (TypeError, IndexError, AttributeError) as e:
            print(x, e)
            raise


def parse_issue3(content: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(content, "lxml")
    td_content = soup.find("td", class_="content")
    if td_content is None:
        return []

    read_titles = td_content.find_all("div", class_="subtitle")
    # , attrs={"style": "font-family:Helvetica, Arial, sans-serif;font-size:16px;font-weight:600;color:#2469A0"})
    contents = td_content.find_all("div", class_="body-text", attrs={
        "style": "font-family:Helvetica, Arial, sans-serif;font-size:14px;line-height:20px;text-align:left;color:#333333"})

    data_links = []
    for idx, title in enumerate(read_titles):

        try:
            a_tag = title.find('a')
            link = a_tag['href'] if a_tag['href'] != '' else '#'
            title = a_tag.next.strip()
        except TypeError:
            continue

        try:
            description = contents[idx].next.strip()
        except (IndexError, TypeError) as e:
            description = ''

        data_links.append({
            'link': link,
            'title': title,
            'description': description
        })

    return data_links


def parse_issue1(content: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(content, "lxml")
    body = soup.find_all("table", class_="twelve columns")

    data_links = []
    links = []
    for x in body:
        elements = x.find_all("tr")
        if len(elements) < 2:
            continue

        for y in elements:
            _link = y.find('a')
            description = y.find('p')
            if description:
                description = " ".join(description.text.strip().split())
                link = _link['href']
                title = " ".join(_link.text.strip().split())

                if link not in links:
                    data_links.append({
                        'link': link,
                        'title': title,
                        'description': description
                    })
                    links.append(link)

    return data_links


def parse_part3() -> List[Dict[str, str]]:
    links = []
    folder = os.path.join(ISSUE_FOLDER, 'part3')
    for x in glob.glob('%s/*.html' % folder):
        links.extend(parse_issue3(get_issue_from_file(x)))
    return links


def parse_part2() -> List[Dict[str, str]]:
    links = []
    folder = os.path.join(ISSUE_FOLDER, 'part2')
    for x in glob.glob('%s/*.html' % folder):
        links.extend(parse_issue3(get_issue_from_file(x)))

    for link in links:
        try:
            r = requests.get(link['link'])
            if r:
                link["link"] = r.url
        except requests.exceptions.ConnectionError:
            pass

    return links


def parse_part1():
    links = []
    folder = os.path.join(ISSUE_FOLDER, 'part1')
    for x in glob.glob('%s/*.html' % folder):
        links.extend(parse_issue1(get_issue_from_file(x)))
    return links


# def parse_issue2(content):
#     item = fromstring(content).xpath(
#         '//div[@class="[ col-xs-12 col-sm-6 ]"]')[0]
#     title = 'Import Python - %s' % (getlist1(item.xpath('.//h2/a/text()')))
#     title = unescape(title)
#     url = getlist1(item.xpath('.//h2/a/@href'))
#     url = url if url.startswith('http:') else 'http://importpython.com' + url
#     description = tostring(item.xpath('.//div[@class="subtitle"]')[0]).decode('utf-8')
#     description = description.replace('font-size:11px', 'font-size:0.7em').replace('font-size:8px', 'font-size:1em')
#
#
#     print(title)
#
#
# def main():
#     folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'ImportPython'))
#     for x in glob.glob('%s/*.html' % folder):
#         try:
#             parse_issue(get_issue_from_file(x))
#         except (TypeError, IndexError, AttributeError) as e:
#             print(x, e)
#             raise
#
#
# main()

# gen_inbox()
if __name__ == '__main__':

    all_links = []
    all_links.extend(parse_part1())
    all_links.extend(parse_part2())
    all_links.extend(parse_part3())

    with open('import_python.csv', 'w') as fio:
        fieldnames = all_links[0].keys()
        writer = csv.DictWriter(fio, fieldnames=fieldnames)
        headers = dict((n, n) for n in fieldnames)
        writer.writerow(headers)
        for x in all_links:
            writer.writerow(x)
