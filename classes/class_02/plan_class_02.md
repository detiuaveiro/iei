# Plano de Aula: Class 02 — Linux II: Gestão de Ambiente, Automação & IA na Engenharia de Software

Este documento estabelece o plano pedagógico, curricular e técnico para a substituição do módulo de Terminal Windows por uma segunda sessão aprofundada de **Terminal Linux, Gestão de Ambiente & Engenharia de Inteligência Artificial na Linha de Comandos**.

---

## 1. Justificação Curricular & Pedagógica

* **Consolidação Técnica em POSIX/Linux:** A alternância precoce para CMD/PowerShell criava uma quebra na curva de aprendizagem dos caloiros. Aprofundar o ambiente Linux fornece os alicerces necessários para os módulos seguintes de **Virtualização e Docker (C2)**, **Git e GitHub (C3)**, **Redes IP (C4)** e **Web Servers (C5)**.
* **Persistência de Ambiente e Segurança Multi-utilizador:** Compreender como a *shell* carrega configurações através do `~/.bashrc` e como recarregar o ambiente com `source` resolve um problema prático diário dos estudantes. Ao mesmo tempo, reforça os conceitos de permissões Unix (`chmod 600`) para proteger ficheiros de configuração e chaves de API contra leitura por outros utilizadores em sistemas partilhados.
* **Transição de "Prompting Mágico" para "Context Engineering":** Em 2026, modelos de fronteira não beneficiam de "personas" teatrais ("Atua como um perito..."), mas exigem **especificação rigorosa de tarefas, fronteiras de contexto, restrições operacionais e calibragem por exemplos (few-shot)**.
* **Adoção dos Padrões Modernos da Indústria (`AGENTS.md`, Skills & MCP):** Introduzir o ficheiro `AGENTS.md` capacita os estudantes a fornecer contexto arquitetural a assistentes e agentes de código (Antigravity, Cursor, Claude Code, GitHub Copilot). O enquadramento conceitual de **Skills** (playbooks modulares) e **MCP** (Model Context Protocol para conetores de ferramentas) prepara os caloiros para o paradigma contemporâneo do desenvolvimento assistido por IA.
* **Segurança Real (Soft vs. Hard Guardrails):** Ensinar com rigor que instruções em linguagem natural no `AGENTS.md` são apenas orientações suaves (*soft boundaries*), sendo indispensável o uso de salvaguardas deterministas no sistema (*hard boundaries*): intercetores de ferramentas, aprovação humana (*Human-in-the-Loop*) e isolamento em *sandbox*.
* **Engenharia Financeira e Modelos de Consumo:** Explicar a diferença entre subscrições fixas de chat e APIs de pagamento ao token (*pay-as-you-go*), alertando para o risco de explosão de custos em agentes com *loops* infinitos e ensinando a configurar limites orçamentais estritos (*Hard Spend Limits*).

---

## 2. Objetivos de Aprendizagem

Ao concluir esta sessão, o estudante deverá ser capaz de:
1. **Compreender e gerir variáveis de ambiente:** Diferenciar variáveis locais da shell de variáveis exportadas (`export`), analisar herança por subprocessos e gerir a persistência de configurações no `~/.bashrc` com o comando `source`.
2. **Aplicar segurança de permissões a ficheiros de segredos:** Proteger chaves de API e ficheiros de configuração pessoal contra leitura não autorizada em sistemas multi-utilizador utilizando permissões estritas (`chmod 600`).
3. **Criar e restaurar arquivos compactados:** Utilizar o utilitário `tar` (`-czvf` e `-xzvf`) para cópias de segurança e distribuição de projetos.
4. **Compreender os fundamentos operativos de LLMs:** Explicar o papel dos tokens, da janela de contexto, da temperatura e a origem das alucinações.
5. **Diferenciar Modelos de Consumo de IA e Gerir Custos:** Comparar subscrições web de preço fixo com APIs pagas ao token, compreender o risco de custos exponenciais em agentes em ciclo (*loop*) e aplicar boas práticas de contenção de despesas (*Hard Spend Limits*).
6. **Consumir APIs de modelos de linguagem via CLI:** Utilizar o `curl` para enviar pedidos HTTP com credenciais em variáveis de ambiente (`$GEMINI_API_KEY`) e tratar respostas JSON.
7. **Aplicar Engenharia de Contexto:** Estruturar pedidos com instrução direta (Task-first), delimitação clara de contexto, restrições estritas de formato (ex: apenas código Bash cru) e calibração por Few-Shot.
8. **Construir um `AGENTS.md` e desenhar uma `Skill`:** Criar o ficheiro `AGENTS.md` para ancorar o comportamento de agentes no repositório e implementar uma skill modular simples (`safe-cli`) para análise crítica de segurança de comandos de terminal (*shell*).
9. **Diferenciar Soft Guardrails de Hard Guardrails:** Reconhecer que prompts em linguagem natural não são barreiras de segurança e valorizar a validação determinista e o princípio do *Human-in-the-Loop*.

---

## 3. Gestão Temporal (Aula de 3 Horas = 180 min)

* **0h00 – 0h40 (40 min): Bloco Teórico I — Ambiente UNIX, Persistência (`~/.bashrc` / `~/.zshrc`) & Automação Básica**
  * Variáveis locais vs. globais (`export`), herança por processos filhos (subshells).
  * Inspecionar e limpar variáveis (`printenv`, `env`, `unset`).
  * Persistência de configurações: ciclo de arranque da shell no Linux (`~/.bashrc`) e macOS (`~/.zshrc`).
  * Recarregar a sessão ativa com `source` e proteção de credenciais com permissões Unix (`chmod 600`).
  * Cópias de segurança e empacotamento com `tar` (`tar -czvf`, `tar -xzvf`).
* **0h40 – 0h50 (10 min): Intervalo**
* **0h50 – 1h40 (50 min): Bloco Teórico II — Fundamentos de IA, Modelos de Consumo & Engenharia de Agentes**
  * Enquadramento: A IA na engenharia de software (componente computacional vs. oráculo mágico).
  * Como funcionam as LLMs: probabilidades estatísticas de predição de texto.
  * O que são **Tokens**, **Janela de Contexto** e **Temperatura**.
  * Alucinações e o sentido crítico: a IA como copiloto, o engenheiro como piloto responsável.
  * **Paradigmas de Interação com IA:** Web Chat, Agentes de Terminal (Claude Code, Gemini CLI) e APIs.
  * **Modelos de Consumo de IA:** Subscrição mensal vs. APIs *pay-as-you-go*; FinOps e limites rígidos de despesa (*Hard Spend Limits*).
  * Porquê o Terminal e consumo prático via `curl` na linha de comandos com `$GEMINI_API_KEY`.
  * Fim do mito da "persona" e **Engenharia de Contexto** (Task-first, Delimitação de contexto, Restrições estritas e Few-Shot).
  * Além do Chat: Agentes Autónomos (*Perceive $\rightarrow$ Reason $\rightarrow$ Act*) e a Tríade da Autonomia (**`AGENTS.md`**, **Skills** e **MCP**).
  * **Segurança Rigorosa em Agentes:** Soft vs. Hard Guardrails (intercetores deterministas, *sandboxes* e *Human-in-the-Loop*).
* **1h40 – 2h45 (65 min): Trabalho Prático Orientado**
  * Execução dos exercícios do guião prático no laboratório.
* **2h45 – 3h00 (15 min): Síntese, Análise Crítica e Encerramento**
  * **Quiz Interativo Vevox (`02_vevox/`):** Dinamização de 25 questões de consolidação cobrindo a matéria da Class 00, Class 01 e Class 02 (escolha múltipla e matching).
  * Discussão das saídas geradas pela IA, verificação de alucinações e consolidação de boas práticas.

---

## 4. Estrutura dos Slides (`00_slides/`)

1. **Parte I: Gestão de Ambiente Linux e Automação:** Resumo dos tópicos da primeira parte da sessão.
2. **Ponte com a Sessão I:** As variáveis do sistema (`$USER`, `$HOME`, `$PATH`) como variáveis de ambiente.
3. **Variáveis na Shell:** Locais vs. Globais (`export`) e criação de variáveis próprias.
4. **Herança de Variáveis na Shell:** A fronteira dos scripts e porque um script filho não herda variáveis locais sem `export`.
5. **Inspecionar e Gerir o Ambiente:** `printenv`, `env`, `unset`.
6. **Persistência de Ambiente:** O papel do ficheiro `~/.bashrc` e arranque de novas sessões.
7. **Recarregar com `source` & Segurança com `chmod 600`:** Evitar reinícios e proteger credenciais em sistemas partilhados.
8. **Arquivo e Compressão de Dados com `tar`:** Criação e extração de ficheiros comprimidos com `tar -czvf` e `tar -xzvf`.
9. **Parte II: Inteligência Artificial na Engenharia de Software:** Resumo dos tópicos da segunda parte da sessão.
10. **A Postura da Engenharia Informática perante a IA:** Componente computacional vs. oráculo mágico, mudança de paradigma e validação crítica.
11. **Como Funcionam as LLMs:** Da previsão autoregressiva às representações geométricas internas e inferência de intenção.
12. **Unidade de Processamento:** Tokens vs. Palavras, contagem e decomposição.
13. **Janela de Contexto e Hiperparâmetros:** Horizonte de atenção ($L_{\max}$), teto de saída (*Max Output Tokens*), higiene de contexto (*reset*) e Temperatura ($\tau$).
14. **Alucinações & Validação Crítica:** Por que a inferência estatística inventa respostas convincentes e a necessidade de verificação técnica humana.
15. **Paradigmas de Interação com Modelos de IA:** Do Web Chat aos Agentes no Terminal (Claude Code, Gemini CLI) e APIs.
16. **Modelos de Consumo: Subscrição vs. APIs Pay-as-you-go:** Chat fixo no browser vs. chamadas programáticas pagas por milhão de tokens.
17. **O Risco dos Custos na API: O Efeito Multiplicador dos Agentes:** Mecânica do efeito multiplicador de tokens e risco de ciclos infinitos (*retry loops*).
18. **Gestão de Custos em APIs: Salvaguardas e Cuidados:** Limites rígidos (*Hard Spend Limits*), latência de alertas, controlo no código, fuga de chaves e *Free Tier*.
19. **A Linha de Comandos no Ecossistema de IA:** Porquê consumir e orquestrar modelos a partir do terminal (pipes, cron, headless).
20. **Consumindo a API no Terminal:** A primeira chamada com `curl`, variáveis de ambiente e headers HTTP.
21. **Formulação de Instruções (O Mito das Personas):** Da chamada API à instrução técnica e ineficácia de personas em engenharia.
22. **Transição: Da Engenharia de Prompts para Engenharia de Contexto:** De instruções informais a especificações técnicas deterministas.
23. **Os 4 Pilares da Engenharia de Contexto:** Tarefa Direta (Task), Delimitação Estruturada, Restrições (Constraints) e Calibração por Exemplos (Few-Shot).
24. **Delimitação Estruturada de Contexto:** Separação inequívoca entre instruções e dados (tags XML).
25. **Calibração por Exemplos (Zero-Shot vs. Few-Shot):** Ensinar a estrutura desejada por analogia com instâncias.
26. **Além da Invocação Pontual — A Era dos Agentes Autónomos:** Definição formal em Ciência da Computação / IA (*Perceive $\rightarrow$ Reason $\rightarrow$ Act*) e instanciação em agentes de engenharia de software (*Coding Agents*).
27. **A Tríade da Autonomia:** Os três pilares de controlo e extensão: `AGENTS.md`, Skills e MCP.
28. **O Ficheiro `AGENTS.md` (Conceito e Âmbito):** A constituição viva do projeto (âmbito na raiz e subpastas).
29. **O Ficheiro `AGENTS.md` (Objetivos Operacionais):** Controlo de dependências, conformidade e restrições.
30. **Estrutura Típica de um Ficheiro `AGENTS.md`:** Stack, comandos padrão e regras de segurança (exemplo curricular).
31. **Padronização de `AGENTS.md` em Projetos de Software:** Template Builder de Addy Osmani (comandos, testes, estrutura, estilo e fronteiras).
32. **Estudo de Caso — AGENTS.md num Projeto Real:** Especificação completa de produção (FastAPI, PostgreSQL, Poetry e *Do Not Modify*).
33. **Impacto do Contexto no Comportamento do Agente:** Comparação perante a mesma tarefa com e sem `AGENTS.md`.
34. **Segurança Rigorosa (Soft Boundaries):** Porque prompts em linguagem natural não são barreiras de segurança.
35. **Segurança Rigorosa (Hard Guardrails):** Intercetores determinísticos, aprovação humana (*Human-in-the-Loop*) e isolamento em *sandbox*.
36. **Skills (Playbooks Modulares):** Conhecimento especializado sob demanda.
37. **Implementação de uma Skill:** Procedimento prático da skill `safe-cli`.
38. **Model Context Protocol (MCP):** O conetor padrão da indústria para dotar modelos de ferramentas e acesso ao sistema.
39. **MCP na Prática (Implementação e Registo):** Servidor Python (`FastMCP`) e registo de ferramentas no cliente (`mcp_config.json`).
40. **Referências e Recursos Técnicos:** Leituras complementares e documentação oficial (incluindo Addy Osmani).

---

## 5. Estrutura do Guião Prático (`01_exercises/`)

### Parte I: Gestão de Ambiente e Cópias de Segurança
* **Exercício 1: Variáveis de Ambiente, Subprocessos, Persistência (`~/.bashrc` / `~/.zshrc`) e Permissões**
  * Criação de variável local e teste de falha de herança com script executável / processo filho.
  * Exportação com `export` e verificação da herança no script.
  * Inspecionar com `printenv` e `env`, compreendendo o isolamento de variáveis locais, e limpar com `unset`.
  * Persistência de chaves e variáveis através de ficheiro de configuração importado pela shell (`~/.bashrc` no Linux ou `~/.zshrc` no macOS).
  * Recarregar a sessão da *shell* com `source` e validação com abertura de um novo terminal independente.
  * Proteção de ficheiros com segredos contra outros utilizadores com `chmod 600`.
* **Exercício 2: Empacotamento e Cópias de Segurança com `tar`**
  * Criar pasta de projeto de teste `~/IEI/projeto_teste/`.
  * Gerar arquivo `.tar.gz` com `tar -czvf backup_projeto.tar.gz`.
  * Inspecionar o conteúdo sem extrair (`tar -tf`) e descompactar num diretório de teste (`tar -xzvf ... -C /tmp/`).

### Parte II: Engenharia de IA, Contexto e Agentes na CLI
* **Exercício 3: A Primeira Chamada à LLM via `curl`**
  * Obtenção de chave gratuita no Google AI Studio com conta pessoal Google (Gmail).
  * Nota de alerta sobre custos reais de APIs e a importância de *budget alerts* e do Free Tier para aprendizagem.
  * Configuração segura da variável de ambiente `GEMINI_API_KEY` com persistência em `~/.api_keys`.
  * Pedido POST via `curl` com payload JSON e verificação da resposta.
* **Exercício 4: Engenharia de Contexto e Restrições na CLI**
  * Testar prompt vago vs prompt estruturado com delimitação, restrições e few-shot.
  * Forçar a IA a devolver apenas comandos Bash de uma linha sem markdown nem texto para integração direta.
* **Exercício 5: Concluir o Assistente de Terminal (`ask_ai.sh`)**
  * Partir de um esqueleto com validações e formatação JSON seguras, completando a chamada `curl` e canalização para `get_text.py`.
  * Automação da preparação de payloads e integração de utilitários no terminal.
  * Implementação estrita do princípio de *Human-in-the-Loop*: o script **apenas exibe** sugestões e auditorias sem nunca as executar cegamente.
* **Exercício 6: Grounding Arquitetural com `AGENTS.md`**
  * Criar o ficheiro `AGENTS.md` na raiz do projeto com o contexto, convenções e restrições operacionais.
  * Invocação direta e transparente através do assistente (`./ask_ai.sh "Gera script..."`), com deteção automática de `AGENTS.md`.
  * Desafio prático de edição do `AGENTS.md` (adicionando regras personalizadas como restrição a `systemctl` ou logging com timestamp) e validação da alteração comportamental da IA sem alterar o prompt.
* **Exercício 7: Desenhar e Testar uma Skill Modular (`safe-cli`)**
  * Criar o diretório `skills/safe-cli` e o ficheiro `SKILL.md` com o procedimento de classificação de risco para comandos UNIX (Linux e macOS).
  * Testar auditorias de segurança fornecendo a skill como contexto ao assistente (`./ask_ai.sh "comando" skills/safe-cli/SKILL.md`).
  * Discussão crítica sobre o risco da execução cega de ferramentas geradas por IA.
* **Exercício 8 [Desafio de Consolidação]: O Médico do Terminal (`ai_fix.sh`)**
  * Criação da skill modular especializada `skills/error-fix/SKILL.md` para padronizar o diagnóstico em 3 secções ([Causa], [Comando Corrigido] e [Dica]).
  * Partir de um esqueleto em Bash com captura avançada de múltiplos argumentos (`$*`) e canal de erros (`eval "$CMD" 2>&1 || true`), completando a invocação do assistente com a skill.
  * Validação com comandos propositadamente inválidos (`cat` em ficheiros inexistentes, `chmod` com modos inválidos, `tar` com pastas ausentes).

### Exercícios Opcionais de Extensão
* **Exercício 9 [Opcional]: Automação de Cópias com Timestamp (`backup_auto.sh`)**
  * Geração dinâmica de nomes com carimbo temporal (`date +"%Y%m%d_%H%M%S"`).
  * Exclusão de ficheiros temporários (`--exclude="*.tmp"` e `--exclude="*.log"`) com `tar -czf`.
  * Verificação de integridade e sumário estatístico de ficheiros preservados.
* **Exercício 10 [Opcional]: Ponte para Git — Mensagens de Commit com IA (`skills/git-commit`)**
  * Desenho da skill modular `skills/git-commit/SKILL.md` calibrada para a especificação *Conventional Commits* (`feat:`, `fix:`, `docs:`, etc.).
  * Utilitário `ai_commit.sh` para transformar notas de trabalho em mensagens de commit semânticas e estruturadas.
* **Exercício 11 [Opcional]: Painel de Boas-Vindas no Terminal e Atalhos Globais (`welcome.sh`)**
  * Conceito de Message of the Day (MOTD) no ciclo de arranque da shell (`~/.bashrc` ou `~/.zshrc`).
  * Portabilidade estrita POSIX com `printf` para cores ANSI em Linux e macOS.
  * Criação de aliases globais (`ask` e `fix`) para invocação dos assistentes em qualquer diretório.

---

## 6. Recursos & Infraestrutura

1. **Google Gemini API (Free Tier):**
   * Acesso gratuito com conta pessoal Google (Gmail) via [Google AI Studio](https://aistudio.google.com/).
   * Quota generosa (15 RPM), modelo `gemini-3.5-flash-lite` via nova Interactions API sem risco financeiro.
   * Contingência pedagógica para picos de tráfego (`service_unavailable` / 503): fallback imediato via variável `$MODEL` para `gemini-3.8-flash`.
2. **Plataforma Vevox (Consolidação de Conhecimentos):**
   * Banco de 25 questões interativas (`classes/class_02/02_vevox/vevox_pt_00.md` e `vevox_pt_00.csv`).
   * Importação direta de ficheiro CSV com respostas e explicações pedagógicas para dinamização síncrona em aula.

