# ROOMS

## Instalación

1. Descargar el proyecto y ejecutar `pip install -r requirements.txt`. La versión mínima de python es 3.8.10
2. El proyecto incluye una base de datos sqlite, donde ya se migraron los modelos
3. Ejecutar el proyecto con `python manage.py runserver`
4. Ingresar a `http://127.0.0.1:8000/swagger/`. Los endpoints están allí.


Existen endpoints pretegidos por requerimiento. Las credenciales son:

   usuario: admin
   password: 123qeASDASDASD

El método de login es por un token JTW en la cabecera. Por conveniencia, el token tiene larga expiración. 
El método de autenticación en la cabecera es:

    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYyMzk4ODQwLCJpYXQiOjE2NjE5NjY4NDAsImp0aSI6IjcyZDA4NDYxMjUxNzQ1YmFhYTdmMjY2MThlN2Q3YWQ0IiwidXNlcl9pZCI6MX0.TtAaubLYRiu17V39sS0_QRFs7709e3m3kguqjFx7VfI

Se pueden obtener un nuevo token en `http://127.0.0.1:8000/login/`

Se puede ingresar el JWT en la sección authorize en /swagger

![img.png](img.png)

![img_1.png](img_1.png)

Descripción de los endpoints:

### LOGIN
```
POST
/login/
Obtiene un token JWT para autenticar al usuario
```

### Eventos
```
GET
/event/
event_list 
Lista todos los eventos para usuario buisiness (autenticado con token) o solo los públicos para customer(no autenticado)

POST
/event/
event_create
Crea un nuevo evento (requiere autenticación)

GET
/event/{id}/
event_read
Obtiene información de un evento en particular

PUT|PATCH
/event/{id}/
event_update
Actualiza la inroamación de un evento

DELETE
/event/{id}/
event_delete
Elimina un evento (requiere autenticación)

POST
/event/{id}/customer/reservation/
event_customer_create_reservation
Crea una reservación para un evento. Si ya no espacion el el room, se muestra un mensaje de error

POST
/event/{id}/customer/reservation/delete/
Elimina una reservación para un evento
```


### ROOM
```
GET
/room/
room_list
Lista todos los room (requiere autenticacion)

POST
/room/
room_create
Crea un room (requiere autenticacion)

GET
/room/{id}/
room_read
Obtiene información sobre un room (requiere autenticacion)

PUT|PATCH
/room/{id}/
room_update
Actualiza un room (requiere autenticacion)

DELETE
/room/{id}/
Remueve un room si no tiene/ha tenido/tendrá eventos (requiere autenticacion)
```
