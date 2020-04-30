####################
#山火事シミュレーション v1.2 by K.Sakurai 2020.4.29
#Using Python Mode for Processing 3
#
#ウィルス流行シミュレーションを削る方向にいじったら山火事シミュレーションができました．
#アドバンシング物理の山火事モデルを試すことができます．
####################

import copy

#パラメータ入力
n_siz = 101 #モデルのサイズ（奇数にしてください）
n_void = 0.6 #空隙率（初期値）

wait_time = 0 #待ち時間

#箱庭とかの用意（n_siz x n_sizの二次元配列）
cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 
burned = 0

def setup():
    size(n_siz*8, n_siz*8) #ウィンドウサイズは808x808（1セル8x8）
    background(255)
    
    initialize()
                            
def draw():
    
    global cells
    global burned
    
    cells_next = [[0 for i in range(n_siz)] for j in range(n_siz)] 

    
    #drawでは，表示をリフレッシュして次の状態をcells_nextに作る
    for i in range(n_siz):
        for j in range(n_siz):
            
            #表示のリフレッシュ
            paint(i, j)
            
            #☆状態書き出し（更新予定）
            
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
        #println("stopped")
    else:
        burned = burn_now
    
    delay(wait_time)
    
    #フレーム撮影する場合は下の1行のコメントアウトを外す（処理遅くなる）
    #saveFrame("frames/######.png")

#セルの状態を読み取り，塗る色を決める関数
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
    cells = [[0 for i in range(n_siz)] for j in range(n_siz)] 
    global cells
    noLoop()
    delay(100)
    initialize()
    loop()

def initialize():
    
    global cells
    
    #中央に種火
    cells[(n_siz - 1) / 2][(n_siz - 1) / 2] = 1
    
    #空隙を用意（全セル数x空隙率だけ空隙セルを作成）
    index = 0
    while index < n_siz * n_siz * n_void:
        hit = floor(random(0, n_siz * n_siz))
        if cells[floor(hit / n_siz)][hit % n_siz] == 0:
            cells[floor(hit / n_siz)][hit % n_siz] = 3
            index += 1
    
    #境目の点をつける
    stroke(0)
    for i in range(n_siz - 1):
        for j in range(n_siz - 1):
            point(j*8+7, i*8+7)

    #以降，枠線はつけない
    noStroke()
