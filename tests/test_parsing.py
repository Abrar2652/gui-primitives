"""Coordinate parsing must be robust across model output formats and spaces."""
from guiprim.inference.parsing import parse_coordinate

WH = (1000, 800)


def test_click_format_pixel():
    assert parse_coordinate("click(320, 240)", WH, "pixel") == (320, 240)


def test_xy_keyed_format():
    assert parse_coordinate("x=100, y=200", WH, "pixel") == (100, 200)


def test_json_format():
    assert parse_coordinate('{"x": 50, "y": 60}', WH, "pixel") == (50, 60)


def test_bracket_format():
    assert parse_coordinate("the point is [12, 34]", WH, "pixel") == (12, 34)


def test_norm_1_space_scales_to_pixels():
    x, y = parse_coordinate("click(0.5, 0.5)", WH, "norm_1")
    assert (round(x), round(y)) == (500, 400)


def test_norm_1000_space_scales_to_pixels():
    x, y = parse_coordinate("click(500, 400)", WH, "norm_1000")
    assert (round(x), round(y)) == (500, 320)


def test_pixel_space_guard_rescales_unit_values():
    # A model told to use pixels but emitting [0,1] values is rescaled.
    x, y = parse_coordinate("click(0.25, 0.75)", WH, "pixel")
    assert (round(x), round(y)) == (250, 600)


def test_clamps_out_of_bounds():
    x, y = parse_coordinate("click(5000, 9000)", WH, "pixel")
    assert x == WH[0] and y == WH[1]


def test_returns_none_when_no_coordinate():
    assert parse_coordinate("I cannot find it.", WH, "pixel") is None
    assert parse_coordinate("", WH, "pixel") is None


def test_os_atlas_bbox_returns_center_norm_1000():
    # OS-Atlas-style output: <|box_start|>(x1,y1),(x2,y2)<|box_end|>.
    # In norm_1000, image is 1000x800; box center (500,400) -> pixel (500, 320).
    out = "<|object_ref_start|>save<|object_ref_end|><|box_start|>(400,300),(600,500)<|box_end|>"
    x, y = parse_coordinate(out, WH, "norm_1000")
    assert (round(x), round(y)) == (500, 320)


def test_os_atlas_bbox_preferred_over_generic_paren():
    # The generic (x,y) regex would match the FIRST tuple (400,300) — top-left.
    # The bbox pattern must win, returning the center instead.
    out = "<|box_start|>(400,300),(600,500)<|box_end|>"
    x, y = parse_coordinate(out, (1000, 1000), "norm_1000")
    assert (round(x), round(y)) == (500, 400)
