import json
import requests
import anthropic
import streamlit as st

BASE_URL = "http://localhost:8000"

TOOLS = [
    {
        "name": "create_resource",
        "description": "Create a single resource record in the database. Call once per resource.",
        "input_schema": {
            "type": "object",
            "properties": {
                "first_name":           {"type": "string"},
                "last_name":            {"type": "string"},
                "middle_name":          {"type": "string"},
                "company":              {"type": "string"},
                "alloc_work_hours":     {"type": "integer"},
                "alloc_max_hours":      {"type": "integer"},
                "alloc_night_work":     {"type": "boolean"},
                "alloc_overtime":       {"type": "boolean"},
                "alloc_weekend":        {"type": "boolean"},
                "contact_title":        {"type": "string"},
                "contact_mobile_phone": {"type": "string"},
                "contact_fixed_line":   {"type": "string"},
                "contact_email":        {"type": "string"},
                "contact_post_code":    {"type": "string"},
                "contact_other_info":   {"type": "string"},
                "contact_street":       {"type": "string"},
                "contact_city":         {"type": "string"},
                "contact_province":     {"type": "string"},
                "contact_country":      {"type": "string"},
                "registration_status":  {"type": "string"},
                "created_by":           {"type": "string", "description": "Who is uploading this record"},
            },
            "required": ["first_name", "last_name", "created_by"],
        },
    },
    {
        "name": "list_resources",
        "description": "List all resource records currently in the database.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_resource",
        "description": "Get a single resource record by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Resource ID"},
            },
            "required": ["id"],
        },
    },
    {
        "name": "update_resource",
        "description": "Update an existing resource record by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id":                   {"type": "integer", "description": "Resource ID to update"},
                "first_name":           {"type": "string"},
                "last_name":            {"type": "string"},
                "middle_name":          {"type": "string"},
                "company":              {"type": "string"},
                "alloc_work_hours":     {"type": "integer"},
                "alloc_max_hours":      {"type": "integer"},
                "alloc_night_work":     {"type": "boolean"},
                "alloc_overtime":       {"type": "boolean"},
                "alloc_weekend":        {"type": "boolean"},
                "contact_title":        {"type": "string"},
                "contact_mobile_phone": {"type": "string"},
                "contact_fixed_line":   {"type": "string"},
                "contact_email":        {"type": "string"},
                "contact_post_code":    {"type": "string"},
                "contact_other_info":   {"type": "string"},
                "contact_street":       {"type": "string"},
                "contact_city":         {"type": "string"},
                "contact_province":     {"type": "string"},
                "contact_country":      {"type": "string"},
                "registration_status":  {"type": "string"},
                "updated_by":           {"type": "string"},
            },
            "required": ["id"],
        },
    },
    {
        "name": "delete_resource",
        "description": "Delete a resource record by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Resource ID to delete"},
            },
            "required": ["id"],
        },
    },
]

SYSTEM_PROMPT = """You are a helpful assistant for managing Resource records in a database via a REST API.

You can list, create, update, and delete resources using the provided tools.

When the user provides tabular data (from Excel or CSV) with an instruction:
1. Map the column headers to Resource fields (be flexible with naming, e.g. "Phone" → contact_mobile_phone)
2. Apply any filters the user specifies before calling tools:
   - "complete last name" = skip rows where last_name is empty, null, or whitespace-only
   - "valid email" = skip rows where contact_email is missing or malformed
   - Apply common sense for similar conditions
3. Call create_resource (or the relevant tool) once per valid record
4. Set created_by to "ai_agent" unless the user specifies otherwise

Always end with a summary:
- How many records were processed successfully
- How many were skipped and why (list row identifiers if possible)
"""


def _execute_tool(name: str, tool_input: dict) -> str:
    try:
        if name == "create_resource":
            tool_input.setdefault("created_by", "ai_agent")
            r = requests.post(f"{BASE_URL}/resources/", json=tool_input, timeout=10)
            return json.dumps({"status": r.status_code, "data": r.json()})

        elif name == "list_resources":
            r = requests.get(f"{BASE_URL}/resources/", timeout=10)
            return json.dumps(r.json())

        elif name == "get_resource":
            r = requests.get(f"{BASE_URL}/resources/{tool_input['id']}", timeout=10)
            return json.dumps(r.json())

        elif name == "update_resource":
            resource_id = tool_input.pop("id")
            r = requests.put(f"{BASE_URL}/resources/{resource_id}", json=tool_input, timeout=10)
            return json.dumps({"status": r.status_code, "data": r.json()})

        elif name == "delete_resource":
            r = requests.delete(f"{BASE_URL}/resources/{tool_input['id']}", timeout=10)
            return json.dumps({"status": r.status_code})

        else:
            return json.dumps({"error": f"Unknown tool: {name}"})

    except requests.exceptions.ConnectionError:
        return json.dumps({"error": "Cannot connect to API server on port 8000. Make sure it is running."})
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_conversation(claude_messages: list) -> tuple[str, list]:
    """
    Run the agentic tool-use loop with Claude.
    Returns (response_text, updated_claude_messages).
    """
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    messages = list(claude_messages)

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # Serialize SDK objects to plain dicts using only fields the API accepts
        serialized_content = []
        for block in response.content:
            if block.type == "text":
                serialized_content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                serialized_content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": dict(block.input),
                })
        messages.append({"role": "assistant", "content": serialized_content})

        if response.stop_reason == "end_turn":
            text = next((b.get("text", "") for b in serialized_content if b.get("type") == "text"), "")
            return text, messages

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in serialized_content:
                if block["type"] == "tool_use":
                    result = _execute_tool(block["name"], dict(block["input"]))
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
