from textual.app import App
from textual import work
from textual.widgets import Input, RichLog

# Import backend elements
from cipher.tools.guardrail import get_stored_hash, save_security_hash, need_root_escalation
from cipher.tools.executor import execute_linux_command
from cipher.agent.orchestrator import generate_command_plan
from cipher.ui.screens import OnboardingScreen, MainWorkspace, SudoVerificationModal, SecretVerificationModal

class CipherApp(App):
    CSS = """
    #onboard-container, #workspace-container {
        padding: 2;
        align: center middle;
    }
    
    SudoVerificationModal {
        align: center bottom;
        margin: 2 0 0 4; /* Pushes it slightly away from the absolute top-left edge */
        background: rgba(0, 0, 0, 0.2); /* Lighter blur so logs peek through */
    }
    
    #modal-container-sudo, #modal-container-secret {
        padding: 2;
        background: #1a1a1a;
        width: 50;
        height: auto;
        align: center middle;
        layer: modal;
    }
    #modal-container-sudo { border: thick orange; }
    #modal-container-secret { border: thick red; }
    #modal-title-sudo { color: orange; text-style: bold; margin-bottom: 1; }
    #modal-title-secret { color: red; text-style: bold; margin-bottom: 1; }
    
    #terminal-log {
        height: 1fr;
        border: solid green;
        margin-bottom: 1;
        background: #111111;
    }
    Input { dock: bottom; border: double green; }
    Label { margin: 1; text-style: bold; }
    """

    def on_mount(self) -> None:
        if get_stored_hash() is None:
            self.push_screen(OnboardingScreen())
        else:
            self.push_screen(MainWorkspace())

    @work
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        input_widget = event.input
        user_text = event.value.strip()
        
        if not user_text:
            return

        input_widget.value = ""

        if input_widget.id == "setup-input":
            save_security_hash(user_text)
            self.notify("Security hash initialized successfully!")
            self.push_screen(MainWorkspace())

        elif input_widget.id == "query-input":
            log_window = self.screen.query_one("#terminal-log", RichLog)
            log_window.write(f"\n[bold cyan]User:[/bold cyan] {user_text}")
            log_window.write("[italic gray]Cipher translating via Ollama...[/italic gray]")
            
            try:
                plan = generate_command_plan(user_text)
                log_window.write(f"[bold yellow]Intention:[/bold yellow] {plan.intention}")
                log_window.write(f"[bold magenta]Generated Command:[/bold magenta] ` {plan.execution_plan} `")
                
                # Strip raw 'sudo ' out if the model included it, since our pipeline injects it cleanly via stdin
                execution_target = plan.execution_plan
                if execution_target.lower().startswith("sudo "):
                    execution_target = execution_target[5:]

                is_risky = need_root_escalation(plan.execution_plan) or plan.need_root_access
                sudo_password = None
                
                if is_risky:
                    log_window.write("[bold orange]GATEWAY 1: Launching System Sudo Authentication...[/bold orange]")
                    
                    # 1. Trigger Sudo Password Challenge
                    sudo_password = await self.push_screen_wait(SudoVerificationModal())
                    if not sudo_password:
                        log_window.write("[bold red]ABORTED: Sudo validation failed.[/bold red]")
                        return
                    
                    # 2. Trigger Custom Personal Security Challenge
                    log_window.write("[bold red]GATEWAY 2: Launching Personal Security Challenge...[/bold red]")
                    secret_verified = await self.push_screen_wait(SecretVerificationModal())
                    if not secret_verified:
                        log_window.write("[bold red]ABORTED: Custom security signature verification failed.[/bold red]")
                        return
                    
                    log_window.write("[bold green]ACCESS GRANTED: Security clearances verified.[/bold green]")

                # 3. Compile command and execute safely
                log_window.write("[italic gray]Executing target process...[/italic gray]")
                
                # Check if it *actually* needs root execution tools
                needs_root_binary = need_root_escalation(plan.execution_plan) or plan.need_root_access
                
                if needs_root_binary and sudo_password:
                    # ONLY use sudo redirection if the command actually requires administrative authorization
                    final_command = f"echo '{sudo_password}' | sudo -S {execution_target}"
                else:
                    # Otherwise, run it safely as the local standard user
                    final_command = execution_target

                result = await execute_linux_command(final_command)
                
                # 4. Filter output to keep the log look professional
                stdout_clean = result["stdout"]
                stderr_clean = result["stderr"]
                
                # Strip out typical raw bash '[sudo] password' residue lines if present
                if "[sudo] password" in stderr_clean:
                    lines = [l for l in stderr_clean.splitlines() if "[sudo] password" not in l]
                    stderr_clean = "\n".join(lines)

                if stdout_clean.strip():
                    log_window.write("[green]Output:[/green]\n" + stdout_clean)
                if stderr_clean.strip():
                    log_window.write("[red]Error/Logs:[/red]\n" + stderr_clean)
                
                if result["exitcode"] == 0:
                    log_window.write("[bold green]Process completed successfully! Ready for next command.[/bold green]")
                else:
                    log_window.write(f"[bold red]Process terminated with exit code {result['exitcode']}[/bold red]")
                
            except Exception as error:
                log_window.write(f"[bold red]Pipeline Crash: {str(error)}[/bold red]")

if __name__ == "__main__":
    app = CipherApp()
    app.run()