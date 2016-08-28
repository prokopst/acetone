# acetone library

## About
Glue code removal. Acetone is a python library to provide inversion of control in situation where other methods are inconvenient or they are not even possible. Or you just like the library.

## Usage

Create the acetone container somewhere in your application: 
```python
# dependencies.py

from acetone import AcetoneContainer

dependencies = AcetoneContainer()
# or ioc_container
# or lord_of_the_dependencies
# or services
```

Then use it:
```python
# class_with_dependency.py

from dependencies import dependencies

class ClassWithSomeDependency(object):
    # you can use strings or types as a key
    dependency = dependencies.Dependency('key')
    
    def use_the_dependency(self):
        self.dependency.dependency_call('argument')
```
Create a dependency implementation:
```python
# dependency_implementation.py

class DependencyImplementation(object):
    def dependency_call(self, argument):
        print(argument)
```
Later register the implementation and run it!
```python
# __main__.py

from dependencies import dependencies
from class_with_dependency import ClassWithSomeDependency
from dependency_implementation import DependencyImplementation


if __name__ == '__main__':
    dependency_implementation = DependencyImplementation()
    dependencies.register_instance('key', dependency_implementation)
    
    instance = ClassWithSomeDependency()
    instance.use_the_dependency()
```

Or load it from a file:
```json
[
    {
        "name": "key",
        "module": "dependency_implementation",
        "factory": "DependencyImplementation",
        "singleton": true
    }
]
```

```python
import json
from dependencies import dependencies

def main():
    with open('configuration.json') as file:
        content = json.load(file)
        dependencies.load_from_dicts(content)
    
    instance = ClassWithSomeDependency()
    instance.use_the_dependency()
```

## Frequently asked questions

### How fast is it?

It's very fast. It's even faster then a builtin property. The very first dependency access requires some initialization for its own setup and dependency creation (provided it was not created before), but the subsequent calls are as fast as a member instance access. Dependencies use a descriptor protocol (used by ``@property``), they are initialized lazily and once fetched from the container they are set as a normal instance member (class member in case of ``ClassDependency``). This trick is used by several frameworks (for example werkzeuq ``cached_property``).

### How do I mock it?

Technically you can mock it, but I don't think it's necessary. The container is simple and well tested. Its purpose is to provide a requested dependency and the dependency can be a mock as well. You can just consider it as an essential part of your code and not mock it to your advantage (would you mock properties?).

```python
class TestXyz(TestCase):
    def tearDown(self):
        container.clean()
```

Traditionalists wouldn't agree for sure but Python wasn't created by traditionalists in the first place.

### Are there any requirements?

No external dependencies. For the class used the only requirement is that the class has to be a normal python class with ``__dict__``. In other words it can't use ``__slots__``.
