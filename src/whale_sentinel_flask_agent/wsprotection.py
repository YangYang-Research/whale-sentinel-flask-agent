import base64
import hashlib
from user_agents import parse
from datetime import datetime, timezone
from .wslogger import wslogger
from .wsagent import Agent

class Protection(object):
    """
    Whale Sentinel Flask Agent Protection
    """
    def __init__(self):
        """
        Initialize the Whale Sentinel Flask Agent Protection
        """
    
    def _mode_lite(self, request_meta_data) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection in lite mode
        """
        try:
            Agent._write_to_storage(self, request_meta_data)
        except Exception as e:
            wslogger.error(f"Something went wrong at Protection.__init__.\n Error message - {e}")
    
    def _mode_monitor(self, request_meta_data) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection in monitor mode
        """
        try:
            detection = Agent._detection(self, request_meta_data)
            if detection is None:
                Agent._write_to_storage(self, request_meta_data)
        except Exception as e:
            wslogger.error(f"Something went wrong at Protection._mode_monitor.\n Error message - {e}")

    def _mode_protection(self, profile, request_meta_data) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection in protection mode
        """
        try:
            wad_threshold = profile.get("ws_module_web_attack_detection", {}).get("threshold", {})
            dgad_threshold = profile.get("ws_module_dga_detection", {}).get("threshold", {})
            analysis_metrix, analysis_result  = Agent._detection(self, request_meta_data)
            if analysis_metrix is None or analysis_result is None:
                Agent._write_to_storage(self, request_meta_data)
                return False
            wad = analysis_metrix.get("ws_module_web_attack_detection_score", 0)
            dgad = analysis_metrix.get("ws_module_dga_detection_score", 0)
            cad = analysis_metrix.get("ws_module_common_attack_detection", {})
            agent_action = analysis_result
            agent_self_action = "ALLOW" #Default agent action is allow
            if wad >= wad_threshold or dgad >= dgad_threshold or any(cad.values()):
                agent_self_action = "BLOCK"
            if (agent_action == "ABNORMAL_REQUEST") and agent_self_action == "BLOCK":
                return True
            return False
        except Exception as e:
            wslogger.error(f"Something went wrong at Protection._mode_protection.\n Error message - {e}")

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
            wslogger.error(f"Something went wrong at Protection._secure_response.\n Error message - {e}")
               
    def do(self, request) -> None:
        """
        Perform the Whale Sentinel Flask Agent Protection
        """
        try:
            req_method = request.method
            req_path = request.path
            req_host = request.host
            req_headers = request.headers
            req_body = request.get_data(as_text=True) if req_method != 'GET' else None
            req_query_string = request.query_string.decode('utf-8')
            req_ip = request.remote_addr if request.remote_addr else "N/A"
            req_user_agent = request.user_agent.string if request.user_agent else "N/A"
            req_content_type = req_headers.get("Content-Type", "N/A")
            req_content_length = int(req_headers.get("Content-Length", 0))
            req_referrer = request.referrer if request.referrer else "N/A"
            req_device = request.user_agent.platform 
            req_network = request.user_agent.browser

            parsed_ua = parse(req_user_agent)
            req_ua_platform = parsed_ua.os.family
            req_ua_browser = parsed_ua.browser.family
            req_ua_browser_version = parsed_ua.browser.version_string

            uploaded_files_info = []
            if "multipart/form-data" in request.headers.get("content-type", ""):
                for file in request.files.values():
                    contents = file.read()
                    file.seek(0)  # Reset for later use

                    sha256_hash = hashlib.sha256(contents).hexdigest()
                    encoded_content = base64.b64encode(contents).decode("utf-8")
                    file_size = len(contents)

                    file_info = {
                        'file_name': file.filename,
                        'file_size': len(file.read()),
                        'file_content': encoded_content,
                        'file_type': file.content_type,
                        'file_hash256': sha256_hash
                    }
                    uploaded_files_info.append(file_info)
    
            meta_data = {
                "payload": {
                    "data": {
                        "agent_id": self.agent_id,
                        "agent_name": self.agent_name,
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
                            "query_parameters": req_query_string,
                            "files": uploaded_files_info
                        },
                    }
                },
                "request_created_at": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            return meta_data
        except Exception as e:
            wslogger.error(f"Something went wrong at Protection.do.\n Error message - {e}")