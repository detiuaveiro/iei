#!/bin/bash
# ai_commit.sh — Gera mensagens Conventional Commits via assistente
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Validar se o utilizador indicou uma descricao das alteracoes
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 \"descreva brevemente o que alterou no codigo\"" >&2
    exit 1
fi

# Validar se o ficheiro da skill existe
SKILL_FILE="${SCRIPT_DIR}/skills/git-commit/SKILL.md"
if [ ! -f "$SKILL_FILE" ]; then
    echo "Erro: Ficheiro da skill nao encontrado em: $SKILL_FILE" >&2
    exit 1
fi

# 2. Capturar as notas de alteracoes e invocar o assistente com a skill
# TODO [Desafio]:
#  - Guarde todas as palavras passadas pelo utilizador na variavel NOTAS (dica: use "$*")
#  - Invoque o script "$SCRIPT_DIR/ask_ai.sh" passando como primeiro argumento o pedido:
#    "Gera a mensagem de commit para: $NOTAS"
#    e como segundo argumento o ficheiro da skill: "$SKILL_FILE"

# (Escreva aqui a captura de NOTAS e a invocacao de ask_ai.sh)

