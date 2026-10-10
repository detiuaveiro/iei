#!/bin/bash
# ai_fix.sh — Diagnostica e sugere correcoes para comandos com erro (IEI - UA)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Validar se o utilizador forneceu um comando
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 \"comando que falhou\"" >&2
    exit 1
fi

CMD="$*"

# 2. Executar o comando e capturar a mensagem de erro
echo "A executar: $CMD ..."
ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)

# 3. Formatar o pedido de diagnostico para o assistente
PROMPT="O comando de terminal '$CMD' falhou com a seguinte mensagem:\n"
PROMPT="${PROMPT}${ERROR_OUTPUT}\n\n"
PROMPT="${PROMPT}Explica em 1 frase a causa do erro e fornece"
PROMPT="${PROMPT} o comando corrigido exato."

# 4. Invocar o assistente ask_ai.sh com a skill de diagnostico
SKILL_FILE="${SCRIPT_DIR}/skills/error-fix/SKILL.md"
"$SCRIPT_DIR/ask_ai.sh" "$PROMPT" "$SKILL_FILE"
