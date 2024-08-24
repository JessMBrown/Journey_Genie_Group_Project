import datetime
import unittest

import Joana_main


class TestKnowsDestinationFunction(unittest.TestCase):
    def test_knows_destination(self):
        self.start_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        self.end_date = datetime.strptime('2024-05-01', "%Y-%m-%d").date()
        self.planner = ''
        self.expected = None
        self.assertEqual(self.expected, Joana_main.knows_destination()(self.planner, self.start_date, self.end_date))


if __name__ == "__main__":
    unittest.main(verbosity=1)
