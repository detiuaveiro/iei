#!/bin/bash
# welcome.sh — Painel de Boas-Vindas da Workstation IEI (Linux & macOS) (IEI - UA)
set -euo pipefail

# Definicao portatil de cores ANSI compativel com Linux e macOS (POSIX)
VERDE=$(printf '\033[32m')
AMARELO=$(printf '\033[33m')
AZUL=$(printf '\033[34m')
RESET=$(printf '\033[0m')

printf "${AZUL}====================================================${RESET}\n"
printf "${AZUL}    IEI Workstation — Universidade de Aveiro        ${RESET}\n"
printf "${AZUL}====================================================${RESET}\n"
printf " Utilizador : ${VERDE}%s${RESET}\n" "$USER"
printf " Sistema    : %s (%s)\n" "$(uname -s)" "$(uname -m)"
printf " Data/Hora  : %s\n" "$(date +"%Y-%m-%d %H:%M:%S")"

# 1. Verificacao de segredos e estado da API Gemini
if [ -n "${GEMINI_API_KEY:-}" ]; then
    printf " API Gemini : ${VERDE}[OK] Chave ativa${RESET}\n"
else
    printf " API Gemini : ${AMARELO}[AVISO] Chave em falta (~/.api_keys)${RESET}\n"
fi

# 2. Resumo da pasta de trabalho do laboratorio
AULA_DIR="$HOME/IEI/aula02"
if [ -d "$AULA_DIR" ]; then
    TOTAL_FICH=$(find "$AULA_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')
    printf " Ficheiros  : %s ficheiros na pasta ~/IEI/aula02\n" "$TOTAL_FICH"
fi

printf "${AZUL}----------------------------------------------------${RESET}\n"
printf " Atalhos: ${VERDE}ask${RESET} \"pergunta\" | ${VERDE}fix${RESET} \"cmd_com_erro\"\n"
printf "${AZUL}====================================================${RESET}\n\n"
