# JSON Schemas for Techies config validation
# See docs/03-Understand-Crew-Configurations.md for reference
# Note: additionalProperties is set to False to catch typos; relax this if you want to allow extra fields.

AGENT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "goal": {"type": "string"},
        "backstory": {"type": "string"},
        "tools": {
            "type": "array",
            "items": {"type": "string"}
        },
        "verbose": {"type": "boolean"},
        "allow_delegation": {"type": "boolean"}
    },
    "required": ["goal", "backstory"],
    "additionalProperties": False
}

TASK_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "agent": {"type": "string"},
        "description": {"type": "string"},
        "expected_output": {"type": "string"},
        "callback": {"type": "string"},
        "depends_on": {
            "oneOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}}
            ]
        },
        "human_input": {"type": "boolean"},
        "async_execution": {"type": "boolean"},
        "output_file": {"type": "string"}
    },
    "required": ["agent", "description"],
    "additionalProperties": False
}

CREW_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "agents": {
            "type": "array",
            "items": {"type": "string"}
        },
        "tasks": {
            "type": "array",
            "items": {"type": "string"}
        },
        "input_args": {
            "type": "array",
            "items": {"type": "string"}
        },
        "cache": {"type": "boolean"},
        "memory": {"type": "boolean"},
        "max_iter": {"type": "integer"}
    },
    "required": ["agents", "tasks"],
    "additionalProperties": False
} 