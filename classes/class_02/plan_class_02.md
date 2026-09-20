# Plano de Aula: Class 02 — Linux II: Automação, Filtros de Texto, Redes & IA na CLI

Este documento estabelece o plano pedagógico, curricular e técnico para a substituição do módulo de Terminal Windows por uma segunda sessão aprofundada de **Terminal Linux & Ferramentas Modernas de Engenharia**.

---

## 1. Justificação Curricular & Pedagógica

* **Continuidade Técnica:** A alternância precoce para CMD/PowerShell criava uma quebra na curva de aprendizagem dos caloiros. A consolidação em ambiente POSIX/Linux fornece os alicerces necessários para os módulos seguintes de **Virtualização e Docker (C2)**, **Git e GitHub (C3)**, **Redes IP (C4)** e **Web Servers (C5)**.
* **Alinhamento com a Indústria:** No ecossistema profissional contemporâneo de engenharia informática, o trabalho em Windows é maioritariamente realizado através do **WSL 2** (Linux nativo).
* **Integração de IA como Ferramenta de Engenharia:** Introduzir Inteligência Artificial Generativa através do terminal desmistifica a tecnologia, ensinando os alunos a consumir APIs REST na linha de comandos, a proteger credenciais com variáveis de ambiente e a aplicar engenharia de prompts com sentido crítico.

---

## 2. Objetivos de Aprendizagem

Ao concluir esta sessão, o estudante deverá ser capaz de:
1. **Compreender e gerir variáveis de ambiente:** Diferenciar variáveis locais da shell de variáveis exportadas (`export`), inspecionar o ambiente (`printenv`) e aplicar boas práticas de segurança (armazenamento de chaves de API).
2. **Processar fluxos de texto com utilitários Unix:** Utilizar ferramentas padrão (`wc`, `sort`, `uniq`, `cut`, `tr`, `sed`) para analisar ficheiros estruturados e ficheiros de registo (*logs*).
3. **Gerir arquivos compactados:** Criar e extrair arquivos `.tar.gz` e `.zip` para cópias de segurança e distribuição de código.
4. **Comunicar em rede via consola:** Realizar pedidos HTTP (GET e POST) com o `curl` e inspecionar respostas em formato JSON.
5. **Compreender autenticação criptográfica:** Gerar pares de chaves pública/privada com `ssh-keygen` para preparação do trabalho com Git/GitHub.
6. **Interagir com LLMs a partir da CLI:** Fazer chamadas a APIs de modelos de linguagem (ex: Google Gemini Free Tier ou Groq), estruturar *system prompts* eficazes e desenvolver um pequeno assistente de consola em Bash.

---

## 3. Gestão Temporal (Aula de 3 Horas = 180 min)

* **0h00 – 0h45 (45 min): Bloco Teórico I — Variáveis, Filtros de Texto & Rede**
  * Variáveis de ambiente (`export`, `printenv`, segurança de segredos).
  * O poder dos filtros Unix (`cut`, `sort`, `uniq`, `wc`, introdução ao `sed`).
  * Arquivos com `tar` e comunicação web com `curl`.
  * Autenticação com chaves `ssh-keygen`.
* **0h45 – 0h55 (10 min): Intervalo**
* **0h55 – 1h30 (35 min): Bloco Teórico II — IA Generativa no Terminal & Prompt Engineering**
  * O que é uma API REST de LLM (tokens, mensagens, temperatura).
  * Como passar credenciais em segurança (`$GEMINI_API_KEY`).
  * Consumo via `curl` e envio de payloads JSON.
  * Engenharia de Prompts para desenvolvimento: *zero-shot*, *few-shot*, contexto e prevenção de alucinações (cuidado com comandos destrutivos).
* **1h30 – 2h45 (75 min): Trabalho Prático Orientado**
  * Execução dos exercícios do guião prático.
* **2h45 – 3h00 (15 min): Síntese e Discussão Crítica**
  * Análise das respostas geradas pela IA, verificação de erros e encerramento.

---

## 4. Estrutura Proposta para os Slides (`00_slides/`)

1. **Abertura:** De volta à Shell: Do Básico à Automação e Redes.
2. **Variáveis de Ambiente:** Locais vs. Globais (`export`), herança por processos filhos.
3. **Inspecionar e Limpar o Ambiente:** `printenv`, `env`, `unset`.
4. **Segurança de Segredos:** Por que nunca colocar chaves no código (`.bashrc` e `.env`).
5. **Processamento de Texto Unix (Parte 1):** `wc` (linhas/palavras) e `cut` (extrair colunas de CSV / `/etc/passwd`).
6. **Processamento de Texto Unix (Parte 2):** `sort` (ordenação alfabética/numérica) e `uniq -c` (contagem de frequências).
7. **Manipulação Rápida de Strings:** `tr` e substituição básica com `sed 's/velho/novo/g'`.
8. **Arquivos e Cópias de Segurança:** `tar -czvf` e `tar -xzvf`.
9. **A Rede na Linha de Comandos:** `curl` (pedidos GET e descarregamento de dados).
10. **Autenticação Criptográfica:** Introdução ao SSH e geração de chaves com `ssh-keygen -t ed25519`.
11. **IA no Terminal:** Como os modelos de linguagem funcionam através de APIs REST.
12. **Engenharia de Prompts na Prática:** Instruções de sistema, contexto, restrição de formato de saída (ex: devolver apenas código sem explicações).
13. **Segurança e Espírito Crítico:** Alucinações, verificação de sintaxe e o perigo de executar código gerado sem ler.

---

## 5. Estrutura Proposta para o Guião Prático (`01_exercises/`)

### Parte I: Competências Essenciais (Núcleo da Aula)

* **Exercício 1: Variáveis de Ambiente e Herança**
  * Criar variável local `TESTE="123"` e tentar lê-la num script filho (falha).
  * Promover com `export TESTE="123"` e verificar que o processo filho já a herda.
* **Exercício 2: Análise de Ficheiros com Filtros Unix**
  * Analisar o ficheiro `/etc/passwd`: extrair a 1.ª coluna (utilizadores) e a 7.ª coluna (shells) com `cut -d: -f1,7`.
  * Identificar quantas contas utilizam `/bin/bash` encadeando `cut`, `sort`, `uniq -c` e `sort -nr`.
* **Exercício 3: Compactação e Arquivos com `tar`**
  * Criar pasta com ficheiros de teste e gerar um arquivo compactado: `tar -czvf backup_iei.tar.gz pasta/`.
  * Listar o conteúdo do arquivo sem descompactar (`tar -tf`) e descompactar num diretório temporário.
* **Exercício 4: Pedidos Web com `curl`**
  * Fazer uma consulta simples de meteorologia para o terminal: `curl wttr.in/Aveiro?format=3`.
  * Obter dados em JSON de uma API pública gratuita e visualizar no terminal.
* **Exercício 5: Geração de Chaves SSH**
  * Gerar par de chaves `ed25519` com `ssh-keygen`.
  * Inspecionar a chave pública (`~/.ssh/id_ed25519.pub`) e compreender a diferença entre chave pública e privada.

### Parte II: Integração com IA & Automação

* **Exercício 6: Configuração da Chave de API de IA**
  * Obter chave gratuita no [Google AI Studio](https://aistudio.google.com/) (ou Groq Cloud).
  * Configurar a variável de ambiente: `export GEMINI_API_KEY="AIza..."`.
* **Exercício 7: A Primeira Chamada à LLM via `curl`**
  * Enviar um pedido POST com payload JSON pedindo à IA para explicar um comando Unix complexo.
* **Exercício 8: Engenharia de Prompts na CLI**
  * Ajustar o prompt para pedir comandos com requisitos específicos: "Gera apenas o comando bash de uma linha para encontrar todos os ficheiros .log modificados nas últimas 24 horas, sem texto introdutório nem formatação markdown".
  * Comparar a qualidade da resposta com e sem restrições.
* **Exercício 9 (Desafio): Script Assistente de Terminal (`ask_ai.sh`)**
  * Criar um script Bash simples que recebe os argumentos digitados pelo utilizador (`$@`), constrói o JSON, faz o pedido via `curl` e apresenta a sugestão da IA no terminal.

---

## 6. Recursos & Soluções Técnicas Gratuitas

1. **Google Gemini API (Free Tier):**
   * Acesso gratuito com conta Google / UA.
   * Quota generosa (15 RPM), latência reduzida e excelente desempenho no Gemini 1.5 Flash.
2. **Groq Cloud API (Alternativa Ultra-Rápida):**
   * Gratuito, formato compatível com OpenAI, modelo Llama 3.1 8B.
3. **Plano de Contingência Offline (Sem Internet):**
   * Caso haja restrições na rede do laboratório ou falha de ligação externa, o docente pode disponibilizar um endpoint local com **Ollama** na rede local ou demonstrar com modelo compacto local (`qwen2.5:1.5b`).
