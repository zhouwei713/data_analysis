# -*- coding: UTF-8 -*-

import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('bytedance_jobs.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H4(children='字节跳动招聘信息分析'),
        # html.Div(
        #     [
        #     html.Label('过滤城市'),
        #     dcc.Input(id='City1', value='', type='text'),
        #         ]
        # ),
        html.Div(
            [
                html.Div([
                    dcc.Dropdown(
                            id='recruit-type',
                            options=[{'label': i, 'value': i} for i in ['社招', '日常实习生']],
                            value='社招'
                        ),
                ], style={'width': '100px', 'float': 'left'}),
                html.Div([
                    dcc.Dropdown(
                            id='job-type',
                            options=[{'label': i, 'value': i} for i in ['研发', '产品', '运营', '设计', '市场', '职能']],
                            value='研发'
                        ),
                ], style={'width': '100px', 'float': 'left'}),
                html.Div(
                            [
                            dcc.Input(id='City', value='', type='text', placeholder='城市'),
                                ]
                        ),
                # style={'width': '10%', 'float': 'left', 'display': 'inline'}
            ]
        ),
        dash_table.DataTable(
            id='table-id',
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=20,
            # data=df.to_dict('records'),
            style_table={'height': '300px', 'overflowY': 'auto'},
            fixed_rows={'headers': True},
            # style_header={
            #         'overflow': 'hidden',
            #         'textOverflow': 'ellipsis',
            #         'maxWidth': 0,
            #     },
            # filter_query=''
            # style_cell={
            #         'minWidth': 95, 'maxWidth': 95, 'width': 95
            #     }
        ),
        html.Div(
            [],
            style={'height': '50px'}
        ),
        html.Div(
            id='graph-container',
            className="",
            style={'float': 'center'},
        )
    ]
)


@app.callback(
    Output('table-id', 'data'),
    Input('City', 'value'),
    Input('recruit-type', 'value'),
    Input('job-type', 'value')
)
def update_input(city_value, recruit_value, jobtype_value):
    if all([city_value, recruit_value, jobtype_value]):
        df_new = df[(df['city_info'] == city_value) & (df['recruit_type'] == recruit_value) & (
            df['job_category'].str.contains(jobtype_value))]
        return df_new.to_dict('records')
    elif all([city_value, recruit_value]):
        df_new = df[(df['city_info'] == city_value) & (df['recruit_type'] == recruit_value)]
        return df_new.to_dict('records')
    elif all([recruit_value, jobtype_value]):
        df_new = df[(df['recruit_type'] == recruit_value) & (
            df['job_category'].str.contains(jobtype_value))]
        return df_new.to_dict('records')
    elif all([city_value, jobtype_value]):
        df_new = df[(df['city_info'] == city_value) & (
            df['job_category'].str.contains(jobtype_value))]
        return df_new.to_dict('records')
    elif city_value:
        df_new = df[df['city_info'] == city_value]
        return df_new.to_dict('records')
    elif recruit_value:
        df_new = df[df['recruit_type'] == recruit_value]
        return df_new.to_dict('records')
    elif jobtype_value:
        df_new = df[df['job_category'] == jobtype_value]
        return df_new.to_dict('records')
    else:
        return df.to_dict('records')


@app.callback(
    Output('graph-container', "children"),
    Input('table-id', "data"))
def update_graph(rows):
    dff = pd.DataFrame(rows)
    if rows:
        return html.Div(
            [
                dcc.Graph(
                    id='job_category',
                    # id=column,
                    figure={
                        "data": [
                            {
                                # "x": dff["city_info"],
                                "x": dff['city_info'].value_counts().index.tolist()[:20],
                                "y": dff['city_info'].value_counts().values.tolist()[:20],
                                # "y": dff[column] if column in dff else [],
                                "type": "bar",
                                "marker": {"color": "#0074D9"},
                            }
                        ],
                        "layout": {
                            "xaxis": {"automargin": True},
                            "yaxis": {"automargin": True},
                            "height": 250,
                            "margin": {"t": 10, "l": 10, "r": 10}
                        },
                    },
                )
                # for column in ["job_category", "lifeExp", "gdpPercap"]
            ]
        )
    else:
        return


if __name__ == '__main__':
    app.run_server(debug=True)
