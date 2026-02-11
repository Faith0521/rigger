#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/12/1 10:59
# @Author : yinyufei
# @File : de_boor_core.py
# @Project : TeamCode


def get_open_uniform_kv(n, d):
    """
    生成开放式均匀节点向量（Open Uniform Knot Vector）
    开放式节点向量特征：首尾节点重复度=曲线次数+1，中间节点均匀分布在[0,1]区间
    满足B样条曲线插值首尾控制点的特性

    Examples:
        import de_boor_core as core
        import importlib
        importlib.reload(core)

        core.get_open_uniform_kv(4, 1)  # 4个控制点、1次（线性）曲线的节点向量
        core.get_open_uniform_kv(4, 2)  # 4个控制点、2次（二次）曲线的节点向量
        core.get_open_uniform_kv(4, 3)  # 4个控制点、3次（三次）曲线的节点向量

    Attributes:
        n (int): 控制顶点（Control Vertices）的数量
        d (int): B样条曲线的次数（Degree）

    Returns:
        list: 开放式均匀节点向量，长度=控制点数量+次数+1（n+d+1）
    """
    # 1. 首尾节点：重复d+1次0和1（满足开放式B样条的边界条件）
    start_knots = [0] * (d + 1)  # 起始端节点：[0,0,...,0]（共d+1个）
    end_knots = [1] * (d + 1)  # 结束端节点：[1,1,...,1]（共d+1个）

    # 2. 中间节点：均匀分布在[0,1]区间的节点
    # 计算逻辑：i从d+1到n-1遍历，每个节点值=(i-d)/(n-d)，确保中间节点间隔均匀
    middle_knots = [(i - d) / (n - d) for i in range(d + 1, n)]

    # 3. 拼接三部分节点，形成完整节点向量
    return start_knots + middle_knots + end_knots


def get_periodic_uniform_kv(n, d):
    """
    生成周期性均匀节点向量（Periodic Uniform Knot Vector）
    周期性节点向量特征：首尾节点延伸d个均匀间隔的节点，确保曲线周期性连续
    适用于创建闭合/周期性B样条曲线

    Examples:
        import de_boor_core as core
        import importlib
        importlib.reload(core)

        core.get_periodic_uniform_kv(4, 2)  # 4个控制点、2次周期曲线的节点向量

    Attributes:
        n (int): 控制顶点（Control Vertices）的数量
        d (int): B样条曲线的次数（Degree）

    Returns:
        list: 周期性均匀节点向量，长度=控制点数量+2d+1（n+2d+1）
    """
    # 计算节点基础间隔：总间隔数=控制点数量+次数，故每个间隔长度=1/(n+d)
    knot_interval = 1.0 / (n + d)

    # 1. 左侧延伸节点：在0之前添加d个均匀递减的节点（间隔=knot_interval）
    left_extend_knots = [-knot_interval * a for a in range(d, 0, -1)]
    # 例：d=2时，生成[-2*interval, -1*interval]

    # 2. 中间核心节点：从0开始，按间隔均匀分布到1（共n+d+1个节点）
    core_knots = [knot_interval * a for a in range(n + d + 1)]

    # 3. 右侧延伸节点：在1之后添加d个均匀递增的节点（间隔=knot_interval）
    right_extend_knots = [knot_interval * a + 1 for a in range(1, d + 1)]
    # 例：d=2时，生成[1+1*interval, 1+2*interval]

    # 拼接三部分，形成周期性节点向量
    return left_extend_knots + core_knots + right_extend_knots


def knot_vector(kv_type, cvs, d):
    """
    节点向量创建工具函数：根据类型自动生成节点向量，并适配调整控制点列表
    核心作用：统一开放式/周期性节点向量的创建逻辑，简化用户调用

    Examples:
        import de_boor_core as core
        import importlib
        importlib.reload(core)

        core.knot_vector('open', ['a', 'b', 'c', 'd'], 2)  # 开放式：4个控制点、2次曲线
        core.knot_vector('periodic', ['a', 'b', 'c', 'd'], 1)  # 周期性：4个控制点、1次曲线

    Attributes:
        kv_type (str): 节点向量类型（'open'=开放式，'periodic'=周期性）
        cvs (list): 控制顶点列表（可是任意对象，如Maya节点、坐标等）
        d (int): B样条曲线的次数（Degree）

    Returns:
        tuple: (knot_vector, modified_cvs)
               生成的节点向量 + 适配后的控制点列表（周期性会扩展控制点）
    """
    # 复制控制点列表，避免修改原始数据
    cvs_copy = cvs[:]

    if kv_type == 'open':
        # 开放式：直接调用开放式节点向量生成函数
        kv = get_open_uniform_kv(len(cvs), d)

    else:
        # 周期性：调用周期性节点向量生成函数
        kv = get_periodic_uniform_kv(len(cvs), d)

        # 扩展控制点：周期性B样条需要将末尾d个控制点复制到开头，开头d个复制到末尾
        # 目的：保证曲线在周期连接处的连续性（位置、导数均连续）
        for i in range(d):
            # 开头插入：从原始列表末尾倒数第i+1个元素（循环延伸）
            cvs_copy.insert(0, cvs[len(cvs) - i - 1])
            # 末尾添加：从原始列表开头第i个元素（循环延伸）
            cvs_copy.append(cvs[i])

    # 返回生成的节点向量和适配后的控制点列表
    return kv, cvs_copy


def de_boor(n, d, t, kv, tol=0.000001):
    """
    实现De Boor算法：计算给定参数t处的B样条基函数权重（Basis Function Weights）
    核心用途：根据权重加权求和控制点，得到B样条曲线在t处的坐标/属性值
    算法特点：数值稳定、高效，是B样条曲线求值的标准算法

    Examples:
        from maya import cmds
        import de_boor_core as core
        import importlib
        importlib.reload(core)

        # example 1：Maya中可视化基函数权重分布（按分组汇总权重）
        cmds.file(new=True, f=True)

        group_0 = cmds.group(em=True, n='GRP_0')
        group_1 = cmds.group(em=True, n='GRP_1')
        group_2 = cmds.group(em=True, n='GRP_2')
        group_3 = cmds.group(em=True, n='GRP_3')

        n = 8  # 控制点数量
        d = 2  # 曲线次数
        kv = [-0.333, -0.167, 0.0, 0.167, 0.333, 0.5, 0.667, 0.833, 1.0, 1.167, 1.333]  # 周期性节点向量
        parents = [group_2, group_3, group_0, group_1, group_2, group_3, group_0, group_1]  # 控制点分组
        samples = 100  # 采样点数（越多样条越平滑）

        for sample in range(samples):
            t = float(sample) / (samples - 1)  # 参数t在[0,1]区间均匀采样
            wts = core.de_boor(n, d, t, kv)  # 计算每个控制点的权重

            grp_wts = {group_0: 0, group_1: 0, group_2: 0, group_3: 0}
            for i, wt in enumerate(wts):
                grp_wts[parents[i]] += wt  # 按分组汇总权重

            # 用空间定位器可视化每个分组的权重
            for i, grp in enumerate([group_0, group_1, group_2, group_3]):
                loc = cmds.spaceLocator()[0]
                cmds.parent(loc, grp)
                cmds.setAttr('{}.t'.format(loc), *(t, grp_wts[grp], 0))  # t为x轴，权重为y轴
                loc_shp = cmds.listRelatives(loc, s=True)[0]
                cmds.setAttr('{}.localScale'.format(loc_shp), *(0.01, 0.01, 0.01))  # 缩小定位器

        # example 2：Maya中可视化单个控制点的基函数权重
        cmds.file(new=True, f=True)

        group_0 = cmds.group(em=True, n='GRP_0')
        group_1 = cmds.group(em=True, n='GRP_1')
        group_2 = cmds.group(em=True, n='GRP_2')
        group_3 = cmds.group(em=True, n='GRP_3')

        n = 4  # 控制点数量
        d = 3  # 曲线次数（3次=立方B样条）
        kv = core.get_open_uniform_kv(n, d)  # 开放式节点向量
        samples = 100  # 采样点数

        for sample in range(samples):
            t = float(sample) / (samples - 1)  # 参数t均匀采样
            wts = core.de_boor(n, d, t, kv)  # 计算权重
            # 每个控制点对应一个分组，用定位器可视化权重
            for i, wt in enumerate(wts):
                loc = cmds.spaceLocator()[0]
                cmds.parent(loc, 'GRP_{}'.format(i % 4))
                cmds.setAttr('{}.t'.format(loc), *(t, wt, 0))  # x轴=t，y轴=权重
                loc_shp = cmds.listRelatives(loc, s=True)[0]
                cmds.setAttr('{}.localScale'.format(loc_shp), *(0.01, 0.01, 0.01))

    Attributes:
        n (integer): 控制顶点的数量（必须满足：n >= d+1，否则曲线无法生成）
        d (integer): B样条曲线的次数（如1=线性、2=二次、3=三次）
        t (float): 曲线参数值（通常在[0,1]区间，对应曲线的起点到终点）
        kv (list or tuple): 节点向量（长度必须为n+d+1，否则算法会出错）
        tol (float): 数值容差（处理t=1时的边界情况，默认1e-6）

    Returns:
        list: 长度为n的权重列表，每个元素为[0,1]区间的浮点数，所有权重之和=1
              权重[i]表示第i个控制点对t处曲线值的贡献程度
    """
    # 边界处理：当t接近或等于1时（考虑数值误差），直接返回末尾控制点权重=1，其余=0
    # 原因：开放式节点向量的末尾节点重复d+1次，t=1时只有最后一个控制点起作用
    if t + tol > 1:
        return [0.0 if i != n - 1 else 1.0 for i in range(n)]

    # 初始化权重数组（De Boor算法的第0层，即0次B样条基函数）
    # 逻辑：找到包含t的节点区间[kv[i], kv[i+1})，该区间对应的权重=1，其余=0
    # 权重数组长度=节点向量长度-1 = (n+d+1)-1 = n+d
    weights = [1.0 if kv[i] <= t < kv[i + 1] else 0.0 for i in range(n + d)]

    # 基函数宽度：每次迭代后宽度减1（从n+d-1逐步缩减到n-1）
    basis_width = n + d - 1

    # De Boor算法迭代：从1次基函数逐步计算到d次基函数（共d次迭代）
    for degree in range(1, d + 1):
        # 遍历当前基函数宽度内的每个权重，更新为更高次的基函数值
        for i in range(basis_width):
            # 优化：如果当前位置和下一个位置的权重都是0，直接跳过（无贡献）
            if weights[i] == 0 and weights[i + 1] == 0:
                continue

            # 计算De Boor算法的两个分母（节点区间长度）
            a_denom = kv[i + degree] - kv[i]  # 左侧节点区间长度：[kv[i], kv[i+degree]]
            b_denom = kv[i + degree + 1] - kv[i + 1]  # 右侧节点区间长度：[kv[i+1], kv[i+degree+1]]

            # 计算左侧权重系数a：当前权重 * (t - 左节点) / 左侧区间长度
            # 分母为0时（节点重合），系数a=0（避免除零错误）
            a = (t - kv[i]) * weights[i] / a_denom if a_denom != 0 else 0.0

            # 计算右侧权重系数b：下一个权重 * (右节点 - t) / 右侧区间长度
            # 分母为0时（节点重合），系数b=0（避免除零错误）
            b = (kv[i + degree + 1] - t) * weights[i + 1] / b_denom if b_denom != 0 else 0.0

            # 更新当前权重：更高次基函数值 = a + b（线性组合）
            weights[i] = a + b

        # 每次迭代后，基函数宽度减1（因为d次基函数比d-1次少一个节点区间）
        basis_width -= 1

    # 截取前n个权重（对应n个控制点），返回最终的d次B样条基函数权重
    return weights[:n]









