import streamlit as st
from multiapp import MultiApp
import login

app = MultiApp()
app.add_app("Login", login.app)
#app.add_app("Schemas", schemas.app)
app.run()
