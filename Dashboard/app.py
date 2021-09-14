import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

def generate_gender(ds):
    gender = ds["gender"]
    proportion_gender = ds["proportion_gender"]
    fig = px.bar(ds, x=gender, y=proportion_gender, title="Gender distribution", color=gender, labels={'proportion_gender':'Percentage', 'gender': 'Gender'}, color_discrete_sequence=px.colors.qualitative.G10)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return dcc.Graph(
        id="gender",
        figure=fig,
    )


def generate_age(ds):
    age = ds["age"]
    fig = px.histogram(ds, x=age, range_x=[0, 100], color="gender", title="Age distribution")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return dcc.Graph(
        id="age",
        figure=fig,
    )

def generate_pie(ds):
    totd_count = ds["time_of_the_day"].value_counts().to_frame().reset_index()
    totd_count = totd_count.rename(columns={"index": "Moment_of_the_day"})
    fig = px.pie(totd_count, values="time_of_the_day", names="Moment_of_the_day", title="Time of the day")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return dcc.Graph(
        id="totd",
        figure=fig,
    )

def generate_device(ds):
    device_count = ds["device_used"].value_counts().to_frame().reset_index()
    device_count = device_count.rename(columns={"index": "Device_used"})
    fig = px.pie(device_count, values="device_used", names="Device_used", title="Device used")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    return dcc.Graph(
        id="device",
        figure=fig,
    )

def generate_bar_chart(ds, x, y, title, labels, colors_prop):
    fig = px.bar(
        ds,
        x=x,
        y=y,
        title=title,
        labels=labels,
        color=colors_prop
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        coloraxis_showscale=False
    )
    return dcc.Graph(
        id=title,
        figure=fig,
    )

#Load csv with Pandas
ds = pd.read_csv("dataset_salto.csv")
ds_gender = pd.read_csv("dataset_gender.csv")

ds_profile_type = pd.read_csv("dataset_profile_type.csv")
ds_profile_type_jeunesse = pd.read_csv("dataset_profile_type_jeunesse.csv")
ds_tag_genre = pd.read_csv("dataset_tag_genre.csv")
ds_video_format_genre = pd.read_csv("dataset_video_format_genre.csv").fillna("")
ds_program_genre = pd.read_csv("dataset_program_genre.csv")


# External CSS links in an array.
external_stylesheets = [
    {
        "href": "./assets/custom.css",
        "rel": "stylesheet",
    },
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2",
        "crossorigin": "anonymous",
    },
]
external_scripts = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"
]

# Instanciate our web application. This is the big class that will call
# in order to run the server.
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

colors = {
    'background': '#111111',
    'text': '#ffffff'
}

# Here our layout i.e. how our page is going to look.
app.layout = html.Div(children=[    
    html.Div(
        children=[
            html.H3(children="Dashboard SALTO"),
            html.Div(children=html.P(children="Exploratory Data Analysis - Users")),
        ]
    ),
    html.Ul(
        children=[
            html.Li(
                children=html.Button(
                    children="User-based",
                    className="nav-link active",
                    **{ "data-bs-toggle": "pill", "data-bs-target": "#user-based" }
                ),
                className="nav-item"
            ),
            html.Li(
                children=html.Button(
                    children="Content-based",
                    className="nav-link",
                    **{ "data-bs-toggle": "pill", "data-bs-target": "#content-based" }
                ),
                className="nav-item"
            )
        ],
        className="nav nav-pills mb-3"
    ),

    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=generate_gender(ds_gender),
                                className="col-6"
                            ),

                            html.Div(
                                children=generate_age(ds),
                                className="col-6"
                            ),
                        ],
                        className="row"
                    ),

                    html.Div(
                        children=[
                            html.Div(
                                children=generate_pie(ds),
                                className="col-6"
                            ),

                            html.Div(
                                children=generate_device(ds),
                                className="col-6"
                            ),
                        ],
                        className="row"
                    ),
                ],
                className="tab-pane fade show active",
                id="user-based"
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=generate_bar_chart(
                                    ds_profile_type,
                                    ds_profile_type.profile_type,
                                    ds_profile_type.session_count,
                                    "Nombre de sessions par type de profil",
                                    {'session_count':'Sessions', 'profile_type': 'Type de profile'}, 
                                    ds_profile_type.index
                                ),
                                className="col-6"
                            ),
                            html.Div(
                                children=generate_bar_chart(
                                    ds_profile_type_jeunesse,
                                    ds_profile_type_jeunesse.profile_type,
                                    ds_profile_type_jeunesse.session_count,
                                    "Nombre de sessions / programmes jeunesse par type de profile",
                                    {'session_count':'Sessions', 'profile_type': 'Type de profil'},
                                    ds_profile_type_jeunesse.index
                                ),
                                className="col-6"
                            ),
                        ],
                        className="row"
                    ),
                    html.Div(
                        children=html.Div(
                            children=generate_bar_chart(
                                ds_video_format_genre,
                                ds_video_format_genre.video_format,
                                ds_video_format_genre.session_count,
                                "Nombre de sessions par format de vidéo et par genre",
                                {'session_count':'Sessions', 'tag_genre': 'Genre'},
                                ds_video_format_genre.tag_genre
                            ),
                            className="col"
                        ),
                        className="row"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=generate_bar_chart(
                                    ds_tag_genre,
                                    ds_tag_genre.tag_genre,
                                    ds_tag_genre.session_count,
                                    "Nombre de sessions par genre de programme",
                                    {'session_count':'Sessions', 'tag_genre': 'Genre'}, 
                                    ds_tag_genre.index
                                ),
                                className="col-6"
                            ),
                            html.Div(
                                children=generate_bar_chart(
                                    ds_program_genre,
                                    ds_program_genre.tag_genre,
                                    ds_program_genre.title,
                                    "Nombre de programmes par genre",
                                    {'session_count':'Sessions', 'tag_genre': 'Genre'}, 
                                    ds_program_genre.tag_genre
                                ),
                                className="col-6"
                            ),
                        ],
                        className="row"
                    ),
                ],
                className="tab-pane fade",
                id="content-based"
            ),
        ],
        className="tab-content"
    ),

], className="container-fluid")

if __name__ == "__main__":
    # Run the server!
    app.run_server(debug=True)
