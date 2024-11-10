### AI Writing Assistant for Sci-fi Authors

This project was developed for the [Open Source AI Challenge with pgai and Ollama](https://dev.to/challenges/pgai)

It is a tool for science fiction authors to overcome writer's block by using AI as an assistant to help complete the story.

### Tools

#### Dev Challenge Tools
- pgai / postgresql
- ollama

#### Other technologies
- Nuxt.js
- FastAPI
- TailwindCSS

#### Getting Started

This project can be run with docker:

```
docker compose up -d
```

This should start several containers for the frontend, backend, ollama model, and postgresql database. There is also a container for the vectorizer worker, though it is not used in this project since I did not end up using OpenAI.

For more details on the project, check out the [challenge submission]().