# TimelineCreator
This is a Creator for Timeline or Gantt by Python.

## Getting Started

#### CMD run this:

```shell
python mk_data.py
python mk_html.py
start  ./dist/timeline_chart.html
```

## How to create a Timeline HTML with your data:

**mk_data.py** can create a temporary **data.json** file to debug.

Otherwise, you can create a similar file or python dict like that.

Your data should like this:

```python
data = {
    "columns": [
        {"type": 'string', "id": 'pkg'},
        {"type": 'date', "id": 'Start'},
        {"type": 'date', "id": 'End'}
    ],
    "rows": [
        {
            'pkg': 'com.test.demo1',
            'start': ms_str_2_date("1652953734"),
            'end': ms_str_2_date("1652963734")
        },
        {
            'pkg': 'com.test.demo2',
            'start': ms_str_2_date("1652962734"),
            'end': ms_str_2_date("1652973734")
        },
    ]
}
```