# 2次元プロットデータ（3クラス）のデータを読み込んで，k-means法でクラスタリングする
import numpy as np
import matplotlib.pyplot as plt

def main():
  # データを読み込む
  with open('iris.data') as f:
    str = f.readlines()

  data = str
  for i in range(len(data)):
    data[i] = data[i].strip().split(',')
    data[i] = data[i][0:4]

  #//スライスを使おう!
  print(data)
  print('\nスライス')
  data = np.array(data)
  print(data)

if __name__=="__main__":
  main()
