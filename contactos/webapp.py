import web
import requests

urls = (
    '/', 'Index',
    '/create', 'Create',
    '/edit/(\\d+)', 'Edit',
    '/delete/(\\d+)', 'Delete'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

API_CONTACTOS = "http://127.0.0.1:8000/v1/contactos"
API_CONTACTO = "http://127.0.0.1:8000/v1/contacto"

class Index:
    def GET(self):
        res = requests.get(API_CONTACTOS)
        print(res.status_code, res.text)  # DEBUG
        data = res.json()
        return render.index(data["items"])


class Create:
    def GET(self):
        return render.create()

    def POST(self):
        data = web.input()
        payload = {
            "nombre": data.nombre,
            "telefono": data.telefono,
            "email": data.email
        }
        requests.post(API_CONTACTOS, json=payload)
        raise web.seeother('/')


class Edit:
    def GET(self, id):
        res = requests.get(f"{API_CONTACTO}/{id}")  # 👈 CORREGIDO
        data = res.json()

        if not data["items"]:
            return "Contacto no encontrado"

        contacto = data["items"][0]
        return render.edit(contacto)

    def POST(self, id):
        data = web.input()
        payload = {
            "nombre": data.nombre,
            "telefono": data.telefono,
            "email": data.email
        }
        requests.put(f"{API_CONTACTOS}/{id}", json=payload)
        raise web.seeother('/')


class Delete:
    def GET(self, id):
        requests.delete(f"{API_CONTACTOS}/{id}")
        raise web.seeother('/')


if __name__ == "__main__":
    app.run()