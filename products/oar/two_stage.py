"""OAR の2段階推論（一部変更申請の対象）。

粗い位置決めのあとに、臓器ごとの局所モデルを当てる。
輪郭精度に影響するため軽微変更では通らない。承認が下りるまで
develop には入れない。
"""

from core.segmentation import postprocess
from products.oar import organs

STAGE1_PATCH = (256, 256, 128)
STAGE2_PATCH = (96, 96, 64)


def locate(volume_meta: dict) -> dict:
    """第1段階：臓器のおおよその位置を出す（ダミー）。"""
    return {organ: {"bbox": STAGE1_PATCH} for organ in organs.ORGANS}


def refine(rois: dict) -> dict:
    """第2段階：ROI ごとに局所モデルを当てる（ダミー）。"""
    result = {}
    for organ, roi in rois.items():
        mask = {"label": organ, "patch": STAGE2_PATCH, "roi": roi}
        result[organ] = postprocess.smooth(mask)
    return result


def run(volume_meta: dict) -> dict:
    return refine(locate(volume_meta))
