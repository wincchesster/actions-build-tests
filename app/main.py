import os
from db_utils import Mysql
import time
import pymysql
from dotenv import load_dotenv

load_dotenv()


# Wait for mysql to be ready
def wait_for_mysql():
    max_retries = 30
    retries = 0
    password = os.getenv("DB_ROOT_PASSWORD")
    while True:
        try:
            connection = pymysql.connect(
                host='mysql',
                user='root',
                password=password,
            )

            connection.close()
            print("MySQL is hot and ready.")
            break
        except pymysql.Error as err:
            print(f"Waiting for MySQL... ({err})")
            time.sleep(5)
            retries += 1

            if retries >= max_retries:
                print("Unable to connect to MySQL. Exiting.")
                exit(1)

# wait_for_mysql()

# Create custom mysql class
class CustomMysql(Mysql):
    def __init__(self):
        db_host = os.environ.get("DB_HOST")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_USER_PASSWORD")
        db_database = os.environ.get("DB_DATABASE")

        super().__init__(host=db_host, user=db_user, password=db_password, database=db_database)

    def create_shop(self):
        create_table_query = """
            CREATE TABLE shop (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL
            )
        """
        self.execute_query(create_table_query)

    def add_item(self, item, price):
        add_item_query = "INSERT INTO shop (item, price) VALUES (%s, %s)"
        self.execute_query(add_item_query, (item, price))

    def delete_item(self, item):
        delete_item_query = "DELETE FROM shop WHERE item = %s"
        self.execute_query(delete_item_query, (item,))

    def delete_shop(self):
        delete_table_query = "DROP TABLE shop"
        self.execute_query(delete_table_query)

# Create table and add items
# if __name__ == "__main__":
#     mysql_instance = CustomMysql()
#     mysql_instance.create_shop()
#     mysql_instance.add_item("apple", 1.99)
#     mysql_instance.add_item("banana", 3.99)
#     print("Items in the shop:")
#     items = mysql_instance.fetch_all("SELECT * FROM shop")
#     for item in items:
#         print(item)
#     mysql_instance.delete_item("apple")
#     print("Items after deletion:")
#     items = mysql_instance.fetch_all("SELECT * FROM shop")
#     for item in items:
#         print(item)
#     mysql_instance.delete_shop()
#     mysql_instance.close_connection()
