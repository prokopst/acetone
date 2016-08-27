from acetone import AcetoneContainer

ioc = AcetoneContainer()


class X(object):
    def hello(self):
        return "HELLO WORLD"


class Y(object):
    dependency = ioc.Dependency(X)
    class_dependency = ioc.ClassDependency(X)
    class_member = X()

    def __init__(self):
        self.member = X()

    @property
    def property(self):
        return self.member

    def call_member(self):
        return self.member.hello()

    def call_dependency(self):
        return self.dependency.hello()

    def call_property(self):
        return self.property.hello()

    @classmethod
    def call_class_dependency(cls):
        cls.class_dependency.hello()

    @classmethod
    def call_class_dependency(cls):
        cls.class_member.hello()

yyy = Y()

# TODO: load classes from a configuration
ioc.register_instance(X, X())


# primitive benchmark
if __name__ == '__main__':
    import timeit

    result = timeit.timeit("yyy.call_property()", setup="from benchmark import yyy", number=10000)
    print("property           :", result)
    result = timeit.timeit("yyy.call_member()", setup="from benchmark import yyy", number=10000)
    print("member             :", result)
    result = timeit.timeit("yyy.call_dependency()", setup="from benchmark import yyy", number=10000)
    print("dependency         :", result)

    print()

    result = timeit.timeit("yyy.call_class_dependency()", setup="from benchmark import yyy", number=10000)
    print("class dependency   :", result)
    result = timeit.timeit("yyy.call_member()", setup="from benchmark import yyy", number=10000)
    print("class member       :", result)
