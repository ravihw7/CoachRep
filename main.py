import streamlit as st
from services.auth.login_wall import render_login_wall


def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="CoachRep - AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    if not render_login_wall():
        return


if __name__ == "__main__":
    main()