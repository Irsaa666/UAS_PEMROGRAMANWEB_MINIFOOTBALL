<<<<<<< HEAD
import pymysql

conn = pymysql.connect(
    host="8dhchc.h.filess.io",
    port=3307,
    user="mini_football_interestgo",
    password="63891ed4892f485eff5f9617cc55042b29e69fae",
    database="mini_football_interestgo"
)

cursor = conn.cursor()

cursor.execute("""
INSERT INTO users(username,email,password_hash)
VALUES(%s,%s,%s)
""",(
    "admin",
    "admin@gmail.com",
    "123456"
))

conn.commit()

print("Berhasil insert!")

=======
import pymysql

conn = pymysql.connect(
    host="8dhchc.h.filess.io",
    port=3307,
    user="mini_football_interestgo",
    password="63891ed4892f485eff5f9617cc55042b29e69fae",
    database="mini_football_interestgo"
)

cursor = conn.cursor()

cursor.execute("""
INSERT INTO users(username,email,password_hash)
VALUES(%s,%s,%s)
""",(
    "admin",
    "admin@gmail.com",
    "123456"
))

conn.commit()

print("Berhasil insert!")

>>>>>>> 9e86813b6c4f96fe831b3e3eb5d12d76aad2319e
conn.close()