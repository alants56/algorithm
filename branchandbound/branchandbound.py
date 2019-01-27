import copy
import numpy as np
import time

#从文件中读取数据，并且其转化为权值矩阵的d1,d2
def load_data() :
    with open('m1.txt', 'r') as file1:
        m1 = file1.readlines()
    with open('m2.txt', 'r') as file2:
        m2 = file2.readlines()
    d1 = []
    for m in m1 :
        a = m.split()
        d = []
        for x in a :
            d.append(int(x))
        d1.append(d)
    d2 = []
    for m in m2 :
        a = m.split()
        d = []
        for x in a :
            d.append(int(x))
        d2.append(d)
    return d1,d2


d1, d2 = load_data()

#当前路径
path = []
path.append(0)
#已知的最优路径
rpath = []
#当前的路径长度
distance = 0
#已知的满足条件的最优路径
rdistance = 9999
#当前的养路费
cost = 0
#已知的满足条件的最优路径的养路费
rcost = 1500

#求在权值为data时，最短路径的长度，求出每个点到城市乙的
#无约束条件下的极小值，作为分支定界问题的下界
def getlbound(data) :
    C = np.array(data)
    for i in range(50) :
        for j in range(50) :
            for k in range(50) :
                if C[i][j] > C[i][k] + C[k][j] :
                    C[i][j] = C[i][k] + C[k][j]
    return C[:49,49].tolist()
#最短距离，其中城市乙到城市乙的距离赋值为0
sd = getlbound(d1)
sd.append(0)
#最小养路费，其中城市乙到城市乙的养路费赋值为0
sc = getlbound(d2)
sc.append(0)

#判断当前结点k是否需要剪枝
def is_prune(k) :
    #声明全局变量
    global distance
    global cost
    global rdistance
    global d1
    global d2
    global path
    #判断是否存在路径
    if d1[path[-1]][k] == 9999 :
        return 1
    #判断当前路径长度的下界是否比已知最好情况还要差
    if d1[path[-1]][k] + distance + sd[k] > rdistance :
        return 1
    #判断当前路径养路费用的下界是否超过了约束条件
    if d2[path[-1]][k] + cost + sc[k] > 1500 :
        return 1

    #若满足上下界，则无需剪枝
    return 0

#分枝定界算法
def branch_bound() :
    #声明全局变量
    global distance
    global cost
    global rdistance
    global d1
    global d2
    global path
    global rpath
    global rcost

    #如果路径的终点为城市乙，则保存当前状态，返回
    if path[-1] == 49 :
        rdistance = distance
        rcost = cost
        rpath = copy.copy(path)
        return

    #否则从城市乙开始遍历，判断每个城市其是否满足上下界
    for j in range(49) :
        i = 49-j
        #根据上下界，判断是否需要剪枝
        if is_prune(i) == 0 :
            #更新当前的状态
            distance +=  d1[path[-1]][i]
            cost += d2[path[-1]][i]  
            path.append(i) 
            #无需剪枝则继续搜索       
            branch_bound()
            #搜索完成后，撤销之前的更新
            path.pop()
            distance -= d1[path[-1]][i]
            cost -= d2[path[-1]][i]

def main() : 
    branch_bound()
    #输出当前的路径序列
    print(rpath)
    #输出当前路径序列的长度
    print(rdistance)
    #输出当前路径的总的养路费
    print(rcost)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print(end - start)
