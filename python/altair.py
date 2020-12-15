"""Themes and snippets for altair: https://github.com/altair-viz/altair."""
import altair as alt


def material():
    """Material theme for altair.

    Based on material design's data visualization guidance.
    https://material.io/design/communication/data-visualization.html
    """
    mark_color = "#6300EE"
    grid_color = "#E0E0E0"
    default_font = "Roboto, Helvetica, Arial, sans-serif"
    background = "#FFFFFF"
    text_color = "#757575"
    tick_color = grid_color
    title_color = "#424242"
    tick_width = 2
    gradient_color = ["#e1bee7", "#ba68c8", "#9c27b0", "#7b1fa2", "#4a148c"]
    return {
        "config": {
            "mark": {"color": mark_color},
            "point": {"filled": True, "size": 100, "fill": mark_color, "opacity": 0.3},
            "arc": {"fill": mark_color},
            "area": {"stroke": background, "fill": mark_color, "strokeWidth": 3},
            "path": {"stroke": mark_color},
            "rect": {"fill": mark_color},
            "shape": {"stroke": mark_color},
            "symbol": {"stroke": mark_color},
            "circle": {"fill": mark_color, "size": 100, "opacity": 0.3, "filled": True},
            "bar": {"cornerRadiusTopLeft": 5, "cornerRadiusTopRight": 5, "size": 40},
            "background": background,
            "padding": {"top": 10, "right": 10, "bottom": 10, "left": 10},
            "style": {
                "guide-label": {
                    "font": default_font,
                    "fontSize": 12,
                    "fill": text_color,
                    "fontWeight": "Normal",
                },
                "guide-title": {
                    "font": default_font,
                    "fontSize": 12,
                    "fill": text_color,
                    "fontWeight": "Normal",
                },
                "group-title": {
                    "font": default_font,
                    "fontSize": 12,
                    "fill": text_color,
                    "fontWeight": "Normal",
                },
            },
            "title": {
                "font": default_font,
                "fontSize": 20,
                "anchor": "start",
                "color": title_color,
                "align": "left",
                "fontWeight": "Normal",
            },
            "axis": {
                "tickColor": tick_color,
                "gridColor": grid_color,
                "domainColor": tick_color,
                "domainWidth": tick_width,
                "tickWidth": tick_width,
                "labelPadding": 10,
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "ticks": False,
                "labelBaseline": "right",
                "maxExtent": 45,
                "minExtent": 45,
                "titleAlign": "right",
                "titleAngle": 0,
                "titleX": 48.5,
                "titleY": -13,
                "titleAnchor": "end",
                "orient": "right",
            },
            "axisX": {
                "domain": True,
                "grid": False,
                "titlePadding": 10,
                "titleAlign": "left",
                "titleAnchor": "start",
            },
            "range": {
                "category": [
                    "#6300EE",
                    "#00A2AC",
                    "#FF8435",
                    "#FF4193",
                    "#007EEE",
                    "#c1CA33",
                    "#FFC206",
                    "#B00020",
                ],
                "heatmap": gradient_color,
                "diverging": gradient_color,
                "ordinal": gradient_color,
                "ramp": gradient_color,
            },
            "view": {"strokeWidth": 0, "width": 700, "height": 500},
            "legend": {"orient": "bottom"},
        }
    }


alt.themes.register("material", material)
alt.themes.enable("material")

# Encoding codes
"""
| Data Type    | Shorthand Code | Description                       |
| ------------ | -------------- | --------------------------------- |
| quantitative | Q              | a continuous real-valued quantity |
| ordinal      | O              | a discrete ordered quantity       |
| nominal      | N              | a discrete unordered category     |
| temporal     | T              | a time or date value              |
| geojson      | G              | a geographic shape                |
"""
