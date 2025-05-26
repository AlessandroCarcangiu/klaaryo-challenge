# Klaaryo Assessment - Notification Dispatcher

## Environment Configuration
The project requires the following environment variables defined in a `.env` file:
```
SECRET_KEY=your_django_secrets
DJANGO_ALLOWED_HOSTS=*
DJANGO_MIGRATIONS=True
DJANGO_LOADDATA=True
DJANGO_INTIAL_DATA_PATH=stack/django/initial_data
DJANGO_PORT=your_django_port
GRPC_PORT=your_grpc_port
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=your_db_port
```

## Setup

To build and run the full stack, use the following command:

```
docker-compose up --build -d
```

The *command* specified in the Django container automatically:

* Applies database migrations
* Loads initial data from the path defined in *DJANGO\_INTIAL\_DATA\_PATH*. It creates an admin with this credentials:
  * *username*: admin
  * *password*: passwordklaaryo
* Starts the django server

## REST API Endpoints

In the folder you will find the collection for Insomnia.

All app candidate's endpoints are protected with JWT authentication. Use the token endpoints to authenticate.

### Token

**POST** Obtain token:
`http://localhost:{*DJANGO_PORT*}/api/token/`
Payload:

```
*username*: admin  
*password*: passwordklaaryo
```

**POST** Refresh token:
`http://localhost:{*DJANGO_PORT*}/api/token/refresh/`

### Candidate Management

**POST** Create candidate:
`http://localhost:{*DJANGO_PORT*}/candidates/`
Payload:

```
*full_name*: string  
*email*: string
```

**GET** Get candidate details:
`http://localhost:{*DJANGO_PORT*}/candidates/{*candidate_id*}/`

## gRPC Service

Service name: `CandidateStatusService`
Method: `GetCandidateStatus`

Request:

```
*candidate_id*: UUID
```

NB: I chose to use django-grpc instead of django-grpc-framework because the former is more actively maintained and up to date. 