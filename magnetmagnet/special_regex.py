import re
import unittest


class TestRegex(unittest.TestCase):
    def test_regex_functions(self):
        reg = re.compile("(?<=btih:).*(?=&dn)")

        test_string = "magnet:?xt=urn:btih:54276C2C1D8C3912F7E95ECDBEB87F8FC65AF297&dn=The+Righteous+Gemstones+S02E01+AAC+MP4-Mobile&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2F47.ip-51-68-199.eu%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce"

        output = reg.findall(test_string)

        self.assertEqual(["54276C2C1D8C3912F7E95ECDBEB87F8FC65AF297"], output)
