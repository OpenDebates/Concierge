import hmac
import logging

import toml
from discord.ext import ipc
from quart import Quart, request, Response

logger = logging.getLogger(__name__)

app = Quart(__name__)

config = toml.load('config.toml')
ipc_client = ipc.Client(
    secret_key=config['global']['ipc_secret']
)


@app.route('/webhook', methods=['POST'])
async def respond():
    token = request.headers.get('Digest').split("=", 1)[1]
    request_data = await request.get_data()
    new_digest = hmac.new(
        key=config['webhook']['signature'].encode(),
        msg=request_data,
        digestmod="md5"
    ).hexdigest()
    comparison = hmac.compare_digest(token, new_digest)
    json = await request.json
    if comparison:
        sent = await ipc_client.request(
            'on_webhook_received',
            request_json=json
        )
        if sent:
            logger.info(f"[{request.host}] Status: Success")
            return Response(
                status=200, response={
                    "Status": "Success"
                }
            )
        else:
            logger.info(f"[{request.host}] Status: Bad Request")
            return Response(
                status=400, response={
                    "Status": "Bad Request"
                }
            )
    else:
        logger.info(f"[{request.host}] Status: Forbidden")
        return Response(
            status=403,
            response={"Status": "Forbidden"}
        )
