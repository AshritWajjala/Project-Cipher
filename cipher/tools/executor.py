import asyncio

async def execute_linux_command(command: str) -> dict:
    """Executes a Linux command asynchronously to prevent UI freezing.

    Args:
        command (str): Linux command

    Returns:
        dict: returns stdout, stderr, exitcode
    """
    try:
        # Launch the process asynchronously using the system shell
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Await the results smoothly without locking the terminal thread
        stdout, stderr = await process.communicate()
        
        return {
            "stdout": stdout.decode().strip(),
            "stderr": stderr.decode().strip(),
            "exitcode": process.returncode
        }
    
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exitcode": 1
        }