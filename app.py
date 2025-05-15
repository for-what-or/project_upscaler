import streamlit as st
import src.interface as interface

pages = [
    st.Page(interface.main, title="Главная"),
]

pg = st.navigation(pages)
pg.run()