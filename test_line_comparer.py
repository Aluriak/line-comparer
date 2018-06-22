
from line_comparer import detect_malformed, show_malformed

def test_basic_comparison():
    results = detect_malformed('1 13 78\n1 78 13\n\n89 34 54\n89 34 54')
    assert tuple(results) == (
        ( (('1', '13', '78'), ('1', '78', '13')), (1, 2), (1, 2, 2)),
        ( (('89', '34', '54'), ('89', '34', '54')), (), (2, 2, 2)),
    )
