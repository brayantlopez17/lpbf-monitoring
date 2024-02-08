import unittest
from Layer import Layer


answers = {
    'layer_10':
        {
            "time on": 190925,
            "time off": 150014,
            "distance on": 2267.7110503533795,
            "distance off": 727.5558494919211,
            "number events on": 1347,
            "number events off": 1347
        },
    'layer_42':
        {
            "time on": 201229,
            "time off": 156627,
            "distance on": 2450.721714043127,
            "distance off": 756.5636896046537,
            "number events on": 1407,
            "number events off": 1407
        }
}

test_file = "data/transformed_id-010.csv"


class TestLayer(unittest.TestCase):

    def test_get_number_events_on(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["number events on"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_number_events_on()
        self.assertEqual(expected_ans,
                         test_ans,
                         f" Events ON | Expected: {expected_ans} | Calculates: {test_ans}")

    def test_get_number_events_off(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["number events off"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_number_events_off()
        self.assertEqual(expected_ans,
                         test_ans,
                         f" Events OFF | Expected: {expected_ans} | Calculates: {test_ans}")

    def test_time_on(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["time on"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_time_on()
        self.assertEqual(expected_ans,
                         test_ans,
                         f" Time ON | Expected: {expected_ans} | Calculates: {test_ans}")

    def test_time_off(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["time off"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_time_off()
        self.assertEqual(expected_ans,
                         test_ans,
                         f" Time OFF | Expected: {expected_ans} | Calculates: {test_ans}")

    def test_distance_on(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["distance on"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_distance_on()
        self.assertAlmostEqual(expected_ans,
                               test_ans, 3,
                               f" Distance ON | Expected: {expected_ans} | Calculates: {test_ans}")

    def test_distance_off(self, layer: int = 10):
        expected_ans = answers[f"layer_{layer}"]["distance off"]
        test_layer = Layer(test_file)
        test_ans = test_layer.get_distance_off()
        self.assertAlmostEqual(expected_ans,
                               test_ans, 3,
                               f" Distance OFF | Expected: {expected_ans} | Calculates: {test_ans}")


if __name__ == "__main__":

    x = TestLayer()

    x.test_get_number_events_off()
    x.test_get_number_events_on()
