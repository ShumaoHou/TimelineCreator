#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import dominate
from dominate.tags import *

DEBUG = True
js_str = ''


def parse_json_data_file(json_data_file):
    with open(json_data_file) as f:
        return json.load(f)


def parse_json_data_str(json_data_str):
    return json.loads(json_data_str)


def print_groups(arr_groups_dict):
    """
    It will print like this:

    // create groups
    var groups = new vis.DataSet(
    [
      { id: 1, content: "Truck&nbsp;1" },
      { id: 2, content: "Truck&nbsp;2" },
      { id: 3, content: "Truck&nbsp;3" },
      { id: 4, content: "Truck&nbsp;4" },
    ]
    );
    """
    groups_str = """
    // create groups
    var groups = new vis.DataSet(
    """
    groups_str += json.dumps(arr_groups_dict)
    groups_str += """
    );
    """
    if DEBUG:
        print(groups_str)
    return groups_str


def print_rows(arr_items_dict):
    """
    It will print like this:

    // create items
    var items = new vis.DataSet([
        {
          id: order,
          group: truck,
          start: start,
          end: end,
          content: "Order " + order,
        }
    ]);
    """
    items_str = """
    // create items
    var items = new vis.DataSet(
    """
    items_str += json.dumps(arr_items_dict)
    items_str += """
    );
    """
    if DEBUG:
        print(items_str)
    return items_str.replace('"<<<', '').replace('>>>"', '')


def print_chart_options(colors):
    """Print Options provided to the visualization."""
    res = "var options = {"
    res += "timeline: { },"
    res += "tooltip: {isHtml: true},"
    if len(colors) > 0:
        color_string = ""
        for i in range(len(colors)):
            color_string += "'" + colors[i] + "',"
            pass
        res += "colors: [%s]" % color_string
    res += "};"
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
        # double download
        script(src='https://unpkg.com/vis-timeline/standalone/umd/vis-timeline-graph2d.min.js',
               type="text/javascript")
        script(src='scripts/vis-timeline-graph2d.min.js', type="text/javascript")
        link(href='https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css',
             rel="stylesheet", type="text/css")
        link(href='scripts/vis-timeline-graph2d.min.css',
             rel="stylesheet", type="text/css")
        pass
    json_data = parse_json_data_file(json_data_file)

    append_js_str(print_groups(json_data['groups']))
    append_js_str(print_rows(json_data['items']))
    append_js_str("""
    // specify options
    var options = {
      stack: true,
      editable: false,
      margin: {
        item: 10, // minimal margin between items
        axis: 5, // minimal margin between items and the axis
      },
      orientation: "top",
    };

    // create a Timeline
    var container = document.getElementById("visualization");
    timeline = new vis.Timeline(container, null, options);
    timeline.setGroups(groups);
    timeline.setItems(items);
    
    window.addEventListener("resize", () => {
      /*timeline.checkResize();*/
    });
    """)

    with doc:
        with h1("Timeline"):
            attr(style='width: 100%;')
        with div():
            attr(id='visualization', style='width: 100%; height: 98vh;')
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


if __name__ == '__main__':
    if DEBUG:
        create_html()
    # main(sys.argv)
