import importlib


def resolve_type(type_name: str, class_separator: str='.'):
    """
    Resolves type in format 'module.submodule.ClassName' where the class separator can be set
    via class_separator.

    :param type_name: name in format 'module.submodule.ClassName'
    :rtype: type
    """
    module_name, _, class_name = type_name.rpartition(class_separator)

    module = importlib.import_module(module_name)
    factory = getattr(module, class_name)

    return factory
