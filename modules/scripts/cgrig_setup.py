import os, sys, json


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir))


def add_python_path():
    """adds the python path to during launch"""
    rootPath = os.getenv("CGRIG_ROOT", "")
    rootPythonPath = os.path.join(rootPath, "")
    rootPythonPath = os.path.abspath(rootPythonPath)

    if rootPythonPath is None:
        return False
    elif not os.path.exists(rootPythonPath):
        return False
    if rootPythonPath not in sys.path:
        sys.path.append(rootPythonPath)

    pkg_path = os.path.abspath(os.path.join(rootPythonPath, 'packages'))
    pkg_names = []
    for item in os.listdir(pkg_path):
        item_path = os.path.join(pkg_path, item)
        if os.path.isdir(item_path):
            if item_path not in sys.path:
                sys.path.append(item_path)
            pkg_names.append(item)
            addPackageEnv(item_path)

    os.environ['package_items'] = json.dumps(pkg_names)

    if 'cgrig' in sys.modules:
        del sys.modules['rigger']


def addPackageEnv(path):
    environ_json_path = os.path.abspath(os.path.join(path, "environment.json"))
    if os.path.exists(environ_json_path):
        with open(environ_json_path, 'r') as json_file:
            environ_data = json.load(json_file)["environment"]
            for env, pathList in environ_data.items():
                real_path_list = [p.format(self=path) for p in pathList]
                addToEnv(env, real_path_list)


def addToEnv(env, newPaths):
    """Adds the specified environment paths to the environment variable
    if the path doesn't already exist.

    :param env: The environment variable name
    :type env: str
    :param newPaths: A iterable containing strings
    :type newPaths: iterable(str)
    """
    # to cull empty strings or strings with spaces
    from vendor import six
    paths = [i for i in os.getenv(env, "").split(os.pathsep) if i]

    for p in newPaths:
        if p not in paths:
            paths.append(p)

    os.environ[six.ensure_str(env)] = six.ensure_str(os.pathsep.join(paths))



