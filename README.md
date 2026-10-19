# Cloud Native AI - Exercises

*Tom Berger, HTWG*

## Exercises

Exercise results are found in [exercises/](exercises/index.md).

## Architecture

### Services
- **ollama:** loads the model and offers an OpenAI-compatible API
- **modell-laden:** runs on setup and downloads two models through ollama
- **app:** the actual python app to run and utilize the model

### Model Interaction

The app connects to the ollama service through the docker network and requests the completions from the model provided as `LLM_MODEL` in the environment variables.

## Startup

Expects a `.env` file similar to `env.example` in the project root.

```sh
docker compose run --rm app <any python script in app/>

// example:
docker compose run --rm app einordnen.py
```

