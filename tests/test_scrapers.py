import pytest
from asos import parse_price as asos_parse_price
from revolve import parse_price as revolve_parse_price

class TestAsosScraper:
    def test_parse_price_normal(self):
        assert asos_parse_price("Now 250.50 ILS") == 250.50

    def test_parse_price_original(self):
        assert asos_parse_price("Was 300 ILS") == 300.0

    def test_parse_price_with_comma(self):
        assert asos_parse_price("1,250 ILS") == 1250.0

    def test_parse_price_edge_cases(self):
        assert asos_parse_price(None) is None
        assert asos_parse_price("") is None
        assert asos_parse_price("Sold Out") is None

class TestRevolveScraper:
    def test_parse_price_normal(self):
        assert revolve_parse_price("₪350.00") == 350.0

    def test_parse_price_with_comma(self):
        assert revolve_parse_price("₪1,450.99") == 1450.99

    def test_parse_price_edge_cases(self):
        assert revolve_parse_price("Not a price") is None
        assert revolve_parse_price(None) is None