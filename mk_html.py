#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import dominate
from dominate.tags import *
import json

js_str = ''


def print_rows(data_dict_arr=[]):
    """  [ 'Washington', new Date(1789, 3, 30), new Date(1797, 2, 4) ],"""
    rows_str = ''
    for data in data_dict_arr:
        row_str = "['"
        row_str += str(data['pkg']) + "',"
        row_str += str(data['start']) + ','
        row_str += str(data['end']) + '],'
        rows_str += row_str
    return rows_str


def create_html(html_file_path='./timeline_chart.html', json_data=""):
    """
    Create HTML by json_data.
    :param html_file_path: HTML file path
    :param json_data: source data
    :return: None
    """
    doc = dominate.document(title='LogShow')

    with doc.head:
        # 冗余处理，当无法下载时，需要在同目录下放置两个js库文件
        script(src='https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js')
        script(src='scripts/jquery.min.js')
        script(src='https://www.gstatic.com/charts/loader.js')
        script(src='scripts/loader.js')

    # eg = 'creator/echart_gantt.js'
    # egf = get_resource_path(eg)
    # egd = 'creator/echart_gantt_data.js'
    # egdf = get_resource_path(egd)
    # with open(egf, "r+", encoding='UTF-8') as fi, \
    #         open(egdf, "w", encoding='UTF-8') as fo:
    #     old = fi.read()
    #     fo.write("var _rawData = ")
    #     fo.write(get_json_data())
    #     fo.write(";")
    #     fo.write(old)
    # with open(egdf, 'r', encoding='UTF-8') as f:
    #     js = f.read()

    append_js_str("""
    google.charts.load("current", {packages:["timeline","controls"],'language': 'ja'});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
    var dashboard = new google.visualization.Dashboard(
        document.getElementById('dashboard')
    );

    var control = new google.visualization.ControlWrapper({
    controlType: 'ChartRangeFilter',
    containerId: 'control',
    options: {
      filterColumnIndex: 1,
      ui: {
        minRangeSize: (60 * 60 * 1000),
        chartType: 'TimeLine',
        chartOptions: {
          width: '100%',
          height: 70,
          chartArea: {
            width: '90%',
            height: '80%'
          },
          hAxis: {
            baselineColor: 'none'
          }
        },
        chartView: {columns: [1, 2]}
        }
      }
    });

  var chart = new google.visualization.ChartWrapper({
    chartType: 'Timeline',
    containerId: 'chart',
    options: {
      width: '100%',
      height: '100%',
      chartArea: {
        width: '100%',
        height: '80%'
      },
      tooltip: {
        isHtml: true
      }
    },
    view: {
      columns: [0, 1, 2]
    }
  });

    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'pkg' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([""")
    # TODO: get real data and convert to data_dict_arr
    data = {
        'pkg': 'com.baidu',
        'start': ms_str_2_date("200"),
        'end': ms_str_2_date("300"),
    }
    data_dict_arr = [data]
    append_js_str(print_rows(data_dict_arr))
    append_js_str("""]);
    dashboard.bind(control, chart);
    dashboard.draw(dataTable);
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

    # 去掉转义字符串
    doc_str = str(doc)
    doc_str = doc_str.replace('&amp;', '&')
    doc_str = doc_str.replace('&lt;', '<')
    doc_str = doc_str.replace('&gt;', '>')
    doc_str = doc_str.replace('&quot;', '"')

    with open(html_file_path, 'w') as f:
        f.write(doc_str)

    os.startfile(os.path.abspath(html_file_path))


def ms_str_2_date(ms_str):
    """
    Convert timeMs to js Date.
    :param ms_str: timeMs string.
    :return: js Date str.
    """
    return "new Date(%s * 1000)" % ms_str


def append_js_str(js_append):
    global js_str
    js_str += js_append


def get_js_str():
    global js_str
    return js_str


if __name__ == '__main__':
    create_html()
