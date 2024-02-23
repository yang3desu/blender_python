import bpy
import bmesh
from math import radians

# デバッグ用
print("##############################")
# bpy.ops.mesh.select_all(action='SELECT')
# bpy.ops.mesh.delete(type='VERT')


##############################

kabe_takasa=2 # 壁の平たい面の高さ
kabe_haba=4 # 壁の平たい面の幅
kabe_atsumi=0.1 # 壁の厚み
dan=0.01 # 段々の1個の長さ及び高さ
dansu=5 # 段々の数

##############################


# メッシュの追加（メッシュがないと編集モードに入れないため）
bpy.ops.mesh.primitive_cube_add()

# 編集モードに切り替え
bpy.ops.object.mode_set(mode='EDIT')

# デバッグ用
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')

# bmeshオブジェクトに変換
bm = bmesh.from_edit_mesh(bpy.context.object.data)



#-----------------------------
# 平らな面を作る（kabe_taksaの高さ）
#-----------------------------

i=0
v = [None] * 4  # vリスト初期化
#点を打つ座標
ten=[(0, 0, 0)
	 ,(0, kabe_haba, 0)
	 ,(0, kabe_haba, kabe_takasa)
	 ,(0, 0, kabe_takasa)]

# 4点を打って面を貼る
for i in range(4): # range(4)は4回繰り返し(0~3)
	v[i]=bm.verts.new(ten[i])
	v[i].select = True

# 辺をつなげる
bpy.ops.mesh.edge_face_add()
# すべての面の選択を外しておく
bpy.ops.mesh.select_all(action='DESELECT')

# 次の面のために頂点を撰択
v[2].select = True
v[3].select = True



#-----------------------------
# 段々になっている場所を作る
#-----------------------------

i=0
j=1
v = [None] * 4  # vリスト初期化

for i in range(dansu):
	j=i+1
	#点を打つ座標
	ten=[(0+dan*j, 0+dan*j, kabe_takasa+dan*i)
		,(0+dan*j, kabe_haba-dan*j, kabe_takasa+dan*i)
		,(0+dan*j, 0+dan*j, kabe_takasa+dan*j)
		,(0+dan*j, kabe_haba-dan*j, kabe_takasa+dan*j)]
	print(ten)

	# 水平の辺を貼る
	v[0]=bm.verts.new(ten[0]) #2点を打つ
	v[1]=bm.verts.new(ten[1]) #2点を打つ
	v[0].select = True #点を撰択
	v[1].select = True #点を撰択
	bpy.ops.mesh.edge_face_add() # 面を貼る
	bpy.ops.mesh.select_all(action='DESELECT') #選択解除
	v[0].select = True #点を撰択
	v[1].select = True #点を撰択

	# 垂直の辺を貼る
	v[2]=bm.verts.new(ten[2]) #2点を打つ
	v[3]=bm.verts.new(ten[3]) #2点を打つ
	v[2].select = True #点を撰択
	v[3].select = True #点を撰択
	bpy.ops.mesh.edge_face_add() # 面を貼る
	bpy.ops.mesh.select_all(action='DESELECT') #選択解除
	v[2].select = True #点を撰択
	v[3].select = True #点を撰択
