"""GTV（肉眼的腫瘍体積）の定義。GTV 品目専用。"""

TARGETS = [
    "GTV_primary",
    "GTV_node",
]

# 腫瘍輪郭に付与するマージン（mm）。臨床から過小評価の指摘があり見直した。
MARGIN_MM = 3.0


def with_margin(mask: dict, margin: float = MARGIN_MM) -> dict:
    """輪郭にマージンを付ける（ダミー）。"""
    return {**mask, "margin_mm": margin}
