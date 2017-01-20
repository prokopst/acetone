import importlib


def resolve_type(type_name: str):
    """
    Resolves type in format 'module.submodule.ClassName'.

    :param type_name: name in format 'module.submodule.ClassName'
    :rtype: type
    """
    module_name, _, class_name = type_name.rpartition('.')

    module = importlib.import_module(module_name)
    factory = getattr(module, class_name)

    return factory
