# meteoflow

A study and portfolio project: a weather aggregator based on a simple microservices architecture. It is designed to help you practice calling external APIs (OpenWeatherMap), caching with Redis, and orchestrating services with Docker Compose.

Overview
- This repository contains a minimal FastAPI-based weather service that retrieves current weather information for a given city and caches recent results in Redis. A placeholder `frontend-service/` directory is included as a starting point for a minimal frontend (CLI or web).

Goals
- Build a simple multi-service setup to learn microservices patterns.
- Demonstrate integration with an external API (OpenWeatherMap) and the benefits of caching.
- Provide a small, extendable example suitable for containerization and demos.

Project layout
- `weather-service/` — FastAPI application exposing endpoints to get weather data and cache statistics.
- `frontend-service/` — placeholder for a minimal frontend (empty by default).

Key endpoints (provided by `weather-service`)
- GET /weather/{city}
  - Returns weather data for `city`. If cached in Redis, the cached value is returned. Otherwise the service calls OpenWeatherMap and stores the result in cache (TTL = 3600s).
- GET /cache/stats
  - Returns cache information (number of keys and the list of cached cities).

Implementation notes
- Entrypoint: `weather-service/main.py` (FastAPI app).
- Router: `weather-service/routers/weather.py`.
- Core logic: `weather-service/services/weather_service.py` — handles external API calls, caching with `redis.Redis`, and loads `OPENWEATHERMAP_API_KEY` via `python-dotenv` or environment variables.

Prerequisites
- Python 3.10+ (or compatible)
- pip
- Docker (optional, recommended to run Redis and orchestrate services)
- OpenWeatherMap API key (`OPENWEATHERMAP_API_KEY`) — register at https://openweathermap.org/ to obtain one.

Run locally (PowerShell on Windows)

1) Start Redis quickly with Docker:

```powershell
docker run --name meteoflow-redis -p 6379:6379 -d redis:7
```

2) Set your OpenWeatherMap API key. You can create a `.env` file inside `weather-service/` with `OPENWEATHERMAP_API_KEY=your_key`, or set it in the environment:

```powershell
setx OPENWEATHERMAP_API_KEY "your_key"
# or for the current PowerShell session only:
$env:OPENWEATHERMAP_API_KEY = "your_key"
```

3) Install dependencies and start the weather service:

```powershell
cd weather-service
python -m pip install -r requirements.txt
# Start the FastAPI server (development)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000.

Examples
- Using curl:

```bash
curl http://localhost:8000/weather/London
curl http://localhost:8000/cache/stats
```

- Using PowerShell:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/weather/Rome
Invoke-RestMethod -Uri http://localhost:8000/cache/stats
```

Caching details
- The service currently caches responses with `cache.set(city, json.dumps(weather_data), ex=3600)` — TTL = 3600 seconds (1 hour).
- Redis configuration in `weather_service.py` is currently hardcoded as `redis.Redis(host="localhost", port=6379, db=0)`. Consider reading host/port from environment variables for flexibility.

Example `docker-compose.yml` (minimal)

```yaml
version: '3.8'
services:
  redis:
	image: redis:7
	ports:
	  - "6379:6379"

  weather-service:
	build: ./weather-service
	# if you don't have a Dockerfile you can run without build using an image:
	# image: python:3.11-slim
	environment:
	  - OPENWEATHERMAP_API_KEY=${OPENWEATHERMAP_API_KEY}
	ports:
	  - "8000:8000"
	depends_on:
	  - redis

  frontend-service:
	build: ./frontend-service
	ports:
	  - "8080:8080"
	depends_on:
	  - weather-service

# Note: this is an example. Add Dockerfiles for services if you want to build them with Compose.
```

Next steps / improvements
- Split caching into a dedicated component or wrapper service.
- Add authentication and rate limiting.
- Implement a minimal web frontend (React/Vue) or a richer CLI.
- Improve error handling and make Redis host/port configurable by environment variables.
- Add automated tests and CI configuration.

License
- (Add the project license or keep the one already present in the repository.)

Contributing
- This repository is intended as a personal study/portfolio project. Feel free to fork, propose improvements, or use it as a starting point for exercises.

Happy learning and happy coding!
