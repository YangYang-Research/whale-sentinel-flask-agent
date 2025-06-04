import redis
import json

r = redis.Redis(
    host='localhost',
    port=6379,
    password="your-redis-password",
    decode_responses=True
)

# Dữ liệu JSON cấu hình agent
agent_config = {
  "profile": {
    "running_mode": "protection",
    "last_run_mode": "lite",
    "lite_mode_data_is_synchronized": False,
    "lite_mode_data_synchronize_status": "fail",
    "ws_module_web_attack_detection": {
      "enable": True,
      "detect_header": False,
      "threshold": 70,
    },
    "ws_module_dga_detection": {
      "enable": True,
      "threshold": 70,
    },
    "ws_module_common_attack_detection": {
      "enable": True,
      "detect_cross_site_scripting": True,
      "detect_http_large_request": True,
      "detect_sql_injection": True,
      "detect_http_verb_tampering": True
    },
    "secure_response_headers": {
      "enable": True,
      "headers": {
        "Server": "Whale Sentinel",
        "X-Whale-Sentinel": "1",
        "Referrer-Policy": "no-referrer-when-downgrade",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "X-Frame-Options": "SAMEORIGIN",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "X-Permitted-Cross-Domain-Policies": "none",
        "Expect-CT": "enforce; max-age=31536000",
        "Feature-Policy": "fullscreen 'self'",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "X-UA-Compatible": "IE=Edge,chrome=1",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST",
        "Access-Control-Allow-Credentials": "True",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
      }
    }
  }
}

r.set("ws_agent_1", json.dumps(agent_config))

print("✅ Pushed ws_agent_1 configuration to Redis.")

