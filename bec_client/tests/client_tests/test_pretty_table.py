from bec_client.prettytable import PrettyTable


def test_get_header():
    header = ["header1", "header2", "header3"]
    pt = PrettyTable(header)
    assert pt.get_header() == "|      header1     |      header2     |      header3     |"
