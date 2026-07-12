import pymysql

# Test standard passwords to connect to local MySQL server
passwords = ['root', '', 'admin']
connected = False

print("Attempting to connect to MySQL server to create the database 'it_monitor_db'...")

for pwd in passwords:
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password=pwd)
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS it_monitor_db;")
        conn.commit()
        conn.close()
        print(f"\n[SUCCESS] Database 'it_monitor_db' created/verified successfully using password: '{pwd}'")
        connected = True
        break
    except Exception as e:
        print(f"[Info] Connection attempt with password '{pwd}' failed: {e}")

if not connected:
    print("\n[ERROR] Could not connect to local MySQL server to create the database.")
    print("Please verify that your MySQL server is running on port 3306 and check if the credentials match.")
