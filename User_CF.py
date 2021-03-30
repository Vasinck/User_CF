import numpy as np


def LoadDatas():
    # 用户
    datas = [
        [5, 4, 3, 2, 1, 0, 5],
        [3, 1, 0, 1, 5, 5, 0],
        [4, 0, 5, 0, 1, 1, 0],
        [2, 3, 0, 5, 4, 1, 5],
        [1, 0, 1, 0, 5, 5, 3],
        [5, 3, 2, 1, 0, 3, 5],
        [0, 5, 2, 3, 4, 5, 0],
    ]
    goods = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
    ]
    datas = np.array(datas)
    return datas, goods


def GetDistance(user, datas):
    distances = np.tile(user, (np.shape(datas)[0], 1)) - datas
    distances = distances ** 2
    distances = np.sum(distances, axis=1)
    distances = distances ** 0.5

    return distances


def Normalization(distances):
    distances = np.ones(np.shape(distances)) / (1 + distances)

    return distances


def Recommend(user, datas, distances, goods):
    recommends_item = []
    k = len(list(temp for temp in distances if temp >
                 sum(distances)/len(distances)))
    user_argsort = np.argsort(-distances)
    distance_sum = 0
    data_sum = np.zeros((np.shape(user)))
    # 获得用户与邻居的相关度的总和
    for each_distance in range(k):
        distance_sum += distances[user_argsort[each_distance]]

    # 得到邻居的各个商品加权值
    for each_item in range(k):
        data = datas[user_argsort[each_item]]
        data = data * distances[user_argsort[each_item]]
        data = data / distance_sum
        data_sum += data*(7-each_item)

    # 得到推荐商品的列表
    recommends_good_arg = np.argsort(-data_sum)
    for each_recommend_good in range(k):
        each_item = goods[recommends_good_arg[each_recommend_good]]
        if user[recommends_good_arg[each_recommend_good]] < 4:
            recommends_item.append(each_item)

    return recommends_item


datas, goods = LoadDatas()
user = np.array([1, 1, 2, 1, 3, 0, 5])
distances = Normalization(GetDistance(user, datas))
recommends_item = Recommend(user, datas, distances, goods)
if recommends_item:
    print('需要给这个用户推荐的内容商品是：', end='')
    for each_item in recommends_item:
        print('商品' + each_item + '  ', end='')
else:
    print('此用户不需要推荐商品...')
