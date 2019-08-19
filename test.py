import unittest
import person

""" Uses limited data from S2 moved to S99 folder """


class TestPersonMethods(unittest.TestCase):
    def setUp(self):
        self.p99 = person.Person(person.base_dir, 99)

    def test_get_timing(self):
        timing_df = self.p99.getTiming()
        self.assertEqual(len(timing_df.index), 2)
        self.assertEqual(len(timing_df.columns), 6)

    def test_get_panas(self):
        panas_df = self.p99.getPANAS()
        self.assertEqual(len(panas_df.index), 5)
        self.assertEqual(len(panas_df.columns), 28)

    def test_get_stai(self):
        stai_df = self.p99.getSTAI()
        self.assertEqual(len(stai_df.index), 5)
        self.assertEqual(len(stai_df.columns), 8)

    def test_get_sam(self):
        sam_df = self.p99.getSAM()
        self.assertEqual(len(sam_df.index), 5)
        self.assertEqual(len(sam_df.columns), 4)

    def test_get_sssq(self):
        sssq_df = self.p99.getSSSQ()
        self.assertEqual(len(sssq_df.index), 1)
        self.assertEqual(len(sssq_df.columns), 7)

    def test_get_respi(self):
        respi_df = self.p99.getRespi()
        self.assertEqual(len(respi_df.columns), 9)

        self.assertGreater(respi_df['TEMP'].min(), 0)
        self.assertLess(respi_df['TEMP'].max(), 50)


if __name__ == '__main__':
    unittest.main()
