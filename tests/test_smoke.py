"""ダミーの自動テスト。必須チェックの見え方を確認するためのもの。"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from products.gtv import main as gtv_main  # noqa: E402
from products.oar import main as oar_main  # noqa: E402


def test_oar_returns_all_organs():
    result = oar_main.run("./dummy")
    assert len(result) == 5


def test_gtv_returns_all_targets():
    result = gtv_main.run("./dummy")
    assert set(result) == {"GTV_primary", "GTV_node"}
