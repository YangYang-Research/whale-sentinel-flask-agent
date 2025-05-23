
import os
import base64
from datetime import datetime
from .wslogger import logger
import requests
import time

class Agent(object):
    def __init__(self):
        """
        Initialize the Whale Sentinel Flask Agent
        """
        ws_auth_string = f"ws-agent:{self.ws_agent_auth_token}"
        ws_base64_auth_string = base64.b64encode(ws_auth_string.encode()).decode()
        self.ws_authentication = ws_base64_auth_string
        Agent._communication(self)
    
    def _communication(self):
        """
        Communicate with the Whale Sentinel Gateway API
        """
        try:
            endpoint = self.ws_gateway_api + "/agent-configuration"
            data = {
                "agent_id": self.agent_id,
                "request_created_at": datetime.now().astimezone().isoformat()
            }
            call_response = Agent._make_call(self, endpoint, data)
            if call_response is None:
                logger.info("Whale Sentinel Flask Agent Protection: Communication with Whale Sentinel Gateway failed")
                for i in range(3):
                    time.sleep(30)
                    logger.info(f"Whale Sentinel Flask Agent Protection: Attempt communication {i + 1} failed")
                    call_response = Agent._make_call(self, endpoint, data)
                    if call_response is not None:
                        break
            else:
                logger.info("Whale Sentinel Flask Agent Protection: Commmunication with Whale Sentinel Gateway successful")
        except Exception as e:
            logger.error(f"Error in Whale Sentinel Flask Agent Protection: {e}")

    def _configuration(self):
        """
        Get the configuration of the Whale Sentinel Flask Agent
        """
        try:
            endpoint = self.ws_gateway_api + "/agent-configuration"
            data = {
                "agent_id": self.agent_id,
                "request_created_at": datetime.now().astimezone().isoformat()
            }
            call_response = Agent._make_call(self, endpoint, data)
            if call_response is None:
                logger.info("Whale Sentinel Flask Agent Protection: Communication with Whale Sentinel Gateway failed")
                return None
            else:
                return call_response.get("configurations", {})
        except Exception as e:
            logger.error(f"Error in Whale Sentinel Flask Agent Protection: {e}")

    def _make_call(self, endpoint, data) -> None:
        """
        Make a call to the Whale Sentinel Gateway API
        """
        try:
            print("API", endpoint)
            print("AUTH", self.ws_authentication)
            print("DATA", data)
            print("+++++++++++++++++2++++++++++++++")
            response = requests.post(
                url=endpoint,
                headers={
                    "Authorization": f"Basic {self.ws_authentication}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            if response.status_code != 200:
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Request failed: {e}")
        except Exception as e:
            # Log the error
            logger.error(f"Error in Whale Sentinel Flask Agent Protection: {e}")