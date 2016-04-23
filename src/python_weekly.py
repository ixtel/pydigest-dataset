# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from urllib.error import URLError
# from urllib.request import urlopen
#
# import lxml.html as html
# from bs4 import BeautifulSoup
# from bs4.element import Tag
# from lxml import etree
#
#
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
