# 2次元プロットデータ（3クラス）のデータを読み込んで，k-means法でクラスタリングする
import numpy as np
import copy
import matplotlib.pyplot as plt


def data2list(data):
  #数値部分のみ取り出す．
  for i in range(len(data)):
    data[i] = data[i].strip().split(',')
    data[i] = data[i][0:4]
    data[i] = list(map(float,data[i]))

  data = np.array(data)
  
  return data

# 2点間距離を測る関数
def distance(a, b):
    dist = 0.0
    for i in range(len(a)):
        dist += (a[i] - b[i]) ** 2
    dist = np.sqrt(dist)
    return dist

##初めの重心を決める
def initCenterCluster(data,k,dim):
  center = np.zeros((k,dim)) #クラスタの重心
  labelCount = np.zeros(k) #同じラベルの総和

  for i,d in enumerate(data):
    rand = np.random.randint(0,k,1)
    center[rand] += d
    labelCount[rand] += 1 
    #print(rand,"init:",d)

  for (c,i) in zip(center,range(k)):
    c /= labelCount[i]
    c = ((c - 0.5) * 2) + 0.5 #上だと，点が左上に移動するから，点を0,0に移して倍率して戻す．だめでした
  #print("center:\n",center)

  return center

def clustering(data,k,dim):
  #重心の初期化
  center = initCenterCluster(data,k,dim) #クラスタの重心
  before = np.zeros((k,dim)) #前回のクラスタの重心
  labelCount = np.zeros(k) #同じラベルの総和

  ## kmeansの核
  while(not np.all(center == before)):
    label = [] #各データのラベル
    before = center #重心の保存
    labelCount = np.zeros(k) #同じラベルの総和
    for i,d in enumerate(data):
      dist = [distance(d,i) for i in center] #データの点と重心を比較
      label.append(dist.index(min(dist))) #距離が小さい方のインデクスをラベル付け
      #print(i + 1,'dist:',dist.index(min(dist)),dist,d)

    center = np.zeros((k,dim)) #新しいクラスタの重心
  
    ##重心の割り出しとラベルのカウント
    for i,d in enumerate(data):
      center[label[i]]+=d
      labelCount[label[i]]+=1
 
    for (c,i) in zip(center,range(k)):
      c /= labelCount[i]

    #クラスタが規定数なかったらやり直し
    if(np.sum(np.isnan(center))):
      center = initCenterCluster(data,k,dim)
      continue

  print("Center Position")
  print(center)
  return data,label

def main():
  clust = 3
  dimension = 4

  path = 'iris.data'
  with open(path) as f:
    stri = f.readlines()
  stri.remove('\n')
  data = copy.copy(stri)
  data = data2list(data)
  print(data)  # データを読み込む

  print(data[0],data[1])
  print(distance(data[0],data[1]))

  data,label = clustering(data,clust,dimension)


  fout = open("clust_iris.data",'w')
  for (s,l) in zip(stri,label):
    disp = str(s[:-1]) + ' ,cluster' + str(l)
    print(disp)
    fout.write(disp + '\n')
  fout.close()

  colors = ["red","blue","green"]
  for (d,l) in zip(data, label):
    plt.scatter(d[0],d[1],c=colors[l],s=10,alpha=0.25)
  plt.show()

  for (d,l) in zip(data, label):
    plt.scatter(d[0],d[2],c=colors[l],s=10,alpha=0.25)
  plt.show()

  for (d,l) in zip(data, label):
    plt.scatter(d[0],d[3],c=colors[l],s=10,alpha=0.25)
  plt.show()

  for (d,l) in zip(data, label):
    plt.scatter(d[1],d[2],c=colors[l],s=10,alpha=0.25)
  plt.show()

  for (d,l) in zip(data, label):
    plt.scatter(d[1],d[3],c=colors[l],s=10,alpha=0.25)
  plt.show()

  for (d,l) in zip(data, label):
    plt.scatter(d[2],d[3],c=colors[l],s=10,alpha=0.25)
  plt.show()


if __name__ == "__main__":
  main()
