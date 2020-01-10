import numpy as np

# 读入数据
file = open(r"test2.csv", 'r', encoding='utf-8')
data = []
for line in file:
    line = line.replace("\n", "")
    data.append(line.split(","))
file.close()
print(data)

numDims = len(data[0])  # 维的总数
cardinality = []  # cardinality[i]存放第i维的取值个数
min_sup = 3  # 最小支持度为3
outputRec = []  # 当前输出记录
dataCount = []  # 存放每个值的出现次数
result = {}

for i in range(numDims):
    cardinality.append(0)
    tmp = {}
    dataCount.append(tmp)
# 计算每个值在data中出现的次数，储存在dataCount中
for i in range(len(data)):
    for j in range(numDims):
        # print(data[i][j])
        if data[i][j] not in list(dataCount[j].keys()):
            cardinality[j] = cardinality[j] + 1  # 如果该值没有出现过，则该维度上的取值数目加一
            dataCount[j][data[i][j]] = 1  # 如果该值没有出现过，把该值出现的次数初始化为一
        else:
            dataCount[j][data[i][j]] = dataCount[j][data[i][j]] + 1  # 如果该值之前出现过，则该值出现的次数加一

print("cardinality:", cardinality)
print("dataCount:", dataCount)


# 计算某个项集组合出现的次数，target是一个列表，比如想要计算['a1','b2']出现过多少次，则写成countPairs(['a1','b2'])
def countPairs(input, target):
    count = 0
    for record in input:
        flag = True
        for x in target:
            if x not in record:
                flag = False
        if flag:
            count = count + 1
    return count


# 递归计算
# input是子列表
# dim是当前计算的维度(从dim计算到last dim）
def BUC(input, dim):
    if dim >= numDims:
        return

    # 得到子记录，从dim->lastDim
    sub_input = []
    for record in input:
        tmp = []
        for i in range(dim, numDims):
            tmp.append(record[i])
        sub_input.append(tmp)

    for line in sub_input:
        # print(line)
        xx = []
        print(len(line))
        xx.append(line[0])
        if countPairs(sub_input, xx) < min_sup:  # 先判断当前值是否满足min_sup，若不满足，剪枝
            continue
        else:
            result[tuple(xx)] = countPairs(sub_input, xx)  # 将单项加入到result中
            # if dim>=1:
            for i in range(1, numDims - dim):  # 若当前维值满足min_sup，则从dim+1->numDims依次计算count值
                xy = []
                # print(x)
                xy.append(line[0])
                # print("i:",i)
                xy.append(line[i])
                if xy not in list(result.keys()) and countPairs(sub_input,
                                                                xy) >= min_sup:  # 如果未在结果中但是count>=min_sup，那么把它加到结果中
                    result[tuple(xy)] = countPairs(sub_input, xy)
                print(result)

    BUC(input, dim + 1)


BUC(data, 0)
print("result:", result)