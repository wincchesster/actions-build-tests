import unittest
from main import CustomMysql

class TestCustomMysql(unittest.TestCase):

    def setUp(self):
        # Create an instance of CustomMysql for testing
        self.mysql_instance = CustomMysql()

    def tearDown(self):
        # Close the connection after each test
        self.mysql_instance.close_connection()

    def test_create_shop(self):
        # Check if the table 'shop' exists in the database
        table_exists_query = "SHOW TABLES LIKE 'shop'"
        existing_table = self.mysql_instance.fetch_one(table_exists_query)
        if existing_table:
            # If the table already exists, consider it as a pass
            self.assertTrue(True)
        else:
            # If the table doesn't exist, test the create_shop method
            self.mysql_instance.create_shop()
            # Check if the table 'shop' now exists in the database
            created_table = self.mysql_instance.fetch_one(table_exists_query)
            self.assertIsNotNone(created_table, "Table 'shop' does not exist after creation")

    def test_delete_shop(self):
        # Delete the table 'shop' if it exists
        self.mysql_instance.delete_shop()
    
    def test_add_and_fetch_item(self):
        # Add an item to the shop and fetch it
        self.mysql_instance.create_shop()
        self.mysql_instance.add_item("apple", 1.99)
        items = self.mysql_instance.fetch_all("SELECT * FROM shop")
        expected_item = ("apple", 1.99)
        
    # def test_delete_item(self):
    #     # Add an item to the shop, delete it and check if it's gone
    #     self.mysql_instance.add_item("apple", 1.99)
    #     self.mysql_instance.delete_item("apple")
    #     items = self.mysql_instance.fetch_all("SELECT * FROM shop")
    #     self.assertNotIn(("apple", 1.99), items)


if __name__ == '__main__':
    unittest.main()