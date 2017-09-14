import unittest
from switchlang import switch, closed_range


# here is a custom type we can use as a key for our tests
class TestKeyObject:
    pass


class CoreTests(unittest.TestCase):
    def test_has_matched_case_int(self):
        value = 7
        with switch(value) as s:
            s.case(1, lambda: "one")
            s.case(5, lambda: "five")
            s.case(7, lambda: "seven")
            s.default(lambda: 'default')

        self.assertEqual(s.result, "seven")

    def test_has_matched_case_object(self):
        t1 = TestKeyObject()
        t2 = TestKeyObject()
        t3 = TestKeyObject()

        with switch(t2) as s:
            s.case(t1, lambda: t1)
            s.case(t2, lambda: t2)
            s.case(t3, lambda: t3)
            s.default(lambda: None)

        self.assertEqual(s.result, t2)

    def test_default_passthrough(self):
        value = 11
        with switch(value) as s:
            s.case(1, lambda: '1')
            s.case(2, lambda: '2')
            s.default(lambda: 'default')

        self.assertEqual(s.result, "default")

    def test_none_as_valid_case(self):
        with switch(None) as s:
            s.case(1, lambda: 'one')
            s.case(None, lambda: 'none')
            s.default(lambda: "default")

        self.assertEqual(s.result, 'none')

    def test_error_no_match_no_default(self):
        with self.assertRaises(Exception):
            with switch('val') as s:
                s.case(1, lambda: None)
                s.case(2, lambda: None)

    def test_error_duplicate_case(self):
        with self.assertRaises(ValueError):
            with switch('val') as s:
                s.case(1, lambda: None)
                s.case(1, lambda: None)

    def test_multiple_values_one_case_range(self):
        for value in range(1, 5):
            with switch(value) as s:
                s.case(range(1, 6), lambda: "1-to-5")
                s.case(range(6, 7), lambda: "6")
                s.default(lambda: 'default')

            self.assertEqual(s.result, "1-to-5")

        for value in range(6, 7):
            with switch(value) as s:
                s.case(range(1, 6), lambda: "1-to-5")
                s.case(range(6, 7), lambda: "6")
                s.default(lambda: 'default')

            self.assertEqual(s.result, "6")

        with switch(7) as s:
            s.case(range(1, 6), lambda: "1-to-5")
            s.case(range(6, 7), lambda: "6")
            s.default(lambda: 'default')

        self.assertEqual(s.result, "default")

    def test_multiple_values_one_case_list(self):
        with switch(6) as s:
            s.case([1, 3, 5, 7], lambda: "odd")
            s.case([0, 2, 4, 6, 8], lambda: "even")
            s.default(lambda: 'default')

        self.assertEqual(s.result, "even")

    def test_return_value_from_case(self):
        value = 4
        with switch(value) as s:
            s.case([1, 3, 5, 7], lambda: value + 1)
            s.case([0, 2, 4, 6, 8], lambda: value * value)
            s.default(lambda: 0)

        self.assertEqual(s.result, 16)

    # noinspection PyStatementEffect
    def test_result_inaccessible_if_hasnt_run(self):
        with self.assertRaises(Exception):
            s = switch(7)
            s.result

    def test_closed_range(self):
        for value in [1, 2, 3, 4, 5]:
            with switch(value) as s:
                s.case(closed_range(1, 5), lambda: "1-to-5")
                s.case(closed_range(6, 7), lambda: "6")
                s.default(lambda: 'default')

            self.assertEqual(s.result, "1-to-5")

        with switch(0) as s:
            s.case(closed_range(1, 5), lambda: "1-to-5")
            s.case(closed_range(6, 7), lambda: "6")
            s.default(lambda: 'default')

        self.assertEqual(s.result, "default")

        with switch(6) as s:
            s.case(closed_range(1, 5), lambda: "1-to-5")
            s.case(closed_range(6, 7), lambda: "6")
            s.default(lambda: 'default')

        self.assertEqual(s.result, "6")
