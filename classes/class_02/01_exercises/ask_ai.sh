#!/bin/bash
# ask_ai.sh — Assistente de Consola com Contexto Local
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="https://generativelanguage.googleapis.com"
API_URL="${BASE}/v1beta/interactions"
MODEL="${MODEL:-gemini-3.5-flash-lite}"

# 1. Validar se a chave de API esta configurada no ambiente
if [ -z "${GEMINI_API_KEY:-}" ]; then
    echo "Erro: GEMINI_API_KEY nao definida!" >&2
    echo "Execute: export GEMINI_API_KEY=\"a_sua_chave\"" >&2
    exit 1
fi

# 2. Validar argumento de pergunta
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 \"pergunta ou instrucao\" [ficheiro_contexto]" >&2
    exit 1
fi

USER_QUERY="$1"
CONTEXT_FILE="${2:-}"

# 3. Carregar contexto (do ficheiro indicado ou de AGENTS.md)
CONTEXT_TEXT=""
if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
    CONTEXT_TEXT="<contexto>\n$(cat "$CONTEXT_FILE")\n</contexto>\n\n"
    echo "[INFO] Contexto carregado de: $CONTEXT_FILE" >&2
elif [ -f "AGENTS.md" ]; then
    CONTEXT_TEXT="<project_guidelines>\n"
    CONTEXT_TEXT="${CONTEXT_TEXT}$(cat AGENTS.md)\n"
    CONTEXT_TEXT="${CONTEXT_TEXT}</project_guidelines>\n\n"
    echo "[INFO] Contexto carregado de: AGENTS.md" >&2
fi

FULL_INPUT="${CONTEXT_TEXT}Tarefa: ${USER_QUERY}"

# 4. Montar o payload JSON de forma segura com Python
PAYLOAD=$(python3 -c '
import json, sys
print(json.dumps({
    "model": sys.argv[1],
    "input": sys.argv[2],
    "generation_config": {"thinking_level": "low"}
}))
' "$MODEL" "$FULL_INPUT")

# 5. Executar o pedido via curl e apresentar a resposta limpa
echo ""
echo "=== Resposta da IA ==="
# TODO [Desafio]: Complete com a chamada curl (Exercicios 3 e 4).
# Requisitos:
#  - Metodo POST para "$API_URL"
#  - Header "x-goog-api-key: ${GEMINI_API_KEY}"
#  - Header "Content-Type: application/json"
#  - Enviar dados de "$PAYLOAD"
#  - Canalizar (|) a saida para: python3 "$SCRIPT_DIR/get_text.py"

# (Escreva aqui o seu comando curl)

echo "======================="
