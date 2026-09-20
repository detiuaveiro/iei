---
title: "47138 - INTRODUÇÃO À ENGENHARIA INFORMÁTICA"
subtitle: "Guião de Unidade Curricular"
author:
  - "Luis Moutinho (Docente Responsável - DETI)"
  - "Joaquim Sousa Pinto (Docente - IEETA)"
institute: "Universidade de Aveiro — Licenciatura em Engenharia Informática"
date: "Ano Letivo 2026/2027"
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2.5cm
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

# Informações Gerais da Unidade Curricular

| Campo | Descrição |
| :--- | :--- |
| **Unidade Curricular** | 47138 – Introdução à Engenharia Informática (IEI) |
| **Curso** | Licenciatura em Engenharia Informática (LEI) – 1.º Ano / 1.º Semestre |
| **Instituição** | Universidade de Aveiro — Departamento de Eletrónica, Telecomunicações e Informática (DETI) |
| **Créditos ECTS** | 6 ECTS (Carga de trabalho total estimada: 168 horas) |
| **Horas de Contacto** | 3 Horas Teórico-Práticas (TP) por semana |
| **Orientação Tutorial (OT)** | 1 Hora por semana (Segunda-feira, 12h00 – 13h00, Gabinete/Sala 4.2.15 DETI) |

### Equipa Docente

* **Luis Moutinho (Docente Responsável / Regente-Coordenador)**
  * **Email:** [lems@ua.pt](mailto:lems@ua.pt)
  * **Gabinete:** 04.3.21 (DETI)
* **Joaquim Sousa Pinto (Docente)**
  * **Email:** [jsp@ua.pt](mailto:jsp@ua.pt)
  * **Gabinete:** 24.0.05 (IEETA)

---

# Índice

1. [Objetivos da Unidade Curricular](#1-objetivos-da-unidade-curricular)
2. [Conteúdos Programáticos e Calendarização](#2-conteúdos-programáticos-e-calendarização)
3. [Métodos de Ensino e Funcionamento das Aulas](#3-métodos-de-ensino-e-funcionamento-das-aulas)
4. [Avaliação e Classificação](#4-avaliação-e-classificação)
5. [Regime de Assiduidade e Faltas](#5-regime-de-assiduidade-e-faltas)
6. [Política de Integridade Académica, Fraude e Uso de Inteligência Artificial](#6-política-de-integridade-académica-fraude-e-uso-de-inteligência-artificial)
7. [Bibliografia e Recursos de Apoio](#7-bibliografia-e-recursos-de-apoio)

---

# 1. Objetivos da Unidade Curricular

A Unidade Curricular de **Introdução à Engenharia Informática (IEI)** tem como propósito fornecer uma visão abrangente, estruturada e eminentemente prática dos pilares tecnológicos fundamentais que sustentam a profissão de Engenheiro de Informática. Numa fase de transição para o ensino superior, a UC desempenha um papel agregador, conferindo aos estudantes autonomia técnica, métodos de resolução de problemas e sentido de boas práticas profissionais.

Ao concluir com aproveitamento a unidade curricular, cada estudante deverá ser capaz de:

* **O1. Linha de Comandos:** Compreender a arquitetura de sistemas operativos e administrar sistemas Linux e Windows através de interface de linha de comandos (CLI).
* **O2. Ambientes Isolados:** Distinguir e aplicar conceitos de virtualização (máquinas virtuais) e contentorização (Docker) para executar software de forma isolada, reprodutível e organizada.
* **O3. Gestão de Código e Colaboração:** Compreender a necessidade de controlo de versões e dominar ferramentas de colaboração em equipa (Git e GitHub).
* **O4. Redes e Comunicação IP:** Compreender os conceitos básicos de redes de computadores, protocolos de comunicação e configurar uma rede local IP.
* **O5. Tecnologias Web:** Desenvolver páginas web bem estruturadas e semânticas (HTML5, CSS3, JavaScript) e publicar aplicações web simples apoiadas em servidores dedicados.
* **O6. Manipulação e Análise de Dados:** Manipular e processar dados em formatos comuns (estruturados e semiestruturados, como CSV e JSON) e utilizar ferramentas e bibliotecas para análise e visualização gráfica.
* **O7. Ética e Legislação:** Compreender os princípios éticos e o quadro legal associado à atividade profissional em TI, nomeadamente o Regulamento Geral sobre a Proteção de Dados (RGPD), o Regulamento Europeu de Inteligência Artificial (AI Act), direitos de autor, propriedade intelectual e licenciamento de software (código aberto vs. proprietário).

---

# 2. Conteúdos Programáticos e Calendarização

Os conteúdos da unidade curricular distribuem-se por 9 módulos temáticos (C0 a C8), articulados temporalmente com o lançamento e acompanhamento de dois projetos práticos de desenvolvimento em equipa.

### Módulos Temáticos

* **C0. Preparação de Ambiente:** Conceitos de sistema operativo e sistema de ficheiros; padronização em Linux; configuração do posto de trabalho digital (Dual-boot, Máquinas Virtuais com VirtualBox/UTM, WSL 2).
* **C1. Linha de Comandos e Terminal:** Filosofia Unix; navegação, gestão de ficheiros e permissões; fluxos de entrada/saída, redirecionamentos e pipes; processos e serviços; introdução à automação com shell scripting (Bash).
* **C2. Virtualização e Contentores:** Hipervisores e máquinas virtuais; contentores de aplicação com Docker (imagens, Dockerfile, volumes e redes); orquestração local com Docker Compose.
* **C3. Controlo de Versões e Colaboração:** Sistemas de controlo de versões distribuídos (Git); ciclo de vida de ficheiros, commits, branches, resolução de conflitos e fluxos de trabalho colaborativos em equipa no GitHub.
* **C4. Redes de Comunicação IP:** Modelo em camadas e pilha TCP/IP; endereçamento IPv4, máscaras e routing local; diagnóstico e configuração de rede (ping, traceroute, netstat, ss, curl); noções de programação de redes (sockets e APIs cliente-servidor).
* **C5. Tecnologias Web e Servidores:** Estrutura e semântica com HTML5; estilização e design responsivo com CSS3; interatividade com JavaScript; publicação de páginas e configuração básica de servidores web (Nginx/Apache).
* **C6. Manipulação e Visualização de Dados:** Formatos de intercâmbio semiestruturados (JSON, CSV, YAML); técnicas de extração, filtragem e agregação de dados; geração de gráficos e dashboards interativos.
* **C7. Compilação de Documentos Técnicos:** Redação técnica e académica estruturada; sintaxe Markdown e sistemas tipográficos com LaTeX e Pandoc; boas práticas de formatação de relatórios de engenharia.
* **C8. RGPD, AI Act, Propriedade Intelectual e Ética:** Quadro europeu de privacidade e proteção de dados pessoais; diretrizes do Regulamento de Inteligência Artificial; regimes de propriedade intelectual e direitos de autor; licenças de software livre (MIT, GPL, Apache) e responsabilidade profissional do engenheiro.

### Calendarização Detalhada das Sessões

A tabela seguinte ilustra o planeamento semanal das 14 aulas teórico-práticas para cada turno e os marcos de avaliação associados:

| Aula | Data TP1/TP2 (2.ª) | Data TP3 (4.ª) | Data TP4 (5.ª) | Módulo | Conteúdo Principal | Marcos de Avaliação |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | 14/09/2026 | 16/09/2026 | 17/09/2026 | C0 | Preparação de ambiente de trabalho | |
| **2** | 21/09/2026 | 23/09/2026 | 24/09/2026 | C1 | Terminal Linux I (Fundamentos e ficheiros) | |
| **3** | 28/09/2026 | 30/09/2026 | 01/10/2026 | C1 | Terminal Linux II (Automação, redes e IA na CLI) | |
| — | *05/10/2026* | — | — | — | *Feriado Nacional (Sem aula TP1/TP2)* | |
| **4** | 12/10/2026 | 07/10/2026 | 08/10/2026 | C2 | Virtualização de sistemas | |
| **5** | 19/10/2026 | 14/10/2026 | 15/10/2026 | C2 | Contentores e tecnologia Docker | |
| **6** | 26/10/2026 | 21/10/2026 | 22/10/2026 | C2 | Contentores de aplicação (Docker Compose) | |
| **7** | 02/11/2026 | 28/10/2026 | 29/10/2026 | C3 | Controlo de versões com Git e GitHub | 🚀 **Lançamento do Projeto 1** |
| **8** | 09/11/2026 | 04/11/2026 | 05/11/2026 | C4 | Configuração de redes locais IP | Acompanhamento do Projeto 1 |
| **9** | 16/11/2026 | 11/11/2026 | 12/11/2026 | C4 | Programação e diagnóstico de redes | Acompanhamento do Projeto 1 |
| **10** | 23/11/2026 | 18/11/2026 | 19/11/2026 | C5 | Páginas Web e publicação em servidores | 📥 **Entrega do Projeto 1** |
| **11** | 30/11/2026 | 25/11/2026 | 26/11/2026 | C5 | Programação Web (HTML, CSS e JavaScript) | 🚀 **Lançamento do Projeto 2** |
| **12** | 07/12/2026 | 02/12/2026 | 03/12/2026 | C6 | Manipulação e visualização de dados | Acompanhamento do Projeto 2 |
| **13** | 14/12/2026 | 09/12/2026 | 10/12/2026 | C7 | Compilação de documentos (LaTeX e Pandoc) | Acompanhamento do Projeto 2 |
| **14** | 21/12/2026 | 16/12/2026 | 17/12/2026 | C8 | RGPD, AI Act, Prop. Intelectual e Síntese | 📥 **Entrega e Defesa do Projeto 2** |

---

# 3. Métodos de Ensino e Funcionamento das Aulas

A unidade curricular adota uma metodologia pedagógica centrada na prática experimental ativa (*learning by doing*), orientada à resolução de problemas e à autonomia técnica:

### Aulas Teórico-Práticas (TP — 3 horas semanais)
As sessões TP decorrem em laboratórios de computadores e integram de forma contínua duas dinâmicas:
1. **Exposição Dialogada e Demonstrações ao Vivo:** Apresentação dos conceitos teóricos essenciais com demonstrações práticas em tempo real pelo docente (*live coding* e execução em terminal).
2. **Trabalho Laboratorial Prático:** Execução supervisionada de guiões de exercícios estruturados pelos estudantes, promovendo o raciocínio crítico, a experimentação e a familiarização com os ambientes de desenvolvimento.

### Orientação Tutorial (OT — 1 hora semanal)
* **Horário e Local:** Segunda-feira, **12h00 – 13h00**, Sala **4.2.15** (DETI).
* **Finalidade:** Espaço aberto e informal dedicado ao esclarecimento de dúvidas, revisão de tópicos de programação e terminal, e acompanhamento próximo e mentoria das equipas no desenvolvimento dos **Projetos 1 e 2**.
* A frequência das sessões de OT é facultativa (sem marcação de faltas), sendo vivamente recomendada para a consolidação de conhecimentos.

---

# 4. Avaliação e Classificação

A avaliação de IEI contempla equilibradamente a aquisição de competências conceptuais e a capacidade de conceção e implementação prática em engenharia:

$$\text{Nota Final (NF)} = 0.50 \times \text{NTP} + 0.50 \times \text{NP}$$

* **$\text{NTP}$:** Nota da Componente Teórico-Prática (Exame escrito individual).
* **$\text{NP}$:** Nota da Componente Prática (Projetos práticos de desenvolvimento).

### 4.1. Regimes de Avaliação

#### A. Avaliação Discreta (Regime Padrão / *Default*)
A avaliação discreta é o regime geral de frequência e decorre ao longo do semestre letivo:

* **Componente Prática ($\text{NP}$ — 50% da Nota Final):**
  * **Projeto 1 (P1) — 25%:** Trabalho em equipa (grupos de 2 a 3 alunos) abordando controlo de versões, virtualização/contentores e redes locais. Desenvolvido ao longo de 3 semanas (lançado na Aula 7 e entregue na Aula 10).
  * **Projeto 2 (P2) — 25%:** Trabalho em equipa abordando desenvolvimento web, manipulação/visualização de dados e documentação técnica. Desenvolvido ao longo de 3 semanas (lançado na Aula 11 e entregue/defendido na Aula 14).
  $$\text{NP} = 0.50 \times P_1 + 0.50 \times P_2$$
* **Componente Teórico-Prática ($\text{NTP}$ — 50% da Nota Final):**
  * Exame individual escrito, realizado em suporte digital via plataforma Moodle na época normal de exames, incidindo sobre todos os tópicos lecionados.

#### B. Avaliação Final
* Destinada a estudantes que optem expressamente por este regime ou a situações regulamentarmente previstas.
* **Constituição:**
  * **50%:** Exame individual teórico-prático escrito na época de exames ($\text{NTP}$).
  * **50%:** Projeto Prático Final Individual, com início na última aula do semestre e prazo de entrega e defesa de 3 semanas.
* **Opção formal:** Os estudantes que pretendam optar pela avaliação final devem comunicar essa decisão por escrito ao docente responsável ([lems@ua.pt](mailto:lems@ua.pt)) até ao **final da 2.ª semana de aulas** do semestre.

### 4.2. Condições de Aprovação e Notas Mínimas
* A aprovação na unidade curricular requer:
  1. **Classificação Final:** $\text{NF} \ge 9.5$ valores (escala de 0 a 20).
  2. **Nota Mínima na Componente Teórico-Prática:** $\text{NTP} \ge 8.0$ valores.
  3. **Nota Mínima na Componente Prática:** $\text{NP} \ge 8.0$ valores.
* A falta a uma prova escrita, a não submissão de um projeto prático nos prazos fixados ou a ausência à sua defesa implica a classificação de **0 (zero) valores** nesse elemento de avaliação.

### 4.3. Época de Recurso
* Na época de recurso mantêm-se os pesos relativos de 50% para a componente teórico-prática e 50% para a componente prática.
* É permitido aos estudantes realizar apenas o exame de recurso da componente teórico-prática, preservando a classificação obtida na componente prática ($\text{NP}$), desde que esta tenha sido $\ge 8.0$ valores.
* A recuperação ou melhoria da componente prática em época de recurso consiste na revisão e defesa de um projeto prático e está condicionada à obtenção prévia de aprovação no exame teórico-prático com nota $\ge 8.0$ valores.

### 4.4. Validade da Nota Prática para Repetentes
Os estudantes que tenham obtido aprovação na componente prática no ano letivo imediatamente anterior com nota igual ou superior a 10.0 valores ($\text{NP} \ge 10.0$) podem requerer a dispensa da frequência das aulas práticas e manter a respetiva classificação. Esta intenção deve ser formalizada por e-mail ao docente responsável durante a primeira semana de aulas. Caso o estudante opte por inscrever-se num grupo e frequentar as aulas práticas, renuncia automaticamente à nota do ano anterior.

---

# 5. Regime de Assiduidade e Faltas

Nos termos do Regulamento de Estudos da Universidade de Aveiro (REUA) para unidades curriculares do 1.º ano de licenciatura:

1. **Presença Obrigatória:**
   * O controlo de assiduidade é obrigatório em todas as turmas Teórico-Práticas (TP).
   * O limite máximo de **faltas injustificadas é de 30%** do número total de aulas lecionadas ao longo do semestre.
   * A ultrapassagem deste limite de faltas determina a **reprovação por faltas** na unidade curricular e a consequente perda de frequência, ficando o estudante impedido de realizar o exame na época normal.
2. **Estatutos Especiais:**
   * Estudantes com estatuto comprovado de Trabalhador-Estudante, atletas de alta competição ou outros regimes legalmente equiparados estão dispensados da obrigatoriedade do limite de assiduidade mínima, devendo acordar com o docente responsável o acompanhamento das entregas e avaliações.
3. **Justificação de Faltas:**
   * Todas as faltas passíveis de justificação devem ser submetidas através do portal PACO dentro do prazo regulamentar estipulado (até 5 dias úteis após a ocorrência do motivo de impedimento).
   * Faltas devidamente comprovadas e justificadas a momentos formais de avaliação conferem o direito à realização de momento de substituição.

---

# 6. Política de Integridade Académica, Fraude e Uso de Inteligência Artificial

A integridade académica e o rigor deontológico são princípios basilares da formação em Engenharia na Universidade de Aveiro.

### 6.1. Colaboração vs. Plágio
* **A cooperação intelectual é encorajada:** Discutir conceitos gerais de arquitetura de software, comandos de terminal e estratégias de resolução com colegas de outras equipas é uma prática recomendada.
* **Limites estritos:** Todo o trabalho submetido para avaliação deve ser da autoria estrita dos elementos do respetivo grupo. É expressamente proibido:
  * Partilhar ficheiros de código-fonte, configurações ou relatórios com outros grupos;
  * Copiar código de colegas ou facultar repositórios próprios;
  * Utilizar soluções desenvolvidas em anos letivos anteriores;
  * Incorporar código de repositórios públicos sem a devida referenciação e autorização.

### 6.2. Política Específica de Uso de Inteligência Artificial (IA)

A introdução de modelos generativos na prática da engenharia requer responsabilidade, espírito crítico e transparência:

1. **Provas Escritas e Exames Individuais:**
   * **Proibição Absoluta:** É estritamente proibida a utilização de quaisquer assistentes, ferramentas de IA ou dispositivos externos. A infração a esta norma constitui fraude académica direta.
2. **Projetos Práticos de Desenvolvimento:**
   * **Proibida a Resolução Integral:** É expressamente proibido recorrer a ferramentas de IA para gerar integralmente o projeto, as suas componentes centrais ou os respetivos relatórios.
   * **Usos Autorizados (Uso Condicionado de Suporte):**
     * Apoio em tarefas de *debugging* e interpretação de erros e *stack traces*;
     * Discussão de alternativas de desenho de arquitetura de software;
     * Auxílio na geração de casos e dados de teste;
     * Revisão linguística, diagramação e apoio estilístico no relatório.
   * **Transparência e Responsabilidade Crítica:**
     * Sempre que for utilizada IA na conceção de código ou documentação, o facto deve ser **explicitamente declarado** no relatório, indicando as ferramentas usadas, os *prompts* fornecidos e uma justificação crítica da solução adotada (*"a sugestão foi aceite após validação porque... / foi corrigida porque apresentava a vulnerabilidade..."*).
     * O grupo é integralmente responsável por qualquer erro, vulnerabilidade ou incorreção no código gerado.

### 6.3. Fiscalização e Sanções Disciplinares
* Todos os projetos e artefactos submetidos são sujeitos a ferramentas automáticas de deteção de similaridade de código e plágio (como o *Moss* e o *Ouriginal*), bem como a comparações com bases de dados de anos anteriores.
* A disponibilização voluntária do trabalho próprio a terceiros é considerada facilitação de fraude, sendo o autor original punido de forma solidária com quem copiou.
* **Consequências:** A verificação de situações de fraude académica ou plágio implica a **atribuição de 0 (zero) valores** a todos os intervenientes no elemento de avaliação em causa e a comunicação à Direção do DETI e Reitoria para abertura do competente **procedimento disciplinar**.

---

# 7. Bibliografia e Recursos de Apoio

A bibliografia e os recursos de apoio da unidade curricular estruturam-se em quatro componentes fundamentais: manuais e livros de texto de referência geral, documentação técnica e manuais oficiais dos ecossistemas abordados nas aulas práticas, folhas de consulta rápida (*cheat sheets*) e simuladores interativos recomendados, e fontes legislativas, éticas e institucionais.

### 7.1. Livros de Texto e Manuais de Referência Recomendados

* **Administração de Sistemas e Linha de Comandos (Módulo C1):**
  * William Shotts, *The Linux Command Line: A Complete Introduction*, 2.ª Edição, No Starch Press, 2019. ISBN: 978-1593279523.
* **Virtualização e Contentores de Software (Módulo C2):**
  * Adrian Mouat, *Using Docker: Developing and Deploying Software with Containers*, O'Reilly Media, 2015. ISBN: 978-1491915714.
* **Controlo de Versões e Trabalho Colaborativo (Módulo C3):**
  * Scott Chacon e Ben Straub, *Pro Git*, 2.ª Edição, Apress, 2014. Disponível gratuitamente em formato de acesso aberto em: [https://git-scm.com/book/](https://git-scm.com/book/).
* **Redes de Computadores e Protocolos de Comunicação (Módulo C4):**
  * James F. Kurose e Keith W. Ross, *Computer Networking: A Top-Down Approach*, 8.ª Edição, Pearson, 2021. ISBN: 978-0136681557.
  * Odette Windows, *Python Networking 101: Navigating Essentials of Networking, Socket Programming, AsyncIO, Network Testing, Simulations and Ansible*, GiftforGits, 2023. ISBN: 978-8196144883.
* **Desenvolvimento Web Frontend, JavaScript e Servidores (Módulo C5):**
  * Paul McFedries, *HTML, CSS, & JavaScript All-in-One For Dummies*, Wiley, 2023. ISBN: 978-1119904250.
  * Ilya Kantor, *The Modern JavaScript Tutorial*, 2024. Disponível online em formato aberto em: [https://javascript.info/](https://javascript.info/).
* **Formatos, Estruturas e Análise de Dados (Módulo C6):**
  * Wes McKinney, *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter*, 3.ª Edição, O'Reilly Media, 2022. ISBN: 978-1098104030.
* **Documentação Técnica, LaTeX e Markdown (Módulo C7):**
  * Thomas Mailund, *Introducing Markdown and Pandoc: Using Markup Language and Document Converter*, Apress, 2019. ISBN: 978-1484251485.
  * Leslie Lamport, *LaTeX: A Document Preparation System*, 2.ª Edição, Addison-Wesley Professional, 1994. ISBN: 978-0201529838.
* **Ética, Proteção de Dados e Legislação Tecnológica (Módulo C8):**
  * European Union Agency for Fundamental Rights (FRA) e Conselho da Europa, *Handbook on European Data Protection Law*, Publications Office of the European Union, Edição de 2018. ISBN: 978-92-9474-001-4.

### 7.2. Documentação Técnica Oficial dos Ecossistemas Tecnológicos

* **Módulo C1 — Terminal, Shell & Bash Scripting:**
  * *GNU Bash Reference Manual:* [https://www.gnu.org/software/bash/manual/](https://www.gnu.org/software/bash/manual/)
  * *The Linux Kernel and System Man-Pages Project (Michael Kerrisk):* [https://man7.org/linux/man-pages/](https://man7.org/linux/man-pages/)
  * *Microsoft PowerShell Documentation:* [https://learn.microsoft.com/powershell/](https://learn.microsoft.com/powershell/)
* **Módulo C2 — Virtualização, Contentorização e Sandboxing:**
  * *Docker Official Documentation & Reference:* [https://docs.docker.com/](https://docs.docker.com/)
  * *Docker Curriculum (Hands-on Container Tutorial):* [https://docker-curriculum.com/](https://docker-curriculum.com/)
  * *Oracle VM VirtualBox User Manual:* [https://www.virtualbox.org/manual/](https://www.virtualbox.org/manual/)
  * *QEMU Documentation & ArchWiki Advanced Networking:* [https://www.qemu.org/docs/](https://www.qemu.org/docs/) e [https://wiki.archlinux.org/title/QEMU](https://wiki.archlinux.org/title/QEMU)
  * *Podman Documentation (Daemonless Container Engine):* [https://podman.io/](https://podman.io/)
  * *AppImage Official Documentation:* [https://docs.appimage.org/](https://docs.appimage.org/)
  * *Flatpak Documentation & Flathub:* [https://docs.flatpak.org/](https://docs.flatpak.org/) e [https://flathub.org/](https://flathub.org/)
  * *Canonical Snapcraft User Guide:* [https://snapcraft.io/docs](https://snapcraft.io/docs)
  * *LinuxServer.io Community Container Hub:* [https://www.linuxserver.io/](https://www.linuxserver.io/)
* **Módulo C3 — Controlo de Versões Distribuído:**
  * *Git Official Documentation & Reference Manual:* [https://git-scm.com/doc](https://git-scm.com/doc)
  * *GitHub Documentation & GitHub Classroom Guides:* [https://docs.github.com/](https://docs.github.com/)
* **Módulo C4 — Redes de Computadores, Sockets e Mensageria:**
  * *Wireshark User's Guide (Protocol Analyzer):* [https://www.wireshark.org/docs/](https://www.wireshark.org/docs/)
  * *Nmap Network Scanning (Gordon Lyon / Fyodor):* [https://nmap.org/book/](https://nmap.org/book/)
  * *Let's Encrypt Documentation & Certbot (TLS/SSL):* [https://letsencrypt.org/docs/](https://letsencrypt.org/docs/)
  * *Python Low-Level Networking (`socket` & `asyncio` modules):* [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html) e [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
  * *FastAPI Interactive Web & API Framework:* [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
  * *MQTT 5.0 Protocol Specification & Eclipse Paho Client:* [https://mqtt.org/](https://mqtt.org/) e [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
  * *RabbitMQ Tutorials & ZeroMQ Guide:* [https://www.rabbitmq.com/tutorials](https://www.rabbitmq.com/tutorials) e [https://zeromq.org/](https://zeromq.org/)
* **Módulo C5 — Desenvolvimento Web, JavaScript e Servidores:**
  * *MDN Web Docs (HTML5, CSS3, DOM & Fetch API):* [https://developer.mozilla.org/](https://developer.mozilla.org/)
  * *W3Schools Online Web Tutorials:* [https://www.w3schools.com/](https://www.w3schools.com/)
  * *Nginx Documentation & Reverse Proxy Configuration:* [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
  * *Philip Roberts, "What the heck is the event loop anyway?" (JSConf):* [https://www.youtube.com/watch?v=8aGhZQkoFbQ](https://www.youtube.com/watch?v=8aGhZQkoFbQ)
  * *Node.js Best Practices Repository:* [https://github.com/goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)
  * *React Official Documentation:* [https://react.dev/](https://react.dev/)
* **Módulo C6 — Formatos, Estruturas e Manipulação de Dados:**
  * *Especificações dos Formatos de Dados:* JSON (RFC 8259), YAML 1.2 ([https://yaml.org/](https://yaml.org/)), XML (W3C Recommendation), CSV (RFC 4180).
  * *Pandas User Guide & API Reference:* [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
  * *Polars User Guide (Fast Multithreaded DataFrames):* [https://pola.rs/](https://pola.rs/)
  * *Matplotlib Visual Anatomy of a Plot & Gallery:* [https://matplotlib.org/](https://matplotlib.org/)
  * *Seaborn Statistical Data Visualization:* [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
  * *Project Jupyter (JupyterLab & Notebooks):* [https://jupyter.org/](https://jupyter.org/)
* **Módulo C7 — Documentação Técnica, LaTeX e Markdown:**
  * *Pandoc User's Guide (Universal Document Converter):* [https://pandoc.org/MANUAL.html](https://pandoc.org/MANUAL.html)
  * *Overleaf Learn (LaTeX Tutorials and Package References):* [https://www.overleaf.com/learn](https://www.overleaf.com/learn)
  * *Comprehensive TeX Archive Network (CTAN):* [https://ctan.org/](https://ctan.org/)
  * *Detexify (LaTeX Handwritten Symbol Recognition):* [https://detexify.kirelabs.org/classify.html](https://detexify.kirelabs.org/classify.html)
  * *GitHub Flavored Markdown (GFM) Specification:* [https://github.github.com/gfm/](https://github.github.com/gfm/)
  * *The Markdown Guide (Syntax and Tools):* [https://www.markdownguide.org/](https://www.markdownguide.org/)
  * *JabRef (BibTeX and BibLaTeX Reference Manager):* [https://www.jabref.org/](https://www.jabref.org/)
* **Módulo C8 — Ética, Proteção de Dados, Licenciamento e IA:**
  * *Open Source Initiative (OSI) — Open Source Licenses:* [https://opensource.org/licenses](https://opensource.org/licenses)
  * *Free Software Foundation (FSF) — GNU Licenses & Philosophy:* [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)

### 7.3. Folhas de Consulta Rápida (*Cheat Sheets*) e Plataformas Interativas

* *GeeksforGeeks Linux Commands Cheat Sheet:* [https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/](https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/)
* *Crontab Guru (Editor e Verificador Visual de Expressões Cron):* [https://crontab.guru/](https://crontab.guru/)
* *Red Hat Bash Shell Cheat Sheet:* [https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet](https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet)
* *Docker Official CLI Cheat Sheet:* [https://docs.docker.com/get-started/docker_cheatsheet.pdf](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
* *Collabnix Ultimate Docker Cheatsheet:* [https://dockerlabs.collabnix.com/docker/cheatsheet/](https://dockerlabs.collabnix.com/docker/cheatsheet/)
* *Learn Git Branching (Simulador Interativo de Grafos Git):* [https://learngitbranching.js.org/](https://learngitbranching.js.org/)
* *Atlassian Git Cheat Sheet:* [https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)
* *StationX Windows CMD & PowerShell Cheat Sheets:* [https://www.stationx.net/windows-command-line-cheat-sheet/](https://www.stationx.net/windows-command-line-cheat-sheet/)

### 7.4. Legislação, Normas e Recursos Institucionais

* *Regulamento Geral sobre a Proteção de Dados (Regulamento UE 2016/679 - RGPD):* [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
* *Regulamento Europeu de Inteligência Artificial (EU AI Act - Regulamento UE 2024/1689):* [https://artificialintelligenceact.eu/](https://artificialintelligenceact.eu/)
* *Comissão Nacional de Proteção de Dados (CNPD — Diretrizes e Notificações):* [https://www.cnpd.pt/](https://www.cnpd.pt/)
* *Gabinete do Encarregado da Proteção de Dados da Universidade de Aveiro (DPO/UA):* [https://www.ua.pt/pt/rgpd](https://www.ua.pt/pt/rgpd)
* *Regulamento de Estudos da Universidade de Aveiro (REUA):* Disponível no portal da Universidade de Aveiro.
* *Plataformas de Apoio Pedagógico da Universidade de Aveiro (PACO e Moodle):* [https://paco.ua.pt/](https://paco.ua.pt/) e [https://moodle.ua.pt/](https://moodle.ua.pt/)
* *Repositório e GitHub Classroom da Unidade Curricular:* [https://github.com/detiuaveiro/iei](https://github.com/detiuaveiro/iei)

