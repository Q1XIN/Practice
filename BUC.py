import csv
import copy

dimension = ["a", "b", "c", "d"]  # 一共有哪几个维度
min_sup = 4  # 最小支持度
output = {}  # 输出结果


# 读取csv中的数据
def load_data(file_name):
    data_output = []
    with open(file_name, "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data_output.append(row)

    return data_output


# 工具函数：判断a是否包含b
def contain(a, b):
    flag = True
    for item in b:
        if item not in a:
            flag = False
            break

    return flag


# 工具函数：根据输入的item，获取其在data_set中的出现次数
def get_times(input_item, data_set):
    times = 0
    for data in data_set:
        if contain(data, input_item):
            times = times + 1

    return times


# 工具函数：判断某个元组是否在某个list里
def item_in_list(item, input_list):
    for input in input_list:
        if set(item) == set(input):
            return True

    return False


# 工具函数：去掉每一层中的重复元素
def check_data(level_output):
    set_output = []
    for item in level_output:
        if not item_in_list(item, set_output):
            set_output.append(item)

    return set_output


# 根据input_data，获取包含a，维度为（a的维度+1）的元组
def get_data_by_input(data_set_item, a):
    # 深拷贝参数
    data_set_item = copy.deepcopy(data_set_item)
    a = copy.deepcopy(a)
    output_data = []

    if contain(data_set_item, a):
        # 从input_data中删去a的数据
        for item in a:
            data_set_item.remove(item)

        # 删去后为a增加一个维度
        for data in data_set_item:
            output_item = copy.deepcopy(a)
            output_item.append(data)
            output_data.append(output_item)

    return output_data


# 获取维度为dim，并且支持度大于min_sup的所有元组，即维度为dim的一层元素
def get_next_data_layer_by_min_sup(data_set, input_data, dim, min_sup):
    final_level_output = copy.deepcopy(input_data)

    if len(input_data) == 0 and dim == 1:
        # 处理从0维度到1维度，即为首先根据data_set对应的值，获取维度+1的元组，然后计算其出现的次数，大于min_sup就加入output
        for b in range(len(data_set)):
            layer_data = get_data_by_input(data_set[b], [])
            for c in range(len(layer_data)):
                if get_times(layer_data[c], data_set) >= min_sup:
                    final_level_output.append(layer_data[c])
    else:
        # 处理从n维度到（n+1）维度，即为首先根据data_set对应的值，获取维度+1的元组，然后计算其出现的次数，大于min_sup就加入output
        for a in range(len(input_data)):
            for b in range(len(data_set)):
                if len(input_data[a]) == dim - 1:
                    layer_data = get_data_by_input(data_set[b], input_data[a])
                    for c in range(len(layer_data)):
                        if get_times(layer_data[c], data_set) >= min_sup:
                            final_level_output.append(layer_data[c])

    # 这里进行去重操作
    final_level_output = check_data(final_level_output)
    return final_level_output


# buc算法
def buc(data_set, input_list, dim, min_sup):
    if dim < len(dimension):
        dim = dim + 1
        level_output = get_next_data_layer_by_min_sup(data_set, input_list, dim, min_sup)
        return buc(data_set, level_output, dim, min_sup)
    else:
        return input_list


# 程序入口
buc_data_set = load_data("test.csv")
buc_output = buc(buc_data_set, [], 0, min_sup)
for item in buc_output:
    print(str(",".join(item)) + ": " + str(get_times(item, buc_data_set)))

