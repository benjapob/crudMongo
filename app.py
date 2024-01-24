from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient

app = Flask(__name__)
app.config.update(dict(SECRET_KEY="yoursecretkey"))

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["my_db"]
collection = db["ejercicioCrud"]


# Rutas
@app.route("/")
def index():
    # Mostrar todos los documentos
    documentos = list(collection.find())
    return render_template("index.html", documentos=documentos)


@app.route("/nuevo", methods=["POST"])
def nuevo():
    documentos = list(collection.find())
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    precio = request.form["precio"]
    # Agregar nuevo documento
    libro = {
        "id": len(documentos) + 1,
        "titulo": titulo,
        "autor": autor,
        "precio": precio,
    }

    collection.insert_one(libro)
    flash("Libro insertado correctamente")
    return redirect("/")


@app.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    # Obtener y editar un documento por ID
    if request.method == "GET":
        documento = collection.find_one({"id": int(id)})
        return render_template("editar.html", documento=documento)
    elif request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        precio = request.form["precio"]
        collection.update_one(
            {"id": int(id)},
            {"$set": {"titulo": titulo, "autor": autor, "precio": precio}},
        )

        flash("Libro actualizado correctamente")
        return redirect("/")


@app.route("/eliminar/<id>", methods=["GET", "POST"])
def eliminar(id):
    # Eliminar un documento por ID
    collection.delete_one({"id": int(id)})
    flash("Libro eliminado correctamente")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
