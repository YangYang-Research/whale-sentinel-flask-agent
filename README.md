# 🐋 Whale Sentinel Flask Agent

The **Whale Sentinel Flask Agent** is a security middleware for Flask applications. It enables request monitoring, metadata collection, and protection against abnormal or malicious behaviors through various operating modes.

---

## 🚀 Operation Modes

The agent supports four operation modes, defined in the agent’s `profile`:

| Mode         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `off`        | Disables protection. All requests are processed normally without any interception or data collection. |
| `lite`       | Collects basic metadata for each request. Executes lightweight background analysis. |
| `monitor`    | Collects full request metadata and performs in-depth analysis in monitoring mode. Requests are not blocked. |
| `protection` | Full protection mode. Detects and blocks suspicious or malicious requests.  |

**Additional Feature**:
- `secure_response_headers`: If enabled in the profile, security-related HTTP headers are added to each response.

---

## 📦 `@whale_sentinel_agent_protection` Decorator

This decorator is applied to Flask route handlers to enable Whale Sentinel's protection logic. Based on the configured mode, it may:

- Collect and store request metadata.
- Analyze requests in the background.
- Block potentially harmful requests (`protection` mode only).
- Synchronize runtime data if required.

**Example**:

```python
@app.route('/api/secure-data')
@agent.whale_sentinel_agent_protection()
def secure_endpoint():
    return jsonify({"status": "protected"})
```

## 🧾 Metadata Collected by Agent

Each processed request will generate a structured metadata payload containing detailed runtime, request, client, and file information.

### 1. Agent Information
- `agent_id`
- `agent_name`

### 2. Client Information
- `ip`: Client IP address
- `device_type`: Mobile, Desktop, etc.
- `platform`: Operating system platform
- `browser`, `browser_version`
- `network_type`

### 3. HTTP Request Information
- `method`, `url`, `scheme`, `host`, `endpoint`
- `headers`:
  - `user-agent`
  - `content-type`
  - `content-length`
  - `referrer`
- `body`: Request body content
- `query_parameters`: Query string parameters

### 4. Uploaded Files Metadata

For each uploaded file, the following metadata is collected:

- `file_name`: Name of the uploaded file
- `file_size`: File size in bytes
- `file_type`: MIME type of the file
- `file_content`: Base64-encoded content of the file
- `file_hash256`: SHA-256 hash of the file content

### 5. Runtime Environment Information
- `ip_address`: Server IP
- `pid`: Process ID
- `run_as`: Current user running the process
- `executable_path`, `executable_name`, `executable_version`
- `process_name`, `process_path`, `process_command`
- `platform`: OS platform
- `cpu_usage`: CPU usage %
- `memory_usage`: Memory usage %
- `architecture`: System architecture (e.g., x86_64)
- `os_name`, `os_version`, `os_build`

### 6. Timestamp
- `request_created_at`: Time when the request was processed (UTC ISO 8601 format)

## 🛠 Integration Guide

Apply the decorator to any Flask route you want to protect:

```python
@app.route('/login')
@agent.whale_sentinel_agent_protection()
def login():
    return jsonify({"message": "This route is monitored and protected."})
```

## 📌 Notes

- All analysis and data storage are performed asynchronously to minimize performance impact.
- The agent behavior can be fully customized using a JSON-based profile.
- If profile is missing, the agent defaults to collecting metadata in lite mode without any protection enforcement.
