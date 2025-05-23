from dotenv import load_dotenv
import os
from flask import request, make_response
from .wslogger import logger
from .wsprotection import Protection
from .wsagent import Agent
import threading
import datetime

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
        try:
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
        except Exception as e:
            logger.error(f"Error initializing Whale Sentinel Flask Agent: {e}")
            raise

    def _initialize(self):
        """
        Initialize the Whale Sentinel Flask Agent
        """
        try:
            if not self.ws_gateway_api:
                raise ValueError("WS_GATEWAY_API must be set")
            if not self.ws_agent_auth_token:
                raise ValueError("WS_AGENT_AUTH_TOKEN must be set")
            if not self.agent_id:
                raise ValueError("WS_AGENT_ID must be set")
            Agent.__init__(self)
        except Exception as e:
            logger.error(f"Error in Whale Sentinel Flask Agent initialization: {e}")

    def whale_sentinel_agent_protection(self):
        def _whale_sentinel_agent_protection(func):
            """
            Decorator to protect the Flask with Whale Sentinel Protection
            """
            def wrapper(*args, **kwargs):
                profile = Agent._profile(self)
                if profile is None:
                    logger.info("Whale Sentinel Flask Agent Protection: No profile found, skipping protection")
                    return func(*args, **kwargs)
                
                running_mode = profile.get("running_mode", "lite")
                secure_respone = profile.get("secure_response_headers", {}).get("enable", False)
                response = make_response(func(*args, **kwargs))
                
                if running_mode  == "lite":
                    Protection._mode_lite(self)

                if running_mode == "monitor":
                    threading.Thread(target=Protection._mode_monitor(self), daemon=True).start()
                
                if running_mode == "protection":
                    protection = Protection._mode_protection(self, profile)
                    if protection:
                        logger.info("Whale Sentinel Flask Agent Protection: Request blocked by Whale Sentinel Protection")
                        response.status_code = 403
                        response.data = f"Forbidden: Request blocked by Whale Sentinel Protection.\nTime: {datetime.datetime.now()}\nIP: {request.remote_addr}"
                        return response

                if secure_respone:
                    new_response = Protection._secure_response(self, profile, response)
                    return new_response

                return response
            return wrapper
        return _whale_sentinel_agent_protection
    