import json
import sys
import subprocess
from pathlib import Path

from openai import OpenAI


client = OpenAI()


SOURCE_FILE = "game_logic.py"
TEST_NAME = "test_player_takes_damage"


def run_tests():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        capture_output=True,
        text=True,
    )

    return result.returncode, result.stdout + result.stderr


def ask_ai(test_output, source_code):
    prompt = f"""
You are an autonomous gameplay debugging agent.

A small game has a failing automated test.

GAMEPLAY SOURCE:
{source_code}

TEST FAILURE:
{test_output}

Find the gameplay bug and fix it.

Return ONLY the complete corrected Python source file.
Do not return markdown.
Do not explain anything.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text


def save_result(
    test_output,
    old_source,
    fixed_source,
    status,
):
    result = {
        "bug": "Player damage heals instead of hurting",
        "test": TEST_NAME,
        "file": SOURCE_FILE,
        "log": test_output,
        "original_code": old_source,
        "patch": fixed_source,
        "status": status,
    }

    Path("result.json").write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\nSaved debugging result to result.json")


def main():
    print()
    print("====================================")
    print("        GAMEBUG HUNTER")
    print("====================================")

    print("\nScanning gameplay tests...")

    code, output = run_tests()

    if code == 0:
        print("\nNo bugs detected.")
        print("All tests pass.")
        return

    print("\nBUG DETECTED")
    print("-----------------------------")
    print("Player damage behavior failed.")
    print("-----------------------------")

    print(output)

    original_source = Path(
        SOURCE_FILE
    ).read_text(
        encoding="utf-8"
    )

    print("\nAI analyzing gameplay logic...")

    try:
        fixed_source = ask_ai(
            output,
            original_source,
        )

    except Exception as error:
        print(f"\nAI ERROR: {error}")
        return

    fixed_source = (
        fixed_source
        .replace("```python", "")
        .replace("```", "")
        .strip()
    )

    print("\nAI generated patch:")
    print("-----------------------------")
    print(fixed_source)
    print("-----------------------------")

    Path(
        SOURCE_FILE
    ).write_text(
        fixed_source + "\n",
        encoding="utf-8",
    )

    print("\nVerifying fix...")

    verify_code, verify_output = run_tests()

    print(verify_output)

    if verify_code == 0:
        print()
        print("====================================")
        print("      BUG FIXED AND VERIFIED")
        print("====================================")

        save_result(
            test_output=output,
            old_source=original_source,
            fixed_source=fixed_source,
            status="fixed",
        )

    else:
        print("\nAI patch failed.")

        print(
            "Restoring original gameplay code..."
        )

        Path(
            SOURCE_FILE
        ).write_text(
            original_source,
            encoding="utf-8",
        )

        save_result(
            test_output=output,
            old_source=original_source,
            fixed_source=fixed_source,
            status="failed",
        )


if __name__ == "__main__":
    main()