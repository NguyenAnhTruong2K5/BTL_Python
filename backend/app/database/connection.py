import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",       # your MySQL host (local machine)
        port=3306,                
        user="root",           
        password="yourpassword",# Điền mật khẩu vào đây
        database="QuanLyBaiDoXe" 
    )
    return connection
