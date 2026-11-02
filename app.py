from flask import Flask, jsonify, request
import mysql.connector

from servicio import Servicio


app = Flask(__name__)

servicio = Servicio()


# ========================================
# REGISTRO DE USUARIO
# ========================================

@app.route("/api/auth/registro", methods=["POST"])
def registrar_usuario():

    datos = request.get_json(
        silent=True
    ) or {}

    try:
        usuario_id = servicio.registrar_usuario(
            datos.get("nombre"),
            datos.get("correo"),
            datos.get("password")
        )

        return jsonify({
            "mensaje": "Usuario registrado correctamente",
            "id": usuario_id
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400

    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 500


# ========================================
# LOGIN
# ========================================

@app.route("/api/auth/login", methods=["POST"])
def login():

    datos = request.get_json(
        silent=True
    ) or {}

    usuario = servicio.login(
        datos.get("correo"),
        datos.get("password")
    )

    if usuario is None:

        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    return jsonify({
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "correo": usuario["correo"]
        }
    }), 200


# ========================================
# REGISTRAR PRODUCTO
# ========================================

@app.route("/api/almacen/productos", methods=["POST"])
def registrar_producto():

    datos = request.get_json(
        silent=True
    ) or {}

    try:

        producto_id = servicio.registrar_producto(
            datos.get("codigo_sku"),
            datos.get("nombre_producto"),
            datos.get("descripcion"),
            datos.get("stock"),
            datos.get("precio_unitario"),
            datos.get("categoria")
        )

        return jsonify({
            "mensaje": "Producto registrado correctamente",
            "id": producto_id
        }), 201

    except (
        ValueError,
        TypeError
    ) as error:

        return jsonify({
            "error": str(error)
        }), 400

    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 500


# ========================================
# LISTAR PRODUCTOS
# ========================================

@app.route("/api/almacen/productos", methods=["GET"]
)
def listar_productos():

    try:

        productos = (servicio.listar_productos())

        return jsonify(productos), 200

    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )