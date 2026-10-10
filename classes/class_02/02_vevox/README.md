# Exercícios de Consolidação Vevox — Class 02

Este diretório contém o banco de **25 questões pedagógicas de consolidação técnica** desenhadas para dinamização interativa com os estudantes na plataforma **Vevox** no final da **Class 02**, integrando e consolidando os conceitos fundamentais da **Class 00**, **Class 01** e **Class 02**.

Os enunciados e opções foram **otimizados para máxima concisão**, assegurando excelente legibilidade e fluidez em ecrãs de telemóvel e projeção em sala de aula.

---

## 🎯 Distribuição por Nível de Dificuldade

O banco de questões foi calibrado segundo uma curva pedagógica equilibrada para sessões interativas síncronas:

| Nível de Dificuldade | Qtd | % | Questões | Foco Pedagógico |
| :--- | :---: | :---: | :--- | :--- |
| **Baixa** | **9** | **36%** | Q02, Q05, Q06, Q07, Q08, Q12, Q14, Q18, Q20 | Recordação e identificação direta de comandos, convenções de ficheiros, atalhos e hiperparâmetros. |
| **Média** | **11** | **44%** | Q01, Q04, Q09, Q10, Q11, Q13, Q16, Q17, Q19, Q22, Q23 | Aplicação de comandos, cálculo de permissões octais, sintaxe temporal do cron, composição por pipes e conceitos de tokenização e contexto. |
| **Média-Alta** | **5** | **20%** | Q03, Q15, Q21, Q24, Q25 | Diagnóstico de falhas de ambiente, isolamento em subshells, modelos económicos de APIs (FinOps), fronteiras de segurança (*Soft* vs. *Hard Guardrails*) e arquitetura de agentes. |

---

## 📚 Distribuição Curricular dos Tópicos

* **Bloco I — Class 00 (Sistemas Operativos, Ficheiros e Ambientes Linux):** Questões 1 a 4
  * Q01 [Média]: Organização do sistema de ficheiros (Linux raiz unificada `/` e *case-sensitive* vs. Windows `C:` e *case-insensitive*).
  * Q02 [Baixa]: Vantagens da Máquina Virtual (*sandbox* e *snapshots*) face a instalação nativa.
  * Q03 [Média-Alta]: WSL 2 (acesso a `/mnt/c/` e boa prática de I/O na pasta nativa `/home/utilizador/`).
  * **Q04 [Matching | Média]:** Correspondência de abordagens de ambiente (Nativa, VM, WSL 2, utilitário `uname -a`).
* **Bloco II — Class 01 (Terminal Linux e Ferramentas de Shell):** Questões 5 a 14
  * Q05 [Baixa]: Terminal vs. Shell e o sinal `Ctrl + C` (`SIGINT`).
  * Q06 [Baixa]: Navegação relativa no sistema de ficheiros (`cd ../..`).
  * Q07 [Baixa]: Ficheiros ocultos (prefixo `.`) e comando `ls -la`.
  * Q08 [Baixa]: Redirecionamento de saída: sobrescrever (`>`) vs. concatenar (`>>`).
  * Q09 [Média]: Composição por pipes (`cat \| grep \| wc -l`).
  * Q10 [Média]: Permissões octais e de segurança (`chmod 600`).
  * Q11 [Média]: Gestão de processos e encerramento incondicional (`kill -9` / `SIGKILL`).
  * Q12 [Baixa]: Gestão de pacotes com APT (`apt update` vs. `apt upgrade`).
  * Q13 [Média]: Sintaxe dos 5 campos temporais do `crontab`.
  * **Q14 [Matching | Baixa]:** Correspondência entre comandos essenciais (`pwd`, `head -n 5`, `touch`, `grep -i`).
* **Bloco III — Class 02 (Gestão de Ambiente, Automação & IA na Engenharia de Software):** Questões 15 a 25
  * Q15 [Média-Alta]: Variáveis locais vs. variáveis de ambiente globais (`export`) e isolamento em subprocessos.
  * Q16 [Média]: Persistência no `~/.bashrc` e recarregamento com `source` na sessão ativa.
  * Q17 [Média]: Segurança rigorosa de credenciais e ficheiros de segredos (`chmod 600`).
  * Q18 [Baixa]: Arquivo e compressão com `tar` (`-czvf`).
  * Q19 [Média]: Fundamentos de LLMs: *Tokens* vs. *Palavras*.
  * Q20 [Baixa]: Hiperparâmetros: Temperatura ($\tau$) determinista para código.
  * Q21 [Média-Alta]: Modelos económicos de IA: Chat web vs. APIs *pay-as-you-go*, riscos em *retry loops* e *Hard Spend Limits*.
  * Q22 [Média]: Engenharia de Contexto vs. personas teatrais (os 4 pilares: Task-first, tags XML, restrições e Few-Shot).
  * Q23 [Média]: O papel do ficheiro `AGENTS.md` como contrato do repositório.
  * Q24 [Média-Alta]: Segurança em Agentes: *Soft Guardrails* (prompts) vs. *Hard Guardrails* deterministas no SO.
  * **Q25 [Matching | Média-Alta]:** Correspondência de conceitos-chave de IA (`MCP`, `Alucinação`, `Few-Shot`, `Hard Spend Limit`).

---

## 📁 Ficheiros Disponíveis

1. **[`vevox_pt_00.xlsx`](vevox_pt_00.xlsx) ⭐ (Ficheiro de Importação Oficial):**
   * Preenchido segundo o template oficial do Vevox (`Vevox_QuestionImportTemplate.xlsx`).
   * **22 Questões do tipo `MCQ`** com opções curtas e objetivas, resposta correta em `CorrectAnswer1` e explicação em `CorrectAnswerExplanation`.
   * **3 Questões nativas do tipo `Matching` (Q04, Q14, Q25)**, com pares diretos em `Choice1..4` $\leftrightarrow$ `CorrectAnswer1..4`.

2. **[`vevox_pt_00.md`](vevox_pt_00.md):**
   * Documento mestre de estudo e suporte ao docente, com classificação explícita de dificuldade e justificações pedagógicas completas.
   * Compilável para PDF via Pandoc/LuaLaTeX (`make pdf`).

3. **[`vevox_pt_00.csv`](vevox_pt_00.csv):**
   * Exportação alternativa em formato CSV.

4. **[`Vevox_QuestionImportTemplate.xlsx`](Vevox_QuestionImportTemplate.xlsx):**
   * Template original da plataforma Vevox.

5. **[`Makefile`](Makefile):**
   * Script de compilação PDF (`make pdf` ou `make clean`).

---

## 🚀 Como Importar no Vevox

1. Aceda ao painel [Vevox Dashboard](https://dashboard.vevox.com/) e entre na sessão pretendida.
2. No menu lateral, selecione **Polls** (Votações).
3. Clique em **Import** no canto superior direito.
4. Selecione o ficheiro **`vevox_pt_00.xlsx`**.
5. Todas as **25 questões** (incluindo as 3 de correspondência interativa) serão criadas instantaneamente, prontas para dinamização!
