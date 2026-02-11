# coding=utf-8
import maya.cmds as cmds

Group = 'InfluencesHierarchy'


def get_distance_to_parent(child, parent):
    child_position = cmds.xform(child, query=True, worldSpace=True, translation=True)
    parent_position = cmds.xform(parent, query=True, worldSpace=True, translation=True)

    distance = ((child_position[0] - parent_position[0]) ** 2 +
                (child_position[1] - parent_position[1]) ** 2 +
                (child_position[2] - parent_position[2]) ** 2) ** 0.5

    return distance


def sort_joints_and_groups_by_distance(parent):
    children = cmds.listRelatives(parent, children=True) or []

    # 筛选关节和组
    joints_and_groups = [child for child in children if cmds.nodeType(child) in ['joint', 'transform']]

    # 按照距离排序
    sorted_children = sorted(joints_and_groups, key=lambda child: get_distance_to_parent(child, parent))

    sorted_list = []
    for child in sorted_children:
        long_name = cmds.ls(child, long=True)[0]
        sorted_list.append(long_name)
        sorted_list.extend(sort_joints_and_groups_by_distance(child))

    return sorted_list


def create_inf_joints_from_list(obj_list):
    created_inf_joints = []

    for i, obj in enumerate(obj_list):
        # 替换名称中的竖线
        inf_joint_name = obj.replace('|', '__')

        # Check if an inf_joint with the same name already exists
        if not cmds.objExists(inf_joint_name):
            inf_joint = cmds.createNode('joint', name=inf_joint_name)
            cmds.matchTransform(inf_joint, obj, pos=True, rot=True)
            created_inf_joints.append(inf_joint)

        else:
            print("Inf joint with the name {} already exists. Skipping.".format(inf_joint_name))

    return created_inf_joints


def check_and_move_to_hierarchy(obj_list, threshold=3):
    for obj in obj_list:
        # 获取 '__' 的数量
        count_in_obj = obj.count('__')
        parent = cmds.listRelatives(obj, parent=True, fullPath=True)

        if parent:
            parent_long = cmds.ls(parent[0], long=True)[0]
            parent_short = parent_long.split('|')[-1]
            count_in_parent = parent_short.count('__')

            # 如果 '__' 数量差值超过阈值，将元素移到 LayerHierarchy 下
            if abs(count_in_obj - count_in_parent) > threshold:
                try:
                    print("Moving {} to {}. Parent: {}, Count in Parent: {}, Count in Object: {}".format(obj, Group, parent_short, count_in_parent, count_in_obj))
                    cmds.parent(obj, Group)
                except:
                    pass
                # 这里可以选择是否保留原始层级关系，如果不保留，取消下面一行的注释
                # cmds.parent(obj, world=True)


def get_skin_joints(obj):
    # Check if the object is a valid skin cluster
    skin_cluster = cmds.ls(cmds.listHistory(obj), type='skinCluster')

    if not skin_cluster:
        print("No skin cluster found for {}. Skipping.".format(obj))
        return []

    # Get all skin joints from the skin cluster
    skin_joints = cmds.skinCluster(skin_cluster[0], query=True, inf=True)

    if not skin_joints:
        print("No skin joints found for {}. Skipping.".format(obj))
        return []

    return skin_joints


def get_common_prefix(strings):
    if not strings:
        return ""

    prefix = strings[0]
    for string in strings[1:]:
        index = 0
        while index < len(prefix) and index < len(string) and prefix[index] == string[index]:
            index += 1
        prefix = prefix[:index]

    return prefix


def delete():
    try:
        cmds.delete(Group)
    except:
        pass


def create():
    # 选择需要操作的物体
    selected_objects = cmds.ls(selection=True)

    # 如果没有父组，则创建父组
    parent_group = Group
    if not cmds.objExists(Group):
        cmds.group(empty=True, name=Group)

        # 获取所有物体的蒙皮骨骼
    all_skin_joints = []
    for obj in selected_objects:
        skin_joints = get_skin_joints(obj)
        all_skin_joints.extend(skin_joints)

    # 获取所有蒙皮骨骼的长名
    long_names = cmds.ls(all_skin_joints, long=True)

    # 找到所有长名中的最长公共前缀
    common_prefix = get_common_prefix(long_names)
    if not cmds.objExists(common_prefix):
        last_pipe_index = common_prefix.rfind('|')
        if last_pipe_index != -1:
            common_prefix = common_prefix[:last_pipe_index]

    corresponding_objects = cmds.listRelatives(common_prefix, parent=True, fullPath=True)
    root_objects = [corresponding_objects]

    # 对关节和组按照距离排序
    sorted_list = []
    for obj in root_objects:
        sorted_list.extend(sort_joints_and_groups_by_distance(obj))

        # 为排序后的每个元素创建同名的joint并与原元素对齐
    created_inf_joints = create_inf_joints_from_list(sorted_list)

    # 在这里设置父子关系
    for i in range(len(created_inf_joints)):
        if i > 0:
            cmds.parent(created_inf_joints[i], created_inf_joints[i - 1])
        else:
            cmds.parent(created_inf_joints[i], parent_group)

            # 检查并移动到 LayerHierarchy, 使用默认阈值 1
    check_and_move_to_hierarchy(created_inf_joints, 1)

    # 遍历 all_skin_joints 中的元素，将长名中的'|'替换成'__'形成新的列表 all_skin_joints_long
    all_skin_joints_long = [cmds.ls(joint, long=True)[0].replace('|', '__') for joint in all_skin_joints]
    for item in all_skin_joints_long:
        print(item.split('__')[-1])
    for item in created_inf_joints:
        print(item.split('__')[-1])

    # 找出不在 all_skin_joints_long 但是在 created_inf_joints 中的元素
    elements_to_delete = [elem for elem in created_inf_joints if elem not in all_skin_joints_long]

    # 逐个修改父子关系，然后删除这些元素
    for elem in elements_to_delete:
        print(elem.split('__')[-1])
        parent = cmds.listRelatives(elem, parent=True, fullPath=True)
        children = cmds.listRelatives(elem, children=True, fullPath=True) or []
        if parent and children:
            # 将子物体连接到父物体
            cmds.parent(children, parent)
        # 删除元素
        cmds.delete(elem)



