# -*- encoding: utf-8 -*-


def get_issue_from_file(file_path):
    with open(file_path, 'r') as fio:
        return fio.read()