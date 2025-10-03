# weather-app

An MCP server built with [Smithery CLI](https://smithery.ai/docs/getting_started/quickstart_build_python)


# Functions of the tools that are being connected
This weather app has two functions: get alert and get forecast. Get alert gets any weather alert within the U.S. state, and get forecast gets the weather forecast for that location.

To make things more interesting, if you ask the it to speak in a pirate like tone, it can answer your requests with such a tone.


## Prerequisites

- **Smithery API key**: Get yours at [smithery.ai/account/api-keys](https://smithery.ai/account/api-keys)

## Getting Started with running the server

1. Run the server:
   ```bash
   uv run dev
   ```

2. Test interactively:

   ```bash
   uv run playground
   ```

Try saying "Say hello to John" to test the example tool.

## Development of the server

Your server code is in `src/hello_server/server.py`. Add or update your server capabilities there.

## Deploying the server

Ready to deploy? Push your code to GitHub and deploy to Smithery:

1. Create a new repository at [github.com/new](https://github.com/new)

2. Initialize git and push to GitHub:
   ```bash
   git add .
   git commit -m "Hello world 👋"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. Deploy your server to Smithery at [smithery.ai/new](https://smithery.ai/new)
