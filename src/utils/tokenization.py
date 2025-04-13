import os
from typing import Optional
from tiktoken import encoding_for_model, Encoding
import signal
import atexit
import logging

"""
Token counting utilities for the Obsidian MCP Server
"""

logger = logging.getLogger(__name__)

# Load token limits from environment or use defaults
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "20000"))
TRUNCATION_MESSAGE = "\n\n[Response truncated due to length]"

class TokenCounter:
    def __init__(self):
        self._tokenizer: Optional[Encoding] = None
        self.is_shutting_down = False
        
        # Register cleanup handlers
        self._setup_signal_handlers()
    
    @property
    def tokenizer(self) -> Encoding:
        """Lazy load tokenizer only when needed"""
        if self._tokenizer is None:
            self._tokenizer = encoding_for_model("gpt-4")
        return self._tokenizer

    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        try:
            atexit.register(self.cleanup)
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except Exception as e:
            logger.warning(f"Failed to setup signal handlers: {e}")

    def _signal_handler(self, signum: int, frame) -> None:
        """Handle shutdown signals"""
        signame = signal.Signals(signum).name
        logger.info(f"Received signal {signame}")
        self.cleanup()
        # Re-raise the signal for proper process termination
        signal.default_int_handler(signum, frame)

    def cleanup(self, *args) -> None:
        """
        Clean up resources and remove signal handlers
        """
        if not self.is_shutting_down:
            try:
                self.is_shutting_down = True
                # Remove signal handlers
                signal.signal(signal.SIGINT, signal.default_int_handler)
                signal.signal(signal.SIGTERM, signal.default_int_handler)
                # Remove atexit handler
                atexit.unregister(self.cleanup)
                # Clear tokenizer reference
                self._tokenizer = None
                logger.info("TokenCounter cleanup completed")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a string
        """
        return len(self.tokenizer.encode(text))

    def truncate_to_token_limit(self, text: str, limit: int = MAX_TOKENS) -> str:
        """
        Truncate text to stay within token limit
        """
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= limit:
            return text

        # Reserve tokens for truncation message
        message_tokens = self.tokenizer.encode(TRUNCATION_MESSAGE)
        available_tokens = limit - len(message_tokens)

        # Decode truncated tokens back to text
        truncated_text = self.tokenizer.decode(tokens[:available_tokens])
        return truncated_text + TRUNCATION_MESSAGE

# Export a singleton instance
token_counter = TokenCounter()