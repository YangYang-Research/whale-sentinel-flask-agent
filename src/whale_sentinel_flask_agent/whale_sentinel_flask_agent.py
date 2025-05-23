from dotenv import load_dotenv
import os
import json
from .wslogger import logger
from .wsprotection import Protection
from .wsagent import Agent

class WhaleSentinelFlaskAgent(object):
    """
    Whale Sentinel Flask Agent
    """

    def __init__(self):
        """
        Initialize the Whale Sentinel Flask Agent

        :param config: Configuration dictionary
        """
        # Load environment variables from .env file
        load_dotenv()

        LOG_MAX_SIZE = os.getenv("LOG_MAX_SIZE", 10000000)  # in bytes
        LOG_MAX_BACKUPS = os.getenv("LOG_MAX_BACKUPS", 3)  # number of backup files
        WS_GATEWAY_API = os.getenv("WS_GATEWAY_API")
        WS_AGENT_AUTH_TOKEN = os.getenv('WS_AGENT_AUTH_TOKEN')
        WS_AGENT_ID = os.getenv("WS_AGENT_ID")
        self.log_max_size = int(LOG_MAX_SIZE)
        self.log_max_backups = int(LOG_MAX_BACKUPS)
        self.ws_gateway_api = WS_GATEWAY_API
        self.ws_agent_auth_token = WS_AGENT_AUTH_TOKEN
        self.agent_id = WS_AGENT_ID
        self._initialize()

    def _initialize(self):
        """
        Initialize the Whale Sentinel Flask Agent
        """
        if not self.ws_gateway_api:
            raise ValueError("WS_GATEWAY_API must be set")
        if not self.ws_agent_auth_token:
            raise ValueError("WS_AGENT_AUTH_TOKEN must be set")
        if not self.agent_id:
            raise ValueError("WS_AGENT_ID must be set")
        Agent.__init__(self)

    def whale_sentinel_agent_protection(self):
        def _whale_sentinel_agent_protection(func):
            """
            Decorator to protect the Flask with Whale Sentinel Protection
            """

            def wrapper(*args, **kwargs):
                agent_config = Agent._configuration(self)
                agent_mode = agent_config.get("running_mode", "lite")
                if agent_mode  == "lite":
                    Protection._mode_lite(self)
                    return func(*args, **kwargs)
                if agent_mode == "monitor":
                    Protection._mode_monitor(self)
                    return func(*args, **kwargs)
                if agent_mode == "protection":
                    protection = Protection.do(self)
                return func(*args, **kwargs)
            return wrapper
        return _whale_sentinel_agent_protection
    