---
title: 47138 - Introdução à Engenharia Informática
subtitle: Apresentação da unidade curricular
institute: Universidade de Aveiro
date: September 14, 2026
colorlinks: true
highlight-style: tango
mainfont: NotoSans
fontsize: 9pt
titlegraphic: "../../../resources/ua_logo2.png"
titlegraphicoptions: "width=6.5cm"
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
header-includes:
 - \usetheme[sectionpage=none,numbering=fraction,progressbar=none]{metropolis}
 - \definecolor{uagreen}{HTML}{92D400}
 - \setbeamercolor{title separator}{fg=uagreen}
 - \setbeamersize{text margin left=1.5em, text margin right=1.5em}
 - |
    \setbeamertemplate{title graphic}{
      \begin{tikzpicture}[remember picture,overlay]
        \node[anchor=north west, xshift=0cm, yshift=-0cm] at (current page.north west) {
          \inserttitlegraphic
        };
        \node[anchor=south east, xshift=-0.2cm, yshift=0.6cm, opacity=0.08] at (current page.south east) {
          \includegraphics[width=4.8cm]{../../../resources/_deti_black.png}
        };
      \end{tikzpicture}
    }
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Docente Responsável

::: columns

:::: column
- **Nome:** Luis Moutinho
- **E-Mail:** [lems@ua.pt](mailto:lems@ua.pt)
- **Gabinete:** 04.3.21 (DETI)
::::

:::: column
![](figures/lmoutinho.png)
::::

:::

# Docentes

::: columns

:::: column
- **Nome:** Joaquim Sousa Pinto
- **E-Mail:** [jsp@ua.pt](mailto:jsp@ua.pt)
- **Gabinete:** 24.0.05 (IEETA)
::::

:::: column
![](figures/jsp.jpg)
::::

:::

# Objetivos da Unidade Curricular

Após frequência da unidade curricular, cada estudante deverá ser capaz de:

- O1. Compreender como administrar **sistemas operativos Linux** e Windows através de **linha de comandos**.
- O2. Distinguir o uso de **máquinas virtuais e containers** para executar software em **ambientes isolados e organizados**.
- O3. Compreender a necessidade das **ferramentas de versionamento de código e trabalho colaborativo**.
- O4. Compreender os **conceitos básicos de redes** e configurar uma rede local.

# Objetivos da Unidade Curricular

- O5. Adquirir as capacidades necessárias para **desenvolver páginas web básicas** e utilizar tecnologias web para desenvolver **aplicações web simples**.
- O6. Manipular dados em formatos comuns e utilizar **ferramentas para análise de dados**.
- O7. Perceber os princípios do **RGPD, propriedade intelectual e licenciamento de software** do ponto de vista ético e profissional.

# Calendarização

: \ {#tbl:cal}

| Aula | TP1/2 |  TP3  |  TP4  | Tópico |            Descrição             |     Projeto      |
|:----:|:-----:|:-----:|:-----:|:------:|:---------------------------------|:----------------:|
|  1   | 14/09 | 16/09 | 17/09 |   C0   | Preparação de ambiente           |                  |
|  2   | 21/09 | 23/09 | 24/09 |   C1   | Terminal Linux                   |                  |
|  3   | 28/09 | 30/09 | 01/10 |   C1   | Terminal Windows (ou IA)         |                  |
|  4   | 12/10 | 07/10 | 08/10 |   C2   | Virtualização                    |                  |
|  5   | 19/10 | 14/10 | 15/10 |   C2   | Contentores                      |                  |
|  6   | 26/10 | 21/10 | 22/10 |   C2   | Contentores de aplicação         |                  |
|  7   | 02/11 | 28/10 | 29/10 |   C3   | Git e GitHub                     | **P1** (Início)  |
|  8   | 09/11 | 04/11 | 05/11 |   C4   | Configuração de redes            |      **P1**      |
|  9   | 16/11 | 11/11 | 12/11 |   C4   | Programação de redes             |      **P1**      |
|  10  | 23/11 | 18/11 | 19/11 |   C5   | Páginas Web e publicação         | **P1** (Entrega) |
|  11  | 30/11 | 25/11 | 26/11 |   C5   | Programação Web                  | **P2** (Início)  |
|  12  | 07/12 | 02/12 | 03/12 |   C6   | Visualização de dados            |      **P2**      |
|  13  | 14/12 | 09/12 | 10/12 |   C7   | LaTeX e Markdown                 |      **P2**      |
|  14  | 21/12 | 16/12 | 17/12 |   C8   | RGPD, IA Act e Prop. Intelectual | **P2** (Entrega) |

# Avaliação

Nota Final = 50% Componente Teórica-Prática + 50% Componente Prática

- **Nota mínima para cada componente de 8.0 valores** (aprovação à unidade curricular requer nota final $\ge$ 9.5 valores)

Tipos de avaliação:

- **Discreta (*regime por omissão / default*)**: 25% Projeto 1 + 25% Projeto 2 + 50% Exame TP
- **Final**: 50% Projeto Final + 50% Exame TP
  - Para optar por avaliação final, informar o docente responsável por e-mail até ao **final da 2.ª semana de aulas**.

- Exame TP realizado na época normal de exames (via Moodle)
- Projeto final com início na última aula e entrega 3 semanas depois

# Regime de Assiduidade e Faltas

De acordo com o Regulamento de Estudos da Universidade de Aveiro (1.º ano):

- **Presença obrigatória (Aulas Teórico-Práticas)**:
  - O controlo de assiduidade é obrigatório para estudantes do 1.º ano.
  - Limite máximo de **faltas injustificadas: 30%** das aulas lecionadas.
  - Ultrapassar este limite implica **reprovação por faltas** e perda de acesso à época normal.

- **Estatutos especiais**:
  - Estudantes com estatuto de **Trabalhador-Estudante** (e outros legalmente equiparados) estão dispensados do cumprimento do limite de assiduidade mínima.

- **Justificação de faltas**:
  - Devem ser submetidas via PACO no prazo legal (até 5 dias úteis).
  - Faltas justificadas a momentos de avaliação conferem direito a momento de substituição.

# Orientação Tutorial (OT)

- **Horário**: Segunda-feira, **12h00 – 13h00**
- **Local**: Sala **4.2.15** (DETI)

- **Objetivos e Apoio**:
  - Acompanhamento no desenvolvimento dos **Projetos 1 e 2**;
  - Esclarecimento de dúvidas sobre matérias, ferramentas e linha de comandos;
  - Apoio ao estudo e consolidação de competências.

- **Funcionamento**:
  - Sessão semanal aberta a estudantes de todas as turmas;
  - Frequência facultativa (sem marcação de faltas), mas recomendada.

# Política de Uso de Inteligência Artificial

1. **Provas e Exames**
   - **Não utilização de IA**: É estritamente proibido o recurso a ferramentas de inteligência artificial em todas as provas e exames.
   - **Fraude académica**: O uso não autorizado de IA constitui fraude académica e incorre nos respetivos processos disciplinares.

# Política de Uso de Inteligência Artificial

2. **Projetos Práticos (Uso Condicionado)**
   - **Proibida a resolução integral**: A IA não pode ser utilizada para resolver o desafio na totalidade.
   - **Apoio autorizado**:
     - *Debugging* e resolução de erros;
     - Geração e execução de testes;
     - Discussão de arquitetura e tecnologias para a resolução;
     - Apoio na escrita do relatório (correção de erros, polimento do texto, diagramas e imagens).
   - **Transparência e espírito crítico**: Se usada na conceção ou código, incluir excertos no relatório fundamentando opções (*aceitei/recusei porque...*).


# Bibliografia: Livros de Referência

- **William Shotts** (2019). *The Linux Command Line: A Complete Introduction* (2.ª ed.). No Starch Press.
- **Scott Chacon & Ben Straub** (2014). *Pro Git* (2.ª ed.). Apress / Acesso Aberto.
- **James F. Kurose & Keith W. Ross** (2021). *Computer Networking: A Top-Down Approach* (8.ª ed.). Pearson.
- **Odette Windows** (2023). *Python Networking 101*. GiftforGits.
- **Paul McFedries** (2023). *HTML, CSS, & JavaScript All-in-One For Dummies*. Wiley.
- **Wes McKinney** (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.
- **Thomas Mailund** (2019). *Introducing Markdown and Pandoc*. Apress.
- **Leslie Lamport** (1994). *LaTeX: A Document Preparation System* (2.ª ed.). Addison-Wesley.

# Bibliografia: Manuais Técnicos e Documentação Oficial

- **Sistemas & Shell**: *GNU Bash Reference Manual* & *Linux Kernel Man-Pages*
- **Virtualização & Contentores**: *Docker Docs*, *Docker Curriculum*, *VirtualBox Manual*, *QEMU Docs*
- **Redes & Sockets**: *Wireshark User's Guide*, *Nmap Book*, *FastAPI Docs*, *Python Socket/AsyncIO*
- **Desenvolvimento Web**: *MDN Web Docs (HTML/CSS/JS)*, *JavaScript.info*, *Nginx Documentation*
- **Formatos & Análise de Dados**: *Pandas User Guide*, *Polars*, *Matplotlib*, *Project Jupyter*
- **Documentação Técnica**: *Pandoc User's Guide*, *Overleaf Learn*, *The Markdown Guide*
- **Ética & Legislação**: *Regulamento Geral sobre a Proteção de Dados (RGPD)*, *EU AI Act*, *FRA Handbook*

