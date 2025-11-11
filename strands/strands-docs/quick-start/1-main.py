"""Command-line entry point for interacting with the `my_agent` package."""

import argparse
from typing import Optional

from my_agent.agent import agent as default_agent, message as default_prompt


def run_agent(prompt: str, agent=default_agent) -> Optional[str]:
    """Send the provided prompt to the configured agent and return its response."""
    return agent(prompt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the my_agent package against a custom or default prompt.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=default_prompt,
        help="Prompt to send to the agent. Defaults to the package's built-in sample prompt.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    response = run_agent(args.prompt)
    if response is not None:
        print(response)


if __name__ == "__main__":
    main()
