# 🎮 GameBug Hunter

> An autonomous AI debugging agent that **detects gameplay bugs, fixes the code, verifies the repair, and remembers what it learned.**

Built at the **Daytona HackSprint Tokyo 2026**.

GameBug Hunter combines **Daytona**, **OpenAI**, **pytest**, and **Neo4j** into a closed-loop debugging workflow:

**Execute → Detect → Diagnose → Patch → Verify → Remember**

---

## 🚀 What is GameBug Hunter?

Debugging a game usually involves several manual steps:

1. Reproduce the bug
2. Inspect logs and failing tests
3. Find the responsible code
4. Create a fix
5. Test the fix
6. Document what happened

GameBug Hunter turns this into an autonomous agent workflow.

Given a broken project, the agent can:

- run the project's tests
- detect a failure
- collect the relevant error output
- send the failure and source code to an AI debugging agent
- generate a code patch
- modify the source automatically
- rerun the tests
- verify that the fix actually works
- store the bug, test, file, logs, and successful patch in Neo4j

The goal is not just to fix one bug.

The goal is to create a debugging agent that **gets more useful as it accumulates debugging knowledge.**

---

# 🕹️ Demo

The hackathon prototype contains a small Pygame combat demo.

The player starts with:

```text
100 HP
```

An enemy attack should deal `20` damage.

But the game contains an intentional gameplay bug:

```python
def take_damage(current_health, damage):
    return current_health + damage
```

So when the enemy attacks:

```text
100 HP → 120 HP
```

Instead of taking damage, the player gets healed.

The automated test detects this:

```python
def test_player_takes_damage():
    assert take_damage(100, 20) == 80
```

GameBug Hunter then analyzes the failure and repairs the gameplay logic:

```python
def take_damage(current_health, damage):
    return current_health - damage
```

The agent reruns the tests.

```text
100 HP → 80 HP
```

✅ Bug fixed.

The successful debugging session is then stored in Neo4j.

---

# 🧠 Architecture

```text
                  GAMEBUG HUNTER

     ┌─────────────────────────────┐
     │          Daytona            │
     │   Isolated Code Sandbox     │
     └──────────────┬──────────────┘
                    │
                    ▼
             Run Game Tests
                    │
                    ▼
            ┌───────────────┐
            │    pytest     │
            │ Detect Failure│
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │    OpenAI     │
            │ Diagnose Bug  │
            │ Generate Patch│
            └───────┬───────┘
                    │
                    ▼
              Modify Source
                    │
                    ▼
              Rerun Tests
                    │
             ┌──────┴──────┐
             │             │
           FAIL           PASS
             │             │
          Restore          ▼
          Source        result.json
                           │
                           ▼
                    ┌─────────────┐
                    │    Neo4j    │
                    │ Debug Memory│
                    └─────────────┘
```

---

# 🧩 Technology

### Daytona

GameBug Hunter uses Daytona as the execution environment for running project code and tests inside an isolated sandbox.

This is important for autonomous debugging agents because they need to do more than read code — they need to **execute commands, reproduce failures, modify files, and verify their changes**.

### OpenAI

The debugging agent receives:

- the failing test
- pytest output
- the relevant source code

It reasons about the root cause and generates a corrected source file.

The generated patch is **not automatically assumed to be correct**.

GameBug Hunter verifies it by running the tests again.

### Neo4j

Successful debugging sessions become structured graph knowledge.

For example:

```text
                 Player Damage Bug
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
        TEST           FILE           LOG
          │
          ▼
        PATCH
```

The graph captures relationships such as:

```text
(Bug)-[:CAUSED_FAILURE_IN]->(Test)

(Bug)-[:FOUND_IN]->(File)

(Bug)-[:PRODUCED]->(Log)

(Bug)-[:FIXED_BY]->(Patch)
```

Instead of treating every debugging session as an isolated event, this creates the foundation for **persistent agent debugging memory**.

---

# 🔮 Why Graph Memory?

Imagine GameBug Hunter encounters another combat bug six months later.

Instead of debugging entirely from scratch, a future version could query Neo4j:

> Have we seen a similar failure before?

It could retrieve:

- related bugs
- affected systems
- similar stack traces
- previous patches
- tests that caught them
- fixes that succeeded or failed

This turns Neo4j into a **debugging knowledge graph for AI agents**.

---

# 📁 Project Structure

```text
bug-hunter/
│
├── agent.py
│   └── AI debugging agent
│
├── game.py
│   └── Visual Pygame combat demo
│
├── game_logic.py
│   └── Gameplay logic modified by the agent
│
├── test_game_logic.py
│   └── Automated gameplay tests
│
├── push_to_neo4j.py
│   └── Stores debugging knowledge in Neo4j
│
├── demo.ps1
│   └── End-to-end demo runner
│
└── README.md
```

---

# ⚡ Running the Demo

## 1. Install dependencies

```bash
pip install pygame pytest openai
```

## 2. Configure credentials

Set your OpenAI API key and Neo4j password as environment variables.

PowerShell:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY"
$env:NEO4J_PASSWORD="YOUR_PASSWORD"
```

**Never commit API keys or passwords to the repository.**

## 3. Run the broken game

```bash
python game.py
```

Press:

```text
SPACE
```

The enemy attacks.

Because of the intentional bug:

```text
100 HP → 120 HP
```

## 4. Run GameBug Hunter

```bash
python agent.py
```

The agent will:

```text
BUG DETECTED

AI analyzing gameplay logic...

AI generated patch...

Verifying fix...

BUG FIXED AND VERIFIED
```

## 5. Run the game again

```bash
python game.py
```

Now:

```text
100 HP → 80 HP → 60 HP
```

## 6. Save the debugging memory

```bash
python push_to_neo4j.py
```

The bug and successful repair are stored in the Neo4j knowledge graph.

---

# 🧪 Verification First

A key design principle of GameBug Hunter is:

> **An AI-generated patch is not a successful fix until the project proves it.**

The workflow therefore separates:

```text
Generate Patch
      ↓
Apply Patch
      ↓
Run Tests
      ↓
   PASS?
   /   \
 NO     YES
 │       │
 ▼       ▼
Reject   Accept
Patch    Patch
```

This reduces the risk of treating plausible-looking AI output as working code.

---

# 🎯 Beyond the Prototype

The Pygame example demonstrates the debugging loop with a bug that is easy to see during a live demo.

The same architecture can be extended to real game-development workflows.

### Unity / C#

GameBug Hunter could integrate with:

- Unity Test Framework
- C# compilation errors
- Unity Editor logs
- stack traces
- gameplay tests
- scene validation
- asset/configuration validation

### Smarter Neo4j Retrieval

Before generating a patch:

```text
New failure
    ↓
Search Neo4j
    ↓
Find similar historical bugs
    ↓
Retrieve successful fixes
    ↓
Give context to debugging agent
    ↓
Generate better patch
```

### Parallel Daytona Sandboxes

Multiple agents could investigate different hypotheses simultaneously:

```text
                 BUG
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   Sandbox A  Sandbox B  Sandbox C
        │         │         │
   Hypothesis  Hypothesis  Hypothesis
        │         │         │
        └─────────┼─────────┘
                  ▼
             Best verified fix
```

---

# 💡 Vision

Modern coding agents are becoming increasingly capable of writing code.

But debugging agents need three additional capabilities:

**a safe place to execute, a way to prove their fix, and memory of what they learned.**

GameBug Hunter combines those ideas:

```text
Daytona
   ↓
Safe execution

OpenAI
   ↓
Reasoning + repair

pytest
   ↓
Verification

Neo4j
   ↓
Persistent debugging memory
```

### Give the agent a broken game.

### Get back a verified fix — and knowledge that survives the debugging session.

---

## Built at Daytona HackSprint Tokyo 2026

**GameBug Hunter**

Autonomous AI gameplay debugging with **Daytona + OpenAI + Neo4j**.
