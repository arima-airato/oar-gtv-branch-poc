"""後処理（Core）。両品目が呼ぶ。"""

SMOOTHING_ITERATIONS = 2
MIN_COMPONENT_VOXELS = 50


def largest_component(mask: dict, min_voxels: int = MIN_COMPONENT_VOXELS) -> dict:
    """最大連結成分だけを残す（ダミー）。

    体積が min_voxels に満たない成分は雑音として捨てる。
    """
    return {**mask, "components": 1, "min_voxels": min_voxels}


def smooth(mask: dict, iterations: int = SMOOTHING_ITERATIONS) -> dict:
    """輪郭を平滑化する（ダミー）。"""
    return {**mask, "smoothed_by": iterations}
