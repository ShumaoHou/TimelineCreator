#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys

import dominate
from dominate.tags import *

DEBUG = True
js_str = ''


def parse_json_data_file(json_data_file):
    with open(json_data_file) as f:
        return json.load(f)


def parse_json_data_str(json_data_str):
    return json.loads(json_data_str)


def print_columns(data_table='dataTable', column_dict_arr=None):
    """
    It will print like this:

    dataTable.addColumn(
    { type: 'string', id: 'pkg' }
    );
    :param data_table:
    :param column_dict_arr:
    :return:
    """
    if column_dict_arr is None:
        column_dict_arr = []
    columns_str = ''
    for column in column_dict_arr:
        row_str = data_table + ".addColumn({"
        for key, value in column.items():
            row_str += key + ":'" + value + "',"
            pass
        row_str = row_str[:-1]
        row_str += "});"
        columns_str += row_str
    if DEBUG:
        print(columns_str)
    return columns_str


def print_rows(data_dict_arr=None):
    """
    It will print like this:

    [ 'Washington', 'fine', new Date(1789, 3, 30), new Date(1797, 2, 4) ],
    """
    if data_dict_arr is None:
        data_dict_arr = []
    rows_str = ''
    for data in data_dict_arr:
        row_str = "["
        row_str += "'" + str(data['pkg']) + "',"
        row_str += "'" + str(data['label']) + "',"
        row_str += "'" + str(data['tooltip']) + "',"
        row_str += str(data['start']) + ','
        row_str += str(data['end']) + '],'
        rows_str += row_str
    if DEBUG:
        print(rows_str)
    return rows_str


def print_chart_options(colors):
    """Print Options provided to the visualization."""
    res = "var options = {" \
          "timeline: { colorByRowLabel: true }," \
          "backgroundColor: '#ffd'," \
          "tooltip: {isHtml: true},"
    color_string = ""
    for i in range(len(colors)):
        color_string += "'" + colors[i] + "',"
        pass
    res += "colors: [%s]" \
           "};" % color_string
    return res


def create_html(json_data_file='./data/data.json', dist_html_file='./dist/timeline_chart.html'):
    """
    Create HTML by json_data.
    :param dist_html_file: HTML file path
    :param json_data_file: source data
    :return: None
    """
    doc = dominate.document(title='LogShow')

    with doc.head:
        # 冗余处理，当无法下载时，需要在同目录下放置两个js库文件
        script(src='https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js')
        script(src='scripts/jquery.min.js')
        script(src='https://www.gstatic.com/charts/loader.js')
        script(src='scripts/loader.js')

    append_js_str("""
    google.charts.load("current", {packages:["timeline"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var container = document.getElementById('dashboard');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();
    """)
    append_js_str(print_chart_options(['black', 'gray']))
    json_data = parse_json_data_file(json_data_file)
    append_js_str(print_columns('dataTable', json_data['columns']))
    append_js_str("""dataTable.addRows([""")
    append_js_str(print_rows(json_data['rows']))
    append_js_str("""]);
        chart.draw(dataTable, options);
    }
    """)

    with doc:
        with div():
            attr(id='dashboard', style='width: 100%; height: 98vh;')
            with div():
                attr(id='control', cls='chart', style='width: 100%; height: 10%;')
            with div():
                attr(id='chart', cls='chart', style='width: 100%; height: 90%;')
        with script(get_js_str()):
            attr(type='text/javascript')

    # Delete & string.
    doc_str = str(doc)
    doc_str = doc_str.replace('&amp;', '&')
    doc_str = doc_str.replace('&lt;', '<')
    doc_str = doc_str.replace('&gt;', '>')
    doc_str = doc_str.replace('&quot;', '"')

    with open(dist_html_file, 'w') as f:
        f.write(doc_str)

    os.startfile(os.path.abspath(dist_html_file))


def append_js_str(js_append):
    global js_str
    js_str += js_append


def get_js_str():
    global js_str
    return js_str


def main(argv):
    help_info = "Please enter cmd: python " + argv[0] + " [data file] [html file]"
    try:
        data_file = argv[1]
        html_file = argv[2]
        create_html(data_file, html_file)
    except Exception as e:
        print(help_info)
        print(e)
        if DEBUG:
            create_html()


if __name__ == '__main__':
    main(sys.argv)
