import streamlit as st
from multiapp import MultiApp
from apps import login,schemas

app = MultiApp()
app.add_app("Login", login.app)
#app.add_app("Schemas", schemas.app)
app.run()