import unittest
import json

from unittest.mock import patch

from main import (get_api_repositories, list_repositories, get_db_repositories,
                  check_for_new_repositories)


class GithubWatcherTestCase(unittest.TestCase):
    def test_get_api_repositories(self):
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            # TODO: replace with a proper json response example
            mock_get.return_value.json.return_value = "expected_response"
            repositories = get_api_repositories(base_url='test', headers='test')
            self.assertEqual(repositories, "expected_response")

    def test_list_repositories(self):
        git_api_response = [{'id': '1'}, {'id': '2'}]
        repositories = list_repositories(git_api_response=git_api_response)
        expected_repositories = ['1', '2']
        self.assertEqual(repositories, expected_repositories)

    def test_get_db_repositories(self):
        with patch('main.redis.get') as redis_get_mock:
            redis_get_mock.return_value = b'[419081787, 419081847, 418690638]'
            repositories = get_db_repositories()
            expected_repositories = [419081787, 419081847, 418690638]
            self.assertEqual(repositories, expected_repositories)

    def test_get_db_repositories_empty(self):
        with patch('main.redis.get') as redis_get_mock:
            redis_get_mock.return_value = None
            repositories = get_db_repositories()
            self.assertEqual(repositories, [])

    def test_check_for_new_repositories_positive(self):
        new_repositories_input = [
            (['1', '2', '3'], ['1', '2']),
            (['1', '45', '2345', '1'], []),
            (['12', '1'], ['1']),
            (['1', '12', '23'], []),
        ]
        with patch('main._update_repositories_state') as update_mock:
            update_mock.return_value = 'test'
            for input_pair in new_repositories_input:
                repositories = check_for_new_repositories(
                    api_repositories=input_pair[0],
                    db_repositories=input_pair[1]
                )
                self.assertTrue(repositories)

    def test_check_for_new_repositories_negative(self):
        new_repositories_input = [
            ([], []),
            (['1'], ['1']),
            (['1'], ['1', '234']),
            ([], ['12324'])
        ]
        with patch('main._update_repositories_state') as update_mock:
            update_mock.return_value = 'test'
            for input_pair in new_repositories_input:
                repositories = check_for_new_repositories(
                    api_repositories=input_pair[0],
                    db_repositories=input_pair[1]
                )
                self.assertFalse(repositories)


if __name__ == '__main__':
    unittest.main()
