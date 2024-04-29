import hashlib
import os
import sqlite3

from typing import Any, List, Optional


class Database:
    HASH_NAME: str = "sha256"
    HASH_ITERATIONS: int = 100000

    _connection: Optional[sqlite3.Connection]
    _cursor: Optional[sqlite3.Cursor]

    def __init__(self) -> None:
        self._connection = None
        self._cursor = None

    def open(self, path: str) -> None:
        if self._connection is not None:
            self.close()

        self._connection = sqlite3.connect(path)
        self._cursor = self._connection.cursor()
        self._create_tables()

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()

        self._connection = None
        self._cursor = None

    def _create_tables(self) -> None:
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT,
                    salt TEXT
                )"""
        )

        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            description TEXT,
                            price REAL
                        )"""
        )

        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS purchases (
                            id INTEGER PRIMARY KEY,
                            product_id INTEGER,
                            user_id INTEGER,
                            FOREIGN KEY (product_id) REFERENCES products (id),
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )"""
        )

        self._connection.commit()

    def _insert(
        self, table_name: str, value_names: List[str], values: List[Any]
    ) -> None:
        try:
            v = ", ".join(value_names)
            vq = ", ".join(["?" for value in value_names])
            self._cursor.execute(
                f"INSERT INTO {table_name} ({v}) VALUES ({vq})", values
            )
            self._connection.commit()
        except Exception as e:
            print(e)
            self._connection.rollback()

    def _count(self, table_name: str, value_names: List[str], values: List[Any]) -> int:
        result = self._select_where(["COUNT(*)"], table_name, value_names, values)
        count = result[0]
        return count

    def _exists(
        self, table_name: str, value_names: List[str], values: List[Any]
    ) -> bool:
        return self._count(table_name, value_names, values) > 0

    def _select_where(
        self,
        field_selector: List[str],
        table_name: str,
        value_names: List[str],
        values: List[Any],
    ) -> Optional[Any]:
        v = " AND ".join([f"{x} = ?" for x in value_names])
        self._cursor.execute(
            f"SELECT {', '.join(field_selector)} FROM {table_name} WHERE {v}", values
        )
        result = self._cursor.fetchone()
        return result

    def _select_all(self, table_name: str) -> List[str]:
        self._cursor.execute(f"SELECT * FROM {table_name}")
        items = self._cursor.fetchall()
        return items

    # db functions
    def get_user_id(self, email: str) -> Optional[int]:
        user = self._select_where(["id"], "users", ["email"], [email])
        return user

    def register_user(self, email: str, password: str) -> bool:
        try:
            if self.is_user_registered(email):
                print("user already registered")
                return False

            salt: bytes = os.urandom(16)
            hashed_password: str = hashlib.pbkdf2_hmac(
                Database.HASH_NAME,
                password.encode("utf-8"),
                salt,
                Database.HASH_ITERATIONS,
            )
            self._insert(
                "users", ["email", "password", "salt"], (email, hashed_password, salt)
            )
            return True
        except:
            return False

    def is_user_registered(self, email: str) -> bool:
        return self._exists("users", ["email"], [email])

    def get_products(self) -> List:
        products = self._select_all("products")
        return products

    def register_product(self, name: str, description: str, price: str) -> bool:
        try:
            self._insert(
                "products", ["name", "description", "price"], [name, description, price]
            )
            return True
        except:
            return False

    def purchase_product(self, user_id: int, product_id: int) -> bool:
        try:
            if self.does_user_own_product(user_id, product_id):
                print("user already owns this product")
                return False

            self._insert("purchases", ["user_id", "product_id"], [user_id, product_id])
            return True
        except:
            return False

    def does_user_own_product(self, user_id: int, product_id: int) -> bool:
        return self._exists(
            "purchases", ["user_id", "product_id"], [user_id, product_id]
        )


if __name__ == "__main__":
    email = "ramon_meza@live.com"
    password = "password123"

    db = Database()
    db.open("test.db")

    db.register_user(email, password)
    user_id = db.get_user_id(email)[0]

    products = db.get_products()
    if len(products) == 0:
        print("registering a new product")
        db.register_product("Test Product", "Just a test", 19.99)
    else:
        print(products)

    product_id = db.get_products()[0][0]

    if db.purchase_product(user_id, product_id):
        print('user purchased product')
    
    db.close()
