import sqlite3
import tempfile
import easyocr
import re
from PIL import Image
import pandas as pd
import streamlit as st


def updated_data():
    db_paths = "C:\\Users\\visha\\Desktop\\SQLite3\\ocr.db"

    connection = sqlite3.connect(db_paths)
    mycursor = connection.cursor()

    # Fetch data from the 'card_data' table
    query = "SELECT * FROM card_data"
    mycursor.execute(query)

    # Fetch all rows and column names
    rows = mycursor.fetchall()
    columns_names = [description[0] for description in mycursor.description]

    # Create a DataFrame from the fetched data
    updated_data_df1 = pd.DataFrame(rows, columns=columns_names)

    connection.close()

    return updated_data_df1


def extract_text(x):
    reader = easyocr.Reader(['en'], gpu=True)

    text_para = reader.readtext(x, detail=0, paragraph=True)
    text = reader.readtext(x, detail=0, paragraph=False)

    name = text[0]
    des = text[1]
    mob = []

    for i in text:
        if '-' in i:
            mob.append(i)
    if len(mob) == 2:
        p_c = mob[0]
        s_c = mob[1]
    else:
        p_c = mob[0]
        s_c = 'NA'

    mail = ''
    for i in text:
        if "@" in i:
            mail = i
            break
        else:
            mail = 'NA'

    web = ''
    for i in text:
        if re.findall(r'[wW]+.[a-zA-Z0-9]+.[a-zA-Z]+', i):
            web = i
            break
        else:
            web = 'NA'
    w = web.replace(web[:4], 'www.')
    if '.com' not in w:
        w = web.replace('com', '.com')

    adds = ''
    for i in text_para:
        if len(i) > 30:
            adds = i

    address = adds.replace(';', ',')

    area_pattern = r'\b\d+\s+\w+\s+St\b'  # r'^123.*?St'
    area = re.findall(area_pattern, address)

    city_pattern = r',\s*([\w\s]+),\s*TamilNadu'
    city = re.findall(city_pattern, address)

    state_pattern = 'TamilNadu'
    state = re.findall(state_pattern, address)

    pin_pattern = r'\d{6,7}'
    pincode = re.findall(pin_pattern, address)

    if '.' not in text_para[-1]:
        org = text_para[-1]
    else:
        org = text_para[-2]

    data = {
        "Name": name,
        "Designation": des,
        "Primary_Contact": p_c,
        "Secondary_Contact": s_c,
        "Email_Id": mail,
        "Website": w,
        "Area": area,
        "City": city,
        "State": state,
        "Pincode": pincode,
        "Organization": org
    }

    return data



st.set_page_config(page_title="Image DataExtraction",
                   layout="wide", )
page_bg_img = """
    <style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://cdn.pixabay.com/photo/2017/04/20/07/08/magnifying-glass-2244781_1280.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
}
</style>
    """

st.markdown(page_bg_img, unsafe_allow_html=True)

app_title = """
    color: aquamarine;
    text-align: center;
    font-family: Serif;
    font-size: 50px;
"""
st.markdown(
    f'<h1 style="{app_title}">BizCardX</h1>',
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["$\\huge Home $", "$\\huge Upload-Extract $", "$\\huge Update $"])

with tab1:
    st.session_state.video_playing = True

    drive_link = "https://drive.google.com/file/d/1yg7gKx3929vttY_3vq4QCA_GE_sxOS62/view?usp=drive_link"
    file_id = drive_link.split("/file/d/")[1].split("/view")[0]
    direct_download_link = f"https://drive.google.com/uc?id={file_id}"

    auto_play_js = f"""
        <video id="video" src="{direct_download_link}" autoplay controls>
        Your browser does not support the video tag.
        </video>
        <script>
        var video = document.getElementById("video");
        video.play();
        </script>
    """
    st.markdown(auto_play_js, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([0.4, 0.6], gap='large')

    image = col1.file_uploader('Upload your Image here', label_visibility="collapsed", type=["png", "jpeg", "jpg"])
    if image is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file.write(image.read())  # Write the uploaded image data to the temporary file
        temp_file.close()  # Close
        img = Image.open(temp_file.name)

        st.write("Your Image was successfully uploaded")
        if st.button('View Image'):
            st.image(image)
        if st.button("Extract Text"):
            d = extract_text(temp_file.name)
            st.write("Text in the image was successfully extracted")

            df = pd.DataFrame(d)
            st.dataframe(d)
        if st.button("Store"):
            db_path = "C:\\Users\\visha\\Desktop\\SQLite3\\ocr.db"
            conn = sqlite3.connect(db_path)

            cursor = conn.cursor()

            table_schema = """
            CREATE TABLE IF NOT EXISTS card_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Designation TEXT,
                Primary_Contact TEXT,
                Secondary_Contact TEXT,
                Email_Id TEXT,
                Website TEXT,
                Area TEXT,
                City TEXT,
                State TEXT,
                Pincode TEXT,
                Organization TEXT
            );
            """

            cursor.execute(table_schema)
            conn.commit()

            d = extract_text(temp_file.name)
            df = pd.DataFrame(d)

            df.to_sql('card_data', conn, if_exists='append', index=False)
            st.write("Extracted Text was successfully stored in the Database")
            conn.close()

with tab3:
    col, cl = st.columns([0.3, 0.7])
    selec = col.selectbox("", ['Select any one Option', 'View all Data', 'Update', 'Remove'])

    if selec == 'View all Data':
        db_path = "C:\\Users\\visha\\Desktop\\SQLite3\\ocr.db"
        conn = sqlite3.connect(db_path)

        q = "select * from card_data"
        cursor = conn.execute(q)
        t = cursor.fetchall()
        cursor.close()

        column_names = [description[0] for description in cursor.description]

        df1 = pd.DataFrame(t, columns=column_names)
        st.dataframe(df1)
        conn.close()

        updated_data_df2 = updated_data()

        st.download_button("Download", data=updated_data_df2.to_csv(index=False),
                           file_name="updated_data.csv")

if selec == 'Update':
    db_path = "C:\\Users\\visha\\Desktop\\SQLite3\\ocr.db"
    conn = sqlite3.connect(db_path)

    q = "select * from card_data"
    cursor = conn.execute(q)
    t = cursor.fetchall()
    cursor.close()

    column_names = [description[0] for description in cursor.description]

    df1 = pd.DataFrame(t, columns=column_names)
    # st.dataframe(df1)
    conn.close()

    c, cl = st.columns([0.4, 0.6])

    org = df1['Organization'].tolist()
    org.insert(0, 'Choose the Organization')

    select_org = c.selectbox("", org)

    column_name = column_names[1:]

    column_name.insert(0, "Choose the Update Field")

    select_update = c.selectbox("", column_name)

    if select_update == 'Name':
        name = c.text_input("Name")

        if c.button("Update"):
            selected_org = select_org
            updated_name = name

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Name = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Name was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Designation':
        desi = c.text_input("Designation")

        if c.button("Update"):
            selected_org = select_org
            updated_name = desi

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Designation = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Designation was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Primary_Contact':
        pc = c.text_input("Primary_Contact")

        if c.button("Update"):
            selected_org = select_org
            updated_name = pc

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Primary_Contact = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Primary_Contact was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Secondary_Contact':
        sc = c.text_input("Secondary_Contact")

        if c.button("Update"):
            selected_org = select_org
            updated_name = sc

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Secondary_Contact = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Secondary_Contact was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Email_Id':
        email = c.text_input("Email_Id")

        if c.button("Update"):
            selected_org = select_org
            updated_name = email

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Email_Id = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Email_Id was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Website':
        web = c.text_input("Website")

        if c.button("Update"):
            selected_org = select_org
            updated_name = web

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Website = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Website was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Area':
        ar = c.text_input("Area")

        if c.button("Update"):
            selected_org = select_org
            updated_name = ar

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Area = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Area was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'City':
        cit = c.text_input("City")

        if c.button("Update"):
            selected_org = select_org
            updated_name = cit

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET City = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("City was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'State':
        sat = c.text_input("State")

        if c.button("Update"):
            selected_org = select_org
            updated_name = sat

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET State = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("State was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Pincode':
        pin = c.text_input("Pincode")

        if c.button("Update"):
            selected_org = select_org
            updated_name = pin

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Pincode = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Pincode was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

    if select_update == 'Organization':
        orgz = c.text_input("Organization")

        if c.button("Update"):
            selected_org = select_org
            updated_name = orgz

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            update_query = f"UPDATE card_data SET Organization = ? WHERE Organization = ?"
            cursor.execute(update_query, (updated_name, selected_org))
            conn.commit()

            st.write("Organization was Updated successfully")

            updated_data_query = f"SELECT * FROM card_data WHERE Organization = ?"
            cursor.execute(updated_data_query, (selected_org,))
            updated_data = cursor.fetchone()

            conn.close()

            if updated_data:
                updated_df = pd.DataFrame([updated_data], columns=column_names)
                st.dataframe(updated_df)
            else:
                st.warning("No data found for the selected organization.")

if selec == 'Remove':
    db_path = "C:\\Users\\visha\\Desktop\\SQLite3\\ocr.db"
    conn = sqlite3.connect(db_path)

    q = "select * from card_data"
    cursor = conn.execute(q)
    t = cursor.fetchall()
    cursor.close()

    column_names = [description[0] for description in cursor.description]

    df1 = pd.DataFrame(t, columns=column_names)

    c, cl = st.columns([0.4, 0.6])

    orgs = df1['Organization'].tolist()
    # conn.close()

    orgs.insert(0, 'Choose the Organization to Remove')

    select_org = c.selectbox("Select", orgs)

    if st.button("Remove"):
        cursor = conn.cursor()

        delete_query = f"DELETE FROM card_data WHERE Organization = ?"
        cursor.execute(delete_query, (select_org,))
        conn.commit()
        conn.close()

        st.write(f"All data associated with '{select_org}' has been removed.")

        updated_data_df = updated_data()

        st.download_button("Download Updated Data", data=updated_data_df.to_csv(index=False),
                           file_name="updated_data.csv")
