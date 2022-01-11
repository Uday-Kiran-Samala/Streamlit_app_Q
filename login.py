import streamlit as st
import numpy as np
from PIL import Image
import time
import cx_Oracle
import pandas as pd
#from apps import schemas


def oracle_single_connection(username, password, hostname, port, sid):
    dsn = cx_Oracle.makedsn(host=hostname, port=port, service_name=sid)
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("connected to the Oracle Database For Single Time")
    return connection


def oracle_connection_for_mainscreen(query, connection):
    df_ora = pd.read_sql(query, con=connection)
    return df_ora


def all_users(username, password, hostname, port, sid):
    extract_data = """SELECT username FROM DBA_USERS WHERE username NOT IN ( 'SYSTEM', 'SYS', 'APPQOSSYS', 'REMOTE_SCHEDULER_AGENT', 'DBSFWUSER', 'CTXSYS', 'SI_INFORMTN_SCHEMA', 'PUBLIC', 'AUDSYS', 'OJVMSYS', 'DVSYS', 'GSMADMIN_INTERNAL', 'ORDPLUGINS', 'ORDDATA', 'MDSYS', 'LBACSYS', 'OLAPSYS', 'OUTLN', 'ORACLE_OCM', 'XDB', 'WMSYS', 'ORDSYS', 'DBSNMP', 'DVF', 'APEX_030200', 'EXFSYS', 'OWBSYS', 'OWBSYS_AUDIT', 'SYSMAN', 'SCOTT') AND Account_status = 'OPEN' order by Username"""
    query_oracle = str(extract_data)
    connection = oracle_single_connection(username, password, hostname, port, sid)
    orac_df = oracle_connection_for_mainscreen(query_oracle, connection)
    lists_all_schemas = orac_df[orac_df.columns[0]].values.tolist()
    return connection, lists_all_schemas

def validate(username, password, hostname, port, sid):
    x = username
    y = password
    z = hostname
    a = port
    b = sid
    try:
        if x == '' or y == '' or z == '' or a == '' or b == '':
            st.error('Error : Please Enter Database Details')
        else:
            connection, all_schemas_list = all_users(x, y, z, a, b)
    except cx_Oracle.DatabaseError as x:
        st.error('Error : Invalid Credentials Please Try Again')

    return all_schemas_list

def app():
    schemas_list = []
    col1, col2, col3 = st.columns([2, 4, 1])
    with col2:
        st.title('QMIGRATOR')

    holder = st.empty()
    with holder.form("my_form"):
        user_input_schemaname = st.text_input("User Name(*)", '')
        user_input_password = st.text_input("Password(*)", '')
        user_input_hostname = st.text_input("Host Name(*)", '')
        user_input_port = st.text_input("Port(*)", '')
        user_input_servicename = st.text_input("Service Name(*)", '')
        submitted = st.form_submit_button("Next")
                                          #, on_click=validate, args=(user_input_schemaname, user_input_password, user_input_hostname, user_input_port, user_input_servicename))
    if submitted:
        schema_list = validate(user_input_schemaname, user_input_password, user_input_hostname, user_input_port, user_input_servicename)
        for i in schema_list:
            schemas_list.append(i)
        holder.empty()
        st.write(schemas_list)
        for schema in schema_list:
            st.checkbox(label=schema)




    # col1, col2, col3 = st.columns([2, 4, 1])
    # with col2:
    #     st.title('Schemas List')
    #
    # l2 = []
    # l2 = schemas_list[:]
    # l2.append('Select all')
    # state_dropdown = st.multiselect('State', l2)
    #
    # if 'Select all' in state_dropdown:
    #     state_dropdown = schemas_list
    #
    # st.write(state_dropdown)
    # #selected_options = st.multiselect("Select one or more options:",schemas_list)
    # container = st.container()
    # all = st.checkbox("Select all")
    # if all:
    #     selected_options = container.multiselect("Select one or more options:",schemas_list,schemas_list)
    #     print(selected_options)
    # else:
    #     selected_options = container.multiselect("Select one or more options:",schemas_list)
    #     print(selected_options)
    # for schema in schema_list:
    #     st.checkbox(label=schema)
    #submitted2 = st.button("Submit")
