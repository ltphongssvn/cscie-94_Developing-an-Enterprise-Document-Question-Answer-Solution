# src/config_validator.py
# Full path: /src/config_validator.py

import os
from typing import List, Tuple


class ConfigValidator:
    """Validate Azure configuration before running application."""

    REQUIRED_VARS = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME",
    ]

    @staticmethod
    def validate() -> Tuple[bool, List[str]]:
        """Validate all required environment variables."""
        missing = []

        for var in ConfigValidator.REQUIRED_VARS:
            if not os.getenv(var):
                missing.append(var)

        return len(missing) == 0, missing

    @staticmethod
    def print_status():
        """Print validation status."""
        is_valid, missing = ConfigValidator.validate()

        if is_valid:
            print("✓ All configuration variables set")
            return True
        else:
            print("✗ Missing configuration variables:")
            for var in missing:
                print(f"  - {var}")
            print("\nPlease set these in your .env file")
            return False


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    ConfigValidator.print_status()
