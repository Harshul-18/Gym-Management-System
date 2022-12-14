import webbrowser
import toml

import datetime
import pandas as pd
import streamlit as st
import sqlite3

from PIL import Image

st.set_page_config(page_title="Gymnasium")
primaryColor = toml.load(".streamlit/config.toml")['theme']['primaryColor']
s = f"""
<style>
div.stButton > button:first-child {{ border: 1px solid {primaryColor}; color: black; border-radius:20px 20px 20px 20px; background: none;}}
div.stButton > button:first-child:hover {{
    background: #FFA351FF;
    color: black;
}}
<style>
"""
st.markdown(s, unsafe_allow_html=True)

# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://cdn.shopify.com/s/files/1/0062/4309/0499/products/oc-1-naturalwicker_2000x.png?v=1587129694")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

def hide_streamlit_style():
    hideStreamlitStyle = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hideStreamlitStyle, unsafe_allow_html=True)

def add_sidebar_menu():
    with st.sidebar:

        st.markdown("### Team Members ")

        if st.button("Harshul Nanda"):
            webbrowser.open_new_tab("https://www.linkedin.com/in/harshulnanda/")
        if st.button("Abhijeet Saroha"):
            webbrowser.open_new_tab('https://www.linkedin.com/in/abhijeet-saroha-a19031229/')
        if st.button("Rishabh Sagar"):
            webbrowser.open_new_tab('https://www.linkedin.com/in/rishabh-sagar-1b0b74229/')

        st.markdown("### Contact us ")

        if st.button("GitHub"):
            webbrowser.open_new_tab('https://github.com/Harshul-18')
    
    page_bg_img = """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        background-color: #FFBE7BFF;
        text-color: white;
        color: white;
        background-position: center;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def add_footer():
    footer="""<style>
a:link , a:visited{
color: white;
font-weight: bold;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}

</style>
<div class="footer">
<p>Copyright ©, Designed by <b>Harshul, Rishabh, and Abhijeet</b>.</p>
</div>
"""

    st.markdown(footer, True)

conn = sqlite3.connect('data.db')
c = conn.cursor()

# c.execute("drop table gymmers")

# Customers
c.execute("""
CREATE TABLE IF NOT EXISTS gymmers(
    Customer_ID INT NOT NULL PRIMARY KEY,
    Customer_Name TEXT NOT NULL,
    Contact INT NOT NULL,
    Age INT NOT NULL,
    Personal_Trainer_and_Timings TEXT NOT NULL UNIQUE,
    Start_Date DATE NOT NULL,
    Gym_Pack_ID TEXT NOT NULL,
    FOREIGN KEY(Gym_Pack_ID) REFERENCES packages(Pack_ID)
)""")

def add_custs(custs):
    c.executemany("INSERT INTO gymmers VALUES(?, ?, ?, ?, ?, ?, ?)", custs)
    conn.commit()

def update_cust(at_column, set_value, where_column, value_is):
    c.execute(f''' 
        UPDATE gymmers
        SET {at_column}={set_value}
        WHERE {where_column}={value_is}
    ''')
    conn.commit()

def search_custs(by_column, with_value, fields):
    df = pd.read_sql_query(f"SELECT {fields} FROM gymmers WHERE {by_column}={with_value}", conn)
    return df

def delete_cust(by_column, with_value):
    c.execute(f"DELETE FROM gymmers WHERE {by_column}={with_value}")
    conn.commit()

# Packages
c.execute("""
CREATE TABLE IF NOT EXISTS packages(
    Pack_ID INT NOT NULL PRIMARY KEY,
    Gym_Package TEXT NOT NULL,
    Duration TEXT NOT NULL,
    Price_in_₹ INT NOT NULL
)""")

def add_packs(packs):
    c.executemany("INSERT INTO packages VALUES(?, ?, ?, ?)", packs)
    conn.commit()

def update_packs(at_column, set_value, where_column, value_is):
    c.execute(f''' 
        UPDATE packages
        SET {at_column}={set_value}
        WHERE {where_column}={value_is}
    ''')
    conn.commit()

def search_packs(by_column, with_value, fields):
    df = pd.read_sql_query(f"SELECT {fields} FROM packages WHERE {by_column}={with_value}", conn)
    return df

def delete_pack(by_column, with_value):
    c.execute(f"DELETE FROM packages WHERE {by_column}={with_value}")
    conn.commit()

def show_table(named):
    df = pd.read_sql_query(f"SELECT * FROM {named}", conn)
    return df

def main():
    st.image(Image.open("./assets/gym.png"))

    menu = ["Home", "Add Customer", "Update Customer Data", "Show all Customers", "Search Customers", "Delete Customer", "Add Package", "Update Package", "Show all Packs", "Search Packs", "Delete Packs"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown("A DataBase Management System Project made by __Harshul Nanda__, __Abhijeet Saroha__, and __Rishabh Sagar__.")
        st.markdown("Head over to menu and select the features you want to perform.")
        st.markdown("""<a href="https://www.buymeacoffee.com/HARMBOT" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-red.png" alt="Buy Us A Coffee" height="40" width="164" style="border: 1px solid white; border-radius: 16px;"></a>""", unsafe_allow_html=True)
    elif choice == "Add Customer":
        cust_id = st.text_input("Enter the Customer ID")
        cust_id = int(cust_id) if cust_id else 0
        cust_name = st.text_input("Enter the Customer Name")
        contact = st.text_input("Enter the contact")
        contact = int(contact) if contact else 0
        age = st.text_input("Enter the age")
        age = int(age) if age else 0
        per_trainer = st.text_input("Enter the personal trainer and its' timings (space separated)")
        start_date = st.date_input(
            "Enter the joining date",
            datetime.datetime.now()
        )
        pack_id = st.text_input("Enter the Package ID")
        pack_id = int(pack_id) if pack_id else 0

        custs = [
            (cust_id, cust_name, contact, age, per_trainer, start_date, pack_id),
        ]

        if st.button("Add Customer"):
            try:
                if pack_id==0 or cust_id==0 or age==0 or contact==0:
                    raise Exception
                else:
                    add_custs(custs)
                    st.write("Added Successfully")
                    st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Either the entries are none or already in the database.{e}")
    elif choice == "Update Customer Data":
        cust_fields = [
            "Customer_ID",
            "Customer_Name",
            "Contact",
            "Age",
            "Personal_Trainer_and_Timings",
            "Start_Date",
            "Gym_Pack_ID",
        ]
        at_column = st.selectbox("Select the customer field to update", cust_fields)
        set_value = st.text_input("Enter the value to be set")
        if at_column == "Customer_ID Contact Age Gym_Pack_ID":
            set_value = int(set_value) if set_value else 0
        else:
            set_value = '\'' + set_value + '\''
        where_column = st.selectbox("Enter the column to search with", cust_fields)
        value_is = st.text_input("Enter the value of the column you search with")
        if where_column in "Customer_ID Contact Age Gym_Pack_ID":
            value_is = int(value_is) if value_is else 0
        else:
            value_is = '\'' + value_is + '\''

        if st.button("Update Customer Data"):
            try:
                if set_value==0 or value_is==0:
                    raise Exception
                else:
                    update_cust(at_column=at_column, set_value=set_value, where_column=where_column, value_is=value_is)
                    st.write("Updated Successfully")
                    st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Either the entries are none or already in the database. {e}")
        
        st.write(show_table(named="gymmers"))
    elif choice == "Show all Customers":
        st.write(show_table(named="gymmers"))
    elif choice == "Search Customers":
        cust_fields = {
            "Customer_ID": False,
            "Customer_Name": False,
            "Contact": False,
            "Age": False,
            "Personal_Trainer_and_Timings": False,
            "Start_Date": False,
            "Gym_Pack_ID": False
        }
        by_column = st.selectbox("Enter the column to search with", cust_fields)
        with_column = st.text_input("Enter the value of the above column")
        if by_column in "Customer_ID Age Contact Gym_Pack_ID":
            with_column = int(with_column) if with_column else 0
        else:
            with_column = '\'' + with_column + '\''
        st.write("Check the boxes of the columns you want in your search")
        cust_fields["Customer_ID"] = st.checkbox("Customer_ID")
        cust_fields["Customer_Name"] = st.checkbox("Customer_Name")
        cust_fields["Contact"] = st.checkbox("Contact")
        cust_fields["Age"] = st.checkbox("Age")
        cust_fields["Personal_Trainer_and_Timings"] = st.checkbox("Personal_Trainer_and_Timings")
        cust_fields["Start_Date"] = st.checkbox("Start_Date")
        cust_fields["Gym_Pack_ID"] = st.checkbox("Gym_Pack_ID")
        fields = ""
        for field in cust_fields:
            if cust_fields[field]:
                fields += field + ", "
        if st.button("Search"):
            try:
                if with_column==0:
                    raise Exception
                else:
                    st.write(search_custs(by_column=by_column, with_value=with_column, fields=fields[:-2]))
            except Exception as e:
                st.warning(f"⚠️ Either entries are none or not in the database. {e}")
    elif choice == "Delete Customer":
        cust_fields = [
            "Customer_ID",
            "Customer_Name",
            "Contact",
            "Age",
            "Personal_Trainer_and_Timings",
            "Start_Date",
            "Gym_Pack_ID",
        ]
        by_column = st.selectbox("Enter the column to delete the row of", cust_fields)
        with_value = st.text_input("Enter the value of the above enetered column")
        if by_column in "Customer_ID Contact Age Gym_Pack_ID":
            with_value = int(with_value) if with_value else 0
        else:
            with_value = '\'' + with_value + '\''

        if st.button("Delete Customer Data"):
            try:
                if with_value==0:
                    raise Exception
                else:
                    delete_cust(by_column=by_column, with_value=with_value)
                    st.write("Deleted Successfully")
                    st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Either the entries are none. {e}")
        st.write(show_table(named="gymmers"))
    elif choice == "Add Package":
        pack_id = st.text_input("Enter the package ID")
        pack_id = int(pack_id) if pack_id else 0
        gym_package = st.text_input("Enter the package name")
        duration = st.text_input("Enter the duration of the package")
        price = st.text_input("Enter the price of the package")
        price = int(price) if price else 0

        packs = [
            (pack_id, gym_package, duration, price),
        ]

        # packs = [
        #     (1, "Gold Card", "1 Year", "13999"),
        #     (2, "Regular Card", "1 Month", "3499"),
        #     (3, "Silver Card", "6 Months", "8999"),
        #     (4, "Bronze Card", "3 Months", "5999"),
        # ]

        if st.button("Add Package"):
            try:
                if pack_id==0 or price==0:
                    raise Exception
                else:
                    add_packs(packs)
                    st.write("Added Successfully")
                    st.balloons()
            except Exception as e:
                st.warning("⚠️ Either the entries are none or already in the database.")
    elif choice == "Update Package":
        package_fields = [
            "Pack_ID",
            "Gym_Package",
            "Duration",
            "Price_in_₹"
        ]
        at_column = st.selectbox("Select the package field to update", package_fields)
        set_value = st.text_input("Enter the value to be set")
        if at_column == "Pack_ID" or at_column == "Price_in_₹":
            set_value = int(set_value) if set_value else 0
        else:
            set_value = '\'' + set_value + '\''
        where_column = st.selectbox("Enter the column to search with", package_fields)
        value_is = st.text_input("Enter the value of the column you search with")
        if where_column == "Pack_ID" or where_column == "Price_in_₹":
            value_is = int(value_is) if value_is else 0
        else:
            value_is = '\'' + value_is + '\''

        if st.button("Update Package"):
            try:
                if set_value==0 or value_is==0:
                    raise Exception
                else:
                    update_packs(at_column=at_column, set_value=set_value, where_column=where_column, value_is=value_is)
                    st.write("Updated Successfully")
                    st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Either the entries are none or already in the database. {e}")
        
        
        st.write(show_table(named="packages"))
    elif choice == "Show all Packs":
        st.write(show_table(named="packages"))
    elif choice == "Search Packs":
        package_fields = {
            "Pack_ID": False,
            "Gym_Package": False,
            "Duration": False,
            "Price_in_₹": False
        }
        by_column = st.selectbox("Enter the column to search with", package_fields)
        with_column = st.text_input("Enter the value of the above column")
        if by_column == "Pack_ID" or by_column == "Price_in_₹":
            with_column = int(with_column) if with_column else 0
        else:
            with_column = '\'' + with_column + '\''
        st.write("Check the boxes of the columns you want in your search")
        package_fields["Pack_ID"] = st.checkbox("Pack_ID")
        package_fields["Gym_Package"] = st.checkbox("Gym_Package")
        package_fields["Duration"] = st.checkbox("Duration")
        package_fields["Price_in_₹"] = st.checkbox("Price")
        fields = ""
        for field in package_fields:
            if package_fields[field]:
                fields += field + ", "
        if st.button("Search"):
            try:
                if with_column==0:
                    raise Exception
                else:
                    st.write(search_packs(by_column=by_column, with_value=with_column, fields=fields[:-2]))
            except Exception as e:
                st.warning(f"⚠️ Either entries are none or not in the database. {e}")
    elif choice == "Delete Packs":
        package_fields = [
            "Pack_ID",
            "Gym_Package",
            "Duration",
            "Price_in_₹"
        ]
        by_column = st.selectbox("Enter the column to delete the row of", package_fields)
        with_value = st.text_input("Enter the value of the above enetered column")
        if by_column in "Customer_ID Contact Age Gym_Pack_ID":
            with_value = int(with_value) if with_value else 0
        else:
            with_value = '\'' + with_value + '\''

        if st.button("Delete Package"):
            try:
                if with_value==0:
                    raise Exception
                else:
                    delete_cust(by_column=by_column, with_value=with_value)
                    st.write("Deleted Successfully")
                    st.balloons()
            except Exception as e:
                st.warning(f"⚠️ Either the entries are none. {e}")
        st.write(show_table(named="packages"))

if __name__ == "__main__":
    st.sidebar.image(Image.open("./assets/gymnasium.png"), width=274)
    hide_streamlit_style()
    main()
    add_sidebar_menu()
    add_footer()