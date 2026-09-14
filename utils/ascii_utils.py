def to_ascii_diagram(text: str) -> str:
    """Convert Qiskit circuit Unicode box-drawing characters into ASCII equivalents."""
    replacements = {
        "─": "-",
        "━": "-",
        "│": "|",
        "┃": "|",
        "┌": "+",
        "┐": "+",
        "└": "+",
        "┘": "+",
        "├": "+",
        "┤": "+",
        "┬": "+",
        "┴": "+",
        "┼": "+",
        "╫": "+",
        "╩": "+",
        "╦": "+",
        "╬": "+",
        "═": "-",
        "║": "|",
        "╪": "+",
        "╧": "+",
        "╨": "+",
        "╤": "+",
        "╥": "+",
        "╟": "+",
        "╢": "+",
        "╣": "+",
        "╠": "+",
        # Control and target symbols
        "●": "o",   # control dot
        "■": "O",   # filled square
        "□": "O",   # empty square
    }
    for uni, ascii in replacements.items():
        text = text.replace(uni, ascii)
    return text