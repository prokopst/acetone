from functools import partial
from threading import Event, Thread
from unittest.case import TestCase
from unittest.mock import Mock

import acetone


class TestClassDependency(TestCase):
    def setUp(self):
        self._container = acetone.AcetoneContainer()

        class DummyObject(object):
            dependency = self._container.ClassDependency('dummy_dependency')

        self.DummyObject = DummyObject

    def test_access_from_class_multiple_times(self):
        return_mock = Mock()
        mock = Mock(return_value=return_mock)

        self._container.register_factory(
            'dummy_dependency', mock
        )

        result1 = self.DummyObject.dependency
        result2 = self.DummyObject.dependency

        mock.assert_called_once_with()

        self.assertEqual(result1, return_mock)
        self.assertEqual(result2, return_mock)

    def test_access_multiple_instances_and_class(self):
        return_mock = Mock()
        mock = Mock(return_value=return_mock)

        self._container.register_factory(
            'dummy_dependency', mock
        )

        dummy_object1 = self.DummyObject()
        dummy_object2 = self.DummyObject()

        result1 = self.DummyObject.dependency
        result2 = dummy_object1.dependency
        result3 = dummy_object2.dependency

        mock.assert_called_once_with()

        self.assertEqual(result1, return_mock)
        self.assertEqual(result2, return_mock)
        self.assertEqual(result3, return_mock)

    def test_access_from_multiple_threads(self):
        event = Event()
        mock_result = Mock()

        def create_with_event():
            nonlocal event
            event.wait()
            return mock_result

        mock_factory = Mock(side_effect=create_with_event)

        self._container.register_factory(
            'dummy_dependency', mock_factory
        )

        results = [None, None, None]

        def assignment(offset):
            nonlocal results
            results[offset] = self.DummyObject.dependency

        threads = [
            Thread(target=partial(assignment, offset=0)),
            Thread(target=partial(assignment, offset=1)),
            Thread(target=partial(assignment, offset=2)),
        ]

        for thread in threads:
            thread.start()

        event.set()

        for thread in threads:
            thread.join()

        for result in results:
            self.assertEqual(result, mock_result)

        mock_factory.assert_called_once_with()

    def test_inheritance(self):
        class DerivedDummyObject(self.DummyObject):
            derived_dependency = self._container.ClassDependency('derived_dummy_dependency')

        mock_result = Mock()
        mock_factory = Mock(return_value=mock_result)

        mock_result_derived = Mock()
        mock_factory_derived = Mock(return_value=mock_result_derived)

        self._container.register_factory(
            'dummy_dependency', mock_factory
        )
        self._container.register_factory(
            'derived_dummy_dependency', mock_factory_derived
        )

        result1 = DerivedDummyObject.dependency
        result2 = self.DummyObject.dependency
        result_derived = DerivedDummyObject.derived_dependency

        mock_factory.assert_called_once_with()
        mock_factory_derived.assert_called_once_with()

        self.assertEqual(result1, mock_result)
        self.assertEqual(result2, mock_result)
        self.assertEqual(result_derived, mock_result_derived)
