import web
import requests
import os

urls = (
    '/', 'Index',
    '/create', 'Create',
    '/edit/(\\d+)', 'Edit',
    '/delete/(\\d+)', 'Delete'
)

web.config.debug = False

app_web = web.application(urls, globals())
render = web.template.render('templates/')

PUERTO = os.environ.get("PORT", "8000")
BASE_URL = f"http://127.0.0.1:{PUERTO}/v1"

API_CONTACTOS = f"{BASE_URL}/contactos"
API_CONTACTO = f"{BASE_URL}/contacto"

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


wsgi_app = app_web.wsgifunc()

if __name__ == "__main__":
    app_web.run()