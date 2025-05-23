from user_agents import parse
from flask import request
from datetime import datetime
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
    
    def _mode_lite(self):
        """
        Perform the Whale Sentinel Flask Agent Protection in lite mode
        """
        try:
            request_meta_data = Protection.do(self)
            Agent._write_to_storage(self, request_meta_data)
        except Exception as e:
            logger.error(f"Something went wrong at {0}.\n Error message - {1}".format("Protection._mode_lite", e))
    
    def _mode_monitor(self):
        """
        Perform the Whale Sentinel Flask Agent Protection in monitor mode
        """
        try:
            request_meta_data = Protection.do(self)
            Agent._detection(self, request_meta_data)
        except Exception as e:
            logger.error(f"Something went wrong at {0}.\n Error message - {1}".format("Protection._mode_monitor", e))

    def _mode_protection(self, profile) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection in protection mode
        """
        try:
            wad_threshold = profile.get("ws_module_web_attack_detection", {}).get("threshold", {})
            dgad_threshold = profile.get("ws_module_dga_detection", {}).get("threshold", {})
            request_meta_data = Protection.do(self)
            detection = Agent._detection(self, request_meta_data)
            if detection is not None:
                wad = detection.get("ws_module_web_attack_detection_score", 0)
                dgad = detection.get("ws_module_dga_detection_score", 0)
                cad = detection.get("ws_module_common_attack_detection", {})
                if wad >= wad_threshold or dgad >= dgad_threshold or any(cad.values()):
                    return True
                return True
            return False
        except Exception as e:
            logger.error(f"Something went wrong at {0}.\n Error message - {1}".format("Protection._mode_protection", e))

    def _secure_response(self, profile, response):
        """
        Secure the response headers
        """
        try:
            secure_headers = profile.get("secure_response_headers", {}).get("headers", {})
            for key, value in secure_headers.items():
                response.headers[key] = value
            return response
        except Exception as e:
            logger.error(f"Something went wrong at {0}.\n Error message - {1}".format("Protection._secure_response", e))
  
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

            meta_data = {
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
            return meta_data
        except Exception as e:
            logger.error(f"Something went wrong at {0}.\n Error message - {1}".format("Protection.do", e)) 