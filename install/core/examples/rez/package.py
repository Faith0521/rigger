name = "cgrigtoolspro"
version = "2.0.0"

tools = [
    "cgrig_cmd"
]
requires = [
    "python"
]


def commands():
    global env
    env.PATH.append("{root}/install/core/bin")
    env.MAYA_MODULE_PATH.append("{root}/install/core/extensions/maya")
