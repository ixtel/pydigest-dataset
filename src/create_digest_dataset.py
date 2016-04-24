# -*- encoding: utf-8 -*-

import csv
import json
import os

from langid import classify
from lxml.etree import XMLSyntaxError
from readability import Document
from readability.readability import Unparseable

DATASET_POSITIVE_KEYWORDS = list({
    'blog',
    'article',
    'news-item',
    'section',
    'content',
    'body-content',
    'hentry',
    'entry-content',
    'page-content',
    'readme',
    'markdown-body entry-content',
    'maia-col-6',
    'maia-col-10',
    'col-md-9',
    'col-md-12',
    'maia-article',
    'col-md-6',
    'post_show',
    'content html_format',
    'watch-description-content',
    'watch-description',
    'watch-description-text',
    'article-content',
    'post',
    'container',
    'summary',
    'articleBody',
    'article hentry',
    'article-content',
    'entry-content',
    'viewitem-content',
    'main',
    'post',
    'post-content',
    'section-content',
    'articleBody',
    'section',
    'document',
    'rst-content',
    'markdown-content',
    'wy-nav-content',
    'toc',
    'book',
    'col-md-12',

})

DATASET_NEGATIVE_KEYWORDS = list({
    "mysidebar",
    "related",
    "ads",
    'footer',
    'menu',
    'navigation',
    'navbar',
    '404',
    'error 404',
    'error: 404',
    'page not found',
    'file-wrap',
    'navbar',
})


def main():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'links.csv'))

    all_links = []
    with open(csv_path, 'r') as fio:
        reader = csv.DictReader(fio)
        all_links = [row for row in reader]

    info = {
        'links': [],
    }
    for i, link in enumerate(all_links):
        if i % 100 == 0:
            print("%s of %s" % (i, len(all_links)))

        if not os.path.exists(link['path']):
            continue

        with open(link['path'], 'r') as fio:
            text = fio.read()
        try:
            article = Document(text,
                               min_text_length=50,
                               positive_keywords=','.join(DATASET_POSITIVE_KEYWORDS),
                               negative_keywords=','.join(DATASET_NEGATIVE_KEYWORDS)
                               ).summary()
            language = classify(article)[0]
            language = 'ru' if language == 'ru' else 'en'
        except (Unparseable, XMLSyntaxError):
            article = text
            language = 'en'

        type_link = 'library' if 'github.com' in link['link'] else 'article'
        info['links'].append({
            'link': link['link'],
            'data': {
                'language': language,
                'title': link['title'],
                'description': link['description'],
                'article': text,
                'type': type_link,
            }
        })

    with open('output.json', 'w') as fio:
        json.dump(info, fio)


if __name__ == '__main__':
    main()
