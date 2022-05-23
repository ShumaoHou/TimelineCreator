#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from utils.util import ms_str_2_date

data = {
    "columns": [
        {"type": 'string', "id": 'pkg'},
        {"type": 'string', "id": 'label'},
        {"type": 'string', "role": 'tooltip'},
        {"type": 'date', "id": 'Start'},
        {"type": 'date', "id": 'End'}
    ],
    "rows": [
        {
            'pkg': 'com.test.demo1',
            'label': "null",
            'tooltip': '<img src="https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg" style="width:75px;height:50px"><br/>',
            'start': ms_str_2_date("1652953734"),
            'end': ms_str_2_date("1652963734")
        },
        {
            'pkg': 'com.test.demo2',
            'label': "null",
            'tooltip': '<img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Flag_of_the_United_Kingdom.svg" style="width:75px;height:50px"><br/>',
            'start': ms_str_2_date("1652954734"),
            'end': ms_str_2_date("1652973734")
        },
    ]
}


def create_data_file():
    """
    Create a temporary data.json file to debug.
    Otherwise, you can create a similar file or python dict like this.
    :return:
    """
    with open("data/data.json", "w") as file:
        json.dump(data, file)


if __name__ == '__main__':
    create_data_file()
