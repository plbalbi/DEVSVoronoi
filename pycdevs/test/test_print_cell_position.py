from unittest import TestCase
from ..voronoi import print_cell_position


class PrintCellPositionTests(TestCase):

    def test_single_digit_printed_position_has_no_spaces(self):
        position = (9,9)
        printed_position = print_cell_position(position)
        assert printed_position == "(9,9)"

    def test_mixed_digit_printed_position_has_no_spaces(self):
        position = (209,9)
        printed_position = print_cell_position(position)
        assert printed_position == "(209,9)"
