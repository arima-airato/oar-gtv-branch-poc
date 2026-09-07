"""AutoContouring (OAR) のエントリポイント。

このファイルからの import グラフが、OAR の実行ファイルに入る範囲になる。
build/oar.paths の宣言が正しいかどうかを CI がここから検証する。
"""

from core.io import dicom_reader
from core.segmentation import postprocess, preprocess
from products.oar import organs, two_stage


TWO_STAGE = True


def run(series_path: str) -> dict:
    volume = dicom_reader.read_series(series_path)
    preprocess.normalize(volume)
    preprocess.resample(volume)

    if TWO_STAGE:
        return two_stage.run({"series_uid": volume.series_uid})

    result = {}
    for organ in organs.ORGANS:
        mask = {"label": organ}
        mask = postprocess.largest_component(mask)
        result[organ] = postprocess.smooth(mask)
    return result


if __name__ == "__main__":
    print(run("./dummy"))
