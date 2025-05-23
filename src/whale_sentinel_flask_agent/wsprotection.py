from user_agents import parse
from flask import request
from datetime import datetime
import requests
import json
import base64
import time
from .wslogger import logger
from .wsagent import Agent

class Protection(object):
    """
    Whale Sentinel Flask Agent Protection
    """
    def __init__(self):
        """
        Initialize the Whale Sentinel Flask Agent Protection
        """

    def do(self) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection
        """
        try:
            req_method = request.method
            req_path = request.path
            req_host = request.host
            # req_headers = request.headers
            req_body = request.get_data(as_text=True)
            req_query_string = request.query_string.decode('utf-8')
            req_ip = request.remote_addr
            req_user_agent = request.user_agent.string
            req_content_type = request.content_type
            req_content_length = request.content_length
            req_referrer = request.referrer
            req_device = request.user_agent.platform
            req_network = request.user_agent.browser

            parsed_ua = parse(req_user_agent)
            req_ua_platform = parsed_ua.os.family

            req_ua_browser = parsed_ua.browser.family
            req_ua_browser_version = parsed_ua.browser.version_string
            data = {
                "agent_id": self.agent_id,
                "payload": {
                    "data": {
                        "client_information": {
                            "ip": req_ip,
                            "device_type": req_device,
                            "platform": req_ua_platform,
                            "browser": req_ua_browser,
                            "browser_version": req_ua_browser_version,
                            "network_type": req_network,
                        },
                        "http_request": {
                            "method": req_method,
                            "url": req_path,
                            "host": req_host,
                            "headers": {
                                "user-agent": req_user_agent,
                                "content-type": req_content_type,
                                "content-length": req_content_length,
                                "referrer": req_referrer
                            },
                            "body": req_body,
                            "query_parameters": req_query_string
                        },
                    }
                },
                "request_created_at": datetime.now().astimezone().isoformat()
            }
            call_request = Agent._make_call(self, data)
        except Exception as e:
            # Log the error
            logger.error(f"Error in Whale Sentinel Flask Agent Protection: {e}")