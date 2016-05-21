#![Simple Load-Balancer](http://blog.pysoy.org/images/python-square-64.png "Simple Load-Balancer")   Simple Load-Balancer


## Introducción
Se trata de un proyecto personal por el cual aprender un poco mas sobre *Python, flask, jwt y términos como balanceador de carga y gestión de microservicios*.


### ¿Qué es un balanceador de carga?
Según [Wikipedia][wikipedia-loadbalancer]:
>Un balanceador de carga fundamentalmente es un dispositivo de hardware o software que se pone al frente de un conjunto de servidores que atienden una aplicación y, tal como su nombre lo indica, asigna o balancea las solicitudes que llegan de los clientes a los servidores usando algún algoritmo *(desde un simple Round Robin hasta algoritmos más sofisticados)*.

### ¿Qué son los microservicios?
Según [Diego Uribe Gamez @ Platzi][platzi-microservicios]:
>Un sistema basado en Microservicios es aquel que distribuye toda su organización de forma vertical, aquí el detalle es que un tipo de información solicitada puede ser consultada a su servicio específico, este servicio independiente en recursos es capaz de responder la solicitud.

### ¿Qué es flask?
Escrito por [kmilo @ doutdeslibertas][flask-doutdeslibertas]:
>Flask es un microframework de python para aplicaciones web, que emplea objetos locales de subprocesos para peticiones, secciones y algún objeto extra [...] En pocas palabras Flask es ideal para aplicaciones grandes o para servidores asincrónicos, pero su objetivo es lograr esto de manera rápida y fácil.

### ¿Qué es JWT o Autenticación con JSON Web Tokens?
Explicado en [jwt.io][jwt.io]
>JSON Web Token *(JWT)* es un estándar abierto [RFC 7519][rfc-jwt] que define una forma compacta y auto contenida para la transmisión segura de información entre cliente/servidor con un objeto JSON. Esta información puede ser verificada y de confianza porque es firmada digitalmente. Estos tokens pueden ser firmados utilizando una clave secreta *(con el algoritmo HMAC)* o con un par de claves pública / privada *(utilizando RSA)*.

## ¿Qué funcionalidad ofrece este proyecto?
### Registro de usuarios
Para comenzar a utilizar este balanceador de carga, un usuario se debe registrar en él. Para ello:
```
curl -H "Content-Type: application/json" -X POST -d '{"email":"your@email.com","password":"yourpassword"}' http://localhost:5000/api/users
```
El json enviado se valida contra un json schema:
```
{
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"},
        "password": {"type": "string", "minLength": 6, "maxLength": 30},
    },
    "required": ["email", "password"]
}
```

### Generación de tokens


### Disclaimer
Es un proyecto simple, es decir, falta funcionalidad clave para convertirse en un producto terminado y plenamente productivo. Alguna funcionalidad no implementada que puede echarse en falta puede ser:
1. Registro en dos pasos *(email de confirmación, sms u otro método)*
2. Baja de usuario en dos pasos *(email de confirmación, sms u otro método)*
    * Baja *lógica*, en lugar de borrado *físico*
3. Logs de auditoria de aplicaciones.
    * Está implementado una auditoria muy ligera en MongoDB.
4. Aplicar un rate limit de peticiones.
5. Gestión de errores mas depurada.

Seguro que falta alguna funcionalidad crítica mas :), sed creativos, espero vuestros pr.


[wikipedia-loadbalancer]: https://es.wikipedia.org/wiki/Balanceador_de_carga
[platzi-microservicios]: https://platzi.com/blog/arquitectura-microservicios/
[flask-doutdeslibertas]: https://doutdeslibertas.wordpress.com/python-en-la-web2-0/
[jwt.io]: https://jwt.io/introduction/
[rfc-jwt]: https://tools.ietf.org/html/rfc7519
