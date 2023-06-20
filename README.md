# LegalBot challenge

## Prerequisites
- Docker and Docker Compose should be installed on your system.

## Getting Started
1. Clone the repository: `git clone https://github.com/LucasDavid1/legalbot-coding-test.git`
2. Navigate to the project directory: `cd legalbot-coding-test`

## Starting the App
To start the app and run the necessary services, use the following command:

```bash
make up
```

Migrations: 
```bash
make migrate
```

Creating a Superuser
```bash
make createsuperuser
```


Run tests
```bash
make test
```


Follow the prompts to enter the superuser's username and password.

Obtaining a Token in Postman
1. Open Postman and make a POST request to `http://localhost:8000/api-token-auth/`.
2. In the request body, provide the superuser's credentials:

```json
{
    "username": "<username>",
    "password": "<password>"
}
```


3. Send the request, and the response will contain an authentication token:

```json
{
    {"token":"6f47ff0a9410da3ab8df61f64f41ef18b6fa9263"}
}
```


## Creating a New Society in Postman
1. Open Postman and make a POST request to `http://localhost:8000/societies/`.
2. In the request body, provide the necessary data for the new society:

```json
{
    "name": "<name>",
    "rut": "<rut>",
}
```

Set the request headers:
Add the authentication token to the headers. Set the Authorization header with the value Token <token_value>, where <token_value> is the authentication token obtained earlier.
Set the Content-Type header to application/json.


## Creating a new Partner
1. Open Postman and make a POST request to `http://localhost:8000/partners/`.
2. In the request body, provide the necessary data for the new partner:

```json
{
    "name": "<name>",
    "rut": "<rut>",
    "address": "<address>",
    "participation": "<participation>",
    "society": "<society_id>"
}
```

## Creating a new Administrator
1. Open Postman and make a POST request to `http://localhost:8000/administrators/`.
2. In the request body, provide the necessary data for the new administrator:

```json
{
    "name": "John Doe",
    "rut": "123456789",
    "society": 1,
    "faculties": [
        {
            "name": "Abrir una cuenta corriente"
        },
        {
            "name": "Firmar cheques"
        },
        {
            "name": "Firmar contratos"
        }
    ]
}
```

## Delete a Society
1. Open Postman and make a DELETE request to `http://localhost:8000/societies/delete/<society_id>/`.


## Retrieve a Society that contains a Partner or a Administrator
1. Open Postman and make a GET request to `http://localhost:8000/societies/partner/<partner_id>/`


## Retrieve partners and administrators of a Society given a rut
1. Open Postman and make a GET request to `http://localhost:8000/societies/partners-administrators/<rut>/`
