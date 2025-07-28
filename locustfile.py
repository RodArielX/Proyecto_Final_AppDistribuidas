from locust import HttpUser, task, between

class InventarioUser(HttpUser):
    wait_time = between(1, 3)  # Simula espera entre solicitudes

    def on_start(self):
        # Autenticación (ajusta si usas otra cuenta)
        self.client.post("/login", data={
            "email": "admin@gmail.com",
            "password": "1234"
        })

    @task
    def dashboard(self):
        self.client.get("/dashboard")

    @task
    def registrar(self):
        self.client.post("/registrar", data={
            "nombre": "Mouse Gamer",
            "codigo": "MG999",
            "descripcion": "Mouse con luces RGB",
            "unidad": "pza",
            "categoria": "Accesorios"
        })

    @task
    def consultar(self):
        self.client.get("/consultar")
