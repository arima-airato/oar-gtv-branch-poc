"""前処理（Core）。両品目が呼ぶ。"""

from core.io import dicom_reader


HU_WINDOW = (-1024, 3071)


def normalize(volume: "dicom_reader.Volume") -> dict:
    """HU 値を [0, 1] に正規化する（ダミー）。

    HU の窓が実データの範囲より狭く、上下端が飽和していた。
    """
    low, high = HU_WINDOW
    return {"series_uid": volume.series_uid, "range": (low, high), "normalized": True}


def resample(volume: "dicom_reader.Volume", spacing=(1.0, 1.0, 1.0)) -> dict:
    """等方ボクセルにリサンプルする（ダミー）。"""
    return {"series_uid": volume.series_uid, "spacing": spacing}
