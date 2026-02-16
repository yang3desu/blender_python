# 漫画背景線画抽出用スクリプト
# --------------------------------------------------
# クラスとか関数にまとめてしまうとn年後にいじろうとしたときにわけわからないので、ベタ書き繰り返し上等です。マルチカーソルを使って手直ししてください。



# bpyをインポートし、シーンを操作できるようにする
import bpy

# Fleestyleで捉えきれない線を取得するため、オブジェクトをどぎつい色で塗る（のちほどコンポジットノードで、色の差から境界線を抽出し、補助線画を出力する）
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
bpy.context.scene.display.shading.light = 'MATCAP'
bpy.context.scene.display.shading.studio_light = 'check_normal+y.exr'
bpy.context.scene.display.shading.color_type = 'OBJECT'

# 背景を白に。（黒く塗りつぶされてしまうの防止）
bpy.context.scene.world.color = (0.999999, 0.999999, 1)


# --------------------------------------------------
# Freestyleの調整
# --------------------------------------------------

# --------------------------------------------------
# 初期設定

bpy.context.scene.render.use_freestyle = True
bpy.context.scene.render.line_thickness = 6

freestyle = bpy.context.scene.view_layers[0].freestyle_settings
freestyle.as_render_pass = True
linesets =  freestyle.linesets

# 一旦クリア
for n in linesets:
    linesets.remove(n)



# --------------------------------------------------
# 輪郭用ラインセットを追加

styleOutline = freestyle.linesets.new('outline')

# 描画するのは輪郭・外部輪郭
styleOutline.select_silhouette = False # 一旦リセット
styleOutline.select_crease = False # 一旦リセット
styleOutline.select_border = False # 一旦リセット

styleOutline.select_contour = True
styleOutline.select_external_contour = True

# インク溜まりを追加
kabuOutline = styleOutline.linestyle.thickness_modifiers.new('kabuOutline', 'ALONG_STROKE')
kabuOutline.mapping = 'CURVE'
kabuOutline.curve.curves[0].points.new(0,0)
kabuOutline.curve.curves[0].points.new(0,0)
kabuOutline.curve.curves[0].points[0].location = (0, 1.0000)
kabuOutline.curve.curves[0].points[1].location = (0.25, 0.5)
kabuOutline.curve.curves[0].points[2].location = (0.75, 0.5)
kabuOutline.curve.curves[0].points[3].location = (1.0000, 1.0000)

# 筆圧による遠近法を追加
distOutline = styleOutline.linestyle.thickness_modifiers.new('distOutline', 'DISTANCE_FROM_CAMERA')
distOutline.invert = True
distOutline.range_max = 10
distOutline.value_min = 0.3

# 手ブレを追加
noiseOutline = styleOutline.linestyle.thickness_modifiers.new('noiseOutline', 'NOISE')
noiseOutline.amplitude = 0.1
noiseOutline.period = 1



# --------------------------------------------------
# 物体の内側用ラインセットを追加

styleInline = freestyle.linesets.new('Inline')

# 描画するのはクリース・辺マーク・マテリアル境界
styleInline.select_silhouette = False # 一旦リセット
styleInline.select_crease = False # 一旦リセット
styleInline.select_border = False # 一旦リセット

styleInline.select_crease = True
styleInline.select_edge_mark = True
styleInline.select_material_boundary = True

# インク溜まりを追加
kabuInline = styleInline.linestyle.thickness_modifiers.new('kabuInline', 'ALONG_STROKE')
kabuInline.mapping = 'CURVE'
kabuInline.curve.curves[0].points.new(0,0)
kabuInline.curve.curves[0].points.new(0,0)
kabuInline.curve.curves[0].points[0].location = (0, 0.5000)
kabuInline.curve.curves[0].points[1].location = (0.25, 0.25)
kabuInline.curve.curves[0].points[2].location = (0.75, 0.25)
kabuInline.curve.curves[0].points[3].location = (1.0000, 0.5000)

# 手ブレを追加
noiseInline = styleInline.linestyle.thickness_modifiers.new('noiseInline', 'NOISE')
noiseInline.amplitude = 0.1
noiseInline.period = 1



# --------------------------------------------------
# コンポジットノードの調整
# --------------------------------------------------

# --------------------------------------------------
# ■初期設定

tree = bpy.data.node_groups

node_tree = tree.new(name="COMP", type="CompositorNodeTree")
bpy.context.scene.compositing_node_group = node_tree
nodes = node_tree.nodes

# 一旦クリア
for n in nodes:
    nodes.remove(n)

# --------------------------------------------------
# ■ノードを追加していく

# 追加　入力→レンダーレイヤー
inNode = nodes.new(type='CompositorNodeRLayers')
inNode.location = (0, 0)

# 追加　出力→ファイル出力
outNode = nodes.new(type='CompositorNodeOutputFile')
outNode.directory = "//cmp/"
outNode.file_name = "line_sobel"
# outNode.file_name("line_freestyle")
outNode.location = (400, -300)

# 追加　フィルター→フィルター
soNode = nodes.new(type='CompositorNodeFilter')
soNode.inputs[2].default_value = 'Sobel'
soNode.location = (300, 0)

# 追加　コンバーター→カラーランプ
coNode = nodes.new(type='ShaderNodeValToRGB')
coNode.color_ramp.elements[0].color = (1, 1, 1, 0)
coNode.color_ramp.elements[0].position = 0.45
coNode.color_ramp.elements[1].color = (0, 0, 0, 1)
coNode.color_ramp.elements[1].position = 0.55
coNode.location = (500, 0)


# --------------------------------------------------
# ■ノード同士をつなげていく
links = node_tree.links

# リンク　レンダーレイヤの画像ー→ソーベル→カラーランプ→ファイル出力
links.new(inNode.outputs[0], soNode.inputs[1])
links.new(soNode.outputs[0], coNode.inputs[0])

outNode.name = 'images_exporter'

next_index = len(outNode.outputs)
outNode.file_output_items.new('RGBA', 'Color')
links.new(coNode.outputs[0], outNode.inputs[next_index])


# リンク　レンダーレイヤーのFreestyle→ファイル出力
# links.new(inNode.outputs[2], outNode.inputs[1])




