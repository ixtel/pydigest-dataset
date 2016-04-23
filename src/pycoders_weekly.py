# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import requests

ISSUE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'PycodersWeekly'))


# def _get_content(url: str) -> str:
#     try:
#         result = urlopen(url, timeout=10).read()
#     except URLError:
#         return ''
#     else:
#         return result
#
#
# def _get_blocks(content) -> list:
#     result = []
#     if content:
#         try:
#             page = html.parse(content)
#             result = page.getroot().find_class('bodyTable')[0].xpath('//span[@style="font-size:14px"]')
#         except OSError:
#             page = BeautifulSoup(content, 'lxml')
#             result = page.findAll('table', {'class': 'bodyTable'})[0].findAll('span', {'style': "font-size:14px"})
#     return result
#
#
# def _get_block_item(block) -> dict:
#     if isinstance(block, Tag):
#         link = block.findAll('a')[0]
#         url = link['href']
#         title = link.string
#         try:
#             text = str(block.nextSibling.nextSibling).replace('<br/>', '').strip()
#         except AttributeError:
#             return {}
#     else:
#         link = block.cssselect('a')[0]
#         url = link.attrib['href']
#         title = link.text
#         _text = block.getnext()
#         if _text is None:
#             return {}
#         text = etree.tostring(block.getnext()).decode('utf-8').replace('<br/>', '').strip()
#
#     return {
#         'title': title,
#         'link': url,
#         'raw_content': text,
#         'http_code': 200,
#         'content': text,
#         'description': text,
#         'language': 'en',
#     }
#
#
# def main():
#     pass
#     # map(_get_block_item, _get_blocks)
#


def download_issues():
    path = os.path.join(ISSUE_FOLDER, 'issues.txt')
    with open(path, 'r') as fio:
        issues = [x.strip() for x in fio.readlines() if x]
    for i, issue in enumerate(reversed(issues), start=1):
        res = requests.get(issue)
        print(i, issue)
        issue_path = os.path.join(ISSUE_FOLDER, '%s.html' % i)
        with open(issue_path, 'w') as fio:
            fio.write(res.text)


download_issues()
