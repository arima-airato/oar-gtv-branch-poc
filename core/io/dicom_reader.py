"""DICOM 読み込み（Core）。品目に依存しない共通処理。

PoC 用のダミー実装。実際の画像処理は行わない。
"""

from dataclasses import dataclass


@dataclass
class Volume:
    """3次元ボリューム（ダミー）。"""

    series_uid: str
    spacing: tuple
    shape: tuple


def read_series(path: str) -> Volume:
    """DICOM シリーズを読み込んで Volume を返す。"""
    return Volume(series_uid="1.2.826.0.1.dummy", spacing=(1.0, 1.0, 2.0), shape=(512, 512, 120))
