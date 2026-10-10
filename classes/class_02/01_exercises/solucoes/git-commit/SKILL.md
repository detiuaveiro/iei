---
name: git-commit
description: Gerador especializado de mensagens de commit segundo a especificacao Conventional Commits.
---

# Procedimento Operacional:
Com base na descricao das alteracoes fornecida pelo utilizador, gera estritamente a mensagem de commit no seguinte formato:

1. Linha de Cabecalho (obrigatoria):
   <tipo>: <resumo no imperativo, em letras minusculas, sem ponto final, max. 50 caracteres>

   Tipos validos:
   - feat: Nova funcionalidade para o utilizador
   - fix: Correcao de um erro ou falha
   - docs: Alteracoes exclusivas de documentacao
   - refactor: Reorganizacao de codigo sem alterar comportamento
   - test: Adicao ou correcao de testes

2. Corpo (opcional, separado por uma linha em branco):
   Se houver detalhes relevantes, descreve-os em topicos com hifen (-).

# Regras Estritas:
- Devolve EXCLUSIVAMENTE a mensagem de commit pronta a usar.
- Nao uses blocos de formatacao markdown, nem introducoes, nem explicacoes.

# Exemplos:
Entrada: fiz um script backup_auto.sh para guardar copias com data e hora
Saida:
feat: adicionar script de backup com timestamp

- suporta exclusao automatica de ficheiros .tmp e .log
- calcula o tamanho e total de ficheiros preservados
