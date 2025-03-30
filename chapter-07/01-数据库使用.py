from pymysql import Connection

conn = Connection(
    host='localhost',
    user='root',
    password='Guoyu@657',
    port=3306,
    charset='utf8'
)

print(conn.get_server_info())

cursor = conn.cursor()  # 创建游标
conn.select_db('sys')
cursor.execute('select * from value')

conn.close()   #关闭连接