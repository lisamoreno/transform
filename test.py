#!/usr/bin/python
#
# Usage:
#   To run all tests, run `./test.py`

import argparse
import json
import transform
import unittest


class TestTransformMethods(unittest.TestCase):

    def setUp(self):
        self.transform = transform.ApplyTransformations(
            args.transformspec, args.dataset
        )
        self.transform.column_operations = {
            'RecordedDate': self.transform.hst_to_unix,
            'RecordLocation': self.transform.slugify_string,
            'Temperature': self.transform.fahrenheit_to_celsius
        }

    def test_slugify_string(self):
        test_string = 'test TEST test!'

        self.assertEqual(
            self.transform.slugify_string(test_string), 'test-test-test'
        )
        self.assertRaisesRegexp(
            transform.TransformationException,
            'Cannot sluggify {0} with type {1}. Only strings may be converted'.format(
                48, int
            ),
            self.transform.slugify_string,
            48
        )

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(
            self.transform.fahrenheit_to_celsius(42), '5.6'
        )
        self.assertRaisesRegexp(
            transform.TransformationException,
            'Cannot convert "{0}" to celsius. Unable to interpolate value as a float.'.format(
                'temperature'
            ),
            self.transform.fahrenheit_to_celsius,
            'temperature'
        )

    def test_hst_to_unix(self):
        date = '1/12/18'
        time = '12:34:56'
        bad_date = '1/12/2018'

        self.assertEqual(
            self.transform.hst_to_unix(date, time), 1515825296
        )
        self.assertRaisesRegexp(
            transform.TransformationException,
            'Cannot convert RecordedDate {0} and RecordedTime {1} to datetime object.'.format(
                bad_date, time
            ),
            self.transform.hst_to_unix,
            bad_date,
            time
        )

    def test_build_column_operations(self):
        self.assertEqual(
            self.transform.build_column_operations(
                './test_valid_json_transform_spec.json'
            ),
            None
        )
        self.assertRaisesRegexp(
            ValueError,
            ('"Column" and "Operation" are required for each transform specification. '
             'Spec with issue: {0}').format(
                json.dumps({'operation': 'hst-to-unix'})
            ),
            self.transform.build_column_operations,
            './test_json_transform_spec_missing_column.json'
        )
        self.assertRaisesRegexp(
            transform.OperationNotSupportedException,
            'Transformation operations not available for: {0}'.format(
                'fake-transformation'
            ),
            self.transform.build_column_operations,
            './test_json_transform_spec_bad_transformation.json'
       )

    def test_get_column_operation_func(self):
        self.assertEqual(
            self.transform.get_column_operation_func('invalid function name'), None
        )

        self.assertRegexpMatches(
            self.transform.get_column_operation_func('RecordLocation').__str__(),
            r'^<bound method ApplyTransformations.slugify_string of <transform.ApplyTransformations object.*'
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--transformspec', default=None, help='json transform spec file'
    )
    parser.add_argument('--dataset', default=None, help='csv dataset file')
    args = parser.parse_args()

    unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase)
