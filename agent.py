from enum import Enum

from uagents import Agent, Model, Context
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage


###################
# Main Logic Code #
###################
class SampleRequest(Model):
    # TODO: implement your request
    pass


class SampleResponse(Model):
    # TODO: implement your response
    pass


agent = Agent(
    # TODO: define name, seed, port and endpoint
    name="Sample Agent",
    seed="SampleSeed",
    port=8000,
    endpoint="http://localhost:8000/submit",
)

sample_proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Sample-Name",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=6),
)


@sample_proto.on_message(SampleRequest, replies={SampleResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: SampleRequest):
    try:
        # TODO: Add your logic here
        pass
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error="An error occurred while processing the request. Please try again later."
            ),
        )
        return
    await ctx.send(sender, SampleResponse())


agent.include(sample_proto, publish_manifest=True)


#####################
# Health Check Code #
#####################
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.

    For example, check if the agent can connect to a third party API,
    check if the agent has enough resources, etc.
    """
    condition = True  # TODO: logic here
    return bool(condition)


class HealthCheck(Model):
    pass


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class AgentHealth(Model):
    agent_name: str
    status: HealthStatus


health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)


@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))


agent.include(health_protocol, publish_manifest=True)


#############
# Main Code #
#############
if __name__ == "__main__":
    agent.run()
