import csv
from pathlib import Path

import plotly.graph_objects as go


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "join-impact.csv"
PNG_PATH = PROJECT_ROOT / "charts" / "name-join-impact.png"
HTML_PATH = PROJECT_ROOT / "charts" / "name-join-impact.html"


def load_metrics(path: Path = DATA_PATH) -> dict[str, int | float]:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    metrics: dict[str, int | float] = {}
    for row in rows:
        value = row["value"]
        metrics[row["metric"]] = (
            float(value)
            if row["metric"] == "row_increase_pct"
            else int(value)
        )
    return metrics


def build_figure(metrics: dict[str, int | float]) -> go.Figure:
    original = int(metrics["original_artist_rows"])
    cross_entity = int(metrics["cross_entity_matches"])
    increase_pct = float(metrics["row_increase_pct"])

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            name="Expected entity rows",
            y=["Original artist table", "After joining on exact name"],
            x=[original, original],
            orientation="h",
            marker={"color": "#78A99F", "line": {"width": 0}},
            text=[f"{original / 1_000_000:.2f}M"] * 2,
            textposition="inside",
            insidetextanchor="middle",
            textfont={"color": "#FFFFFF", "size": 28},
            hovertemplate="%{y}<br>%{x:,} rows<extra></extra>",
        )
    )
    figure.add_trace(
        go.Bar(
            name="Cross-entity matches",
            y=["Original artist table", "After joining on exact name"],
            x=[0, cross_entity],
            orientation="h",
            marker={"color": "#E0784F", "line": {"width": 0}},
            text=["", f"+{cross_entity / 1_000_000:.2f}M"],
            textposition="inside",
            insidetextanchor="middle",
            textfont={"color": "#FFFFFF", "size": 28},
            hovertemplate="%{y}<br>%{x:,} cross-entity matches<extra></extra>",
        )
    )

    figure.update_layout(
        title={
            "text": (
                "<b>A valid JOIN nearly doubled the row count</b>"
                "<br><sup>Exact-name self-join on MusicBrainz artists</sup>"
            ),
            "x": 0.055,
            "xanchor": "left",
            "y": 0.95,
        },
        width=1600,
        height=1000,
        barmode="stack",
        paper_bgcolor="#F7F3EA",
        plot_bgcolor="#F7F3EA",
        font={"family": "Arial", "color": "#172A3A", "size": 24},
        margin={"l": 330, "r": 120, "t": 180, "b": 235},
        xaxis={
            "title": {"text": "Rows returned", "standoff": 20},
            "range": [0, 5_900_000],
            "tickvals": [0, 1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000],
            "ticktext": ["0", "1M", "2M", "3M", "4M", "5M"],
            "showgrid": True,
            "gridcolor": "#DAD5CA",
            "gridwidth": 1,
            "zeroline": False,
            "tickfont": {"size": 21},
        },
        yaxis={
            "title": "",
            "tickfont": {"size": 25},
            "showgrid": False,
            "autorange": "reversed",
        },
        legend={
            "orientation": "h",
            "x": 0,
            "y": -0.14,
            "font": {"size": 21},
            "traceorder": "normal",
        },
        bargap=0.34,
        annotations=[
            {
                "text": f"<b>+{increase_pct:.2f}%</b>",
                "xref": "x",
                "yref": "y",
                "x": original + cross_entity,
                "y": "After joining on exact name",
                "xanchor": "right",
                "yshift": 68,
                "showarrow": False,
                "font": {"size": 34, "color": "#A3472C"},
            },
            {
                "text": (
                    "MusicBrainz full export, 2026-07-15<br>"
                    "Exact primary names only. Aliases, [unknown], and "
                    "[no artist] excluded."
                ),
                "xref": "paper",
                "yref": "paper",
                "x": 0,
                "y": -0.29,
                "showarrow": False,
                "align": "left",
                "font": {"size": 18, "color": "#48606F"},
            },
        ],
    )
    return figure


def build_chart(
    png_path: Path = PNG_PATH,
    html_path: Path = HTML_PATH,
) -> tuple[Path, Path]:
    figure = build_figure(load_metrics())
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
