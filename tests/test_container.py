from unittest.case import TestCase
from unittest.mock import Mock, call
import acetone


mock_service1 = None
mock_service2 = None
mock_factory = None


class TestDependency(TestCase):
    def setUp(self):
        self._container = acetone.AcetoneContainer()

    def test_load(self):
        global mock_service1, mock_service2, mock_factory

        mock_service1 = Mock()
        mock_service2 = Mock()
        mock_factory = Mock(side_effect=[mock_service1, mock_service2])

        self._container.load_from_dicts(
            [
                {
                    'name': 'Service',
                    'module': __name__,
                    'factory': 'mock_factory',
                    'args': [1, 3, 2],
                    'kwargs': {'key': 'value'}
                }
            ]
        )

        service1 = self._container['Service']
        service2 = self._container['Service']

        self.assertEqual(service1, mock_service1)
        self.assertEqual(service2, mock_service2)
        mock_factory.assert_has_calls([
            call(1, 3, 2, key='value'), call(1, 3, 2, key='value')
        ])

    def test_load_single(self):
        global mock_service1, mock_service2, mock_factory

        mock_service1 = Mock()
        mock_service2 = Mock()
        mock_factory = Mock(return_value=mock_service1)

        self._container.load_from_dicts(
            [
                {
                    'name': 'Service',
                    'module': __name__,
                    'factory': 'mock_factory',
                    'singleton': True,
                    'args': [1, 3, 2],
                    'kwargs': {'key': 'value'}
                }
            ]
        )

        service1 = self._container['Service']
        service2 = self._container['Service']

        self.assertEqual(service1, mock_service1)
        self.assertEqual(service2, mock_service1)
        mock_factory.assert_called_once_with(1, 3, 2, key='value')
