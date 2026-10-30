---
title: Projetos 01
subtitle: Introdução Engenharia Informática
author: Luis Moutinho, Joaquim Sousa Pinto
institute: Universidade de Aveiro
date: 27 de Outubro de 2026
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
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
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

O repositório deve conter todos os scripts relevantes, ficheiros de configuração, e um `README.md` com instruções sobre como implementar o projeto.
Deve também conter um relatório do projeto em formato `PDF`.

Este é um projeto de três semanas. Têm uma semana para notificar o vosso professor (via e-mail) sobre os membros do vosso grupo, a turma e o tópico escolhido (a lista de tópicos pode ser encontrada [aqui](#tópicos)). Após essa notificação, os docentes atribuirão o respetivo **número de grupo**.

Não se esqueçam de contactar o vosso professor com quaisquer questões.
Instruções adicionais poderão ser adicionadas.

## Tópicos

### 1. Site Estático de Alta Performance com Caching
* **Descrição:** Implementar um serviço web de alta performance utilizando o **Docker Compose**. Esta arquitetura deve orquestrar dois serviços interdependentes numa rede interna: um servidor web de backend (como **NGINX**, **Caddy** ou **Apache `httpd`**) e uma cache de reverse proxy de elevado desempenho à frente (como **Varnish Cache** ou **NGINX** em modo proxy cache). O conteúdo estático do site (uma página rica com estilos CSS, scripts e imagens) deve ser servido a partir de um **volume** montado no contentor do servidor web. Apenas a porta do serviço de cache deve ser exposta para o exterior. Devem ainda realizar testes de carga e desempenho a partir do terminal (utilizando ferramentas como `ab` — Apache Benchmark ou `wrk`), comparando a latência e o débito (*requests/sec*) com e sem cache ativa.
* **Tópicos Principais:** Docker Compose (multi-serviço), servidores web (NGINX/Caddy/Apache), Varnish Cache, redes privadas de contentores, `volumes`, testes de desempenho e latência na CLI (`ab`/`wrk`).

### 2. O Solucionador "Funciona na Minha Máquina": Ambiente de Desenvolvimento em Contentor
* **Descrição:** Criar um ambiente de desenvolvimento hermético e reprodutível baseado em contentores para uma linguagem à escolha (ex: Python, C/C++, Rust ou Node.js), eliminando conflitos de dependências locais.
  1. **Construção do Ambiente:** Criar um `Dockerfile` otimizado com o compilador/interpretador, ferramentas de análise estática (*linters*) e suporte a um utilizador não-root (evitando problemas de permissões de ficheiros gerados no anfitrião).
  2. **Desenvolvimento com Volumes:** Utilizar o Docker Compose e **volumes** (*bind mounts*) para que o código-fonte seja editado na máquina anfitriã, enquanto toda a compilação, execução e testes ocorrem de forma isolada no contentor.
  3. **Automação & Aplicação Exemplo:** Incluir uma pequena aplicação de teste (com funções e respetivos testes unitários) e um script CLI de automação (ou `Makefile`) para compilar, executar os testes e gerar relatórios de linting dentro do contentor com um único comando.
  4. **Integração com IDEs (Opcional / Desafio):** Os grupos podem opcionalmente adotar a especificação aberta de [Development Containers (containers.dev)](https://containers.dev), configurando o ficheiro `.devcontainer/devcontainer.json` para integração automática com o Visual Studio Code.
* **Tópicos Principais:** `Dockerfile`, isolamento de ambientes de desenvolvimento, Docker Compose, `volumes`, gestão de dependências (`apt`), permissões não-root, automação de testes e especificação [containers.dev](https://containers.dev).

### 3. Assistente Desktop Gemini: Aplicação Gráfica com Sandboxing em Flatpak
* **Descrição:** Implementar uma aplicação desktop com interface gráfica (GUI) em Python que permita aos utilizadores interagir com os modelos de linguagem **Google Gemini via API**, empacotando-a e distribuindo-a através de um contentor de aplicação **Flatpak**.
  1. **Interface Gráfica Minimalista:** A aplicação deve disponibilizar uma interface gráfica simples e funcional (desenvolvida com a biblioteca nativa **Tkinter**, sem necessidade de estilos complexos, ou alternativamente com **CustomTkinter**/**PyGObject**): basta um campo de texto para o *prompt*, botão de submissão e área com histórico/apresentação da resposta gerada pelo modelo.
  2. **Consumo de API & Segredos:** A aplicação deve comunicar com a API do Gemini (utilizando cabeçalhos HTTP com a variável de ambiente segura `GEMINI_API_KEY` ou um diálogo de configuração na app), tratando de forma robusta falhas de conectividade e respostas de erro da API.
  3. **Empacotamento Flatpak & Manifesto:** Criar o manifesto Flatpak (`yaml` ou `json`) definindo o runtime/SDK (ex.: `org.gnome.Platform`), os módulos necessários, metadados `.desktop` e ícone da aplicação.
  4. **Auditoria de Permissões no Relatório:** Demonstrar no relatório o isolamento estrito da *sandbox* (bubblewrap) com base no princípio do menor privilégio, documentando o comportamento da app com e sem a permissão de rede (`--share=network`) e confirmando a impossibilidade de aceder a ficheiros confidenciais do anfitrião (ex.: `~/.ssh`).
* **Tópicos Principais:** Interface Gráfica (Python/Tkinter), consumo de APIs REST (Gemini), Contentores de Aplicação (Flatpak), Desktop Sandboxing & Permissões (`finish-args`, `--share=network`, sockets de display), integração no desktop (`.desktop`).

### 4. Plataforma Web com Gestão de Estado e Backups Automatizados
* **Descrição:** Implementar uma plataforma web completa baseada em base de dados (como **WordPress** ou **Ghost CMS**) utilizando o **Docker Compose**. O projeto requer a orquestração segura do contentor da aplicação web e do contentor da base de dados (**MySQL** ou **MariaDB**) numa rede isolada, com persistência total em **volumes**. Para além de configurar e personalizar a plataforma (com publicações iniciais), o grupo deve desenvolver um **script Bash de automação** que execute backups consistentes da base de dados (`mysqldump`) e dos ficheiros carregados, gerando arquivos compactados `.tar.gz` datados com rotação automática (manter os últimos $N$ backups) e um script de restauro (*disaster recovery*).
* **Tópicos Principais:** Docker Compose (multi-serviço), WordPress/Ghost, bases de dados relacionais, redes internas, `volumes`, variáveis de ambiente (`.env`), scripting Bash de backup e restauro (`mysqldump`, `tar`, `cron`).

### 5. Confronto de Performance: Máquina Virtual vs. Contentor
* **Descrição:** Realizar um estudo comparativo rigoroso de desempenho entre virtualização clássica e contentorização. O grupo deve implementar um servidor web **NGINX** idêntico em dois ambientes: 1) dentro de uma **Máquina Virtual Debian** (configurada via VirtualBox ou QEMU) e 2) dentro de um **contentor Docker**. Em seguida, devem executar uma bateria de testes objetivos recolhendo métricas do sistema: tempo de arranque (*boot time* com `systemd-analyze` ou cronómetro), pegada de memória RAM em repouso e sob carga (`free`, `vmstat`, `docker stats`), utilização de espaço em disco (tamanho da imagem de disco `.vdi`/`.qcow2` vs imagem Docker) e tempos de resposta a pedidos HTTP sob carga com ferramentas de benchmark (`ab` ou `wrk`). O relatório deve conter tabelas, gráficos comparativos e uma análise fundamentada dos resultados.
* **Tópicos Principais:** Virtualização de sistemas (VirtualBox/QEMU), Contentores (Docker), monitorização de recursos (`top`, `free`, `df`, `time`), benchmarking de rede (`ab`/`wrk`), análise comparativa de arquiteturas.

### 6. Cockpit de Observabilidade: Monitorização de Contentores com Prometheus & Grafana
* **Descrição:** Implementar uma infraestrutura completa de observabilidade e telemetria de contentores utilizando o **Docker Compose**. A arquitetura deve integrar três serviços orquestrados:
  1. **cAdvisor:** Agente que recolhe telemetria e métricas de utilização de recursos (CPU, RAM, tráfego de rede e I/O de disco) diretamente do daemon do Docker através da montagem do socket `/var/run/docker.sock`.
  2. **Prometheus:** Servidor de base de dados temporal configurado para recolher (*scrape*) periodicamente as métricas disponibilizadas pelo cAdvisor numa rede interna fechada.
  3. **Grafana:** Painel de visualização web conectado ao Prometheus como fonte de dados, sendo o único serviço com porta exposta para o exterior.
  O grupo deve desenhar um *dashboard* interativo no Grafana que apresente a utilização dos contentores do sistema e demonstrar o seu funcionamento prático provocando um pico de consumo de CPU/memória num contentor auxiliar de teste (utilizando ferramentas como `stress` ou `stress-ng`).
* **Tópicos Principais:** Docker Compose (multi-serviço), observabilidade e telemetria (Prometheus, Grafana, cAdvisor), redes de contentores privadas, montagem de sockets do sistema, persistência de métricas em `volumes`, testes de stress.

## Critérios de Avaliação

O projeto será avaliado numa escala de **0 a 20 valores**, distribuídos por cinco vetores fundamentais:

| Vetor de Avaliação | Peso | Cotação | Descrição Principal |
| :------------------------ | :--------: | :---------: | :---------------------------------------------------- |
| **1. Implementação Técnica & Requisitos** | 30% | 6.0 val | Cumprimento rigoroso dos requisitos funcionais do tema, funcionamento correto sem erros, arquitetura modular e boas práticas (Docker/Compose/Flatpak/Bash). |
| **2. Relatório Técnico & Documentação** | 30% | 6.0 val | Clareza, estrutura lógica e fundamentação técnica do relatório em PDF; qualidade das instruções de arranque e replicação no `README.md`. |
| **3. Uso Crítico & Transparente de IA** | 20% | 4.0 val | Engenharia de contexto (ficheiro `AGENTS.md`, *skills*), relevância dos prompts, justificação crítica de aceitação/rejeição e Declaração de IA. |
| **4. Criatividade & Funcionalidades Adicionais** | 10% | 2.0 val | Inovação e extensão além do guião mínimo (funcionalidades extra, resiliência a falhas, polimento visual/UX, automações e scripts complementares). |
| **5. Workflow Colaborativo & Gestão de Projeto** | 10% | 2.0 val | Uso de GitHub Issues/Tarefas, workflow com branches e Pull Requests com revisões cruzadas, histórico de commits atómico e contribuição equilibrada. |

---

### Detalhe dos Vetores de Avaliação

#### 1. Implementação Técnica e Requisitos (6.0 valores)
* O sistema cumpre integralmente todos os requisitos descritos no enunciado do tópico escolhido.
* Ausência de comportamentos anómalos ou dependências quebradas.
* Utilização correta de volumes, redes isoladas, variáveis de ambiente e configurações adequadas de segurança.

#### 2. Relatório Técnico e Reprodutibilidade (6.0 valores)
* O relatório (em formato PDF) deve conter uma estrutura clara:
  * **Introdução & Enquadramento:** Descrição do problema e do objetivo do projeto.
  * **Arquitetura da Solução:** Diagrama conceptual da arquitetura e justificação das decisões técnicas tomadas.
  * **Instruções e Testes:** Demonstração empírica do funcionamento (incluindo capturas de ecrã ou outputs de terminal relevantes).
  * **Dificuldades & Conclusões:** Reflexão honesta sobre obstáculos técnicos superados e lições aprendidas.
* O ficheiro `README.md` no repositório deve ser um guia direto de arranque para que qualquer pessoa (incluindo os avaliadores) consiga clonar o repositório e colocar o projeto a correr com um comando.

#### 3. Uso Crítico e Condicionado de Inteligência Artificial (4.0 valores)


A Inteligência Artificial Generativa (ex: Gemini, ChatGPT, Claude) é permitida como **ferramenta de apoio** à aprendizagem, mas sob regras estritas de transparência, intervenção humana e boas práticas de engenharia:

* **Usos Permitidos:** Apoio no desenho de arquiteturas, auxílio na depuração de erros de sintaxe ou configuração, melhoria de redação no relatório e brainstorming para cenários de teste.
* **Usos Estritamente Proibidos:** Geração em regime *"one-shot"* do projeto completo ou do relatório sem compreensão e validação humana. É expressamente proibida a submissão de código que os membros da equipa não consigam justificar ou explicar detalhadamente.
* **Boas Práticas de Engenharia de Contexto e Agentes:**
  Será positivamente valorizada a aplicação das técnicas introduzidas na **Aula 02**:
  * **Ficheiro `AGENTS.md`:** Criação e manutenção de um ficheiro `AGENTS.md` na raiz do repositório, definindo o contexto do projeto, diretivas de arquitetura, convenções de código e limites de segurança para os assistentes de IA.
  * **Definição de *Skills* e Guardrails:** Criação de *skills* modulares ou regras de execução segura (padrão *safe-cli*) que condicionem as respostas da IA a comandos verificáveis e sem risco para o ambiente.
  * **Engenharia de Prompts Estruturados:** Demonstração de prompts iterativos com contexto delimitado, em oposição a pedidos vagos ou ingénuos.
* **Secção Obrigatória no Relatório ("Declaração de Uso de IA"):**
  O relatório deve conter obrigatoriamente a declaração institucional estruturada com os seguintes campos:
  * **Ferramenta(s) utilizada(s):** Identificação clara das ferramentas e modelos de IA consultados (ex.: Gemini, ChatGPT, Claude, GitHub Copilot).
  * **Tarefas apoiadas:** Discriminação das etapas apoiadas (ex.: depuração de sintaxe no Dockerfile, sugestão de estrutura de testes, revisão gramatical).
  * **Verificação Humana:** Confirmação explícita de que todo o código e texto foram integralmente revistos, testados e validados manualmente pelos estudantes.
  * **Responsabilidade:** Declaração inequívoca de que os membros do grupo assumem a responsabilidade integral pelo conteúdo final e código submetido.
  * **Excertos de Prompts & Reflexão Crítica:** Apresentação dos excertos dos prompts mais relevantes utilizados e fundamentação crítica de por que **aceitaram, adaptaram ou rejeitaram** as sugestões da IA (ex.: *"a IA sugeriu expor a porta 3306 da base de dados, mas rejeitámos para manter a base de dados isolada na rede privada do Docker"*).

#### 4. Criatividade e Funcionalidades Adicionais (2.0 valores)

Este vetor premeia os grupos que vão além dos requisitos mínimos e demonstram autonomia na engenharia:

* **Exemplos de valorização:**
  * Implementação de scripts de teste automático e validação de saúde (*healthchecks*).
  * Mecanismos de segurança adicionais (ex.: restrição estrita de capacidades Linux, utilizadores não-root, encriptação).
  * Melhorias visuais, interfaces mais intuitivas ou polimento superior da experiência do utilizador.
  * Funcionalidades extra relevantes que enriquecem a utilidade real da solução.

#### 5. Workflow Colaborativo, Gestão de Tarefas e Git (2.0 valores)

A colaboração e rastreabilidade são competências essenciais na engenharia de software:

* **Gestão de Tarefas & Issues:** Utilização ativa de **GitHub Issues** (e opcionalmente GitHub Projects/Kanban) para planear, atribuir e acompanhar o progresso das tarefas da equipa.
* **Workflow com Branches e Pull Requests:** O trabalho deve ser desenvolvido em *feature branches* e integrado na `main` através de **Pull Requests** revistos e aprovados por outro elemento da equipa.
* **Rastreabilidade e Divisão de Trabalho:** Associação de commits e PRs aos issues correspondentes (ex.: `closes #3`), com uma distribuição visivelmente equilibrada do esforço entre todos os membros.
* **Higiene do Repositório:** Mensagens de commit atómicas e descritivas (ex.: padrão *Conventional Commits*), uso rigoroso de `.gitignore` e garantia absoluta de que não são versionadas credenciais, ficheiros binários desnecessários ou ficheiros temporários.

## Configuração e Gestão do Repositório no GitHub

Aqui estão instruções detalhadas para configurar o repositório privado da vossa equipa no GitHub.

### 1. Criação do Repositório (Apenas UM elemento do grupo)

Após os docentes confirmarem a equipa e atribuírem o respetivo **número de grupo**:

1. **Aceder ao GitHub:** Iniciar sessão em [github.com](https://github.com) (ou criar uma conta pessoal gratuita se ainda não tiverem).
2. **Criar Novo Repositório:** Clicar no botão **New** (ou no menu `+` no canto superior direito).
3. **Nome do Repositório:** Utilizar obrigatoriamente a seguinte convenção (em minúsculas):
   `iei-2026-p1-[turma]-g[grupo]`
   *(Exemplo para a turma TP1 e grupo 3: `iei-2026-p1-tp01-g03`)*
4. **Visibilidade:** Selecionar obrigatoriamente a opção **Private** (Privado).
5. **Inicialização:** Podem assinalar a criação de um ficheiro `README.md` e selecionar o `.gitignore` adequado (ex.: Python).
6. **Criar:** Clicar em **Create repository**.

-----

### 2. Adicionar Colaboradores (Membros da Equipa e Docentes)

Como o repositório é **privado**, têm de conceder acesso aos restantes colegas do grupo e aos docentes da unidade curricular para efeitos de acompanhamento e avaliação:

1. No repositório criado, aceder ao separador **Settings** (Definições).
2. No menu lateral esquerdo, clicar em **Collaborators**.
3. Clicar no botão verde **Add people**.
4. **Adicionar os colegas de equipa:** Introduzir o nome de utilizador GitHub ou e-mail de cada colega de grupo e enviar o convite com permissões de escrita (*Write*).
5. **Adicionar os docentes:** Introduzir os nomes de utilizador GitHub dos docentes da unidade curricular (indicados nas aulas e no Moodle) e enviar o convite.
6. Todos os convidados devem aceitar o convite recebido por e-mail ou diretamente na sua página inicial do GitHub.

-----

### 3. Configurar uma Chave SSH para Acesso

Isto irá permitir-vos fazer `clone`, `pull` e `push` para o repositório a partir da linha de comandos sem necessidade de introduzir a palavra-passe ou tokens em cada interação.

1. **Verificar se já existe uma chave SSH:**
   Abram o terminal e executem este comando:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Gerar uma nova chave (caso não exista):**

   * Se visualizarem uma chave (iniciada por `ssh-ed25519...`), copiem a linha inteira e saltem para o passo 3.
   * Se visualizarem um erro como "No such file or directory", executem o seguinte comando para gerar uma chave moderna:
     ```bash
     ssh-keygen -q -t ed25519 -N ''
     ```
   * Em seguida, leiam novamente e copiem a nova chave pública:
     ```bash
     cat ~/.ssh/id_ed25519.pub
     ```

3. **Adicionar a chave pública à vossa conta GitHub:**

   * Acedam às definições da vossa conta GitHub (**Settings** no menu do vosso perfil, no canto superior direito).
   * No menu lateral esquerdo, cliquem em **SSH and GPG keys**.
   * Cliquem no botão **New SSH key**.
   * Dêem-lhe um **Title** descritivo (ex.: "Portatil-IEI").
   * Colem a chave pública copiada no campo **Key**.
   * Certifiquem-se de que o campo "Key type" está definido como **Authentication Key**.
   * Cliquem em **Add SSH key**.

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
   [Indicar os sistemas e modelos utilizados, ex.: Gemini 3.5, ChatGPT 4o, Claude 3.5 Sonnet, GitHub Copilot. Caso não tenha existido recurso a ferramentas de IA, preencher explicitamente com "Nenhuma".]

2. **Tarefas apoiadas:**
   [Discriminar detalhadamente onde a IA foi utilizada, ex.: apoio na depuração de sintaxe no Dockerfile, sugestões de casos de teste, revisão gramatical do relatório.]

3. **Verificação Humana:**
   O código, as configurações e o texto submetidos foram integralmente testados, revistos e validados manualmente pelo grupo, garantindo a sua fidelidade aos requisitos técnicos e o seu correto funcionamento.

4. **Responsabilidade e Autoria:**
   Os autores declaram que compreendem e dominam a totalidade da solução apresentada, assumindo a integral responsabilidade académica pelo código e conteúdo do relatório, e que nenhuma componente foi gerada em regime *one-shot* não verificado.