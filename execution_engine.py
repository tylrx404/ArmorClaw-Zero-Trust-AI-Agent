import os
import shutil

# Absolute sandbox path (safe + robust)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SANDBOX_PATH = os.path.join(BASE_DIR, "sandbox")


def execute_action(structured_intent):
    """
    Execution Engine
    
    Executes actions ONLY inside sandbox directory
    Receives structured intent (dict) from policy engine
    
    Safety guarantees:
    - Always uses absolute SANDBOX_PATH
    - Never executes outside sandbox
    - Auto-creates sandbox if missing
    """
    
    action = structured_intent.get("action")
    target_path = structured_intent.get("target_path", "sandbox")

    # Ensure sandbox always exists (auto-create if missing)
    os.makedirs(SANDBOX_PATH, exist_ok=True)

    # Security: Verify target is sandbox
    if target_path != "sandbox":
        return {
            "status": "error",
            "message": "Execution only allowed in sandbox",
            "execution_root": SANDBOX_PATH
        }

    # LIST FILES
    if action == "list":
        files = os.listdir(SANDBOX_PATH)
        return {
            "status": "success",
            "action": "list",
            "files": files,
            "execution_root": SANDBOX_PATH,
            "sandbox_enforced": True
        }

    # DELETE FILES (only files, not folders - safety first)
    if action == "delete":
        deleted_files = []
        for file in os.listdir(SANDBOX_PATH):
            file_path = os.path.join(SANDBOX_PATH, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_files.append(file)

        return {
            "status": "success",
            "action": "delete",
            "deleted": deleted_files,
            "execution_root": SANDBOX_PATH,
            "sandbox_enforced": True
        }

    # ORGANIZE FILES
    if action == "organize":
        organized = []
        for file in os.listdir(SANDBOX_PATH):
            file_path = os.path.join(SANDBOX_PATH, file)

            if not os.path.isfile(file_path):
                continue

            if file.endswith(".txt"):
                new_folder = os.path.join(SANDBOX_PATH, "text_files")
            elif file.endswith(".log"):
                new_folder = os.path.join(SANDBOX_PATH, "log_files")
            else:
                continue

            os.makedirs(new_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(new_folder, file))
            organized.append(file)

        if not organized:
            return {
                "status": "success",
                "action": "organize",
                "message": "No files needed organization",
                "execution_root": SANDBOX_PATH,
                "sandbox_enforced": True
            }

        return {
            "status": "success",
            "action": "organize",
            "organized": organized,
            "execution_root": SANDBOX_PATH,
            "sandbox_enforced": True
        }

    # MOVE FILES
    if action == "move":
        # For now, simple move within sandbox
        return {
            "status": "success",
            "action": "move",
            "message": "Move not fully implemented",
            "execution_root": SANDBOX_PATH,
            "sandbox_enforced": True
        }

    return {
        "status": "error",
        "message": "Action not implemented"
    }

