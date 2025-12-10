# Agent Template for SecretVM

This repository provides a template for creating and deploying Fetch.ai agents to SecretVM.
Agents deployed in SecretVM (using TEE technology) get two important properties:

* 😎 Privacy - agents' memory and storage are encrypted and can't be accessed by the hardware owner or root user of the machine
* ✅ Verifiability - using cryptographic TEE attestation, it is possible to _prove_ which source code is running in the agent

Such agents essentially become **Confidential** and **Trustless**, removing the need to trust the developer, making the code law

# Getting Started


## Preparation
1. Fork this repository.
2. Clone your forked repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```
3. Install dependencies.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development

1. In `agent.py`, update the agent's name and seed with your desired values:
```python
agent = Agent(
    name="YourAgentName",
    seed="YourAgentSecretSeed",
    port=8000,
    endpoint="http://0.0.0.0:8000/submit",
)
```

2. Defining Request and Response Models.

The SampleRequest and SampleResponse classes are placeholders. You should define the structure of the data your agent will receive and send. For example:
```python

class QueryRequest(Model):
    query: str

class QueryResponse(Model):
    response: str
```

3. Implementing Agent Logic

The core logic of your agent resides in the `handle_request` function. This is where you will process incoming requests and generate responses.

```python
@sample_proto.on_message(QueryRequest, replies={QueryResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: QueryRequest):
    try:
        # Your agent's logic here
        ctx.logger.info(f"Received query: {msg.query}")
        response_message = f"I received your query: {msg.query}"
        await ctx.send(sender, QueryResponse(response=response_message))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
```

4. Customizing Health Checks

The `agent_is_healthy` function in `agent.py` allows you to implement custom health checks for your agent. This is useful for monitoring the agent's status and its ability to connect to any required third-party services.
```python
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    # Example: Check connectivity to an external service
    # try:
    #     response = requests.get("https://api.example.com/status")
    #     return response.status_code == 200
    # except requests.RequestException:
    #     return False
    condition = True
    return bool(condition)
```

For more information on FetchAI agents developing, please fisit the [official documentation](https://uagents.fetch.ai/docs/quickstart).

## Deployment to SecretVM

The deployment process is automated through a GitHub Actions workflow defined in `.github/workflows/docker-build-secretvm.yml`.

The workflow is triggered when you create and push a new git tag in the format `v[0-9]+.[0-9]+.[0-9]+` (e.g., `v0.1.0`). After the worklow succeeds, it updates `docker-compose-secretvm.yaml` file and commits it back to your repository. You can then use this file to deploy your agent on SecretVM. Follow the [SecretVM documentation](https://docs.scrt.network/secret-network-documentation/secretvm-confidential-virtual-machines/launching-a-secretvm) to deploy your agent using the generated `docker-compose-secretvm.yaml`.
