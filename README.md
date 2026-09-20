# Introdução Engenharia Informática

Upon completing this course, each student should be able to: 

- O1. Administer Linux and Windows operating systems via command line.
- O2. Differentiate the use of virtual machines and containers to execute software in isolated and organized environments. 
- O3. Understand the need for code versioning and collaborative work tools.
- O4. Grasp the fundamental concepts of networking and configure a local network. 
- O5. Develop basic web pages and utilize web technologies to create simple web applications. 
- O6. Manipulate data in common formats and employ data analysis tools. 
- O7. Comprehend the principles of GDPR, intellectual property, and software licensing from an ethical and professional standpoint. 

The previous objectives will be achieved by working in these topics

* C1. Introduction to Command Line
* C2. Virtualization and Containers 
* C3. Code Versioning and Collaboration 
* C4. IP Networking Communication 
* C5. Web Servers and Technology 
* C6. Semistructured Data Manipulation 
* C7. Document Compilation (Latex and Markdown) 
* C8. GDPR, Intellectual Property, Ethics, and Professionalism in IT 

## Schedule

Can find the spreadsheet [here](iei_plan.ods).

| Date TP1/2 | Date TP3   | Date TP4   | Topic | Description                        |
|-----------:|-----------:|-----------:|:-----:|:-----------------------------------|
| 14-09-2026 | 16-09-2026 | 17-09-2026 |    C0 | Setup                              |
| 21-09-2026 | 23-09-2026 | 24-09-2026 |    C1 | Linux terminal                     |
| 28-09-2026 | 30-09-2026 | 01-10-2026 |    C1 | Windows terminal                   |
| 12-10-2026 | 07-10-2026 | 08-10-2026 |    C2 | Virtualization                     |
| 19-10-2026 | 14-10-2026 | 15-10-2026 |    C2 | Containers                         |
| 26-10-2026 | 21-10-2026 | 22-10-2026 |    C2 | Application containers             |
| 02-11-2026 | 28-10-2026 | 29-10-2026 |    C3 | Git & Github                       |
| 09-11-2026 | 04-11-2026 | 05-11-2026 |    C4 | Network configuration              |
| 16-11-2026 | 11-11-2026 | 12-11-2026 |    C4 | Network programing                 |
| 23-11-2026 | 18-11-2026 | 19-11-2026 |    C5 | WebPage & deployment               |
| 30-11-2026 | 25-11-2026 | 26-11-2026 |    C5 | Web programming                    |
| 07-12-2026 | 02-12-2026 | 03-12-2026 |    C6 | Data visualization                 |
| 14-12-2026 | 09-12-2026 | 10-12-2026 |    C7 | Latex & Markdown                   |
| 21-12-2026 | 16-12-2026 | 17-12-2026 |    C8 | GDPR, AI Act, Intelectual property |

## Grading

- 50% Theory + 50% Practice
- Discrete: 25% Project 1 + 25% Project 2 + 50% Exam
- Final: 50% Final Exame + 50% Project 

## Classes

### Class 0 - Setup

The material can be found [here](classes/class_00/).

## Known Issues and Notes

### Pandoc & Beamer: Disappearing Tables Bug

When compiling Beamer presentation slides with modern versions of Pandoc (≥ 3.8, including 3.11+), uncaptioned Markdown tables are automatically wrapped inside a local TeX group:
```latex
{\def\LTcaptype{none} % do not increment counter
\begin{longtable}[]{@{}...@{}}
...
\end{longtable}
}
```
In LaTeX Beamer, enclosing `longtable` in local braces (`{ ... }`) prevents its internal page output routine (`\output`) from flushing the table box, which causes the table to completely disappear from the slide (leaving an empty frame).

**Workaround / Fix:**
1. Supply an explicit escaped-space caption with an ID in Markdown:
   ```markdown
   : \ {#tbl:cal}

   | Column 1 | Column 2 |
   |:---------|:---------|
   | Value 1  | Value 2  |
   ```
2. In the slide YAML frontmatter (`header-includes`), configure `caption` to suppress any caption labels and vertical spacing:
   ```yaml
   header-includes:
     - \usepackage{caption}
     - \captionsetup[longtable]{labelformat=empty,skip=0pt}
   ```
This instructs Pandoc to emit `\begin{longtable}` at the top level without enclosing `{ ... }` braces, ensuring clean, single-line tables render as intended.

## Bibliography

- James F. Kurose and Keith W. Ross. 2021. Computer Networking: A Top-Down Approach (8th edition). Pearson.  
- Python Networking 101: Navigating essentials of networking, socket programming, AsyncIO, network testing, simulations and Ansible, Odette Windows, GiftforGits, 2023 
- Mailund, Thomas 2019 Introducing Markdown and Pandoc: Using Markup Language and Document Converter  
- William Shotts 2019 The Linux Command Line, 2nd Edition - A Complete Introduction 
- Paul McFedries 2023 HTML, CSS, & JavaScript All-in-One For Dummies 

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details