import json

# Only allow sandbox root
ALLOWED_ROOT = "sandbox"
PROTECTED_KEYWORDS = ["system", "usr", "bin", "windows", "system32", "etc", "passwd"]

ALLOWED_ACTIONS = ["delete", "move", "list", "organize"]


def evaluate_policy(structured_intent):
    """
    Deterministic Policy Engine
    
    Receives STRUCTURED intent (dict) from intent_model.py
    NOT raw LLM output - ensuring AI is not trusted
    
    Returns deterministic policy decision:
    - status: allowed/blocked
    - reason: detailed explanation
    - effective_risk: risk after policy enforcement
    """

    # Handle both dict and JSON string for backwards compatibility
    if isinstance(structured_intent, str):
        try:
            intent = json.loads(structured_intent)
        except:
            return {
                "status": "blocked",
                "reason": "Invalid intent format"
            }
    else:
        intent = structured_intent

    # Extract from structured intent (uses target_path, not target_folder)
    action = intent.get("action")
    target_path = intent.get("target_path", "").lower()
    scope = intent.get("scope", "sandbox")
    risk_level = intent.get("risk_level", "low")

    # ---- Basic Validation ----
    if not action or not target_path:
        return {
            "status": "blocked",
            "reason": "Target path not clearly specified"
        }

    # ---- Action must be valid ----
    if action not in ALLOWED_ACTIONS:
        return {
            "status": "blocked",
            "reason": f"Action '{action}' is not permitted"
        }

    # ---- Block path traversal ----
    if "../" in target_path or target_path.startswith("/"):
        return {
            "status": "blocked",
            "reason": "Path traversal or absolute paths are not allowed",
            "scope_violation": scope
        }

    # ---- Block protected keywords ----
    for word in PROTECTED_KEYWORDS:
        if word in target_path:
            return {
                "status": "blocked",
                "reason": f"Access to protected keyword '{word}' is denied"
            }

    # ---- Scope enforcement ----
    # If structured intent marked as 'system' scope, block it
    if scope == "system":
        return {
            "status": "blocked",
            "reason": "System scope access denied - only sandbox allowed",
            "scope_violation": "system"
        }

    # ---- Only allow sandbox root ----
    if target_path != ALLOWED_ROOT:
        return {
            "status": "blocked",
            "reason": f"Only '{ALLOWED_ROOT}' directory is allowed"
        }

    # ---- Deterministic Risk Override ----
    # Override AI's risk assessment with deterministic policy
    if action == "list":
        effective_risk = "low"
    elif action == "delete":
        effective_risk = "medium"  # Deletion is medium risk, not high
    elif action == "organize":
        effective_risk = "low"
    elif action == "move":
        effective_risk = "medium"
    else:
        effective_risk = "low"

    return {
        "status": "allowed",
        "reason": "Policy check passed - deterministic enforcement complete",
        "effective_risk": effective_risk,
        "enforcement_layer": "ArmorClaw-ArmorIQ"
    }

