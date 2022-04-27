#smc_assignment.py
import part_1
import part_2
import streamlit as st
PAGES = {
    "Part 1": part_1,
    "Part_2": part_2
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()