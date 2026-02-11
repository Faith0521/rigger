from functools import wraps
from maya import mel, cmds
import timeit


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------
def viewport_off(func):
    """Decorator - Turn off Maya display while func is running.

    if func will fail, the error will be raised after.

    type: (function) -> function

    """

    @wraps(func)
    def wrap(*args, **kwargs):
        # type: (*str, **str) -> None

        # Turn $gMainPane Off:
        gMainPane = mel.eval('global string $gMainPane; $temp = $gMainPane;')
        cmds.paneLayout(gMainPane, edit=True, manage=False)

        try:
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            cmds.paneLayout(gMainPane, edit=True, manage=True)

    return wrap


def one_undo(func):
    """Decorator - guarantee close chunk.

    type: (function) -> function

    """

    @wraps(func)
    def wrap(*args, **kwargs):
        # type: (*str, **str) -> None

        try:
            cmds.undoInfo(openChunk=True)
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            cmds.undoInfo(closeChunk=True)

    return wrap


def timeFunc(func):
    """Use as a property to time any desired function
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        start = timeit.default_timer()
        try:
            return func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            end = timeit.default_timer()
            timeConsumed = end - start
            print(("{} time elapsed running {}".format(timeConsumed,
                                                       func.__name__)))

    return wrap


# -----------------------------------------------------------------------------
# selection Decorators
# -----------------------------------------------------------------------------


def _filter_selection(selection, sel_type="nurbsCurve"):
    filtered_sel = []
    for node in selection:
        if node.getShape().type() == sel_type:
            filtered_sel.append(node)
    return filtered_sel


def filter_nurbs_curve_selection(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        args = list(args)
        args[0] = _filter_selection(args[0])
        return func(*args, **kwargs)

    return wrap


def windowsOff(func):
    """Turn off the editors."""

    @wraps(func)
    def _windows_off(*args, **kwargs):
        window_dict = {
            "nodeEditorPanel1Window": cmds.NodeEditorWindow,
            "hyperShadePanel1Window": cmds.HypershadeWindow,
            "blendShapePanel1Window": cmds.BlendShapeEditor,
            "graphEditor1Window": cmds.GraphEditor
        }
        open_windows = cmds.lsUI(type="window")
        # close the windows
        for key, value in window_dict.items():
            if key in open_windows:
                cmds.deleteUI(key)
        try:
            return func(*args, **kwargs)
        except:  # noqa: E722
            for key, value in window_dict.items():
                if key in open_windows:
                    value()
            raise
        finally:
            for key, value in window_dict.items():
                if key in open_windows:
                    value()

    return _windows_off


def suppress_warnings(func):
    """Suppress scripteditor warnings."""

    @wraps(func)
    def _suppress(*args, **kwargs):
        _state = cmds.scriptEditorInfo(query=True, suppressWarnings=True)
        cmds.scriptEditorInfo(edit=True, suppressWarnings=True)
        returned = None
        returned = func(*args, **kwargs)
        try:
            cmds.scriptEditorInfo(edit=True, suppressWarnings=_state)
        except Exception:  # pylint: disable=broad-except
            pass
        return returned  # pylint: disable=lost-exception

    return _suppress


def keepframe(func): # noqa
    """
    Keep the current slider time.
    Useful where the wrapped method messes with the current time
    """

    @wraps(func)
    def _keepfunc(*args, **kwargs):
        original_frame = cmds.currentTime(q=True)
        try:
            # start an undo chunk
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # after calling the func, end the undo chunk and undo
            cmds.currentTime(original_frame)

    return _keepfunc