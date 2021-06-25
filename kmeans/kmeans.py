# 2次元プロットデータ（3クラス）のデータを読み込んで，k-means法でクラスタリングする
import numpy as np
import matplotlib.pyplot as plt

# 2点間距離を測る関数
def distance(a, b):
    dist = 0.0
    for i in range(len(a)):
        dist += (a[i] - b[i]) ** 2
    dist = np.sqrt(dist)
    return dist

##初めの重心を決める
def initCenterCluster(data,k):
  center = np.zeros((k,2)) #クラスタの重心
  labelCount = np.zeros(k) #同じラベルの総和

  for i,d in enumerate(data):
    rand = np.random.randint(0,k,1)
    center[rand] += d
    labelCount[rand] += 1 

  for (c,i) in zip(center,range(k)):
    c /= labelCount[i]
    #c = ((c - 0.5) * 2) + 0.5 #上だと，点が左上に移動するから，点を0,0に移して倍率して戻す．だめでした

  return center


def main():
  # データを読み込む
  data = np.loadtxt("data2.csv", delimiter=",")

  #\my code\
  k = 4 #重心の数
  ##いろ
  cmap_name = 'tab20'
  cm = plt.cm.get_cmap(cmap_name)
  colors = []
  for rgb in cm.colors:
    colors.append(list(rgb))

  ##重心の初期
  center = initCenterCluster(data,k) #クラスタの重心
  before = np.zeros((k,2)) #前回のクラスタの重心
  labelCount = np.zeros(k) #同じラベルの総和

  ## kmeansの核
  while(not np.all(center == before)):
    label = [] #各データのラベル
    before = np.copy(center) #重心の保存
    labelCount = np.zeros(k) #同じラベルの総和
    for i,d in enumerate(data):
      dist = [distance(d,i) for i in center] #データの点と重心を比較
      label.append(dist.index(min(dist))) #距離が小さい方のインデクスをラベル付け

    center = np.zeros((k,2)) #新しいクラスタの重心
  
    ##重心の割り出しとラベルのカウント
    for i,d in enumerate(data):
      center[label[i]]+=d
      labelCount[label[i]]+=1
 
    for (c,i) in zip(center,range(k)):
      if(labelCount[i]==0):
        c = before[i]/1
        continue
      c /= labelCount[i]

    #クラスタが規定数なかったらやり直し
    if(np.sum(np.isnan(center))):
      center = initCenterCluster(data,k)
      continue

  #グラフ表示
  for (d,l) in zip(data, label):
    plt.scatter(d[0],d[1],c=[colors[l]],s=10,alpha=0.25)

  for i,c in enumerate(center):
    plt.scatter(c[0],c[1],c=[colors[i]],marker='x',s=25)

  plt.show()

if __name__ == "__main__":
  main()
