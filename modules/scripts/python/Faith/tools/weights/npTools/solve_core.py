# coding:utf-8
try:
    import numpy as np
except ImportError:
    np = None
import shutil
import os
import subprocess
import sys
import json


def limit_max_influence(weights, max_influence):
    weights = weights.copy()
    sort_ids = np.argsort(weights, axis=1)
    for i, ids in enumerate(sort_ids):
        weights[i, ids[:-max_influence]] = 0
    weights = normal_weights(weights)
    return weights


def normal_weights(weights):
    max_weights = np.sum(weights, axis=1)
    max_weights[max_weights < 0.0001] = 1
    weights = weights / max_weights[:, None]
    return weights


def solve_link_power(points, ids, links):
    link_points = points[links]
    vtx_points = points[ids]
    distance_matrix = np.linalg.norm(link_points[:, :, None, :] - link_points[:, None, :, :], axis=3)
    distance_inv = np.linalg.inv(distance_matrix)
    vtx_distance = np.linalg.norm(vtx_points[:, None] - link_points, axis=2)
    rbf_weights = np.sum(vtx_distance[:, None] * distance_inv, axis=2)
    rbf_weights[rbf_weights < 0] = 0
    rbf_weights = normal_weights(rbf_weights)
    soft_max_weights = normal_weights(np.exp(-vtx_distance))
    return rbf_weights*0.8+soft_max_weights*0.2


def smooth_current_weights(smooth_weights, weights, ids, links, power):
    smooth_weights[ids] = np.sum(weights[links]*power[:, :, None], axis=1)


def smooth_iter_weights(weights, data, points, count=4, step=0.9):
    for row in data.values():
        if "power" not in row:
            row["links"] = np.array(row["links"])
            row["power"] = solve_link_power(points, **row)

    for i in range(count):
        smooth_weights = weights.copy()
        for row in data.values():
            smooth_current_weights(smooth_weights, weights, **row)
        weights = weights*(1-step) + smooth_weights*step
    return weights


def re_weights(weights, max_influence, vv, points, count=4, step=0.9):
    weights = np.clip(weights, 0.0, 1.0)
    weights = limit_max_influence(weights, max_influence)
    weights = 3 * weights ** 2 - 2 * weights ** 3
    weights = smooth_iter_weights(weights, vv, points, count, step)
    weights[weights < 1e-3] = 0
    weights = limit_max_influence(weights, max_influence)
    return weights


def add_ball_point(joint_points):
    max_p = np.max(joint_points, axis=0)
    min_p = np.min(joint_points, axis=0)
    center = max_p*0.5+min_p*0.5
    dis = np.linalg.norm(max_p-min_p) * 1.5
    points = []
    for x in [-1.0, 0.0, 1.0]:
        for y in [-1.0, 0.0, 1.0]:
            for z in [-1.0, 0.0, 1.0]:
                v = np.array([x, y, z])
                v_dis = np.linalg.norm(v)
                if v_dis < 1e-3:
                    continue
                p = center + v / v_dis * dis
                points.append(p)
    points = np.array(points)
    return np.concatenate([joint_points, points], axis=0)


def solve_distance_rbf_weight(vtx_points, joint_points, vv, weights, indexes, max_influence):
    vtx_points = np.array(vtx_points)[:, :3]
    weights = np.array(weights).reshape(vtx_points.shape[0], -1)
    indexes = np.array(indexes)
    joint_points = np.array(joint_points)
    cut_joint_length = joint_points.shape[0]
    joint_points = add_ball_point(joint_points)
    distances_matrix = np.linalg.norm(joint_points[None] - joint_points[:, None], axis=2)
    distance_inv = np.linalg.inv(distances_matrix)
    point_distances = np.linalg.norm(joint_points[None] - vtx_points[:, None], axis=2)
    part_weights = np.matmul(point_distances, distance_inv)
    part_weights = re_weights(part_weights, max_influence, vv, vtx_points, 1, 0.9)
    part_weights = part_weights[:, :cut_joint_length]
    part_weights = re_weights(part_weights, max_influence, vv, vtx_points, 2, 0.9)
    mask = np.sum(weights[:, indexes], axis=1)
    weights[:, indexes] = part_weights * mask[:, None]
    limit_max_influence(weights, max_influence)
    return weights.reshape(-1).tolist()


# -------------- convert -----------


def run_in_numpy_maya(fun, *args, **kwargs):
    # 将参数从list转array并将返回值从array转为list
    return fun(*args, **kwargs)


def run_in_no_numpy_maya(fun, *args, **kwargs):
    data = dict(
        fun=fun.__name__,
        args=args,
        kwargs=kwargs
    )
    path = os.path.abspath(__file__+"/../data.json")
    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)
    name = os.path.splitext(os.path.split(__file__)[-1])[0]
    cmd = os.path.abspath(__file__+"/../"+name+".exe").replace("\\", "/")
    sub = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sub.wait()
    with open(path, "r") as fp:
        result = json.load(fp)
    if os.path.isfile(path):
        os.remove(path)
    return result


def run(fun, *args, **kwargs):
    if np is None:
        return run_in_no_numpy_maya(fun, *args, **kwargs)
    return run_in_numpy_maya(fun, *args, **kwargs)


def run_in_exe():
    path = os.path.abspath(sys.argv[0]+"/../data.json")
    with open(path, "r") as fp:
        data = json.load(fp)
    result = run_in_numpy_maya(globals()[data["fun"]], *data["args"], **data["kwargs"])
    with open(path, "w") as fp:
        json.dump(result, fp, indent=4)


def run_in_python():
    # 打包python文件成exe
    # pyinstaller_path = "C:/Users/mengya/AppData/Local/Programs/Python/Python310/Scripts/pyinstaller.exe"
    python_exe = sys.executable
    pyinstaller_path = os.path.join(os.path.dirname(python_exe), "Scripts/pyinstaller.exe").replace("\\", "/")
    py_path = __file__
    name = os.path.splitext(os.path.split(__file__)[-1])[0]
    cmd = '"{0}" -F "{1}"'.format(pyinstaller_path, py_path)
    cwd = os.path.abspath(__file__+"/../temp/").replace("\\", "/")
    sys.path.append(os.path.dirname(cwd))
    if not os.path.isdir(cwd):
        os.makedirs(cwd)
    popen = subprocess.Popen(cmd, cwd=cwd)
    popen.wait()
    src_exe = os.path.abspath(py_path+"/../temp/dist/{0}.exe".format(name)).replace("\\", "/")
    dst_exe = os.path.abspath(py_path+"/../{0}.exe".format(name)).replace("\\", "/")
    if os.path.isfile(dst_exe):
        os.remove(dst_exe)
    shutil.copyfile(src_exe, dst_exe)
    shutil.rmtree(cwd)


def main():
    _, ext = os.path.splitext(sys.argv[0])
    if ext in [".py"]:
        run_in_python()
    else:
        run_in_exe()


if __name__ == '__main__':
    main()

