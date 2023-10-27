from ..app import utils, main


def test_note2xy_0():
    x, y = utils.note2xy(11)
    assert x == 0
    assert y == 7


def test_note2xy_1():
    x, y = utils.note2xy(81)
    assert x == 0
    assert y == 0


def test_volume_to_buttons(mocker):
    mocker.patch("app.main.Main.update_column")
    mocker.patch("app.utils.get_volume", 0.42)
    app = main.Main()
    vtb = app.volume_to_buttons()
    assert type(vtb) == list
