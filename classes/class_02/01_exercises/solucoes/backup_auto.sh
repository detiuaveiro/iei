#!/bin/bash
# backup_auto.sh — Cria arquivo .tar.gz com timestamp e exclui temporarios (IEI - UA)
set -euo pipefail

# 1. Validar se a pasta de origem foi indicada
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 <diretorio_origem> [diretorio_destino]" >&2
    exit 1
fi

ORIGEM="$1"
DESTINO="${2:-.}"

if [ ! -d "$ORIGEM" ]; then
    echo "Erro: O diretorio '$ORIGEM' nao existe!" >&2
    exit 1
fi

# 2. Gerar timestamp e nome do ficheiro
NOME_BASE=$(basename "$ORIGEM")
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
NOME_ARQUIVO="${DESTINO}/backup_${NOME_BASE}_${TIMESTAMP}.tar.gz"

echo "A empacotar '$ORIGEM' para '$NOME_ARQUIVO'..."

# 3. Criar arquivo comprimido excluindo temporarios
tar --exclude="*.tmp" \
    --exclude="*.log" \
    -czf "$NOME_ARQUIVO" "$ORIGEM"

# 4. Exibir relatorio de sucesso e contagem de ficheiros
TOTAL_FICH=$(tar -tf "$NOME_ARQUIVO" | wc -l | tr -d ' ')
TAMANHO=$(ls -lh "$NOME_ARQUIVO" | awk '{print $5}')

echo "Backup concluido com sucesso!"
echo " - Ficheiro: $NOME_ARQUIVO"
echo " - Tamanho: $TAMANHO"
echo " - Ficheiros preservados: $TOTAL_FICH"
