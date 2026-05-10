#!/usr/bin/env python3
"""
Demo Script for Safe AI Agent - Claw-n-Shield 2026 Hackathon

This script demonstrates the complete security architecture:
1. AI Intent Extraction (LLM - NOT trusted)
2. Structured Intent Model (Deterministic)
3. Policy Engine (ArmorClaw-ArmorIQ enforcement)
4. Sandbox Execution
5. Audit Logging

Run: python demo.py
"""

import json
from datetime import datetime

from intent_model import build_intent
from policy_engine import evaluate_policy
from execution_engine import execute_action


def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_step(step_num, title):
    print(f"\n{'─'*60}")
    print(f"  STEP {step_num}: {title}")
    print(f"{'─'*60}")


def run_demo_command(user_command):
    """Run a single command through the security pipeline"""
    
    print_header(f"COMMAND: {user_command}")
    
    # Step 1: AI Intent Extraction (Mock for demo)
    print_step(1, "AI INTENT EXTRACTION (LLM - NOT TRUSTED)")
    
    # Use mock intent for demo (simulates LLM output)
    intent_dict = mock_intent_extractor(user_command)
    intent_output = json.dumps(intent_dict, indent=2)
    
    print(intent_output)
    
    try:
        intent_dict = json.loads(intent_output)
        if "error" in intent_dict:
            print("❌ AI Intent Extraction Failed")
            return
    except:
        print("Invalid intent output.")
        return

    # Step 1B: Structured Intent Model
    print_step(1.5, "STRUCTURED INTENT MODEL (Deterministic)")
    # This converts LLM output into structured format with constraints
    structured_intent = build_intent(
        action=intent_dict.get("action"),
        target_path=intent_dict.get("target_folder")
    )
    print(json.dumps(structured_intent, indent=4))
    
    # Step 2: Policy Engine
    print_step(2, "DETERMINISTIC POLICY ENGINE (ArmorClaw-ArmorIQ)")
    policy_result = evaluate_policy(structured_intent)
    print(json.dumps(policy_result, indent=4))

    # Step 3: Execution
    if policy_result["status"] == "allowed":
        print_step(3, "SANDBOX EXECUTION")
        execution_result = execute_action(structured_intent)
        print(json.dumps(execution_result, indent=4))
        
        # Write audit log
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
            "execution_result": execution_result
        }
        
        with open("audit_log.txt", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        print("\n✅ ACTION COMPLETED & LOGGED")
    else:
        print("\n🚫 BLOCKED BY POLICY ENGINE")
        print(f"Reason: {policy_result.get('reason')}")
        
        # Log blocked attempt
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
            "policy_reason": policy_result.get("reason")
        }
        
        with open("audit_log.txt", "a") as f:
            f.write(json.dumps(log_entry) + "\n")


def mock_intent_extractor(command):
    """Mock intent extractor - simulates LLM output for demo"""
    command = command.lower()
    
    # Determine action
    if "delete" in command:
        action = "delete"
    elif "list" in command:
        action = "list"
    elif "organize" in command:
        action = "organize"
    else:
        action = "list"
    
    # Determine target - simulate what a potentially manipulated AI might output
    if "../" in command or "/etc" in command or "passwd" in command:
        # Simulating malicious AI output attempting path traversal
        target = "../../etc/passwd"
        risk = "high"
    elif "system" in command:
        # Simulating AI outputting system scope
        target = "system"
        risk = "high"
    elif "sandbox" in command:
        target = "sandbox"
        risk = "low"
    else:
        target = "sandbox"
        risk = "medium"
    
    return {
        "action": action,
        "target_folder": target,
        "risk_level": risk,
        "confidence": "high",
        "intent_id": "mock-" + str(hash(command))[:8]
    }


def main():
    print("\n" + "█"*60)
    print("  SAFE AI AGENT - ARMORCLAW SDK DEMO")
    print("  Claw-n-Shield 2026 Hackathon")
    print("█"*60)
    
    print("\nThis demo shows:")
    print("  1. How AI output is NEVER trusted")
    print("  2. Structured Intent Model adds deterministic constraints")
    print("  3. Policy Engine enforces sandbox isolation")
    print("  4. All actions are logged for audit")
    
    # Demo 1: Allowed command
    print("\n\n" + "▓"*60)
    print("  DEMO 1: ALLOWED COMMAND (List sandbox)")
    print("▓"*60)
    run_demo_command("List sandbox files")
    
    # Demo 2: Allowed command
    print("\n\n" + "▓"*60)
    print("  DEMO 2: ALLOWED COMMAND (Delete in sandbox)")
    print("▓"*60)
    run_demo_command("Delete sandbox/file1.txt")
    
    # Demo 3: Blocked - Path traversal
    print("\n\n" + "▓"*60)
    print("  DEMO 3: BLOCKED - Path Traversal Attack")
    print("▓"*60)
    run_demo_command("Delete ../../etc/passwd")
    
    # Demo 4: Blocked - System scope
    print("\n\n" + "▓"*60)
    print("  DEMO 4: BLOCKED - System Scope Detection")
    print("▓"*60)
    run_demo_command("Delete system files")
    
    print("\n\n" + "█"*60)
    print("  DEMO COMPLETE")
    print("█"*60)
    print("\nCheck audit_log.txt for complete audit trail")
    print("\nKey Architecture Points:")
    print("  ✓ AI is NEVER trusted - output goes through structured model")
    print("  ✓ Policy engine uses DETERMINISTIC rules")
    print("  ✓ Sandbox isolation is ENFORCED at execution layer")
    print("  ✓ Complete AUDIT LOG of all decisions")


if __name__ == "__main__":
    main()

