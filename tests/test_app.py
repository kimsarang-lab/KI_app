import unittest
from streamlit.testing.v1 import AppTest
from scoring import calculate

class AppTests(unittest.TestCase):
    def test_score(self):
        self.assertEqual(calculate([0]*11), 0)
        self.assertEqual(calculate([3]*11), 51)
        self.assertEqual(calculate([1]*11), 17)
        self.assertEqual(calculate([3,2,1,0,1,0,1,0,1,0,1]), 22)
        for bad in ([None]*11, [0]*10, [4]*11):
            with self.assertRaises(ValueError): calculate(bad)

    def test_flow(self):
        at = AppTest.from_file('app.py').run()
        self.assertFalse(at.exception)
        self.assertTrue(all(r.value is None for r in at.radio))
        at.button[1].click().run()
        self.assertEqual(len(at.warning), 1)
        self.assertEqual(len(at.metric), 0)
        for radio in at.radio: radio.set_value(3)
        at.button[1].click().run()
        self.assertEqual(at.metric[0].value, '51점 / 51점')
        self.assertEqual(len(at.radio), 0)
        at.run()
        at.button[0].click().run()
        self.assertTrue(all(r.value == 3 for r in at.radio))
        for radio in at.radio: radio.set_value(0)
        at.button[1].click().run()
        self.assertEqual(at.metric[0].value, '0점 / 51점')
        at.button[1].click().run()
        self.assertEqual(len(at.radio), 11)
        self.assertTrue(all(r.value is None for r in at.radio))
        self.assertEqual(len(at.metric), 0)
        self.assertFalse(at.exception)

if __name__ == '__main__': unittest.main()
