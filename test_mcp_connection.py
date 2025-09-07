import requests

try:
    response = requests.get("http://localhost:8080/health", timeout=5)
    print(f"MCP Server Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ MCP Server is accessible")
    else:
        print(f"❌ MCP Server returned: {response.text}")
except Exception as e:
    print(f"❌ Cannot connect to MCP Server: {e}")