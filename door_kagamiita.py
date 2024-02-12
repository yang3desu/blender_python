# 平面＞鏡板化スクリプト
# --------------------------------------------------
# ドアをドアっぽくするスクリプト。

# 基本、編集モードで使用。
# 2パネルタイプドアを作成する場合、
# ドアの扉1枚のうち、平たい「面」部分（1平方メートル）を、
# 細分化などで「田」の字のように4つに分割する。
# 分割した一つの面を撰択し、このスクリプトを実行する。

# 好みに応じて頂点を動かし、調整して使用。

# クラスとか関数にまとめてしまうとn年後にいじろうとしたときにわけわからないので、ベタ書き繰り返し上等です。マルチカーソルを使って手直ししてください。



# bpyをインポートし、シーンを操作できるようにする
import bpy

# 編集モードでない場合は、編集モードに変更
bpy.ops.object.mode_set(mode='EDIT')

# 鏡板でない「上桟・下桟・小桟・框」部分を作成（面を差し込む I）
bpy.ops.mesh.inset(thickness=0.03, depth=0)

# 斜めに切り込む装飾を作成（面を差し込む I、移動 G）
bpy.ops.mesh.inset(thickness=0.02, depth=0)
bpy.ops.transform.translate(value = (0,0,-0.03))

# 余白を作成（面を差し込む I）
bpy.ops.mesh.inset(thickness=0.01, depth=0)

# 斜めに切り込む装飾を作成（面を差し込む I、移動 G）
bpy.ops.mesh.inset(thickness=0.01, depth=0)
bpy.ops.transform.translate(value = (0,0,-0.01))

# 直角に切り込む装飾を作成（押し出し E）
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -0.01)})

# 直角に出っ張りを作成（面を差し込む I、押し出し E）
bpy.ops.mesh.inset(thickness=0.01, depth=0)
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.01)})
# 出っ張りを直角に引っ込める（面を差し込む I、押し出し E）
bpy.ops.mesh.inset(thickness=0.01, depth=0)
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -0.01)})
