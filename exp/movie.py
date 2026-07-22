import streamlit as st
import os

st.title("🎬 動画アプリ")
st.write("サイドバーから表示したい動画のカテゴリを選択してください。")

MOVIE_DIR_ROOT = "movie"

# 分類メニューをサイドバーに作成する
st.sidebar.markdown("### 動画分類メニュー")

if not os.path.exists(MOVIE_DIR_ROOT):
    st.error(f"エラー: 動画フォルダ '{MOVIE_DIR_ROOT}' が見つかりません。")
    st.stop()

current_path = MOVIE_DIR_ROOT
selected_folder_names = []
display_folder_names = []

depth = 1
while True:
    sub_dirs = [f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))]
    sub_dirs.sort()
    # 中にフォルダがなければ動画のある階層とみなす
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

# 対応する動画の拡張子を指定（.mp4, .mov, .avi など）
valid_extensions = (".mp4", ".mov", ".avi", ".mkv")
video_files = [f for f in os.listdir(category_path) if f.lower().endswith(valid_extensions)]
video_files.sort()

if not video_files:
    st.warning(f"現在、'{title_text if selected_folder_names else 'ルートフォルダ'}' に表示できる動画ファイルはありません。")
else:
    # 動画を2列のグリッド状に表示する
    num_columns = 2
    rows = [video_files[i : i + num_columns] for i in range(0, len(video_files), num_columns)]

    for row_videos in rows:
        cols = st.columns(num_columns)
        for i, video_filename in enumerate(row_videos):
            full_video_path = os.path.join(category_path, video_filename)
            with cols[i]:
                # 動画のタイトル
                display_name = os.path.splitext(video_filename)[0]
                display_name = display_name.split("_", 1)[-1] if "_" in display_name else display_name
                st.subheader(display_name)
                
                # 実際の動画ファイルをプレイヤーで表示
                st.video(full_video_path)
                
                # 必要に応じてダウンロードボタン等も追加できます
                with open(full_video_path, "rb") as file:
                    st.download_button(
                        label="📥 動画をダウンロード",
                        data=file,
                        file_name=video_filename,
                        mime="video/mp4",
                        use_container_width=True,
                        key=f"download_{full_video_path}"
                    )