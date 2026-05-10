import uuid
from datetime import datetime

def build_intent(action, target_path):
    """
    Structured Intent Model
    """

    scope = "sandbox"

    if "../" in target_path or target_path.startswith("/"):
        scope = "system"

    risk_level = "low"

    if action == "delete":
        risk_level = "high"
    elif action == "organize":
        risk_level = "medium"
    elif action == "list":
        risk_level = "low"

    intent = {
        "intent_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "actor": "openclaw_file_agent",
        "action": action,
        "resource_type": "file",
        "target_path": target_path,
        "scope": scope,
        "risk_level": risk_level,
        "constraints": {
            "allowed_root": "sandbox/",
            "allow_subdirectories": True,
            "allow_external_paths": False
        }
    }

    return intent