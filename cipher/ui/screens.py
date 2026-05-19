from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import Header, Footer, Input, RichLog, Label
from textual.containers import Vertical
import hashlib
from cipher.tools.guardrail import get_stored_hash, verify_system_sudo

class OnboardingScreen(Screen):
    """First-time setup screen to configure the security answer hash."""
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="onboard-container"):
            yield Label("=== PROJECT CIPHER: FIRST-TIME SETUP ===")
            yield Label("Set your secret answer to protect administrative access.")
            yield Input(placeholder="Type your secret answer here...", password=True, id="setup-input")
        yield Footer()

class MainWorkspace(Screen):
    """The core dashboard containing the terminal execution log and prompt input."""
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="workspace-container"):
            yield Label("Cipher Terminal Engine Active")
            yield RichLog(id="terminal-log", highlight=True, markup=True)
            yield Input(placeholder="Ask Cipher to execute something...", id="query-input")
        yield Footer()

class SudoVerificationModal(ModalScreen[str | None]):
    """POPUP 1: Dynamic dialog enforcing local system sudo validation."""
    def compose(self) -> ComposeResult:
        with Vertical(id="modal-container-sudo"):
            yield Label("🔒 SYSTEM ELEVATION REQUIRED 🔒", id="modal-title-sudo")
            yield Label("Enter your system root user sudo password:")
            yield Input(placeholder="Sudo password...", password=True, id="sudo-input-field")
            yield Label("", id="modal-error-sudo")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
            raw_password = event.value
            error_label = self.query_one("#modal-error-sudo", Label)
            
            # verify_system_sudo runs a quick shell check, so we keep it clean
            if verify_system_sudo(raw_password):
                self.dismiss(raw_password) # Sync dismissal works perfectly inside async handlers
            else:
                error_label.text = "[bold red]Invalid Sudo Password. Try again.[/bold red]"
                self.query_one("#sudo-input-field", Input).value = ""

class SecretVerificationModal(ModalScreen[bool]):
    """POPUP 2: Cryptographic challenge verifying personal security signature."""
    def compose(self) -> ComposeResult:
        with Vertical(id="modal-container-secret"):
            yield Label("🔒 SECURITY IDENTITY CHALLENGE 🔒", id="modal-title-secret")
            yield Label("Enter your personal secret security answer:")
            yield Input(placeholder="Secret security answer...", password=True, id="secret-input-field")
            yield Label("", id="modal-error-secret")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
            user_answer = event.value.strip()
            error_label = self.query_one("#modal-error-secret", Label)
            
            stored_hash = get_stored_hash()
            hashed_attempt = hashlib.sha256(user_answer.encode()).hexdigest()
            
            if stored_hash and hashed_attempt == stored_hash:
                self.dismiss(True) 
            else:
                error_label.text = "[bold red]Access Denied: Signature Mismatch[/bold red]"
                self.query_one("#secret-input-field", Input).value = ""