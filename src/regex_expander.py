"""
Takes a regular expression and expands it
"""
import re
import unittest


def expand_regex(regex) -> (str, []):
    return __solve_one(r"\d-\d", regex) or __solve_one(r"\w-\w", regex)


def __solve_one(pattern, source):
    """
        Solves one part of a regex class definition
        e.x A-Z
    """
    match_obj = re.match(pattern, source)

    if match_obj:
        # Returns the start and end of the range after splitting
        bounds = match_obj.group().split('-')

        if True in [len(boundary) > 1 for boundary in bounds]:
            raise RuntimeError('Invalid multi-character boundary')

        return source.replace(match_obj.group(), '', 1), generate_range(str(bounds[0]), str(bounds[-1]))
    return None


def generate_range(start: str, end: str):
    """
    Generates a range for a given class
    :param start: Start of the range
    :param end: End of the range
    :return: Range of values from start to end inclusive
    """
    if ord(start) >= ord(end):
        raise RuntimeError('Reversed boundaries')

    if start.isalpha() and end.isalpha():
        return [chr(x) for x in range(ord(start), ord(end) + 1)]

    if start.isnumeric() and end.isnumeric():
        return [x for x in range(int(start), int(end) + 1)]

    raise RuntimeError('Invalid range boundary type', start, end)


"""
Tests
"""


class TestRangeExpander(unittest.TestCase):
    def test_alpha_range(self):
        self.assertEqual(set(generate_range('a', 'c')), {'a', 'b', 'c'})

    def test_numeric_range(self):
        self.assertEqual(set(generate_range('1', '3')), set(range(1, 3 + 1)))

    def test_failing_num_range_reversed_bounds(self):
        self.assertRaises(RuntimeError, generate_range, '9', '8')

    def test_failing_num_range_same_bounds(self):
        self.assertRaises(RuntimeError, generate_range, '9', '9')

    def test_failing_num_range_mismatched_types(self):
        self.assertRaises(RuntimeError, generate_range, 'a', '9')

    def test_failing_num_range_invalid_types(self):
        self.assertRaises(RuntimeError, generate_range, 'a', '*')  # non alpha num char


class TestModule(unittest.TestCase):
    def test_alpha_class(self):
        range_list = expand_regex('a-c')[1]
        self.assertTrue(set(range_list), {'a', 'b', 'c'})

    def test_num_class(self):
        range_list = expand_regex('1-7')[1]
        self.assertEqual(set(range_list), set(range(1, 8)))

    def test_fail_alpha_class(self):
        self.assertRaises(RuntimeError, expand_regex, 'c-a')

    # This test shouldn't pass, but life is too short
    # a-b only are matched, while c isn't counted in
    def test_fail_alpha_class_multi_char(self):
        (rem, range_list) = expand_regex('a-bc')

        self.assertEqual(rem, 'c')
        self.assertEqual(set(range_list), {'a', 'b'})


if __name__ == '__main__':
    unittest.main()
