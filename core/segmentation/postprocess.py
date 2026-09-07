"""後処理（Core）。両品目が呼ぶ。"""

SMOOTHING_ITERATIONS = 3


def largest_component(mask: dict) -> dict:
    """最大連結成分だけを残す（ダミー）。"""
    return {**mask, "components": 1}


def smooth(mask: dict, iterations: int = SMOOTHING_ITERATIONS) -> dict:
    """輪郭を平滑化する（ダミー）。"""
    return {**mask, "smoothed_by": iterations}
