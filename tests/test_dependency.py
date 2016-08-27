from functools import partial
from threading import Event, Thread
from unittest.case import TestCase
from unittest.mock import Mock, call

from acetone import AcetoneNotFoundError, AcetoneAlreadyRegisteredError
import acetone


class TestDependency(TestCase):
    def setUp(self):
        self._container = acetone.AcetoneContainer()

        class DummyObject(object):
            dependency = self._container.Dependency('dummy_dependency')

        self.DummyObject = DummyObject

    def test_simple_access_single_instance(self):
        mock_result = Mock()
        mock_factory = Mock(side_effect=[mock_result])

        self._container.register_factory(
            'dummy_dependency', mock_factory
        )

        dummy_object = self.DummyObject()
        result1 = dummy_object.dependency
        result2 = dummy_object.dependency

        self.assertEqual(result1, mock_result)
        self.assertEqual(result2, mock_result)

        mock_factory.assert_called_once_with()

    def test_simple_access_from_multiple_instances(self):
        mock_result1 = Mock()
        mock_result2 = Mock()
        mock_factory = Mock(side_effect=[mock_result1, mock_result2])

        self._container.register_factory(
            'dummy_dependency', mock_factory
        )

        dummy_object1 = self.DummyObject()
        dummy_object2 = self.DummyObject()

        result1 = dummy_object1.dependency
        result2 = dummy_object2.dependency

        self.assertEqual(result1, mock_result1)
        self.assertEqual(result2, mock_result2)

        mock_factory.assert_has_calls([call(), call()])

    def test_dependency_not_found(self):
        dummy_object = self.DummyObject()
        with self.assertRaises(AcetoneNotFoundError):
            _ = dummy_object.dependency

    def test_access_from_multiple_threads(self):
        event = Event()

        def create_with_event():
            nonlocal event
            event.wait()
            return object()

        self._container.register_factory(
            'dummy_dependency', create_with_event
        )

        dummy_object1 = self.DummyObject()
        dummy_object2 = self.DummyObject()

        results = [None, None, None]

        def assignment(offset, dummy_object):
            nonlocal results
            results[offset] = dummy_object.dependency

        threads = [
            Thread(target=partial(assignment, offset=0, dummy_object=dummy_object1)),
            Thread(target=partial(assignment, offset=1, dummy_object=dummy_object1)),
            Thread(target=partial(assignment, offset=2, dummy_object=dummy_object2)),
        ]

        for thread in threads:
            thread.start()

        event.set()

        for thread in threads:
            thread.join()

        for result in results:
            self.assertIsNotNone(result)

        self.assertEqual(results[0], results[1])
        self.assertNotEqual(results[0], results[2])

    def test_dependency_already_registered(self):
        self._container.register_factory(
            'dummy_dependency', lambda: 1
        )

        with self.assertRaises(AcetoneAlreadyRegisteredError):
            self._container.register_factory(
                'dummy_dependency', lambda: 2
            )

    def test_inheritance(self):
        class DerivedDummyObject(self.DummyObject):
            derived_dependency = self._container.Dependency('derived_dummy_dependency')

        dummy_dependency = object()
        derived_dummy_dependency = object()

        self._container.register_factory(
            'dummy_dependency', lambda: dummy_dependency
        )
        self._container.register_factory(
            'derived_dummy_dependency', lambda: derived_dummy_dependency
        )

        derived_dummy_object = DerivedDummyObject()

        x = derived_dummy_object.derived_dependency
        y = derived_dummy_object.dependency

        self.assertEqual(x, derived_dummy_dependency)
        self.assertEqual(y, dummy_dependency)
