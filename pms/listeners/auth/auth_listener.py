import pms.listeners.auth.user_actions as useractions
import logging, asyncio
import pms.database.db_handlers.user_db_handler as user_db_handler
import json
auth_routing_actions = {"user_account_created": useractions.user_account_create}

LOGGER = logging.getLogger(__name__)


def auth_listener(ch, method, properties, body:str):
    data = json.loads(body)
    asyncio.run(auth_routing_actions["user_account_created"](data_obj=data))
    # asyncio.run(user_db_handler.save_mail(mail=str(body)))

