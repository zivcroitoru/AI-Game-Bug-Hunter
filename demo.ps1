Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "             GAMEBUG HUNTER" -ForegroundColor Cyan
Write-Host "        TWO-STAGE DEBUGGING DEMO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""


# =========================================================
# STAGE 0 - RESET EVERYTHING
# =========================================================

Write-Host "[SETUP] Resetting game to original buggy state..." -ForegroundColor Yellow

@'
def take_damage(current_health, damage):
    return current_health + damage
'@ | Set-Content -Encoding utf8 game_logic.py


# At first, GameBug Hunter knows ONLY about the healing bug.
@'
from game_logic import take_damage


def test_player_takes_damage():
    assert take_damage(100, 20) == 80
'@ | Set-Content -Encoding utf8 test_game_logic.py


Write-Host ""
Write-Host "Initial bug injected:" -ForegroundColor Red
Write-Host "    return current_health + damage" -ForegroundColor Red
Write-Host ""


# =========================================================
# DEMO 1 - HEALING BUG
# =========================================================

Write-Host "============================================" -ForegroundColor Red
Write-Host " BUG #1 - DAMAGE HEALS THE PLAYER" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host ""

Write-Host "Launching game..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press SPACE." -ForegroundColor Cyan
Write-Host ""
Write-Host "Expected: 100 -> 80" -ForegroundColor Green
Write-Host "Actual:   100 -> 120" -ForegroundColor Red
Write-Host ""
Write-Host "Close the game after demonstrating the bug." -ForegroundColor DarkGray
Write-Host ""

python game.py


# =========================================================
# AI FIX #1
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " GAMEBUG HUNTER INVESTIGATION #1" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Running AI debugging agent..." -ForegroundColor Yellow
Write-Host ""

python agent.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Agent failed during Bug #1." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Bug #1 fixed and verified!" -ForegroundColor Green
Write-Host ""
Write-Host "Current gameplay logic:" -ForegroundColor Cyan
Get-Content game_logic.py

Start-Sleep -Seconds 2


# =========================================================
# DEMO 2 - DISCOVER SECOND BUG
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host " TESTING THE FIXED GAME..." -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "The healing bug is fixed." -ForegroundColor Green
Write-Host ""
Write-Host "Now let's test an edge case..." -ForegroundColor White
Write-Host ""
Write-Host "1. Press H to set player health to 10." -ForegroundColor Cyan
Write-Host "2. Press SPACE so the enemy deals 20 damage." -ForegroundColor Cyan
Write-Host ""
Write-Host "Expected: 10 -> 0" -ForegroundColor Green
Write-Host "Actual:   10 -> -10" -ForegroundColor Red
Write-Host ""
Write-Host "Close the game after demonstrating the second bug." -ForegroundColor DarkGray
Write-Host ""

python game.py


# =========================================================
# ADD REGRESSION / EDGE-CASE TEST
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Red
Write-Host " BUG #2 DISCOVERED - NEGATIVE HEALTH" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host ""

Write-Host "Adding a new edge-case test..." -ForegroundColor Yellow
Write-Host ""

@'
from game_logic import take_damage


def test_player_takes_damage():
    assert take_damage(100, 20) == 80


def test_health_never_goes_below_zero():
    assert take_damage(10, 20) == 0
'@ | Set-Content -Encoding utf8 test_game_logic.py


Write-Host "New test added:" -ForegroundColor Cyan
Write-Host "    take_damage(10, 20) must return 0" -ForegroundColor White
Write-Host ""

python -m pytest -v

Write-Host ""


# =========================================================
# AI FIX #2
# =========================================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " GAMEBUG HUNTER INVESTIGATION #2" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Sending the NEW failure to the debugging agent..." -ForegroundColor Yellow
Write-Host ""

python agent.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Agent failed during Bug #2." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Bug #2 fixed and verified!" -ForegroundColor Green
Write-Host ""
Write-Host "Final gameplay logic:" -ForegroundColor Cyan
Get-Content game_logic.py

Start-Sleep -Seconds 2


# =========================================================
# STORE FINAL DEBUGGING KNOWLEDGE
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host " SAVING DEBUGGING MEMORY TO NEO4J" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

python push_to_neo4j.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Neo4j save failed - continuing demo." -ForegroundColor Red
}
else {
    Write-Host ""
    Write-Host "Debugging knowledge saved to Neo4j." -ForegroundColor Green
}


# =========================================================
# FINAL GAME
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "       FINAL VERIFICATION" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Launching fully repaired game..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Test normal damage:" -ForegroundColor Cyan
Write-Host "    SPACE: 100 -> 80 -> 60" -ForegroundColor Green
Write-Host ""
Write-Host "Test low-health edge case:" -ForegroundColor Cyan
Write-Host "    H -> health becomes 10" -ForegroundColor White
Write-Host "    SPACE -> 10 -> 0" -ForegroundColor Green
Write-Host ""
Write-Host "Health should NEVER become negative." -ForegroundColor Green
Write-Host ""

python game.py


# =========================================================
# DONE
# =========================================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "             DEMO COMPLETE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Bug #1:" -ForegroundColor Red
Write-Host "    Damage healed player"
Write-Host "    100 -> 120"
Write-Host "        |"
Write-Host "        v"
Write-Host "    AI FIX #1" -ForegroundColor Cyan
Write-Host "        |"
Write-Host "        v"
Write-Host "    100 -> 80" -ForegroundColor Green
Write-Host ""

Write-Host "Bug #2:" -ForegroundColor Red
Write-Host "    Health could become negative"
Write-Host "    10 -> -10"
Write-Host "        |"
Write-Host "        v"
Write-Host "    AI FIX #2" -ForegroundColor Cyan
Write-Host "        |"
Write-Host "        v"
Write-Host "    10 -> 0" -ForegroundColor Green
Write-Host ""

Write-Host "Execute -> Detect -> Patch -> Verify -> Discover -> Patch -> Verify -> Remember" -ForegroundColor Cyan
Write-Host ""