# FastAPI Notifications API

This is a FastAPI-based notifications application that uses PostgreSQL as its database backend. 
The application is containerized using Docker for easy deployment and development.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

The project consists of a FastAPI application and a PostgreSQL database, both running in separate Docker containers.

## Getting Started

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

### :information_source: Seed DB with mock data:
- To load seeds, go to docker-compose.yml and uncomment `#- SEED=True` line in service `web`, `environment`'s variables.

3. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

This command will build the FastAPI app image and start both the app and the database containers.

:warning: Once Seeded, proceed to comment the `- SEED=True` line in service `web`, `environment`'s variables.

4. The API will be available at `http://localhost:8000`

## Configuration

### Environment Variables

In order to make the project plug-n-play, the following environment variables are explicitly written in compose file:

- `POSTGRES_DB`: The name of the PostgreSQL database (default: `notifications`)
- `POSTGRES_USER`: The PostgreSQL user (default: `challenge`)
- `POSTGRES_PASSWORD`: The PostgreSQL password (default: `rNmRZ6DJwvxqdQP2h7yk8z`)
- `DATABASE_URL`: The URL for connecting to the PostgreSQL database

You can modify these variables in the `docker-compose.yml` file if needed.

In order to handle secrets it can always be set as `.secret` or OS environment variables.

### Database

The PostgreSQL database runs on port 5433 of the host machine to avoid conflicts with any existing PostgreSQL instances.

## Development

To develop the application:

1. Make changes to the FastAPI application code in the `src` directory.
2. Rebuild and restart the containers:
   ```
   docker-compose down
   docker-compose up -d --build
   ```

## Database Migrations

This project uses Alembic for database migrations. Migrations are automatically applied when the container starts up.

To create a new migration:

1. Make changes to your SQLAlchemy models
2. Run the following command:
   ```
   docker-compose exec web alembic revision --autogenerate -m "Description of changes"
   ```
:information_source: You don't need to apply migrations in order to run this tests.

## API Documentation

FastAPI provides automatic API documentation. Once the application is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

To run tests, use the following command:

```
docker-compose exec web pytest
```

## Troubleshooting

If you encounter any issues, try the following steps:

1. Ensure all containers are running:
   ```
   docker-compose ps
   ```

2. Check the logs of the containers:
   ```
   docker-compose logs
   ```

3. If there are database connection issues, ensure the `db` service is fully up before the `web` service starts.

## Uninstalling

1. Removing containers, networks and volumes

```
docker-compose down --volumes
```

2. Removing elements of item 1 + Images

```
docker-compose down --rmi all --volumes
```