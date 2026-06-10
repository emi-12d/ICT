import streamlit as st
import os
import base64 # 画像データの変換

import io
import resvg_py # png変換
from PIL import Image # JPEG変換



st.title("🖼️ 画像アプリ")

# 画像データのルートフォルダのパス
IMAGE_DIR_ROOT = "images"

# 分類メニューをサイドバーに作成する
st.sidebar.markdown("### 画像分類メニュー")

if not os.path.exists(IMAGE_DIR_ROOT):
    st.error(f"エラー: 画像フォルダ '{IMAGE_DIR_ROOT}' が見つかりません。")
    st.stop()

categories = [f for f in os.listdir(IMAGE_DIR_ROOT) if os.path.isdir(os.path.join(IMAGE_DIR_ROOT, f))]
categories.sort()

if not categories:
    st.warning(f"現在、'{IMAGE_DIR_ROOT}' の中に表示できる分類（フォルダ）はありません。")
    st.stop()

# サイドバーにラジオボタンを作成
selected_category = st.sidebar.radio("表示する分類を選択", categories)
# メイン画面の表示
category_path = os.path.join(IMAGE_DIR_ROOT, selected_category)
st.header(f"📂 {selected_category}")
st.markdown("___")

# 拡張子の選択　（.svg）
valid_extensions = (".svg")
image_files = [f for f in os.listdir(category_path) if f.lower().endswith(valid_extensions)]
image_files.sort()

if not image_files:
    st.warning(f"現在、分類 '{selected_category}' に表示できるSVG画像はありません。")
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
                        # 背景を白（0xFFFFFF）に指定してJPEGに変換
                        # 1. resvg_pyで作った綺麗なPNGデータをPillowで開く
                        png_img = Image.open(io.BytesIO(png_data)).convert("RGBA")
                        # 2. 真っ白な背景キャンバスを作成
                        bg = Image.new("RGBA", png_img.size, (255, 255, 255, 255))
                        # 3. 白背景の上に画像を貼り付ける（透明部分が白になる）
                        bg.paste(png_img, (0, 0), png_img)
                        # 4. JPEG専用の形式（RGB）に変換してデータを保存
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