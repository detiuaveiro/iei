#!/bin/bash
# ai_commit.sh — Gera mensagens Conventional Commits via assistente (IEI - UA)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -eq 0 ]; then
    echo "Uso: $0 \"descreva brevemente o que alterou no codigo\"" >&2
    exit 1
fi

NOTAS="$*"

# Determinar caminho da skill (na pasta de trabalho do aluno ou na pasta de solucoes)
if [ -f "${SCRIPT_DIR}/skills/git-commit/SKILL.md" ]; then
    SKILL_FILE="${SCRIPT_DIR}/skills/git-commit/SKILL.md"
elif [ -f "${SCRIPT_DIR}/git-commit/SKILL.md" ]; then
    SKILL_FILE="${SCRIPT_DIR}/git-commit/SKILL.md"
else
    SKILL_FILE="skills/git-commit/SKILL.md"
fi

"$SCRIPT_DIR/ask_ai.sh" "Gera a mensagem de commit para: $NOTAS" "$SKILL_FILE"
