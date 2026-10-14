# Cloud Native AI - Exercises

## Exercises

Exercise results are found in [exercises/](exercises/index.md).

## Architecture

### Services
- **ollama:** loads the model and offers an OpenAI-compatible API
- **modell-laden:** runs on setup and downloads two models through ollama
- **app:** the actual python app to run and utilize the model

### Model Interaction

The app connects to the ollama service through the docker network and requests the completions from the model provided as `LLM_MODEL` in the environment variables.

