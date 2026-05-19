from pathlib import Path
from dotenv import load_dotenv
import hashlib
import os

# Commands that inherently modify system files, disks, or permissions
ROOT_COMMANDS = {
    "apt", "systemctl", "chmod", "chown", "mkfs", 
    "dd", "shred", "fdisk", "parted", "ufw"
}

# Parameters that instantly elevate a command's danger level
DANGEROUS_FLAGS = {"-rf", "-fr", "--no-preserve-root"}

def need_root_escalation(command: str) -> bool:
    """This method determines whether the command needs root access in order to get executed

    Args:
        command (str): The linux command

    Returns:
        bool: True if root access is required. Else, false.
    """
    normalized_command = command.lower().strip().split()
    # If the command is empty string 
    if len(normalized_command) == 0:
        return False
    # Checking if the command contains 'sudo'
    elif normalized_command[0] == 'sudo':
        return True
    # Checking if any of the ROOT_COMMANDS exists in the command
    elif normalized_command[0] in ROOT_COMMANDS:
        return True
    # Checking if any of the DANGEROUS_FLAGS exists in the command
    elif any(danger_flag in normalized_command for danger_flag in DANGEROUS_FLAGS):
        return True
    else:
        return False
    

ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

def env_exists(env_path: Path) -> bool:
    """To determine whether .env file exists

    Args:
        env_path (Path): The path of .env file

    Returns:
        bool: Returns True if .env file exists. Else, False.
    """
    return os.path.exists(env_path) 

def create_env_file() -> None:  ENV_FILE_PATH.touch(exist_ok=True)

def get_stored_hash() -> str | None:
    """Checks if the .env file exists and reads the security hash.
    Returns the 64-character string hash, or None if it doesn't exist.
    """
    if not env_exists(env_path=ENV_FILE_PATH):
        return None
       
    with open(ENV_FILE_PATH, "r") as file:
        for line in file:
            if line.startswith("SECURITY_HASH="):
                return line.split("=")[1].strip()
    
    return None

def save_security_hash(plain_text_answer: str) -> None:
    """Takes the input from the TUI, hashes it, and saves it to the .env file."""
    # Ensuring that the file actually exists before writing
    create_env_file()
    
    # Cleaning the input and run SHA-256 encryption
    cleaned_answer = plain_text_answer.strip()
    hashed_string = hashlib.sha256(cleaned_answer.encode()).hexdigest()
    
    # 3. Write in the .env file
    with open(ENV_FILE_PATH, "w") as file:
        file.write(f"SECURITY_HASH={hashed_string}\n")

import subprocess

def verify_system_sudo(password: str) -> bool:
    """Validates the local machine's sudo password safely via stdin.
    Returns True if valid, False if rejected.
    """
    try:
        # We pass the password into the stdin stream of 'sudo -S -v'
        result = subprocess.run(
            ["sudo", "-S", "-v"],
            input=f"{password}\n",
            capture_output=True,
            text=True,
            check=True # Throws an exception if the password is wrong (returncode != 0)
        )
        return True
    except subprocess.CalledProcessError:
        return False
                
    
if __name__ == "__main__":
    print(Path(__file__).resolve().parent.parent.parent / ".env")
    ENV_FILE_PATH.touch(exist_ok=True)