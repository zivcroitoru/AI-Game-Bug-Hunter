import json
import sys
import subprocess
from pathlib import Path

from openai import OpenAI


client = OpenAI()

SOURCE_FILE = "game_logic.py"


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

A small game has one or more failing automated tests.

SOURCE FILE:
{SOURCE_FILE}

CURRENT SOURCE:
{source_code}

FAILING TEST OUTPUT:
{test_output}

Fix ONLY the bugs demonstrated by the currently failing tests.

Do not redesign unrelated behavior.
Do not anticipate bugs that are not currently demonstrated by the tests.

Return ONLY the complete corrected Python source file.

Do not use markdown.
Do not use code fences.
Do not explain the answer.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text


def clean_ai_output(text):
    return (
        text
        .replace("```python", "")
        .replace("```", "")
        .strip()
    )


def save_result(
    test_output,
    original_source,
    fixed_source,
    status,
):
    result = {
        "bug": "Gameplay logic failure",
        "file": SOURCE_FILE,
        "log": test_output,
        "original_code": original_source,
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

    print("\nDebugging result saved to result.json")


def main():
    print()
    print("========================================")
    print("          GAMEBUG HUNTER")
    print("     Autonomous Debugging Agent")
    print("========================================")
    print()

    print("[1] Running gameplay tests...")

    test_code, test_output = run_tests()

    if test_code == 0:
        print()
        print("No failing tests detected.")
        return

    print()
    print("BUG DETECTED")
    print("----------------------------------------")
    print(test_output)
    print("----------------------------------------")

    source_path = Path(SOURCE_FILE)

    if not source_path.exists():
        print(f"ERROR: {SOURCE_FILE} not found.")
        return

    original_source = source_path.read_text(
        encoding="utf-8"
    )

    print()
    print("[2] AI analyzing failure...")

    try:
        fixed_source = ask_ai(
            test_output,
            original_source,
        )

    except Exception as error:
        print(f"\nAI ERROR: {error}")
        return

    fixed_source = clean_ai_output(
        fixed_source
    )

    print()
    print("AI GENERATED PATCH")
    print("----------------------------------------")
    print(fixed_source)
    print("----------------------------------------")

    source_path.write_text(
        fixed_source + "\n",
        encoding="utf-8",
    )

    print()
    print("[3] Patch applied.")
    print("[4] Verifying fix...")
    print()

    verify_code, verify_output = run_tests()

    print(verify_output)

    if verify_code == 0:

        print()
        print("========================================")
        print("        BUG FIXED AND VERIFIED")
        print("========================================")

        save_result(
            test_output,
            original_source,
            fixed_source,
            "fixed",
        )

    else:

        print()
        print("PATCH FAILED")
        print("Restoring original source...")

        source_path.write_text(
            original_source,
            encoding="utf-8",
        )

        save_result(
            test_output,
            original_source,
            fixed_source,
            "failed",
        )


if __name__ == "__main__":
    main()