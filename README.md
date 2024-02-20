
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

# Nomad World - FAST API
A brief description of what this project does and who it's for


## API
## API REST para la gestión de usuarios y configuración de usuario

Esta API REST proporciona endpoints para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) relacionadas con usuarios, así como para la gestión de la configuración del usuario.

## Endpoints

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
