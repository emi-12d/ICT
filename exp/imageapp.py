import streamlit as st
import os
import base64 # 画像データの変換

import io
import resvg_py # png変換
from PIL import Image # JPEG変換

st.title("🖼️ 画像アプリ")
st.write("サイドバーから表示した画像を選択してください。")

# 画像データのルートフォルダのパス
IMAGE_DIR_ROOT = "images"

# 分類メニューをサイドバーに作成する
st.sidebar.markdown("### 画像分類メニュー")

if not os.path.exists(IMAGE_DIR_ROOT):
    st.error(f"エラー: 画像フォルダ '{IMAGE_DIR_ROOT}' が見つかりません。")
    st.stop()

current_path = IMAGE_DIR_ROOT
selected_folder_names = []
display_folder_names = []

depth = 1
while True:
    sub_dirs = [f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))]
    sub_dirs.sort()
    # 中にフォルダがなければ画像のある階層とみなす
    if not sub_dirs: 
        break
    # 表示名の作成（番号を抜いた形）
    folder_map = {d.split("_", 1)[-1] if "_" in d else d: d for d in sub_dirs}
    selected_dir = st.sidebar.selectbox(
        f"📂 階層 {depth}", 
        list(folder_map.keys()), 
        key=f"depth_{depth}_{current_path}"
    )
    actual_folder_name = folder_map[selected_dir]

    selected_folder_names.append(actual_folder_name)
    display_folder_names.append(selected_dir)

    current_path = os.path.join(current_path, actual_folder_name)
    depth += 1
category_path = current_path

if display_folder_names:
    title_text = " > ".join(display_folder_names)
    st.header(f"📂 {title_text}")
else:
    st.header("📂 ルートフォルダ")

st.markdown("___")

# 拡張子の選択　（.svg）
valid_extensions = (".svg")
image_files = [f for f in os.listdir(category_path) if f.lower().endswith(valid_extensions)]
image_files.sort()

if not image_files:
    st.warning(f"現在、'{title_text if selected_folder_names else 'ルートフォルダ'}' に表示できるSVG画像はありません。")
else:
    # 画像をグリッド状に表示する（3列）
    num_columns = 3
    rows = [image_files[i : i + num_columns] for i in range(0, len(image_files), num_columns)]

    for row_images in rows:
        cols = st.columns(num_columns)
        for i, img_filename in enumerate(row_images):
            full_img_path = os.path.join(category_path, img_filename)
            with cols[i]:
                try:
                    # 画像をバイナリデータとして読み込み、Base64という形式に変換します
                    with open(full_img_path, "rb") as file:
                        image_data = file.read()
                        base64_svg = base64.b64encode(image_data).decode("utf-8")
                    
                    # 高さ（height）200pxで中央揃え
                    html_code = f"""
                        <div style="height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                            <img src="data:image/svg+xml;base64,{base64_svg}" style="max-height: 100%; max-width: 100%; object-fit: contain;">
                        </div>
                    """
                    st.html(html_code)
                    # 表示名の作成
                    display_name = img_filename.replace(".svg", "")
                    st.caption(display_name)

                    btn_cols = st.columns(3)

                    # SVG用ボタン
                    with btn_cols[0]:
                        st.download_button(
                            label="📄 .svg",
                            data=image_data,
                            file_name=img_filename,
                            mime="image/svg+xml",
                            use_container_width=True # ボタンの幅を枠にピタッと合わせる
                        )
                    # PNG用ボタン（svglibを使って変換）
                    with btn_cols[1]:
                        # メモリ上でSVGデータを読み込み、PNGに変換
                        svg_string = image_data.decode("utf-8")
                        png_data = resvg_py.svg_to_bytes(svg_string=svg_string)
                        
                        st.download_button(
                            label="🖼️ .png",
                            data=png_data,
                            file_name=img_filename.replace(".svg", ".png"),
                            mime="image/png",
                            use_container_width=True
                        )

                    # JPEG用ボタン（svglibを使って変換）
                    with btn_cols[2]:
                        # PNGデータをPillowで開く
                        png_img = Image.open(io.BytesIO(png_data)).convert("RGBA")
                        # 真っ白な背景キャンバスを作成
                        bg = Image.new("RGBA", png_img.size, (255, 255, 255, 255))
                        # 白背景の上に画像を貼り付ける
                        bg.paste(png_img, (0, 0), png_img)
                        # JPEG専用の形式（RGB）に変換してデータを保存
                        jpeg_io = io.BytesIO()
                        bg.convert("RGB").save(jpeg_io, format="JPEG")
                        jpeg_data = jpeg_io.getvalue()
                        
                        st.download_button(
                            label="🖼️ .jpg",
                            data=jpeg_data,
                            file_name=img_filename.replace(".svg", ".jpeg"),
                            mime="image/jpeg",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"画像の読み込みエラー: {img_filename} - {e}")