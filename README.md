
# Nomad World - BackEnd

A brief description of what this project does and who it's for


## Authors
- [@AlbertDarchiev](https://github.com/AlbertDarchiev)
- [@DReino03](https://github.com/DReino03) 
- [@LorenzoDalmaau](https://github.com/LorenzoDalmaau)
- [@peronaOscar](https://github.com/peronaOscar)

## FrontEnd Project
- [Nomad World - FrontEnd](https://github.com/LorenzoDalmaau/NomadWorld_Front-end_Flutter)

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

# Nomad World - About
Nomad World es un proyecto diseñado para entusiastas de viajar que desean explorar rutas de viaje compartidas por otros usuarios. La plataforma trabajará a modo de red social, esta permitirá a los usuario poder publicar el itinerario de sus viajes para así poder compartirlo con el resto de usuarios para inspirar a los usuario para sus próximos viajes.

# Technologies
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)




## Endpoints API

### Usuarios

#### Obtener todos los usuarios

- **Método:** `GET`
- **Ruta:** `/users`
- **Respuesta:** Devuelve una lista de todos los usuarios registrados en el sistema.

#### Obtener un usuario por su ID

- **Método:** `GET`
- **Ruta:** `/users/{user_id}`
- **Parámetros de URL:** `user_id` (int) - ID del usuario que se desea obtener.
- **Respuesta:** Devuelve los detalles del usuario correspondiente al ID proporcionado, incluyendo las rutas y ubicaciones guardadas por ese usuario.

#### Registrar un nuevo usuario

- **Método:** `POST`
- **Ruta:** `/register`
- **Parámetros de la solicitud:** Se deben proporcionar los detalles del usuario a registrar en el cuerpo de la solicitud.
- **Respuesta:** Devuelve los detalles del usuario recién registrado.

#### Iniciar sesión de usuario

- **Método:** `POST`
- **Ruta:** `/login`
- **Parámetros de la solicitud:** Se deben proporcionar las credenciales de inicio de sesión del usuario en el cuerpo de la solicitud.
- **Respuesta:** Devuelve los detalles del usuario si las credenciales son válidas.

### Configuración de usuario

#### Restablecer contraseña del usuario

- **Método:** `PATCH`
- **Ruta:** `/users/restore_pass/{user_mail}`
- **Parámetros de URL:** `user_mail` (str) - Correo electrónico del usuario al que se le restablecerá la contraseña.
- **Respuesta:** Si se encuentra el usuario correspondiente al correo electrónico proporcionado, se restablece la contraseña y se envía al usuario por correo electrónico.

#### Modificar detalles del usuario

- **Método:** `PATCH`
- **Ruta:** `/users/modify/{user_id}`
- **Parámetros de URL:** `user_id` (int) - ID del usuario que se desea modificar.
- **Parámetros de la solicitud:** Se deben proporcionar los detalles actualizados del usuario en el cuerpo de la solicitud.
- **Respuesta:** Si se encuentra el usuario correspondiente al ID proporcionado, se actualizan los detalles del usuario.



## Endpoints de Países

### Obtener información de país

- **Método:** `GET`
- **Ruta:** `/country/`
- **Descripción:** Devuelve información sobre todos los países almacenados en la base de datos.
- **Respuesta:** Devuelve una lista de objetos que representan información sobre cada país.

## Endpoints de Rutas

### Obtener rutas por número de "Me gusta"

- **Método:** `GET`
- **Ruta:** `/route/more_likes/`
- **Descripción:** Devuelve las rutas ordenadas por el número de "Me gusta" de forma descendente.
- **Respuesta:** Devuelve una lista de rutas con sus respectivas ubicaciones y el número total de "Me gusta".

### Obtener todas las rutas

- **Método:** `GET`
- **Ruta:** `/route/`
- **Descripción:** Devuelve todas las rutas almacenadas en la base de datos.
- **Respuesta:** Devuelve una lista de todas las rutas con sus respectivas ubicaciones.

### Obtener rutas por país

- **Método:** `GET`
- **Ruta:** `/route/{country_name}`
- **Parámetros de URL:** `country_name` (str) - Nombre del país del que se desean obtener las rutas.
- **Descripción:** Devuelve todas las rutas asociadas con el país especificado.
- **Respuesta:** Devuelve una lista de rutas con sus respectivas ubicaciones para el país especificado.

### Crear una nueva ruta

- **Método:** `POST`
- **Ruta:** `/create_route/{country_name}`
- **Parámetros de URL:** `country_name` (str) - Nombre del país al que pertenece la ruta que se desea crear.
- **Descripción:** Crea una nueva ruta asociada al país especificado.
- **Respuesta:** Devuelve los detalles de la ruta recién creada.

### Guardar una ruta para un usuario

- **Método:** `PATCH`
- **Ruta:** `/save/route/`
- **Descripción:** Guarda una ruta específica para un usuario.
- **Respuesta:** Devuelve los detalles actualizados del usuario después de guardar la ruta.

### Eliminar una ruta guardada de un usuario

- **Método:** `PATCH`
- **Ruta:** `/unsave/route/`
- **Descripción:** Elimina una ruta guardada de un usuario.
- **Respuesta:** Devuelve los detalles actualizados del usuario después de eliminar la ruta.

## Endpoints de Ubicaciones

### Obtener todas las ubicaciones

- **Método:** `GET`
- **Ruta:** `/location`
- **Descripción:** Devuelve información sobre todas las ubicaciones almacenadas en la base de datos.
- **Respuesta:** Devuelve una lista de objetos que representan información sobre cada ubicación.

### Obtener ubicaciones por país

- **Método:** `GET`
- **Ruta:** `/location/{country_name}`
- **Parámetros de URL:** `country_name` (str) - Nombre del país del que se desean obtener las ubicaciones.
- **Descripción:** Devuelve todas las ubicaciones asociadas con el país especificado.
- **Respuesta:** Devuelve una lista de ubicaciones para el país especificado.

### Obtener una ubicación por su ID

- **Método:** `GET`
- **Ruta:** `/location/id/{loc_id}`
- **Parámetros de URL:** `loc_id` (int) - ID de la ubicación que se desea obtener.
- **Descripción:** Devuelve información detallada sobre una ubicación específica.
- **Respuesta:** Devuelve detalles sobre la ubicación especificada por su ID.

### Crear una nueva ubicación

- **Método:** `POST`
- **Ruta:** `/create_location/{country_name}`
- **Parámetros de URL:** `country_name` (str) - Nombre del país al que pertenece la ubicación que se desea crear.
- **Descripción:** Crea una nueva ubicación asociada al país especificado.
- **Respuesta:** Devuelve detalles sobre la ubicación recién creada.

### Guardar una ubicación para un usuario

- **Método:** `PATCH`
- **Ruta:** `/save/location/`
- **Descripción:** Guarda una ubicación específica para un usuario.
- **Respuesta:** Devuelve los detalles actualizados del usuario después de guardar la ubicación.

### Eliminar una ubicación guardada de un usuario

- **Método:** `PATCH`
- **Ruta:** `/unsave/location/`
- **Descripción:** Elimina una ubicación guardada de un usuario.
- **Respuesta:** Devuelve los detalles actualizados del usuario después de eliminar la ubicación.



## Notas
- Se utilizan excepciones HTTP para manejar los posibles errores y devolver códigos de estado adecuados.
- Se implementan medidas de seguridad, como el almacenamiento seguro de contraseñas con hash.
- Se envían correos electrónicos de confirmación y notificación para ciertas operaciones, como el registro de usuarios y el restablecimiento de contraseñas.

## Features
- Crear Rutas / Localizaciones
- Almazenar datos en BD de fl0
- Subir imagenes al servidor de ImageKit
- Restablecer contraseña con EmailSender
- Hashear contraseñas de usuarios al guardar en BD

## EXTRA Features
- añadir / borrar comentarios de Rutas / Localizaciones
- añadir / borrar likes de Rutas / Localizaciones
## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Demo
- [Test VIdeo](https://www.youtube.com/watch?v=OyfQn08FZz8)

## Evolution of Nomad World
### Sprint 1

### Sprint 2
- [Test VIdeo](https://www.youtube.com/watch?v=OyfQn08FZz8)

### Sprint 3

### Sprint 5
- [Test VIdeo](https://www.youtube.com/watch?v=cOfXAh2gW2o)
