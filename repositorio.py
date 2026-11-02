import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


class Repositorio:

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )


    def registrar_usuario(
        self,
        nombre,
        correo,
        password_hash
    ):
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            sql = """
                INSERT INTO usuarios_almacen
                (nombre, correo, password_hash)
                VALUES (%s, %s, %s)
            """

            valores = (
                nombre,
                correo,
                password_hash
            )

            cursor.execute(sql, valores)

            conexion.commit()

            return cursor.lastrowid

        finally:
            cursor.close()
            conexion.close()


    def buscar_usuario_por_correo(self, correo):
        conexion = self.conectar()

        cursor = conexion.cursor(
            dictionary=True
        )

        try:
            sql = """
                SELECT
                    id,
                    nombre,
                    correo,
                    password_hash
                FROM usuarios_almacen
                WHERE correo = %s
            """

            cursor.execute(
                sql,
                (correo,)
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()


    def registrar_producto(
        self,
        codigo_sku,
        nombre_producto,
        descripcion,
        stock,
        precio_unitario,
        categoria
    ):
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            sql = """
                INSERT INTO productos_inventario
                (
                    codigo_sku,
                    nombre_producto,
                    descripcion,
                    stock,
                    precio_unitario,
                    categoria
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (
                codigo_sku,
                nombre_producto,
                descripcion,
                stock,
                precio_unitario,
                categoria
            )

            cursor.execute(
                sql,
                valores
            )

            conexion.commit()

            return cursor.lastrowid

        finally:
            cursor.close()
            conexion.close()


    def listar_productos(self):
        conexion = self.conectar()

        cursor = conexion.cursor(
            dictionary=True
        )

        try:
            sql = """
                SELECT
                    id,
                    codigo_sku,
                    nombre_producto,
                    descripcion,
                    stock,
                    precio_unitario,
                    categoria
                FROM productos_inventario
                ORDER BY id
            """

            cursor.execute(sql)

            productos = cursor.fetchall()

            # Decimal de MySQL → float
            for producto in productos:
                producto["precio_unitario"] = float(
                    producto["precio_unitario"]
                )

            return productos

        finally:
            cursor.close()
            conexion.close()