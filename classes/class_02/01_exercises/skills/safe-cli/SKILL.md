---
name: safe-cli
description: Analisador de seguranca para comandos UNIX (Linux e macOS).
---

# Procedimento Operacional da Skill safe-cli:
Ao receber um comando para inspecionar, segue estes 4 passos:
1. [Nivel de Risco]: Classifica como [SEGURO], [ATENCAO] ou [PERIGOSO].
2. [Objetivo]: Resume em uma frase clara o que o comando faz.
3. [Decomposicao]: Explica cada comando, subcomando e flag utilizada.
4. [Alerta & Alternativa]: Se o comando tiver impacto destrutivo
   (ex: rm -rf, dd, chmod -R 777, diskutil), adverte sobre o perigo
   e apresenta uma alternativa segura com privilegios minimos.
