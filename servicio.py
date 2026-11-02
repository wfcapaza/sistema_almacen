import bcrypt
import mysql.connector

from repositorio import Repositorio


class Servicio:

    def __init__(self):
        self.repositorio = Repositorio()


    def registrar_usuario(
        self,
        nombre,
        correo,
        password
    ):
        if not nombre or not correo or not password:
            raise ValueError(
                "Nombre, correo y password son obligatorios"
            )

        usuario_existente = (
            self.repositorio.buscar_usuario_por_correo(correo)
        )

        if usuario_existente:
            raise ValueError(
                "El correo ya está registrado"
            )

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        return self.repositorio.registrar_usuario(
            nombre,
            correo,
            password_hash
        )


    def login(self, correo, password):

        if not correo or not password:
            return None

        usuario = (
            self.repositorio.buscar_usuario_por_correo(correo)
        )

        if usuario is None:
            return None

        password_correcto = bcrypt.checkpw(
            password.encode("utf-8"),
            usuario["password_hash"].encode("utf-8")
        )

        if not password_correcto:
            return None

        return usuario


    def registrar_producto(
        self,
        codigo_sku,
        nombre_producto,
        descripcion,
        stock,
        precio_unitario,
        categoria
    ):

        if (
            not codigo_sku
            or not nombre_producto
            or not categoria
        ):
            raise ValueError(
                "SKU, nombre y categoría son obligatorios"
            )

        stock = int(stock)
        precio_unitario = float(
            precio_unitario
        )

        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo"
            )

        if precio_unitario <= 0:
            raise ValueError(
                "El precio unitario debe ser mayor a cero"
            )

        return self.repositorio.registrar_producto(
            codigo_sku,
            nombre_producto,
            descripcion,
            stock,
            precio_unitario,
            categoria
        )


    def listar_productos(self):
        return self.repositorio.listar_productos()