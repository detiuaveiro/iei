#!/bin/bash
# ai_fix.sh — Diagnostica e sugere correcoes para comandos com erro
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Validar se o utilizador forneceu um comando
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 \"comando que falhou\"" >&2
    exit 1
fi

# Dica: "$*" agrupa todas as palavras passadas como argumento
CMD="$*"

# 2. Executar o comando e capturar stdout e stderr juntos
echo "A executar: $CMD ..."
ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)

# 3. Formatar o pedido e invocar o assistente com a skill
# TODO [Desafio]: Monte o prompt com o comando ($CMD) e o erro
# ($ERROR_OUTPUT), e invoque o ask_ai.sh passando a skill:
# "$SCRIPT_DIR/skills/error-fix/SKILL.md"

# (Escreva aqui a chamada ao ask_ai.sh)
