from dotenv import load_dotenv
import os
from flask import request, make_response, jsonify
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
                last_run_mode = profile.get("last_run_mode", "lite")
                data_synchronized = profile.get("lite_mode_data_is_synchronized", False)
                data_synchronize_status = profile.get("lite_mode_data_synchronize_status", "fail")
                secure_response_enabled = profile.get("secure_response_headers", {}).get("enable", False)
                
                result = make_response(func(*args, **kwargs))
                                    
                if running_mode  == "lite":
                    request_meta_data = Protection.do(self, request)
                    threading.Thread(target=Protection._mode_lite, args=(self, request_meta_data), daemon=True).start()

                if running_mode != "lite" and last_run_mode == "lite" and not data_synchronized and data_synchronize_status == "fail":
                    threading.Thread(target=Agent._synchronize, args=(self, profile), daemon=True).start()

                if running_mode == "monitor":
                    request_meta_data = Protection.do(self, request)
                    threading.Thread(target=Protection._mode_monitor, args=(self, request_meta_data), daemon=True).start()
                
                if running_mode == "protection":
                    request_meta_data = Protection.do(self, request)
                    blocked = Protection._mode_protection(self, profile, request_meta_data)
                    if blocked:
                        logger.info("Whale Sentinel Flask Agent Protection: Request blocked by Whale Sentinel Protection")
                        return jsonify({
                                "msg": "Forbidden: Request blocked by Whale Sentinel Protection.",
                                "time": str(datetime.datetime.now()),
                                "ip": request.client.host
                            }), 403

                if secure_response_enabled:
                    result = Protection._secure_response(self, profile, result)

                return result
            return wrapper
        return _whale_sentinel_agent_protection
    