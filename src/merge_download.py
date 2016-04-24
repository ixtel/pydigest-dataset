# -*- encoding: utf-8 -*-
import asyncio
import csv
import glob
import os

from aiohttp import ClientSession


def merge():
    LINKS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'links'))

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'links.csv'))
    all_links = []

    for path in glob.glob('%s/*.csv' % LINKS_FOLDER):
        with open(path, 'r') as fio:
            reader = csv.DictReader(fio)
            for row in reader:
                all_links.append(row)

    seen = set()
    new_l = []
    for d in all_links:
        if d['link'] not in seen:
            seen.add(d['link'])
            new_l.append(d)

    all_links = new_l
    with open(csv_path, 'w') as fio:
        fieldnames = all_links[0].keys()
        writer = csv.DictWriter(fio, fieldnames=fieldnames)
        headers = dict((n, n) for n in fieldnames)
        writer.writerow(headers)
        for x in all_links:
            writer.writerow(x)


async def fetch(url, filepath):
    if not os.path.isfile(filepath):
        async with ClientSession() as session:
            async with session.get(url) as response:
                delay = response.headers.get("DELAY")
                date = response.headers.get("DATE")
                print("{}:{} with delay {}".format(date, response.url, delay))
                content = await response.text()
                with open(filepath, 'w') as fio:
                    fio.write(content)


async def run(loop, urls):
    tasks = []
    sem_cnt = len(urls) / 10
    if sem_cnt < 5:
        sem_cnt = 5
    sem = asyncio.Semaphore(sem_cnt)
    for url in urls:
        task = asyncio.ensure_future(fetch(url['link'], url['path']))
        await sem.acquire()
        task.add_done_callback(lambda t: sem.release())
        tasks.append(task)

    responses = asyncio.gather(*tasks)
    await responses


def main():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'digests', 'links.csv'))

    urls = []
    with open(path, 'r') as fio:
        with open(path, 'r') as fio:
            reader = csv.DictReader(fio)
            for i, row in enumerate(reader):
                row['path'] = '/home/warmonger/Develop/Packages/pages/%s.html' % i
                urls.append(row)
    #
    # with open(path, 'w') as fio:
    #     fieldnames = urls[0].keys()
    #     writer = csv.DictWriter(fio, fieldnames=fieldnames)
    #     headers = dict((n, n) for n in fieldnames)
    #     writer.writerow(headers)
    #     for x in urls:
    #         writer.writerow(x)

    # urls = urls[:5]

    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(run(loop, urls))
    loop.run_until_complete(future)


if __name__ == '__main__':
    main()
