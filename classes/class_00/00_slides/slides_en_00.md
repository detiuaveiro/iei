---
title: 47138 - Introduction to Computer Engineering
subtitle: Course presentation
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

# Course Coordinator

::: columns

:::: column
- **Name:** Luis Moutinho
- **Email:** [lems@ua.pt](mailto:lems@ua.pt)
- **Office:** 04.3.21 (DETI)
::::

:::: column
![](figures/lmoutinho.png)
::::

:::

# Teaching Staff

::: columns

:::: column
- **Name:** Joaquim Sousa Pinto
- **Email:** [jsp@ua.pt](mailto:jsp@ua.pt)
- **Office:** 24.0.05 (IEETA)
::::

:::: column
![](figures/jsp.jpg)
::::

:::

# Course Learning Objectives

Upon completing this course, each student should be able to:

- O1. Understand how to administer **Linux and Windows operating systems** via **command line**.
- O2. Distinguish the use of **virtual machines and containers** to run software in **isolated and organized environments**.
- O3. Understand the necessity of **version control tools and collaborative workflows**.
- O4. Understand the **fundamentals of computer networks** and configure a local area network.

# Course Learning Objectives

- O5. Acquire the skills required to **develop basic web pages** and leverage web technologies to build **simple web applications**.
- O6. Manipulate common data formats and utilize **data analysis tools**.
- O7. Understand the principles of **GDPR, intellectual property, and software licensing** from an ethical and professional standpoint.

# Course Schedule

: \ {#tbl:cal}

| Class | TP1/2 |  TP3  |  TP4  | Topic |            Description             |     Project      |
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----------------------------------|:----------------:|
|   1   | 14/09 | 16/09 | 17/09 |  C0   | Environment setup                  |                  |
|   2   | 21/09 | 23/09 | 24/09 |  C1   | Linux terminal                     |                  |
|   3   | 28/09 | 30/09 | 01/10 |  C1   | Windows terminal (or AI)           |                  |
|   4   | 12/10 | 07/10 | 08/10 |  C2   | Virtualization                     |                  |
|   5   | 19/10 | 14/10 | 15/10 |  C2   | Containers                         |                  |
|   6   | 26/10 | 21/10 | 22/10 |  C2   | Application containers             |                  |
|   7   | 02/11 | 28/10 | 29/10 |  C3   | Git and GitHub                     | **P1** (Start)   |
|   8   | 09/11 | 04/11 | 05/11 |  C4   | Network configuration              |      **P1**      |
|   9   | 16/11 | 11/11 | 12/11 |  C4   | Network programming                |      **P1**      |
|  10   | 23/11 | 18/11 | 19/11 |  C5   | Web pages and publishing           | **P1** (Due)     |
|  11   | 30/11 | 25/11 | 26/11 |  C5   | Web programming                    | **P2** (Start)   |
|  12   | 07/12 | 02/12 | 03/12 |  C6   | Data visualization                 |      **P2**      |
|  13   | 14/12 | 09/12 | 10/12 |  C7   | LaTeX and Markdown                 |      **P2**      |
|  14   | 21/12 | 16/12 | 17/12 |  C8   | GDPR, AI Act & Intellectual Prop.  | **P2** (Due)     |

# Grading & Assessment

Final Grade = 50% Theoretical-Practical Component + 50% Practical Component

- **Minimum grade of 8.0/20 for each component** (passing the course requires a final grade $\ge$ 9.5)

Assessment modalities:

- **Discrete (*default regime*)**: 25% Project 1 + 25% Project 2 + 50% TP Exam
- **Final**: 50% Final Project + 50% TP Exam
  - To opt for final evaluation, notify the head instructor by e-mail by the **end of the 2nd week of classes**.

- TP exams taken during the regular examination period (via Moodle)
- Final project begins in the last class and is due 3 weeks later

# Attendance and Absence Policy

According to the University of Aveiro Assessment Regulations (1st year):

- **Mandatory attendance (Theoretical-Practical classes)**:
  - Attendance control is mandatory for 1st-year undergraduate students.
  - Maximum allowed **unjustified absences: 30%** of delivered classes.
  - Exceeding this limit implies **failure by absence** and loss of access to the normal exam season.

- **Special student statuses**:
  - Students with **Working-Student** status (and other legally recognized statuses) are exempt from mandatory minimum attendance.

- **Justification of absences**:
  - Must be officially submitted via PACO within the regulatory deadline (up to 5 working days).
  - Justified absences in evaluation moments entitle the student to a makeup evaluation.

# Tutorial Orientation (OT)

- **Schedule**: Mondays, **12:00 – 13:00**
- **Room**: Room **4.2.15** (DETI)

- **Purpose and Support**:
  - Guidance and support during the development of **Projects 1 and 2**;
  - Clarification of questions regarding course topics, tools, and the command line;
  - Study support and skill consolidation.

- **Organization**:
  - Weekly session open to students from all class groups;
  - Attendance is optional (no absence tracking), but recommended.

# Artificial Intelligence Usage Policy

1. **Exams and Tests**
   - **No AI usage allowed**: The use of artificial intelligence tools is strictly prohibited in all tests and exams.
   - **Academic fraud**: Unauthorized use of AI constitutes academic fraud and entails associated disciplinary proceedings.

# Artificial Intelligence Usage Policy

2. **Practical Projects (Conditioned Use)**
   - **Full automated resolution prohibited**: AI cannot be used to solve the project/challenge in its entirety.
   - **Authorized support**:
     - *Debugging* and troubleshooting errors;
     - Test generation and execution;
     - Discussion of architecture and supporting technologies;
     - Assistance in report writing (error correction, text polishing, diagrams, and images).
   - **Transparency and critical judgment**: If used in design or code, relevant excerpts must be included in the report, justifying design choices (*accepted because...* / *rejected because...*).

# Bibliography: Core Textbooks

- **William Shotts** (2019). *The Linux Command Line: A Complete Introduction* (2nd ed.). No Starch Press.
- **Scott Chacon & Ben Straub** (2014). *Pro Git* (2nd ed.). Apress / Open Access.
- **James F. Kurose & Keith W. Ross** (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- **Odette Windows** (2023). *Python Networking 101*. GiftforGits.
- **Paul McFedries** (2023). *HTML, CSS, & JavaScript All-in-One For Dummies*. Wiley.
- **Wes McKinney** (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
- **Thomas Mailund** (2019). *Introducing Markdown and Pandoc*. Apress.
- **Leslie Lamport** (1994). *LaTeX: A Document Preparation System* (2nd ed.). Addison-Wesley.

# Bibliography: Official Documentation & Standards

- **Systems & Shell**: *GNU Bash Reference Manual* & *Linux Kernel Man-Pages*
- **Virtualization & Containers**: *Docker Docs*, *Docker Curriculum*, *VirtualBox Manual*, *QEMU Docs*
- **Networking & Sockets**: *Wireshark User's Guide*, *Nmap Book*, *FastAPI Docs*, *Python Socket/AsyncIO*
- **Web Development**: *MDN Web Docs (HTML/CSS/JS)*, *JavaScript.info*, *Nginx Documentation*
- **Data Formats & Wrangling**: *Pandas User Guide*, *Polars*, *Matplotlib*, *Project Jupyter*
- **Technical Documentation**: *Pandoc User's Guide*, *Overleaf Learn*, *The Markdown Guide*
- **Ethics & Regulation**: *General Data Protection Regulation (GDPR)*, *EU AI Act*, *FRA Handbook*

