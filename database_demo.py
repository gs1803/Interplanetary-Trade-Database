from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
import pandas as pd
import pymysql.cursors


def reset():
    st.session_state.key += 1

if 'key' not in st.session_state:
    st.session_state.key = 0

def modify_database(dataframe, table_name, query):
    prim_key = f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'"
    if prim_key:
        cursor.execute(prim_key)
        prim_key_col = cursor.fetchall()[0]['Column_name']

    if query:
        cursor.execute(f"SELECT {prim_key_col} FROM {table_name} WHERE {query}")
    else:
        cursor.execute(f"SELECT {prim_key_col} FROM {table_name}")
        
    db_rows = cursor.fetchall()
    db_ids = [row[prim_key_col] for row in db_rows]

    df_ids = set(dataframe[prim_key_col])
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    col_names = tuple(pd.DataFrame(cursor.fetchall())['Field'].tolist())

    for _, row in dataframe.iterrows():
        if row[prim_key_col] not in db_ids:
            insert_query = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(['%s'] * len(col_names))})"
            cursor.execute(insert_query, tuple(row[col] for col in col_names))

    for _, row in dataframe.iterrows():
        update_values = ', '.join(f"{col} = '{row[col]}'" for col in col_names if col != prim_key_col)
        update_query = f"UPDATE {table_name} SET {update_values} WHERE {prim_key_col} = '{row[prim_key_col]}'"
        cursor.execute(update_query)
    
    for db_id in db_ids:
        if db_id not in df_ids:
            delete_query = f"DELETE FROM {table_name} WHERE {prim_key_col} = '{db_id}'"
            cursor.execute(delete_query)


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='PLANET_DB',
                             cursorclass=pymysql.cursors.DictCursor)

st.set_page_config(layout="wide")

sbar = st.sidebar.write("Main Menu")
option = st.sidebar.radio("Select an Option", ["Database Visualizer", "Database Editor"])
st.header("Interplanetary Trade Database")
if option == "Database Editor":
    with connection.cursor() as cursor:
        try:
            table_query = "SHOW TABLES"
            cursor.execute(table_query)
            table_data = cursor.fetchall()
            table_list = [table["Tables_in_planet_db"] for table in table_data]

            table_opt = st.selectbox("Select Table: ", table_list)

            df_query = f"SELECT * FROM {table_opt}"
            filter_query = st.text_input("Optional Filter").strip()
            if filter_query:
                df_query += f" WHERE {filter_query}"

            cursor.execute(df_query)
            main_data = pd.DataFrame(cursor.fetchall())
            
            edit_data = st.data_editor(main_data, hide_index=True, num_rows='dynamic', 
                                       use_container_width=True, key=f'editor_{st.session_state.key}')
            
            col1, col2 = st.columns([0.2, 1.5])
            with col1:
                update_button = st.button("Modify Database")
            with col2:
                st.button('Reset', on_click=reset)

            if update_button:
                modify_database(edit_data, table_opt, filter_query)
                connection.commit()
                st.success("Database modified successfully!")            
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if connection:
        connection.close()


if option == "Database Visualizer":
    with connection.cursor() as cursor:
        query = st.text_area("Enter SQL Query")
        
        if query:
            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                pyg_app = StreamlitRenderer(pd.DataFrame(data), default_tab='data')
                pyg_app.explorer(default_tab='data')

    if connection:
        connection.close()
