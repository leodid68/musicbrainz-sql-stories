import csv
from pathlib import Path

import plotly.graph_objects as go


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "top-duplicated-names.csv"
PNG_PATH = PROJECT_ROOT / "charts" / "top-duplicated-names.png"
HTML_PATH = PROJECT_ROOT / "charts" / "top-duplicated-names.html"


def load_rows(path: Path = DATA_PATH) -> list[dict[str, str | int]]:
    with path.open(newline="", encoding="utf-8") as source:
        raw_rows = list(csv.DictReader(source))

    return [
        {
            "name": row["name"],
            "artist_entities": int(row["artist_entities"]),
            "distinct_types": int(row["distinct_types"]),
            "distinct_areas": int(row["distinct_areas"]),
        }
        for row in raw_rows
    ]


def build_figure(rows: list[dict[str, str | int]]) -> go.Figure:
    ordered = list(reversed(rows))
    customdata = [
        [row["distinct_types"], row["distinct_areas"]]
        for row in ordered
    ]

    figure = go.Figure(
        go.Bar(
            x=[row["artist_entities"] for row in ordered],
            y=[row["name"] for row in ordered],
            orientation="h",
            marker={
                "color": [
                    "#78A99F" if row["name"] != "Indigo" else "#E0784F"
                    for row in ordered
                ],
                "line": {"width": 0},
            },
            text=[f'{row["artist_entities"]:,}' for row in ordered],
            textposition="outside",
            cliponaxis=False,
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x:,} artist entities<br>"
                "%{customdata[0]} artist types<br>"
                "%{customdata[1]} non-null areas"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title={
            "text": (
                "<b>One name, many artist entities</b>"
                "<br><sup>Most duplicated exact primary names in MusicBrainz</sup>"
            ),
            "x": 0.055,
            "xanchor": "left",
            "y": 0.95,
        },
        width=1600,
        height=1000,
        paper_bgcolor="#F7F3EA",
        plot_bgcolor="#F7F3EA",
        font={"family": "Arial", "color": "#172A3A", "size": 24},
        margin={"l": 210, "r": 150, "t": 175, "b": 155},
        xaxis={
            "title": {"text": "Number of artist entities", "standoff": 18},
            "range": [0, 275],
            "showgrid": True,
            "gridcolor": "#DAD5CA",
            "gridwidth": 1,
            "zeroline": False,
            "tickfont": {"size": 20},
        },
        yaxis={
            "title": "",
            "tickfont": {"size": 24},
            "showgrid": False,
        },
        showlegend=False,
        bargap=0.28,
        annotations=[
            {
                "text": (
                    "MusicBrainz full export, 2026-07-15<br>"
                    "Exact primary names only. Aliases, [unknown], and "
                    "[no artist] excluded from the ranking."
                ),
                "xref": "paper",
                "yref": "paper",
                "x": 0,
                "y": -0.19,
                "showarrow": False,
                "align": "left",
                "font": {"size": 19, "color": "#48606F"},
            },
            {
                "text": "Indigo = 249 distinct artist entities",
                "xref": "x",
                "yref": "y",
                "x": 249,
                "y": "Indigo",
                "ax": -235,
                "ay": -52,
                "arrowhead": 2,
                "arrowwidth": 2,
                "arrowcolor": "#E0784F",
                "font": {"size": 20, "color": "#A3472C"},
                "bgcolor": "#FFF7F1",
                "bordercolor": "#E0784F",
                "borderpad": 8,
            },
        ],
    )

    return figure


def build_chart(
    png_path: Path = PNG_PATH,
    html_path: Path = HTML_PATH,
) -> tuple[Path, Path]:
    figure = build_figure(load_rows())
    png_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    figure.write_image(png_path, width=1600, height=1000, scale=1)
    figure.write_html(
        html_path,
        include_plotlyjs="cdn",
        full_html=True,
    )
    return png_path, html_path


if __name__ == "__main__":
    build_chart()
