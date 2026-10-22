import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch

from scripts import search
from scripts.lib.schema import Paper, SearchResult


class SearchRegressionTests(unittest.TestCase):
    def setUp(self):
        self.results = [SearchResult(query='trauma', source='fixture', papers=[
            Paper(title='Trauma narrative', authors=['A'], year=2024,
                  doi='10.1234/example', source='one'),
            Paper(title='Trauma narrative', authors=['A', 'B'], year=2024,
                  doi='10.1234/example', source='two'),
        ])]

    def test_rank_dedupe_and_json_citation(self):
        with patch.object(search, 'search', return_value=self.results):
            result = json.loads(search.search_to_json('trauma'))
        self.assertEqual(result['total'], 1)
        paper = result['papers'][0]
        self.assertEqual(paper['authors'], ['A', 'B'])
        self.assertGreater(paper['score'], 0)
        self.assertIn('Trauma narrative', paper['citation'])

    def test_all_cli_renderers(self):
        for fmt in ('text', 'markdown', 'json'):
            with self.subTest(fmt=fmt), patch.object(search, 'search', return_value=self.results), patch.object(sys, 'argv', ['search.py', 'trauma', '--format', fmt]), contextlib.redirect_stdout(io.StringIO()) as output:
                search.main()
                self.assertIn('Trauma narrative', output.getvalue())

    def test_source_failure_is_reported(self):
        with patch.object(search, 'search', return_value=[SearchResult(query='trauma', source='fixture', error='rate limited')]):
            ranked, errors = search.search_and_rank('trauma')
        self.assertEqual(ranked, [])
        self.assertEqual(errors, ['[fixture] rate limited'])


if __name__ == '__main__':
    unittest.main()
