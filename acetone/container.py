from functools import partial
from threading import Lock

from acetone.exceptions import AcetoneAlreadyRegisteredError, AcetoneNotFoundError
from acetone.dependency import Dependency, ClassDependency


class AcetoneContainer(object):
    def __init__(self):
        self._dependencies = {}
        self._lock = Lock()

        self.Dependency = partial(Dependency, container=self)
        self.ClassDependency = partial(ClassDependency, container=self)

    def register_factory(self, key, factory_functor):
        with self._lock:
            if key in self._dependencies:
                raise AcetoneAlreadyRegisteredError(key)

            self._dependencies[key] = factory_functor

    def register_instance(self, key, instance):
        self.register_factory(key, lambda: instance)

    def clear(self):
        with self._lock:
            self._dependencies.clear()

    def __getitem__(self, key):
        try:
            return self._dependencies[key]()
        except KeyError:
            # Pass and raise the proper exception later to avoid
            # exception raised during 'except'.
            pass

        raise AcetoneNotFoundError(key)
