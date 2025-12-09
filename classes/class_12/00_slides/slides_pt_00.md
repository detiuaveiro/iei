---
title: Latex & Markdown
subtitle: Introdução Engenharia Informática
author: Mário Antunes
institute: Universidade de Aveiro
date: December 8, 2025
colorlinks: true
highlight-style: tango
toc: true
toc-title: "Table of Contents"
mainfont: NotoSans
mainfontfallback: "NotoColorEmoji:mode=harf"
header-includes:
 - \usetheme[sectionpage=none,numbering=fraction,progressbar=frametitle]{metropolis}
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# LaTeX & Markdown

## Paradigmas de Geração de Documentos i

**1. WYSIWYG (What You See Is What You Get - O Que Vês É O Que Obténs)**

  * **Exemplos:** Microsoft Word, Google Docs, LibreOffice Writer.
  * **Conceito:** A interface de edição é um espelho da saída final de impressão.
  * **Mecanismo:** Manipulação direta. A formatação (negrito, tamanho, tipo de letra) é aplicada diretamente aos caracteres de texto.
  * **Prós:** Baixa barreira de entrada; feedback visual imediato.
  * **Contras:** "O Que Vês É Tudo O Que Tens" ("What You See Is All You've Got").
      * O conteúdo está fortemente acoplado à apresentação.
      * Mover um "Cabeçalho" genérico para um "Título de Capítulo" requer reformatação manual.
      * Documentos complexos (teses, livros) quebram frequentemente a formatação quando movidos entre computadores ou versões.

## Paradigmas de Geração de Documentos ii

**2. WYSIWYM (What You See Is What You Mean - O Que Vês É O Que Queres Dizer)**

  * **Exemplos:** LaTeX, Markdown, HTML, AsciiDoc.
  * **Conceito:** Você edita a **estrutura semântica** (significado), um compilador lida com a **apresentação visual**.
  * **Mecanismo:** Separação de responsabilidades.
      * *Fonte:* Texto simples (`.tex`, `.md`) contendo conteúdo e tags lógicas (ex: `\section`, `# Heading`).
      * *Motor:* Um compilador (ex: `pdflatex`, `pandoc`) aplica um modelo de estilo específico para gerar a saída (PDF, HTML, EPUB).
  * **Prós:** Consistência, automação, tipografia superior.

## O Valor dos Documentos Compilados {.allowframebreaks}

Porquê aprender uma sintaxe complexa quando o Word existe?

### A. Utilização de Repositórios (Git)

  * **Texto vs. Binário:** Ficheiros Word (`.docx`) são binários XML comprimidos. Sistemas de controlo de versões (Git) tratam-nos como "blobs". Não é possível fazer diferenças (diff) significativas entre eles.
  * **Rastreamento Linha-a-Linha:** Em LaTeX/Markdown, pode rastrear alterações até ao carácter específico e ver o histórico de commits.
  * **Branching:** Ideal para experimentar uma nova estrutura de capítulos sem quebrar o documento principal.

### B. Colaboração

  * **Sem Problemas de "Ficheiro Bloqueado":** Ao contrário de abrir um `.docx` numa unidade de rede, várias pessoas podem editar ficheiros de texto diferentes num projeto simultaneamente.
  * **Merging:** O Git permite fundir (merge) diferentes ficheiros de texto automaticamente.
  * **Modularidade:** Documentos grandes são divididos usando `\input{chapter1.tex}`, mantendo os ficheiros pequenos e geríveis.

### C. Migração & Modelos

  * **Abstração:** No WYSIWYM, etiqueta o texto como "Title" ou "Abstract". Não escolhe o tamanho da letra ou margens manualmente.
  * **Portabilidade de Conteúdo:**
      * *Cenário:* Escreve uma tese. Mais tarde, quer publicar um capítulo como um artigo de conferência.
      * *Ação:* Altera `\documentclass{thesis}` para `\documentclass{ieee-conf}`.
      * *Resultado:* Todo o documento é reformatado (fontes, colunas, citações) instantaneamente. Nenhuma reformatação manual necessária.

# LaTeX

## Aprofundamento: LaTeX i

LaTeX é o padrão da indústria para comunicação científica e técnica. É praticamente Turing-completo.

### Estrutura do Documento

Um ficheiro LaTeX (`.tex`) tem duas partes distintas:

1.  **O Preâmbulo:** Tudo *antes* de `\begin{document}`.
      * Define a "Classe" (estilo).
      * Carrega "Pacotes" (plugins para funcionalidades extra como imagens, cores, links).
      * Define parâmetros globais (margens, metadados).
2.  **O Corpo:** O ambiente de conteúdo dentro de `\begin{document} ... \end{document}`.

## Aprofundamento: LaTeX ii

### Entidades Chave

  * **Classes:**
      * `article`: Artigos científicos, relatórios curtos.
      * `report`: Documentos mais longos com capítulos (teses).
      * `book`: Livros com suporte para matéria pré/pós-textual.
      * `beamer`: Para criar slides de apresentação.
  * **Ambientes (Environments):**
      * Blocos de lógica definidos por `\begin{name} ... \end{name}`.
      * *Exemplos:* `itemize` (listas), `equation` (matemática), `tabular` (tabelas), `center`.
  * **Flutuantes (Figuras & Tabelas):**
      * O LaTeX decide onde colocar as imagens (`\begin{figure}`) para um fluxo de leitura ideal.

## Aprofundamento: LaTeX iii

### Utilização & Compilação

  * **CLI:** `pdflatex main.tex` (Passagem única).
  * **A Regra das 3 Passagens:** Frequentemente requer executar 3 vezes para sincronizar referências (Passagem 1: Recolher etiquetas; Passagem 2: Atribuir números; Passagem 3: Corrigir esquema).
  * **Automação:** `latexmk -pdf -pvc main.tex` (Vigia alterações de ficheiros, lida com referências cruzadas automaticamente).
  * **Cloud:** **Overleaf**. Um editor baseado no navegador que gere a instalação do compilador por si.

# Markdown

## Aprofundamento: Markdown i

Markdown é uma linguagem de marcação leve desenhada para legibilidade.

### Filosofia & Sintaxe

O objetivo é que o ficheiro fonte original seja legível como texto simples sem parecer código de computador.

  * **Cabeçalhos:** `#` para H1, `##` para H2 (traduz-se para `<h1>`, `<h2>`).
  * **Listas:** `-` ou `*` para pontos; `1.` para numeradas.
  * **Formatação:** `**Bold**` (`<b>`), `*Italic*` (`<i>`), `` `Code` ``.
  * **Links:** `[Text](URL)`.
  * **Imagens:** `![Alt Text](URL)`.

## Aprofundamento: Markdown ii

### Sabores & Extensões

O Markdown evoluiu para vários "Sabores" (Flavors):

  * **CommonMark:** A especificação padronizada.
  * **GFM (GitHub Flavored Markdown):** Adiciona tabelas, listas de tarefas (`- [ ]`), e rasurado.
  * **Pandoc Markdown:** A versão mais poderosa. Adiciona citações (`@author`), notas de rodapé (`[^1]`), blocos de metadados e suporte matemático.

## Aprofundamento: Markdown iii

### Utilização (Pandoc)

**Pandoc** é o "Conversor Universal". Lê Markdown e produz quase tudo.

  * **Lógica:** Markdown $\rightarrow$ Abstract Syntax Tree (AST) $\rightarrow$ Formato de Saída.
  * **Comandos:**
      * `pandoc input.md -o output.pdf` (Usa motor LaTeX).
      * `pandoc input.md -o output.docx` (Gera Word).
      * `pandoc input.md -t beamer -o slides.pdf` (Gera slides LaTeX).

# ToC

## Índice (ToC) i

### LaTeX ToC

O LaTeX gera um Índice (ToC) automaticamente ao analisar as suas tags de Secção (`\section`, `\subsection`).

  * **O Comando:** Simplesmente coloque `\tableofcontents` onde deseja a lista.
  * **Mecanismo de Compilação:**
    1.  *Execução 1:* O LaTeX escreve todos os títulos de secção e números de página num ficheiro temporário `.toc`.
    2.  *Execução 2:* O LaTeX lê o ficheiro `.toc` e renderiza a lista no documento.

## Índice (ToC) ii

  * **Exemplo:**
    ```latex
    \begin{document}
      \maketitle
      \tableofcontents  % Auto-generates here
      \newpage
      \section{Introduction}
    \end{document}
    ```

## Índice (ToC) iii

### Markdown ToC

O Markdown padrão não tem uma tag estrita de ToC, mas as ferramentas lidam com isso de forma diferente:

1.  **Pandoc:** Use a flag `--toc` na linha de comando. Analisa cabeçalhos (`#`, `##`) para construí-lo.
2.  **Editores (VS Code/Typora):** Muitos suportam a macro `[TOC]`.
3.  **Manual:** Escreve-o como uma lista de links: `- [Introduction](#introduction)`.

# Figuras

## Figuras (LaTeX) i

### O Pacote `graphicx`

O LaTeX trata imagens como "flutuantes" (floats)—decide automaticamente a melhor posição (topo da página, fundo, etc.) para evitar quebras de página estranhas.

  * **Pré-requisito:** Deve adicionar `\usepackage{graphicx}` ao seu preâmbulo.
  * **Ambiente:** `\begin{figure}[placement]`.
      * *Opções de posicionamento:* `h` (aqui), `t` (topo), `b` (fundo), `!` (ignorar restrições).

## Figuras (LaTeX) ii

  * **Comandos Chave:**
      * `\includegraphics[options]{filename}`: A inserção real da imagem.
      * `\caption{...}`: Adiciona a descrição e numeração (ex: "Figura 1: ...").
      * `\label{...}`: Cria uma âncora para referenciá-la mais tarde (ex: "Ver Figura \\ref{...}").

## Figuras (LaTeX) iii

**Código LaTeX:**

```latex
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.5\textwidth]{results.png}
    \caption{Experimental Results}
    \label{fig:results}
\end{figure}
```

## Figuras (Markdown) i

### Imagens em Linha

A sintaxe Markdown é concisa (`![]()`) mas tipicamente coloca as imagens **em linha** (exatamente onde as escreve) em vez de as fazer flutuar. O Markdown padrão não tem redimensionamento nativo, mas extensões lidam com isso.

**1. Sintaxe Padrão:**
`![Alt Text for Accessibility](path/to/image.png)`

**2. Com Redimensionamento (Recurso ao HTML):**
Visto que o Markdown suporta HTML puro, este é o método mais compatível para redimensionamento.
`<img src="image.png" width="300" />`

## Figuras (Markdown) ii

**3. Com Redimensionamento (Extensão Pandoc):**
Se usar Pandoc (padrão para escrita académica), pode usar atributos.
`![Results](image.png){ width=50% }`

**4. Adicionar Legendas:**
No Pandoc, o "Texto Alt" (texto dentro de `[]`) torna-se automaticamente a Legenda da Figura abaixo da imagem ao converter para PDF/LaTeX.

# Tabelas

## Tabelas i

### Tabelas LaTeX (`tabular`)

As tabelas LaTeX são precisas mas verbosas. Usam delimitadores específicos.

  * **Ambiente:** `\begin{tabular}{cols}`
  * **Especificação de Colunas:** `{l c r}` define 3 colunas (Alinhada à esquerda, Centrada, Alinhada à direita).
  * **Separadores:** `&` separa células; `\\` termina uma linha.
  * **Linhas:** `\hline` desenha linhas horizontais; `|` na especificação da coluna desenha linhas verticais.

## Tabelas ii

**Código LaTeX:**

```latex
\begin{table}[h]
  \centering
  \begin{tabular}{|l|c|r|}
    \hline
    \textbf{Item} & \textbf{Qty} & \textbf{Price} \\
    \hline
    Apples & 5 & \$1.00 \\
    Oranges & 10 & \$2.50 \\
    \hline
  \end{tabular}
  \caption{Grocery List}
\end{table}
```

## Tabelas iii

### Tabelas Markdown

O Markdown usa pipes estilo "Arte ASCII".
É mais simples e fácil de ler em código bruto, mas menos flexível (sem células fundidas ou alinhamento complexo).

**Código Markdown:**

```markdown
| Item    | Qty | Price |
|:--------|:---:|------:|  <-- Alignment (Left,
| Apples  | 5   | $1.00 |  Center, Right)
| Oranges | 10  | $2.50 |
```

# Bibliografia

## Gestão de Bibliografia i

### LaTeX (BibTeX / BibLaTeX)

As citações são armazenadas num ficheiro de base de dados de texto simples separado (`.bib`).

**1. A Base de Dados (`refs.bib`):**

```bibtex
@article{einstein1905,
    author = "Albert Einstein",
    title = "On the Electrodynamics of Moving Bodies",
    year = "1905"
}
```

## Gestão de Bibliografia ii

**2. O Documento:**

```latex
As stated by \cite{einstein1905}, relativity is
complex.

\bibliographystyle{plain}
\bibliography{refs}
```

## Gestão de Bibliografia iii

### Markdown (Pandoc Citeproc)

O Pandoc pode ler ficheiros BibTeX e processar citações em Markdown.

**A Sintaxe:**

```markdown
As stated by [@einstein1905], relativity is complex.
```

**O Comando:**
`pandoc doc.md --bibliography=refs.bib --citeproc -o doc.pdf`

## Geração de Biografia i

Em artigos académicos (especialmente IEEE), "Biografias" são blocos formatados no final de um artigo contendo a foto do autor e uma pequena biografia.

### LaTeX (Classe IEEEtran)

A classe `IEEEtran` fornece um ambiente específico para isto. Lida com o envolvimento do texto à volta da foto automaticamente e estiliza o nome em letras maiúsculas a negrito.

## Geração de Biografia ii

**Código LaTeX:**

```latex
% Requires \documentclass{IEEEtran}

\begin{IEEEbiography}[{\includegraphics[width=1in,clip,keepaspectratio]{photo.jpg}}]{John Doe}
received the B.S. degree in aerospace engineering...
He is currently a Professor at X University.
His research interests include LaTeX and Typography.
\end{IEEEbiography}
```

## Geração de Biografia iii

### Markdown

O Markdown não tem uma tag semântica nativa de "Biografia".
Cria-a manualmente usando Cabeçalhos e Imagens, ou HTML se estiver a renderizar para a web.

**Código Markdown:**

```markdown
## Author Biography

![John Doe](photo.jpg){ width=100px align=left }

**John Doe** received the B.S. degree in
aerospace engineering...
He is currently a Professor at X University.
```

# Equações Matemáticas

## Equações Matemáticas i

Uma das razões principais para usar WYSIWYM é a renderização superior de matemática.

### Matemática LaTeX

O LaTeX tem dois modos:

1.  **Modo em Linha:** Para matemática dentro de uma frase. Rodeado por `$`.
      * *Sintaxe:* `Let $x$ be a variable.`
2.  **Modo de Exibição:** Para equações centradas e independentes.
      * *Sintaxe:* `\[ E = mc^2 \]` ou `\begin{equation} ... \end{equation}`.

## Equações Matemáticas ii

**Comandos Comuns:**

  * **Frações:** `\frac{numerator}{denominator}`
  * **Grego:** `\alpha`, `\beta`, `\Omega`
  * **Somatório/Integrais:** `\sum_{i=0}^{n}`, `\int_{0}^{\infty}`
  * **Sub/Sobrescritos:** `x_i`, `x^2`

## Equações Matemáticas iii

### Matemática Markdown

A maioria dos motores Markdown (GitHub, Pandoc, Obsidian, Jupyter) usa **MathJax** ou **KaTeX** para renderizar sintaxe LaTeX dentro do Markdown.

  * **Sintaxe:** Geralmente usa exatamente os mesmos delimitadores `$` que o LaTeX.
      * Em linha: `$E=mc^2$`
      * Bloco: `$$E=mc^2$$`

**Exemplo de Comparação (Fórmula Quadrática):**
Tanto LaTeX como Markdown usam:
`x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}`

# Recursos Adicionais

## Recursos Adicionais {.allowframebreaks}

### LaTeX

  * **Overleaf Learn:** [https://www.overleaf.com/learn](https://www.overleaf.com/learn) (A melhor documentação para iniciantes).
  * **CTAN (Comprehensive TeX Archive Network):** [https://ctan.org/](https://ctan.org/) (O repositório central para todos os pacotes LaTeX).
  * **Detexify:** [https://detexify.kirelabs.org/classify.html](https://detexify.kirelabs.org/classify.html) (Desenhe um símbolo para encontrar o seu comando LaTeX).

### Markdown & Pandoc

  * **Markdown Guide:** [https://www.markdownguide.org/](https://www.markdownguide.org/) (Tutorial abrangente sobre sintaxe e sabores).
  * **Pandoc Documentation:** [https://pandoc.org/](https://pandoc.org/) (O manual para o conversor universal).
  * **GitHub Flavored Markdown Spec:** [https://github.github.com/gfm/](https://github.github.com/gfm/)

### Ferramentas

  * **Editores:** VS Code (com LaTeX Workshop & Markdown All in One).
  * **Gestão de Referências:** Jabref (Funciona diretamente com BibTeX).
