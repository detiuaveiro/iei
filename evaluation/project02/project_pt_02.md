---
title: Projetos 02
subtitle: Introdução à Engenharia Informática
author: Luis Moutinho, Joaquim Sousa Pinto
institute: Universidade de Aveiro
date: 24 de Novembro de 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\small}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Projetos

> ### Regime de Utilização de Inteligência Artificial: IA CONDICIONADA
>
> *Em cumprimento das diretrizes institucionais da Universidade de Aveiro (Referencial para Avaliação das Aprendizagens na Era da Inteligência Artificial):*
>
> * **Desenvolvimento de Software:** Pode utilizar sistemas de IA como apoio técnico para depuração de erros (*debugging*) ou sugestão de código repetitivo. A lógica central e a arquitetura da solução não podem ser geradas por IA (é expressamente proibido o regime *"one-shot"* para a totalidade do projeto).
> * **Relatório de Projeto:** É permitida a utilização de IA exclusivamente para apoio na revisão linguística e melhoria da clareza do texto. A estrutura argumentativa, a interpretação de resultados e as conclusões devem resultar do trabalho intelectual e autoral dos estudantes.
> * **Declaração Obrigatória:** O trabalho deve incluir obrigatoriamente no relatório a correspondente **Declaração de Uso de IA** (ver modelo no [Anexo](#anexo-modelo-da-declaração-de-uso-de-ia)), acompanhada dos excertos dos prompts mais relevantes e da justificação crítica das sugestões aceites ou rejeitadas.

Formem grupos de dois ou três estudantes (excecionalmente, os projetos podem ser feitos individualmente) e selecionem **um** dos seguintes projetos. Todos os projetos serão alojados no **GitHub**, através de um repositório privado criado por cada grupo numa conta pessoal gratuita. Consultem [aqui](#configuração-e-gestão-do-repositório-no-github) os detalhes.

O repositório deve conter todo o código-fonte, scripts relevantes, ficheiros de configuração (`Dockerfile`, `docker-compose.yml`, etc.), um ficheiro de licença *open-source* (`LICENSE`, ex.: MIT) e um `README.md` com instruções claras sobre como colocar o projeto em execução.
Deve também conter o **relatório do projeto em formato `PDF`**, **compilado a partir de Markdown (via Pandoc) ou LaTeX**, incluindo o respetivo código-fonte (`.md`/`.tex`) no repositório.

Este é um projeto de três semanas (com entrega e **apresentação presencial na última aula do semestre**, em dezembro de 2026). Têm uma semana para notificar o vosso professor (via e-mail) sobre os membros do vosso grupo, a turma e o tópico escolhido (a lista de tópicos pode ser encontrada [aqui](#tópicos)). Após essa notificação, os docentes confirmarão o respetivo **número de grupo**.

Não se esqueçam de contactar o vosso professor com quaisquer questões.
Instruções adicionais poderão ser adicionadas.

## Tópicos

### 1. Serviço Web "Markdown to PDF"
* **Descrição:** Implementar uma aplicação web em **Docker Compose** (dois contentores) que permite editar, pré-visualizar e converter documentos Markdown em ficheiros PDF através do navegador.
  1. **Backend de Compilação (Python/FastAPI + Pandoc):** Criar um contentor com Python/FastAPI e **Pandoc** (podendo usar uma imagem base ligeira como `pandoc/latex` ou Pandoc + `weasyprint` para evitar compilações pesadas). A API deve expor um *endpoint* `POST /api/convert` que recebe um ficheiro `.md` (ou texto Markdown), gera o PDF correspondente (guardando-o num **volume**) e devolve o ficheiro para *download* (ou uma mensagem de erro clara caso a conversão falhe).
  2. **Frontend Web (HTML5/CSS3/JS em Nginx):** Criar uma interface web com **editor de texto Markdown com pré-visualização HTML em tempo real** (ex.: recorrendo a uma biblioteca ligeira JS como `marked.js`) e/ou *upload* de ficheiro `.md`, enviando o pedido de conversão via JavaScript (`fetch`) para descarregar o PDF gerado.
  3. **Extensões Opcionais (Criatividade):** Seleção de formato de saída (*Relatório PDF* vs. *Slides Beamer*), lista de histórico de PDFs convertidos ou encaminhamento atrás de um **Reverse Proxy Nginx**.
* **Tópicos Principais:** Docker Compose (multi-serviço), APIs REST (FastAPI + CORS), JavaScript assíncrono (`fetch`, manipulação do DOM), compilação de documentos (Markdown, Pandoc & LaTeX), Nginx e `volumes`.

### 2. Dashboard Interativo de Geo-Dados (Meteorologia, Mobilidade ou Ambiente)
* **Descrição:** Construir um *web dashboard* em **Docker Compose** (dois contentores) para visualização de dados georreferenciados num mapa interativo (ex.: meteorologia, qualidade do ar, estações de bicicletas ou ocorrências de tráfego).
  1. **Backend de Dados (Python/FastAPI + Pandas/Polars):** Desenvolver uma API que lê um *dataset* real em CSV (com coordenadas `lat`/`lon`, ex.: dados abertos de `dados.gov.pt`) ou consulta uma API pública gratuita sem registo complexo (ex.: **Open-Meteo**, com *cache* simples em JSON num **volume**). O serviço deve limpar registos inválidos ou valores em falta e expor os dados em **JSON** num *endpoint* REST (ex.: `GET /api/data`), suportando pelo menos um parâmetro de filtragem (ex.: categoria ou região).
  2. **Frontend Geográfico (HTML5/CSS3/JS + Leaflet em Nginx):** Criar uma interface web que consome a API via `fetch()`, exibe os pontos num mapa interativo **Leaflet** (com marcadores e *popups* informativos) e permite filtrar dinamicamente os marcadores visíveis na página.
  3. **Extensões Opcionais (Criatividade):** Gráfico estatístico complementar (**Matplotlib/Seaborn** ou biblioteca JS), agrupamento de marcadores ou publicação via **Reverse Proxy Nginx**.
* **Tópicos Principais:** Programação Web (HTML5/CSS3/JS, DOM, `fetch`, Leaflet), APIs REST (FastAPI + CORS), limpeza e formatação de dados (CSV/JSON com Pandas/Polars), Nginx e Docker Compose.

### 3. Serviço Web de Análise e Visualização de CSV (*CSV Data Explorer*)
* **Descrição:** Criar uma plataforma web em **Docker Compose** (dois contentores) que permite carregar qualquer ficheiro CSV e visualizar automaticamente estatísticas descritivas e gráficos das suas colunas.
  1. **Backend Analítico (Python/FastAPI + Pandas/Polars + Matplotlib/Seaborn):** Implementar uma API com um *endpoint* `POST /api/upload` que recebe um ficheiro CSV, guarda-o num **volume**/diretório temporário, trata valores em falta e devolve em JSON o resumo estatístico das colunas numéricas (`count`, média, mínimo, máximo) e a lista de colunas disponíveis. Um segundo *endpoint* (ex.: `GET /api/plot/{coluna}`) lê o CSV guardado e gera a imagem PNG do gráfico correspondente.
  2. **Frontend Interativo (HTML5/CSS3/JS em Nginx):** Desenvolver uma página web com formulário de *upload* (`fetch` com `FormData`), tabela dinâmica de resumo estatístico gerada no DOM e botões/seletores para abrir e visualizar o gráfico de cada coluna sem recarregar a página.
  3. **Extensões Opcionais (Criatividade):** Deteção de *outliers* (método **IQR**), matriz de correlação (*heatmap* Seaborn), escolha do tipo de gráfico (histograma vs. *boxplot*) ou **Reverse Proxy Nginx**.
* **Tópicos Principais:** *Uploads* em APIs REST (FastAPI + CORS), análise de dados (Pandas/Polars), visualização (Matplotlib/Seaborn), manipulação dinâmica do DOM (`fetch`), Nginx e Docker Compose.

### 4. Portfólio Dinâmico Full-Stack
* **Descrição:** Construir um site de portfólio pessoal em **Docker Compose** (dois contentores) que separa totalmente o conteúdo da apresentação, simulando um *Micro-CMS* moderno com persistência real.
  1. **Backend REST com Persistência (Python/FastAPI):** Criar uma API que expõe os dados do portfólio em JSON (`GET /api/profile` com nome, biografia, competências e lista de projetos com *tags*), aceita submissões em **`POST /api/contact`** (validando os campos e guardando as mensagens num ficheiro JSON ou SQLite num **volume** Docker) e disponibiliza `GET /api/messages` para verificar as mensagens persistidas durante a demonstração.
  2. **Frontend Semântico & Interativo (HTML5/CSS3/JS em Nginx):** Desenvolver uma página em HTML5 semântico e CSS3 (*Box Model*) que carrega dinamicamente os dados da API via `fetch()`/`async`/`await`, permite **filtrar projetos por categoria/*tag*** no DOM, inclui alternância de tema **Dark/Light** (guardada em `localStorage`) e um formulário de contacto com validação *client-side* e confirmação visual de envio.
  3. **Extensões Opcionais (Criatividade):** Adição/edição dinâmica de projetos via API, painel visual das mensagens submetidas ou exposição atrás de um **Reverse Proxy Nginx**.
* **Tópicos Principais:** JavaScript assíncrono (`fetch`/`async`/`await`, manipulação do DOM, `localStorage`), HTML5 semântico & CSS3, APIs REST com persistência (FastAPI + CORS), Nginx e Docker Compose.

### 5. Estação de Telemetria em Tempo Real (MQTT + WebSockets)
* **Descrição:** Desenvolver uma arquitetura de telemetria em tempo real orientada a eventos em **Docker Compose**, integrando recolha de métricas, protocolo **MQTT** e um *dashboard* web atualizado em direto.
  1. **Broker *Pub/Sub* (Eclipse Mosquitto em Docker):** Configurar o *broker* **Mosquitto** com dois *listeners*: TCP (`1883`) para clientes Python e **WebSockets (`9001`)** para o navegador, utilizando tópicos hierárquicos claros (ex.: `iei/telemetria/sistema`).
  2. **Agente Publicador (Python + `paho-mqtt` + `psutil`):** Implementar um script (a executar na máquina anfitriã ligado a `localhost:1883` ou num contentor dedicado) que recolhe periodicamente métricas reais da máquina (CPU e memória RAM) — ou sensores ambientais simulados — e as publica em **JSON**, incluindo uma mensagem ***Last Will and Testament* (LWT)** para assinalar desconexões abruptas.
  3. **Dashboard Web em Tempo Real (Nginx + HTML5/CSS3/JS):** Criar uma página web que se liga ao *broker* por **WebSockets**, subscreve os tópicos MQTT, atualiza valores no DOM em tempo real e apresenta um alerta visual quando um limiar é excedido (ex.: CPU/RAM $> 80\%$) ou quando chega um evento LWT.
  4. **Extensões Opcionais (Criatividade):** Subscritor Python que grava histórico em CSV num volume e gera gráficos de tendência com Pandas/Matplotlib.
* **Tópicos Principais:** *Publish/Subscribe* & MQTT (Mosquitto, tópicos, QoS, LWT), WebSockets no navegador, manipulação dinâmica do DOM, telemetria (`psutil`), Nginx e Docker Compose.

## Critérios de Avaliação

O projeto será avaliado numa escala de **0 a 20 valores**, distribuídos por seis vetores fundamentais:

| Vetor de Avaliação | Peso | Cotação | Descrição Principal |
| :------------------------ | :--------: | :---------: | :---------------------------------------------------- |
| **1. Implementação Técnica & Requisitos** | 30% | 6.0 val | Cumprimento rigoroso dos requisitos funcionais do tema, arquitetura multi-serviço sem erros, boas práticas de rede/configuração (Nginx, FastAPI, MQTT, Docker). |
| **2. Relatório Técnico (Markdown/LaTeX) & Documentação** | 15% | 3.0 val | Relatório conciso em PDF compilado a partir de Markdown/LaTeX (com fonte no repo), arquitetura, testes/resultados, ficheiro `LICENSE` e `README.md` reprodutível. |
| **3. Apresentação & Demonstração do Projeto** | 15% | 3.0 val | Apresentação oral e demonstração funcional ao vivo na última aula do semestre; clareza da exposição, gestão do tempo e domínio técnico individual nas perguntas. |
| **4. Uso Crítico & Transparente de IA** | 20% | 4.0 val | Engenharia de contexto (`AGENTS.md`, *skills*), relevância dos prompts, justificação crítica de aceitação/rejeição e Declaração de IA. |
| **5. Criatividade & Funcionalidades Adicionais** | 10% | 2.0 val | Inovação além do mínimo (ex.: extensões opcionais sugeridas, Reverse Proxy, testes automatizados, responsividade móvel ou polimento UX/UI). |
| **6. Workflow Colaborativo & Gestão de Projeto** | 10% | 2.0 val | Uso de GitHub Issues/Tarefas, workflow com *branches* e Pull Requests com revisões cruzadas, histórico de commits atómico e contribuição equilibrada. |

---

### Detalhe dos Vetores de Avaliação

#### 1. Implementação Técnica e Requisitos (6.0 valores)
* O sistema cumpre integralmente os requisitos base descritos no enunciado do tópico escolhido.
* Ausência de erros de execução, bloqueios de CORS não tratados ou dependências quebradas.
* Utilização correta de Docker Compose, `volumes`, variáveis de ambiente e configuração limpa dos serviços.

#### 2. Relatório Técnico (Markdown/LaTeX) e Reprodutibilidade (3.0 valores)
* O relatório (em formato **PDF**, **compilado a partir de Markdown com Pandoc ou LaTeX**, com os ficheiros fonte versionados no repositório) deve ser **conciso e estruturado (sugestão: 4 a 6 páginas, sem anexos)**:
  * **Introdução & Enquadramento:** Descrição do problema, objetivos e tecnologias utilizadas.
  * **Arquitetura da Solução:** Diagrama conceptual (contentores, portas, fluxos HTTP/MQTT e volumes) e justificação das decisões técnicas.
  * **Testes & Resultados:** Demonstração empírica do funcionamento (capturas de ecrã, exemplos de respostas JSON/gráficos obtidos).
  * **Dificuldades & Conclusões:** Reflexão honesta sobre obstáculos técnicos superados e lições aprendidas.
* O ficheiro `README.md` na raiz do repositório deve permitir a qualquer avaliador clonar o projeto e colocá-lo em funcionamento com instruções diretas e reprodutíveis, acompanhado de um ficheiro `LICENSE`.

#### 3. Apresentação e Demonstração do Projeto (3.0 valores)
* Realizada obrigatoriamente na **última aula do semestre** por todos os membros do grupo:
  * **Exposição & Suporte Visual:** Apresentação clara, objetiva e estruturada do problema, da arquitetura implementada e dos principais resultados (com gestão rigorosa do tempo atribuído).
  * **Demonstração Funcional ao Vivo:** Execução prática da solução (em contentores Docker) evidenciando o funcionamento dos requisitos principais e a resposta do sistema a casos de teste.
  * **Domínio Técnico & Discussão (Perguntas):** Capacidade de cada membro do grupo explicar as escolhas arquiteturais, o código submetido e responder criticamente às questões colocadas pelos docentes.

#### 4. Uso Crítico e Condicionado de Inteligência Artificial (4.0 valores)

A Inteligência Artificial Generativa (ex.: Gemini, ChatGPT, Claude) é permitida como **ferramenta de apoio** à aprendizagem, sob regras estritas de transparência, intervenção humana e boas práticas de engenharia:

* **Usos Permitidos:** Apoio no desenho de arquiteturas, auxílio na depuração de erros de sintaxe ou configuração (Nginx, FastAPI, CORS, JS, LaTeX), melhoria de redação no relatório e *brainstorming* para casos de teste.
* **Usos Estritamente Proibidos:** Geração em regime *"one-shot"* do projeto completo ou do relatório sem compreensão e validação humana. É expressamente proibida a submissão de código que os membros da equipa não consigam justificar ou explicar detalhadamente.
* **Boas Práticas de Engenharia de Contexto e Agentes:**
  Será positivamente valorizada a continuidade e evolução das técnicas introduzidas na **Aula 02**:
  * **Ficheiro `AGENTS.md`:** Criação e manutenção de um ficheiro `AGENTS.md` na raiz do repositório definindo o contexto do projeto, convenções de código, arquitetura e limites de segurança.
  * **Definição de *Skills* e Guardrails:** Regras modulares que condicionem as sugestões da IA a comandos verificáveis e seguros.
  * **Engenharia de Prompts Estruturados:** Demonstração de prompts iterativos com contexto delimitado, em oposição a pedidos vagos ou ingénuos.
* **Secção Obrigatória no Relatório ("Declaração de Uso de IA"):**
  O relatório deve conter obrigatoriamente a declaração institucional estruturada (ver [Anexo](#anexo-modelo-da-declaração-de-uso-de-ia)), acompanhada dos excertos dos prompts mais relevantes e da fundamentação crítica de por que **aceitaram, adaptaram ou rejeitaram** as sugestões da IA (ex.: *"a IA sugeriu configurar `Access-Control-Allow-Origin: *` no FastAPI, mas restringimos à origem do nosso frontend em `localhost:8080`"*).

#### 5. Criatividade e Funcionalidades Adicionais (2.0 valores)

Este vetor premeia os grupos que vão além dos requisitos mínimos e demonstram autonomia técnica:

* **Exemplos de valorização:**
  * Implementação das **extensões opcionais** indicadas no tópico escolhido (ex.: **Reverse Proxy Nginx** a unificar `/` e `/api/`, deteção de *outliers* IQR, *heatmap* de correlação ou histórico persistente).
  * Testes automatizados de API (ex.: `pytest` / scripts `curl`) e *healthchecks* no `docker-compose.yml`.
  * Polimento visual superior, acessibilidade (*a11y*) e design responsivo para dispositivos móveis.
  * Automação da compilação do relatório (ex.: `Makefile` ou *GitHub Actions* para gerar o PDF).

#### 6. Workflow Colaborativo, Gestão de Tarefas e Git (2.0 valores)

* **Gestão de Tarefas & Issues:** Utilização ativa de **GitHub Issues** (e opcionalmente GitHub Projects/Kanban) para planear, atribuir e acompanhar o progresso da equipa.
* **Workflow com Branches e Pull Requests:** Desenvolvimento em *feature branches* e integração na `main` através de **Pull Requests** revistos e aprovados por outro membro da equipa.
* **Rastreabilidade e Divisão de Trabalho:** Associação de commits e PRs aos issues correspondentes (ex.: `closes #4`), com contribuição equilibrada entre todos os elementos.
* **Higiene do Repositório:** Mensagens de commit atómicas e descritivas (ex.: *Conventional Commits*), `.gitignore` rigoroso (sem `node_modules`, `__pycache__`, `.venv`, credenciais ou ficheiros temporários) e presença do ficheiro `LICENSE`.

## Configuração e Gestão do Repositório no GitHub

Aqui estão as instruções para configurar o repositório privado da vossa equipa no GitHub para o Projeto 02.

### 1. Criação do Repositório (Apenas UM elemento do grupo)

Após os docentes confirmarem a equipa e o respetivo **número de grupo**:

1. **Aceder ao GitHub:** Iniciar sessão em [github.com](https://github.com).
2. **Criar Novo Repositório:** Clicar no botão **New** (ou no menu `+` no canto superior direito).
3. **Nome do Repositório:** Utilizar obrigatoriamente a seguinte convenção (em minúsculas):
   `iei-2026-p2-[turma]-g[grupo]`
   *(Exemplo para a turma TP1 e grupo 3: `iei-2026-p2-tp01-g03`)*
4. **Visibilidade:** Selecionar obrigatoriamente a opção **Private** (Privado).
5. **Inicialização:** Podem assinalar a criação de `README.md`, selecionar o `.gitignore` adequado (ex.: Python) e escolher uma licença *open-source* (`LICENSE`, ex.: MIT License).
6. **Criar:** Clicar em **Create repository**.

-----

### 2. Adicionar Colaboradores (Membros da Equipa e Docentes)

Como o repositório é **privado**, têm de conceder acesso aos restantes colegas do grupo e aos docentes da unidade curricular para efeitos de acompanhamento e avaliação:

1. No repositório criado, aceder ao separador **Settings** (Definições).
2. No menu lateral esquerdo, clicar em **Collaborators**.
3. Clicar no botão verde **Add people**.
4. **Adicionar os colegas de equipa:** Introduzir o nome de utilizador GitHub ou e-mail de cada colega de grupo e enviar o convite com permissões de escrita (*Write*).
5. **Adicionar os docentes:** Introduzir os nomes de utilizador GitHub dos docentes da unidade curricular (indicados nas aulas e no Moodle) e enviar o convite.
6. Todos os convidados devem aceitar o convite recebido por e-mail ou diretamente na página inicial do GitHub.

-----

### 3. Chave SSH para Acesso (Caso ainda não configurada no Projeto 01)

Caso já tenham configurado a chave SSH na vossa conta GitHub durante o Projeto 01, podem avançar diretamente para o `git clone`. Caso contrário:

1. **Verificar ou gerar uma chave SSH:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Se o ficheiro não existir, gerem uma nova chave e leiam a chave pública gerada:
   ```bash
   ssh-keygen -q -t ed25519 -N ''
   cat ~/.ssh/id_ed25519.pub
   ```
2. **Adicionar à conta GitHub:** Acedam a **Settings $\rightarrow$ SSH and GPG keys $\rightarrow$ New SSH key**, atribuam um título descritivo (ex.: `Portatil-IEI`), colem a chave pública com o tipo **Authentication Key** e cliquem em **Add SSH key**.

-----

## Anexo: Modelo da Declaração de Uso de IA

*(Este modelo deve ser preenchido com a identificação de todos os elementos do grupo e integrado obrigatoriamente no Relatório do Projeto em PDF. A inclusão dos nomes e números mecanográficos constitui a subscrição formal do compromisso de integridade académica pelo grupo, não sendo necessária assinatura manuscrita ou digital).*

---

### Declaração de Uso de Inteligência Artificial

* **Turma:** [ex.: TP01] | **Grupo:** [ex.: g03]
* **Membros do Grupo:**
  * [Nome do Estudante 1] (NMec: [Número])
  * [Nome do Estudante 2] (NMec: [Número])
  * [Nome do Estudante 3] (NMec: [Número])

1. **Ferramenta(s) utilizada(s):**
   [Indicar os sistemas e modelos utilizados, ex.: Gemini, ChatGPT, Claude, GitHub Copilot. Caso não tenha existido recurso a ferramentas de IA, preencher explicitamente com "Nenhuma".]

2. **Tarefas apoiadas:**
   [Discriminar detalhadamente onde a IA foi utilizada, ex.: apoio na depuração de regras no `nginx.conf`, sugestões de casos de teste na API FastAPI, revisão gramatical do relatório.]

3. **Verificação Humana:**
   O código, as configurações, as análises de dados e o texto submetidos foram integralmente testados, revistos e validados manualmente pelo grupo, garantindo a sua fidelidade aos requisitos técnicos e o seu correto funcionamento.

4. **Responsabilidade e Autoria:**
   Os autores declaram que compreendem e dominam a totalidade da solução apresentada, assumindo a integral responsabilidade académica pelo código e conteúdo do relatório, e que nenhuma componente foi gerada em regime *one-shot* não verificado.
