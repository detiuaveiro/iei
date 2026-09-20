---
title: "47138 - INTRODUCTION TO COMPUTER ENGINEERING"
subtitle: "Course Syllabus & Policy Guide"
author:
  - "Luis Moutinho (Course Coordinator - DETI)"
  - "Joaquim Sousa Pinto (Instructor - IEETA)"
institute: "Universidade de Aveiro — Bachelor in Computer Science & Engineering"
date: "Academic Year 2026/2027"
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

# Course Overview & General Information

| Field | Details |
| :--- | :--- |
| **Course Unit** | 47138 – Introduction to Computer Engineering (IEI) |
| **Degree Program** | Bachelor in Computer Science and Engineering (LEI) – 1st Year / 1st Semester |
| **Institution** | Universidade de Aveiro — Department of Electronics, Telecommunications and Informatics (DETI) |
| **ECTS Credits** | 6 ECTS (Total estimated workload: 168 hours) |
| **Contact Hours** | 3 Theoretical-Practical (TP) hours per week |
| **Tutorial Orientation (OT)** | 1 hour per week (Monday, 12:00 – 13:00, Office/Room 4.2.15 DETI) |

### Teaching Staff

* **Luis Moutinho (Course Coordinator)**
  * **Email:** [lems@ua.pt](mailto:lems@ua.pt)
  * **Office:** 04.3.21 (DETI)
* **Joaquim Sousa Pinto (Instructor)**
  * **Email:** [jsp@ua.pt](mailto:jsp@ua.pt)
  * **Office:** 24.0.05 (IEETA)

---

# Table of Contents

1. [Course Objectives](#1-course-objectives)
2. [Syllabus Topics & Semester Schedule](#2-syllabus-topics--semester-schedule)
3. [Teaching Methodology & Class Dynamics](#3-teaching-methodology--class-dynamics)
4. [Grading Policy & Evaluation Regimes](#4-grading-policy--evaluation-regimes)
5. [Attendance Policy](#5-attendance-policy)
6. [Academic Integrity, Anti-Fraud & Generative AI Policy](#6-academic-integrity-anti-fraud--generative-ai-policy)
7. [Bibliography & Reference Material](#7-bibliography--reference-material)

---

# 1. Course Objectives

The **Introduction to Computer Engineering (IEI)** course provides a structured, hands-on introduction to the core technological foundations, workflows, and professional practices required for modern software and systems engineering. Serving as an anchoring first-semester course, it equips students with technical autonomy, command-line literacy, problem-solving skills, and ethical awareness.

Upon completing this course, each student should be able to:

* **O1. Command Line Administration:** Understand operating system fundamentals and administer Linux and Windows environments via the command-line interface (CLI).
* **O2. Isolated Environments:** Differentiate and apply virtualization (virtual machines) and containerization (Docker) to run software in isolated, reproducible environments.
* **O3. Version Control & Collaboration:** Grasp the necessity of version control and collaborate effectively using Git and GitHub.
* **O4. IP Networking:** Understand the principles of computer networks and protocols, configuring and diagnosing local IP networks.
* **O5. Web Technologies:** Build clean, semantic web pages (HTML5, CSS3, JavaScript) and deploy web applications backed by servers.
* **O6. Data Manipulation & Visualization:** Process structured and semi-structured datasets (JSON, CSV) and generate analytical and graphical representations.
* **O7. Ethics & Legal Frameworks:** Comprehend ethical responsibilities and legal regulations in IT, including GDPR, the European AI Act, intellectual property rights, and software licensing models (open-source vs. proprietary).

---

# 2. Syllabus Topics & Semester Schedule

The course is structured around 9 modular topics (C0 to C8), tightly aligned with two collaborative practical development projects.

### Modular Topics

* **C0. Environment Setup:** Operating systems and filesystems; standardizing on Linux; setting up development environments (Dual-boot, Virtual Machines with VirtualBox/UTM, WSL 2).
* **C1. Command Line & Shell:** Unix philosophy; navigation, file management, and permissions; streams, redirections, and pipes; process management; shell scripting with Bash.
* **C2. Virtualization & Containers:** Hypervisors and virtual machines; application containerization using Docker (images, Dockerfile, volumes, and networking); local orchestration with Docker Compose.
* **C3. Version Control & Collaboration:** Distributed version control with Git; file lifecycles, commits, branches, merge conflicts, and team collaboration workflows on GitHub.
* **C4. IP Network Communication:** Layered architecture and the TCP/IP stack; IPv4 addressing, subnets, and local routing; diagnostics and tools (ping, traceroute, netstat, ss, curl); socket programming basics.
* **C5. Web Technologies & Web Servers:** Semantic HTML5 markup; responsive styling with CSS3; client-side interactivity with JavaScript; deploying applications with web servers (Nginx/Apache).
* **C6. Semi-structured Data Manipulation:** Working with JSON, CSV, and YAML; data filtering, extraction, and aggregation; interactive visualizations.
* **C7. Technical Document Compilation:** Structured technical documentation; Markdown syntax, LaTeX, and Pandoc toolchains; engineering report formatting best practices.
* **C8. GDPR, AI Act, Intellectual Property & Ethics:** European privacy and personal data protection regulations; AI Act compliance guidelines; intellectual property and copyright; open-source licensing (MIT, GPL, Apache); engineering professional ethics.

### Weekly Schedule & Milestones

The table below outlines the 14-week schedule across laboratory groups and assessment milestones:

| Week | Date TP1/TP2 (Mon) | Date TP3 (Wed) | Date TP4 (Thu) | Topic | Main Content | Milestones |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | 14/09/2026 | 16/09/2026 | 17/09/2026 | C0 | Digital Workspace & Setup | |
| **2** | 21/09/2026 | 23/09/2026 | 24/09/2026 | C1 | Linux Terminal I (Core commands & filesystem) | |
| **3** | 28/09/2026 | 30/09/2026 | 01/10/2026 | C1 | Linux Terminal II (Automation, networks & AI CLI) | |
| — | *05/10/2026* | — | — | — | *National Holiday (No TP1/TP2 class)* | |
| **4** | 12/10/2026 | 07/10/2026 | 08/10/2026 | C2 | System Virtualization | |
| **5** | 19/10/2026 | 14/10/2026 | 15/10/2026 | C2 | Application Containers (Docker) | |
| **6** | 26/10/2026 | 21/10/2026 | 22/10/2026 | C2 | Multi-Container Systems (Docker Compose) | |
| **7** | 02/11/2026 | 28/10/2026 | 29/10/2026 | C3 | Version Control with Git & GitHub | 🚀 **Project 1 Kickoff** |
| **8** | 09/11/2026 | 04/11/2026 | 05/11/2026 | C4 | IP Local Network Configuration | Project 1 Mentoring |
| **9** | 16/11/2026 | 11/11/2026 | 12/11/2026 | C4 | Network Programming & Diagnostics | Project 1 Mentoring |
| **10** | 23/11/2026 | 18/11/2026 | 19/11/2026 | C5 | Web Pages & Server Deployment | 📥 **Project 1 Due** |
| **11** | 30/11/2026 | 25/11/2026 | 26/11/2026 | C5 | Web Programming (HTML, CSS & JS) | 🚀 **Project 2 Kickoff** |
| **12** | 07/12/2026 | 02/12/2026 | 03/12/2026 | C6 | Data Processing & Visualization | Project 2 Mentoring |
| **13** | 14/12/2026 | 09/12/2026 | 10/12/2026 | C7 | Document Compilation (LaTeX & Pandoc) | Project 2 Mentoring |
| **14** | 21/12/2026 | 16/12/2026 | 17/12/2026 | C8 | GDPR, AI Act, IP & Course Wrap-up | 📥 **Project 2 Due & Defense** |

---

# 3. Teaching Methodology & Class Dynamics

The course follows an active, practical learning methodology (*learning by doing*), focusing on problem-solving, autonomy, and engineering rigor:

### Theoretical-Practical Classes (TP — 3 hours/week)
Classes take place in computer laboratories, integrating two complementary phases:
1. **Interactive Presentations & Live Demos:** Clear exposition of core concepts followed by real-time demonstrations by the instructor.
2. **Supervised Lab Work:** Hands-on completion of step-by-step lab exercise guides, allowing students to experiment, debug, and consolidate concepts on personal laptops or lab workstations.

### Tutorial Orientation (OT — 1 hour/week)
* **Schedule & Room:** Monday, **12:00 – 13:00**, Room **4.2.15** (DETI).
* **Purpose:** Open drop-in office hours for personalized mentoring on **Projects 1 and 2**, troubleshooting technical blockers, and clearing doubts. Attendance is optional but strongly recommended.

---

# 4. Grading Policy & Evaluation Regimes

Final assessment weights conceptual understanding and practical implementation equally:

$$\text{Final Grade (NF)} = 0.50 \times \text{NTP} + 0.50 \times \text{NP}$$

* **$\text{NTP}$:** Theoretical-Practical Component Grade (Written exam).
* **$\text{NP}$:** Practical Component Grade (Development projects).

### 4.1. Evaluation Regimes

#### A. Discrete Evaluation (Default Regime)
* **Practical Component ($\text{NP}$ — 50% of Final Grade):**
  * **Project 1 (P1) — 25%:** Team project (2 to 3 students) covering version control, virtualization/containers, and local networking. Duration: 3 weeks (Weeks 7 to 10).
  * **Project 2 (P2) — 25%:** Team project covering web development, data processing/visualization, and technical documentation. Duration: 3 weeks (Weeks 11 to 14).
  $$\text{NP} = 0.50 \times P_1 + 0.50 \times P_2$$
* **Theoretical-Practical Component ($\text{NTP}$ — 50% of Final Grade):**
  * Individual written exam held during the regular exam period on the Moodle platform, covering all course syllabus topics.

#### B. Final Evaluation Regime
* Available for eligible students who explicitly request this option.
* **Composition:**
  * **50%:** Written Theoretical-Practical exam during the exam period ($\text{NTP}$).
  * **50%:** Comprehensive Individual Practical Project, assigned in the final week of classes with a 3-week completion and defense deadline.
* **Formal Notification:** Students wishing to switch to the final evaluation regime must notify the course coordinator ([lems@ua.pt](mailto:lems@ua.pt)) by email no later than the **end of the 2nd week of classes**.

### 4.2. Passing Conditions & Minimum Grades
* To pass the course unit, a student must meet the following criteria:
  1. **Final Grade:** $\text{NF} \ge 9.5$ on a 0–20 scale.
  2. **Minimum Theoretical-Practical Grade:** $\text{NTP} \ge 8.0$ out of 20.
  3. **Minimum Practical Grade:** $\text{NP} \ge 8.0$ out of 20.
* Unjustified absence from an exam, failure to submit a project by the deadline, or missing a project defense results in a grade of **0 (zero)** for that component.

### 4.3. Second-Chance Exam Period (Época de Recurso)
* Weights remain 50% NTP and 50% NP.
* Students with a passing practical grade ($\text{NP} \ge 8.0$) may retake only the theoretical-practical exam.
* Recovering or improving the practical grade during this period involves revising and defending a practical project, conditional on obtaining an exam grade $\text{NTP} \ge 8.0$.

### 4.4. Practical Grade Validity for Repeating Students
Students who passed the practical component in the immediately preceding academic year ($\text{NP} \ge 10.0$) may request exemption from lab sessions while keeping their previous practical grade. Requests must be sent to the course coordinator during the first week of classes. Enrolling in a lab team and submitting project work automatically voids the previous grade.

---

# 5. Attendance Policy

In compliance with the Universidade de Aveiro Academic Regulations (REUA) for 1st-year undergraduate courses:

1. **Mandatory Attendance:**
   * Attendance is recorded in all Theoretical-Practical (TP) classes.
   * The maximum allowable limit of **unjustified absences is 30%** of total scheduled classes.
   * Exceeding this limit results in **failure due to absences** (*reprovação por faltas*), forfeiting access to the regular exam period.
2. **Special Student Statuses:**
   * Working students (*Trabalhador-Estudante*) and students with legally recognized exemptions are exempt from minimum attendance rules. They should coordinate project submissions directly with the teaching staff.
3. **Absence Justification:**
   * Validated absence justifications must be formally submitted through the PACO portal within 5 working days of the event. Justified absences during mandatory assessment milestones grant eligibility for make-up sessions.

---

# 6. Academic Integrity, Anti-Fraud & Generative AI Policy

Engineering education relies on intellectual rigor, professional ethics, and authentic individual effort.

### 6.1. Collaboration vs. Plagiarism
* **Constructive dialogue is encouraged:** Brainstorming architecture ideas, terminal commands, and debugging strategies with classmates is welcome.
* **Strict boundaries:** All submitted work must be produced exclusively by the members of the assigned group. The following are strictly forbidden:
  * Sharing source code, configuration files, or report text across groups;
  * Copying code from peers or distributing private repository access;
  * Reusing project solutions from previous academic years;
  * Incorporating code from public repositories without explicit authorization and proper citation.

### 6.2. Generative Artificial Intelligence (AI) Policy

Generative AI models are recognized as powerful modern productivity tools, requiring critical thinking, accountability, and transparency:

1. **Written Exams & Quizzes:**
   * **Absolute Prohibition:** The use of AI assistants or external tools during exams is strictly prohibited and constitutes direct academic fraud.
2. **Practical Development Projects:**
   * **No End-to-End Generation:** Projects, core algorithmic logic, or entire reports must not be generated wholesale by AI tools.
   * **Authorized Support Uses:**
     * Assisting in debugging and explaining error messages/stack traces;
     * Exploring architectural design patterns and alternatives;
     * Generating unit testing datasets and edge-case scenarios;
     * Polishing language clarity and formatting diagrams in reports.
   * **Mandatory Disclosure & Critical Reasoning:**
     * Any use of AI in designing code or drafting documentation must be **explicitly disclosed** in the report, including prompts used and a critical engineering justification (*"the suggestion was adopted because... / we altered the AI response because it introduced a security flaw..."*).
     * The team assumes complete responsibility for any bug, vulnerability, or inaccuracy in AI-assisted code.

### 6.3. Detection & Disciplinary Sanctions
* All submissions are routinely scanned with automated code plagiarism detection platforms (such as *Moss* and *Ouriginal*) against peer submissions and multi-year historical archives.
* Facilitating academic fraud (e.g., providing one's code to others) is subject to identical penalties.
* **Consequences:** Confirmed instances of fraud or plagiarism result in an immediate **grade of 0 (zero)** for all involved students and formal referral to the DETI Directorate and the University Rectorate for **disciplinary proceedings**.

---

# 7. Bibliography & Reference Material

Course references and support materials are structured into four foundational components: core recommended textbooks, official technical documentation and manuals for technologies covered in practical labs, recommended cheat sheets and interactive simulators, and legal, ethical, and institutional sources.

### 7.1. Core Textbooks & Reference Manuals

* **Systems Administration & Command Line (Module C1):**
  * William Shotts, *The Linux Command Line: A Complete Introduction*, 2nd Edition, No Starch Press, 2019. ISBN: 978-1593279523.
* **Virtualization & Software Containers (Module C2):**
  * Adrian Mouat, *Using Docker: Developing and Deploying Software with Containers*, O'Reilly Media, 2015. ISBN: 978-1491915714.
* **Distributed Version Control & Collaboration (Module C3):**
  * Scott Chacon and Ben Straub, *Pro Git*, 2nd Edition, Apress, 2014. Freely available in open access at: [https://git-scm.com/book/](https://git-scm.com/book/).
* **Computer Networks & Communication Protocols (Module C4):**
  * James F. Kurose and Keith W. Ross, *Computer Networking: A Top-Down Approach*, 8th Edition, Pearson, 2021. ISBN: 978-0136681557.
  * Odette Windows, *Python Networking 101: Navigating Essentials of Networking, Socket Programming, AsyncIO, Network Testing, Simulations and Ansible*, GiftforGits, 2023. ISBN: 978-8196144883.
* **Frontend Web Development, JavaScript & Servers (Module C5):**
  * Paul McFedries, *HTML, CSS, & JavaScript All-in-One For Dummies*, Wiley, 2023. ISBN: 978-1119904250.
  * Ilya Kantor, *The Modern JavaScript Tutorial*, 2024. Freely accessible online at: [https://javascript.info/](https://javascript.info/).
* **Data Formats, Structures & Analysis (Module C6):**
  * Wes McKinney, *Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter*, 3rd Edition, O'Reilly Media, 2022. ISBN: 978-1098104030.
* **Technical Documentation, LaTeX & Markdown (Module C7):**
  * Thomas Mailund, *Introducing Markdown and Pandoc: Using Markup Language and Document Converter*, Apress, 2019. ISBN: 978-1484251485.
  * Leslie Lamport, *LaTeX: A Document Preparation System*, 2nd Edition, Addison-Wesley Professional, 1994. ISBN: 978-0201529838.
* **Ethics, Data Protection & Technology Regulation (Module C8):**
  * European Union Agency for Fundamental Rights (FRA) and Council of Europe, *Handbook on European Data Protection Law*, Publications Office of the European Union, 2018 Edition. ISBN: 978-92-9474-001-4.

### 7.2. Official Technical Documentation by Ecosystem

* **Module C1 — Terminal, Shell & Bash Scripting:**
  * *GNU Bash Reference Manual:* [https://www.gnu.org/software/bash/manual/](https://www.gnu.org/software/bash/manual/)
  * *The Linux Kernel and System Man-Pages Project (Michael Kerrisk):* [https://man7.org/linux/man-pages/](https://man7.org/linux/man-pages/)
  * *Microsoft PowerShell Documentation:* [https://learn.microsoft.com/powershell/](https://learn.microsoft.com/powershell/)
* **Module C2 — Virtualization, Containerization & Sandboxing:**
  * *Docker Official Documentation & Reference:* [https://docs.docker.com/](https://docs.docker.com/)
  * *Docker Curriculum (Hands-on Container Tutorial):* [https://docker-curriculum.com/](https://docker-curriculum.com/)
  * *Oracle VM VirtualBox User Manual:* [https://www.virtualbox.org/manual/](https://www.virtualbox.org/manual/)
  * *QEMU Documentation & ArchWiki Advanced Networking:* [https://www.qemu.org/docs/](https://www.qemu.org/docs/) and [https://wiki.archlinux.org/title/QEMU](https://wiki.archlinux.org/title/QEMU)
  * *Podman Documentation (Daemonless Container Engine):* [https://podman.io/](https://podman.io/)
  * *AppImage Official Documentation:* [https://docs.appimage.org/](https://docs.appimage.org/)
  * *Flatpak Documentation & Flathub:* [https://docs.flatpak.org/](https://docs.flatpak.org/) and [https://flathub.org/](https://flathub.org/)
  * *Canonical Snapcraft User Guide:* [https://snapcraft.io/docs](https://snapcraft.io/docs)
  * *LinuxServer.io Community Container Hub:* [https://www.linuxserver.io/](https://www.linuxserver.io/)
* **Module C3 — Distributed Version Control:**
  * *Git Official Documentation & Reference Manual:* [https://git-scm.com/doc](https://git-scm.com/doc)
  * *GitHub Documentation & GitHub Classroom Guides:* [https://docs.github.com/](https://docs.github.com/)
* **Module C4 — Computer Networks, Sockets & Messaging:**
  * *Wireshark User's Guide (Protocol Analyzer):* [https://www.wireshark.org/docs/](https://www.wireshark.org/docs/)
  * *Nmap Network Scanning (Gordon Lyon / Fyodor):* [https://nmap.org/book/](https://nmap.org/book/)
  * *Let's Encrypt Documentation & Certbot (TLS/SSL):* [https://letsencrypt.org/docs/](https://letsencrypt.org/docs/)
  * *Python Low-Level Networking (`socket` & `asyncio` modules):* [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html) and [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
  * *FastAPI Interactive Web & API Framework:* [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
  * *MQTT 5.0 Protocol Specification & Eclipse Paho Client:* [https://mqtt.org/](https://mqtt.org/) and [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
  * *RabbitMQ Tutorials & ZeroMQ Guide:* [https://www.rabbitmq.com/tutorials](https://www.rabbitmq.com/tutorials) and [https://zeromq.org/](https://zeromq.org/)
* **Module C5 — Web Development, JavaScript & Servers:**
  * *MDN Web Docs (HTML5, CSS3, DOM & Fetch API):* [https://developer.mozilla.org/](https://developer.mozilla.org/)
  * *W3Schools Online Web Tutorials:* [https://www.w3schools.com/](https://www.w3schools.com/)
  * *Nginx Documentation & Reverse Proxy Configuration:* [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
  * *Philip Roberts, "What the heck is the event loop anyway?" (JSConf):* [https://www.youtube.com/watch?v=8aGhZQkoFbQ](https://www.youtube.com/watch?v=8aGhZQkoFbQ)
  * *Node.js Best Practices Repository:* [https://github.com/goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)
  * *React Official Documentation:* [https://react.dev/](https://react.dev/)
* **Module C6 — Data Formats, Structures & Wrangling:**
  * *Data Format Specifications:* JSON (RFC 8259), YAML 1.2 ([https://yaml.org/](https://yaml.org/)), XML (W3C Recommendation), CSV (RFC 4180).
  * *Pandas User Guide & API Reference:* [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
  * *Polars User Guide (Fast Multithreaded DataFrames):* [https://pola.rs/](https://pola.rs/)
  * *Matplotlib Visual Anatomy of a Plot & Gallery:* [https://matplotlib.org/](https://matplotlib.org/)
  * *Seaborn Statistical Data Visualization:* [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
  * *Project Jupyter (JupyterLab & Notebooks):* [https://jupyter.org/](https://jupyter.org/)
* **Module C7 — Technical Documentation, LaTeX & Markdown:**
  * *Pandoc User's Guide (Universal Document Converter):* [https://pandoc.org/MANUAL.html](https://pandoc.org/MANUAL.html)
  * *Overleaf Learn (LaTeX Tutorials and Package References):* [https://www.overleaf.com/learn](https://www.overleaf.com/learn)
  * *Comprehensive TeX Archive Network (CTAN):* [https://ctan.org/](https://ctan.org/)
  * *Detexify (LaTeX Handwritten Symbol Recognition):* [https://detexify.kirelabs.org/classify.html](https://detexify.kirelabs.org/classify.html)
  * *GitHub Flavored Markdown (GFM) Specification:* [https://github.github.com/gfm/](https://github.github.com/gfm/)
  * *The Markdown Guide (Syntax and Tools):* [https://www.markdownguide.org/](https://www.markdownguide.org/)
  * *JabRef (BibTeX and BibLaTeX Reference Manager):* [https://www.jabref.org/](https://www.jabref.org/)
* **Module C8 — Ethics, Data Protection, Licensing & AI:**
  * *Open Source Initiative (OSI) — Open Source Licenses:* [https://opensource.org/licenses](https://opensource.org/licenses)
  * *Free Software Foundation (FSF) — GNU Licenses & Philosophy:* [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)

### 7.3. Quick Reference Sheets (*Cheat Sheets*) & Interactive Platforms

* *GeeksforGeeks Linux Commands Cheat Sheet:* [https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/](https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/)
* *Crontab Guru (Visual Cron Schedule Editor & Tester):* [https://crontab.guru/](https://crontab.guru/)
* *Red Hat Bash Shell Cheat Sheet:* [https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet](https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet)
* *Docker Official CLI Cheat Sheet:* [https://docs.docker.com/get-started/docker_cheatsheet.pdf](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
* *Collabnix Ultimate Docker Cheatsheet:* [https://dockerlabs.collabnix.com/docker/cheatsheet/](https://dockerlabs.collabnix.com/docker/cheatsheet/)
* *Learn Git Branching (Interactive Git Graph Simulator):* [https://learngitbranching.js.org/](https://learngitbranching.js.org/)
* *Atlassian Git Cheat Sheet:* [https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)
* *StationX Windows CMD & PowerShell Cheat Sheets:* [https://www.stationx.net/windows-command-line-cheat-sheet/](https://www.stationx.net/windows-command-line-cheat-sheet/)

### 7.4. Legal Regulations, Standards & Institutional Resources

* *General Data Protection Regulation (Regulation EU 2016/679 - GDPR):* [https://eur-lex.europa.eu/eli/reg/2016/679/oj](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
* *European Artificial Intelligence Act (EU AI Act - Regulation EU 2024/1689):* [https://artificialintelligenceact.eu/](https://artificialintelligenceact.eu/)
* *National Data Protection Commission (CNPD — Guidelines & Data Breach Reports):* [https://www.cnpd.pt/](https://www.cnpd.pt/)
* *Data Protection Officer Office (DPO - Universidade de Aveiro):* [https://www.ua.pt/pt/rgpd](https://www.ua.pt/pt/rgpd)
* *Regulamento de Estudos da Universidade de Aveiro (REUA):* Available on the UA institutional portal.
* *Universidade de Aveiro Academic Platforms (PACO & Moodle):* [https://paco.ua.pt/](https://paco.ua.pt/) and [https://moodle.ua.pt/](https://moodle.ua.pt/)
* *Course GitHub Repository & Classroom Organization:* [https://github.com/detiuaveiro/iei](https://github.com/detiuaveiro/iei)
