import streamlit as st
import streamlit_authenticator as stauth


st.set_page_config(page_title="ICT教材バンク")

if "credentials" in st.secrets:
    config = st.secrets.to_dict()
else:
    print("Secretsが見つかりませんでした")


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

# ログイン成功
if st.session_state["authentication_status"]:
    username = st.session_state["username"]

    user_role = config['credentials']['usernames'][username].get('role', 'student')

    # サイドバーに表示する項目
    home = st.Page("exp/home.py", title="ホーム", default=True, icon="🏠")
    calc_hub = st.Page("exp/mathapp.py", title="自動計算アプリ", icon="🧮")
    image_app = st.Page("exp/imageapp.py", title="画像アプリ", icon="🖼️")
    movie_app = st.Page("exp/movie.py", title="動画アプリ", icon="🎬")

    # 自動計算アプリの項目
    riemann = st.Page("pages/リーマン和.py", title="リーマン和")
    regression = st.Page("pages/重回帰分析.py", title="回帰分析")

    # サイドバーに表示させたくない項目
    pg = st.navigation(
        [home, calc_hub, image_app, movie_app, riemann, regression],
        position="hidden"
    )

    # サイドバーに表示したい項目
    with st.sidebar:
        st.write(f"{user_role}用")
        st.write("### メニュー")
        st.page_link(home)
        st.page_link(calc_hub)
        st.page_link(image_app)
        st.page_link(movie_app)

    pg.run()

    st.sidebar.markdown("___")
    authenticator.logout('ログアウト', "sidebar")


elif st.session_state["authentication_status"] is False:
    st.error('ユーザー名、またはパスワードが間違っています。')
elif st.session_state["authentication_status"] is None:
    st.warning('ユーザー名とパスワードを入力してください。')


