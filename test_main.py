import unittest
from unittest.mock import Mock, patch

import requests

from main import search_jobs


class SearchJobsTests(unittest.TestCase):
    @patch("main.requests.get")
    def test_returns_matching_remote_job(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = [
            {},
            {
                "position": "Business Analyst",
                "company": "Example Company",
                "location": "Worldwide",
                "url": "https://example.com/job",
            },
            {
                "position": "Software Engineer",
                "company": "Other Company",
                "location": "Remote",
                "url": "https://example.com/other",
            },
        ]
        mock_get.return_value = response

        results = search_jobs("analyst", "remote")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Business Analyst")
        self.assertEqual(results[0]["company"], "Example Company")

    @patch("main.requests.get")
    def test_returns_empty_list_when_nothing_matches(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = [
            {},
            {
                "position": "Software Engineer",
                "company": "Example Company",
                "location": "Remote",
                "url": "https://example.com/job",
            },
        ]
        mock_get.return_value = response

        results = search_jobs("analyst", "remote")

        self.assertEqual(results, [])

    @patch("main.requests.get")
    def test_returns_none_when_service_fails(self, mock_get):
        mock_get.side_effect = requests.RequestException("offline")

        results = search_jobs("analyst", "remote")

        self.assertIsNone(results)

    @patch("main.requests.get")
    def test_returns_none_for_invalid_response(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("invalid JSON")
        mock_get.return_value = response

        results = search_jobs("analyst", "remote")

        self.assertIsNone(results)


if __name__ == "__main__":
    unittest.main()
