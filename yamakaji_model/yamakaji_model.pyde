####################
#山火事シミュレーション v1.6.2 by K.Sakurai 2020.4.29
#Using Python Mode for Processing 3
#
#ウィルス流行シミュレーションを削る方向にいじったら山火事シミュレーションができました．
#アドバンシング物理の山火事モデルを試すことができます．
#クリックでリセットして再スタート，
####################

import copy
import random

#パラメータ入力
n_siz = 101 #モデルのサイズ（奇数にしてください）
n_void = 0.5 #空隙率（初期値，1以上はエラーになる）

wait_time = 0 #待ち時間

#箱庭とかの用意（n_siz x n_sizの二次元配列）
cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 
burned = 0

def setup():
    size(n_siz*8, n_siz*8 + 120) #1セル8x8からウィンドウサイズを導出
    background(255)
    
    #フォントじゅんび
    myFont = createFont("メイリオ", 48)
    textFont(myFont)
    
    #しょきか
    initialize()
    
    delay(wait_time)
                            
def draw():
    
    global cells
    global burned
    
    cells_next = [[0 for i in range(n_siz)] for j in range(n_siz)] 

    
    #drawでは，表示をリフレッシュして次の状態をcells_nextに作る

            #☆移動処理（更新予定）

            #☆感染処理

            #そのセルが木なら，nextはそのまま木に．
            #if cells[i][j] == 0:
            #    cells_next[i][j] =0
            
    for i in range(n_siz):
        for j in range(n_siz):
            
            #そのセルが火なら，そのセルと接触セルは全て火に
            if cells[i][j] == 1:
                if i > 0 and j > 0 :
                    cells_next[i-1][j-1] = 1
                if i > 0:
                    cells_next[i-1][j] = 1
                if i > 0 and j < n_siz - 1:
                    cells_next[i-1][j+1] = 1
                if j > 0:
                    cells_next[i][j-1] = 1
                    
                cells_next[i][j] = 1
                
                if j < n_siz - 1:
                    cells_next[i][j+1] = 1
                if i < n_siz - 1 and j > 0:
                    cells_next[i+1][j-1] = 1
                if i < n_siz - 1:
                    cells_next[i+1][j] = 1
                if i < n_siz - 1 and j < n_siz - 1:
                    cells_next[i+1][j+1] = 1
        
    for i in range(n_siz):
        for j in range(n_siz):
            #そのセルが空隙なら，火が燃え移ってもも空隙（上書き）
            if cells[i][j] == 3:
                cells_next[i][j] = 3

    
    #全セルの処理が終わったらcells_nextをcellsに移す
    cells = copy.deepcopy(cells_next)
    del cells_next
    
    #燃えた数が0ならばループを止める
    burn_now = sum(v.count(1) for v in cells) 
    
    if burn_now == burned:
        noLoop()
        println("stopped")
    else:
        burned = burn_now
        
    #表示のリフレッシュ
    for i in range(n_siz):
        for j in range(n_siz):
            paint(i, j)
    
    fill(192)
    rect(0, n_siz*8, n_siz*8, 60)
    fill(0)
    text("Burned: " + str(burned) + "(" + str(round(burned / (n_siz * n_siz * (1.0 - n_void))*100, 2)) + "%)", 8, n_siz*8 + 48)
    
    #☆状態書き出し（更新予定）
            
   
    delay(wait_time)
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す（処理遅くなる）
    #saveFrame("frames/######.png")

#セルを塗る関数
def paint(i, j):
    global cells
    
    #セルの色を指定
    if cells[i][j] == 0:    #0は木（緑）
        fill(0, 255, 0)
    elif cells[i][j] == 1:    #1は火（赤）
        fill(255, 0, 0)
    elif cells[i][j] == 3:    #3は空隙（黒）
        fill(0)
    else:               #それ以外はわからん（灰：出たらバグ）
        fill(128)
        
    #セルを塗る
    rect(8*j, 8*i, 7, 7)
    

#クリックしたら，配列をリセットしてinitializeから
def mousePressed():
    global cells
    global n_void
    
    cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 
    noLoop()
    delay(200)
    initialize()

    loop()

def initialize():
    
    global cells
    
    #空隙を用意（全セル数x空隙率だけ空隙セルを作成）
    if n_void <= 0.5:
        cells = [[0 for i in range(n_siz)] for j in range(n_siz)]
        k = int(round(n_siz * n_siz * n_void))
        hits = random.sample(range(n_siz * n_siz - 1), k)
        for hit in hits:
            if hit < ((n_siz * n_siz - 1) / 2):
                cells[hit / n_siz][hit % n_siz] = 3
            else:
                cells[(hit + 1) / n_siz][(hit + 1) % n_siz] = 3
    else:
        cells = [[3 for i in range(n_siz)] for j in range(n_siz)]
        k = int(round(n_siz * n_siz * (1 - n_void)))
        hits = random.sample(range(n_siz * n_siz - 1), k)
        for hit in hits:
            if hit < ((n_siz * n_siz - 1) / 2):
                cells[hit / n_siz][hit % n_siz] = 0
            else:
                cells[(hit + 1) / n_siz][(hit + 1) % n_siz] = 0
    
    #中央に種火
    cells[(n_siz - 1) / 2][(n_siz - 1) / 2] = 1
    

                    
    #境目の点をつける
    stroke(0)
    for i in range(n_siz - 1):
        for j in range(n_siz - 1):
            point(j*8+7, i*8+7)

    #以降，枠線はつけない
    noStroke()
    
    #最初の表示
    for i in range(n_siz):
        for j in range(n_siz):
            paint(i, j)
            
    fill(192)        
    rect(0, n_siz*8, n_siz*8, 120)
    fill(0)
    text(str((1 - n_void)*100) + "%trees", 8, n_siz*8 + 108)
