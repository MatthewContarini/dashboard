from rich.layout import Layout

# Fixed heights and widths
CONTENT_LEFT_WIDTH    = 21
CONTENT_RIGHT_WIDTH   = 20
RIGHT_TOP_HEIGHT      = 12
FOOTER_HEIGHT         = 3

# Left sidebar panel heights
LEFT_PANEL_1_HEIGHT   = 10
LEFT_PANEL_2_HEIGHT   = 25
LEFT_PANEL_3_HEIGHT   = 9
LEFT_PANEL_4_HEIGHT   = 12
# Left sidebar fifth panel will fill remaining space
LEFT_PANEL_5_RATIO    = 1

# middle height
MIDDLE_PANEL_1_HEIGHT = 10
MIDDLE_PANEL_2_RATIO = 1
MIDDLE_PANEL_3_HEIGHT = 5
MIDDLE_PANEL_4_HEIGHT = 15

# middle top height
MIDDLE_PANEL_LEFT_WIDTH = 20
MIDDLE_PANEL_MIDDLE_WIDTH = 20
MIDDLE_PANEL_RIGHT_RATIO = 1


def make_layout() -> Layout:
    """
    Simplified dashboard layout:
    - content area split into left, center, right sidebar
    - left sidebar split into four fixed-height panels plus a ratio panel
    - right sidebar split: top panel fixed height, below panels share remaining space
    - footer fixed height
    """
    layout = Layout()

    # 1) Top: content (expandable), bottom: footer (fixed)
    layout.split_column(
        Layout(name="content", ratio=1),
        Layout(name="footer",  size=FOOTER_HEIGHT),
    )

    # 2) Content → left sidebar, main area, right sidebar
    layout["content"].split_row(
        Layout(name="sidebar_left",  size=CONTENT_LEFT_WIDTH),
        Layout(name="middle_area",     ratio=1),
        Layout(name="sidebar_right", size=CONTENT_RIGHT_WIDTH),
    )

    # 3) Split left sidebar into four fixed-height panels and one ratio panel
    layout["sidebar_left"].split_column(
        Layout(name="left_panel_1", size=LEFT_PANEL_1_HEIGHT),
        Layout(name="left_panel_2", size=LEFT_PANEL_2_HEIGHT),
        Layout(name="left_panel_3", size=LEFT_PANEL_3_HEIGHT),
        Layout(name="left_panel_4", size=LEFT_PANEL_4_HEIGHT),
        Layout(name="left_panel_5", ratio=LEFT_PANEL_5_RATIO),
    )

    # 4) Split right sidebar:
    layout["sidebar_right"].split_column(
        Layout(name="right_top",     size=RIGHT_TOP_HEIGHT),
        Layout(name="right_middle",  ratio=1),
        Layout(name="right_bottom",  ratio=1),
    )

    # 5) Split content
    layout["middle_area"].split_column(
        Layout(name="middle_panel_1", size=MIDDLE_PANEL_1_HEIGHT),
        Layout(name="middle_panel_2", ratio=MIDDLE_PANEL_2_RATIO),
        Layout(name="middle_panel_3", size=MIDDLE_PANEL_3_HEIGHT),
        Layout(name="middle_panel_4", size=MIDDLE_PANEL_4_HEIGHT)
    )

    # 6) Split content

    layout['middle_panel_1'].split_row(
        Layout(name="middle_panel_1_left", size=MIDDLE_PANEL_LEFT_WIDTH),
        Layout(name="middle_panel_1_middle",size=MIDDLE_PANEL_MIDDLE_WIDTH),
        Layout(name="middle_panel_1_right", ratio=MIDDLE_PANEL_RIGHT_RATIO)
    )

    return layout
