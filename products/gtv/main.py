"""AutoContouring (GTV) のエントリポイント。"""

from core.io import dicom_reader
from core.segmentation import postprocess, preprocess
from products.gtv import tumor


def run(series_path: str) -> dict:
    volume = dicom_reader.read_series(series_path)
    preprocess.normalize(volume)

    result = {}
    for target in tumor.TARGETS:
        mask = {"label": target}
        result[target] = postprocess.smooth(mask)
    return result


if __name__ == "__main__":
    print(run("./dummy"))
