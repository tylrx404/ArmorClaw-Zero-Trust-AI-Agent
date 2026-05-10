import json
from datetime import datetime

from intent_model import build_intent
from intent_engine import extract_intent
from policy_engine import evaluate_policy
from execution_engine import execute_action


def write_audit_log(structured_intent, policy_result, execution_result=None):
    """Write audit log with structured intent data"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "timestamp": timestamp,
        "intent_id": structured_intent.get("intent_id"),
        "action": structured_intent.get("action"),
        "target_path": structured_intent.get("target_path"),
        "scope": structured_intent.get("scope"),
        "ai_risk": structured_intent.get("risk_level"),
        "effective_risk": policy_result.get("effective_risk"),
        "policy_status": policy_result.get("status"),
        "policy_reason": policy_result.get("reason"),
        "execution_result": execution_result
    }

    with open("audit_log.txt", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    user_command = input("Enter command: ")

    print("\n" + "="*50)
    print("STEP 1: AI INTENT EXTRACTION")
    print("="*50)
    intent_output = extract_intent(user_command)
    print(intent_output)

    try:
        intent_dict = json.loads(intent_output)

        if "error" in intent_dict:
            print("❌ AI Intent Extraction Failed")
            return

    except:
        print("Invalid intent output.")
        return

    print("\n" + "="*50)
    print("STEP 1B: STRUCTURED INTENT MODEL (Rulebook)")
    print("="*50)
    # Build deterministic structured intent from LLM output
    # This adds: intent_id, timestamp, actor, scope, constraints
    structured_intent = build_intent(
        action=intent_dict.get("action"),
        target_path=intent_dict.get("target_folder")
    )
    print(json.dumps(structured_intent, indent=4))

    print("\n" + "="*50)
    print("STEP 2: DETERMINISTIC POLICY ENGINE")
    print("="*50)
    # CRITICAL: Pass structured intent to policy engine (NOT raw LLM output)
    # This ensures deterministic enforcement on validated structured intent
    # Key: AI output is NOT trusted - must pass through structured model first
    policy_result = evaluate_policy(structured_intent)
    print(json.dumps(policy_result, indent=4))

    print("\n" + "="*50)
    print("FINAL DECISION")
    print("="*50)

    if policy_result["status"] == "allowed":
        print("✅ POLICY ALLOWED - Proceeding to execution")

        print("\n" + "="*50)
        print("STEP 3: SANDBOX EXECUTION")
        print("="*50)
        # Execute action using structured intent
        execution_result = execute_action(structured_intent)
        print(json.dumps(execution_result, indent=4))

        # Write complete audit log with all layers
        write_audit_log(structured_intent, policy_result, execution_result)
        print("\n✅ Action completed and logged to audit_log.txt")

    else:
        print("🚫 BLOCKED BY POLICY")
        print(f"Reason: {policy_result.get('reason')}")
        
        # Log blocked attempt
        write_audit_log(structured_intent, policy_result)
        print("\n🚫 Blocked attempt logged to audit_log.txt")


if __name__ == "__main__":
    main()

