---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Controlo de Versões com Git & Plataforma Colaborativa GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guião Prático de Laboratório

**Enquadramento Pedagógico & Objetivos:**
O controlo de versões distribuído com **Git** e a colaboração através de plataformas na nuvem como o **GitHub** constituem a espinha dorsal da engenharia de software contemporânea. Nesta sessão prática de **3 horas**, irá aplicar passo a passo todos os conceitos abordados na apresentação teórica, adquirindo a disciplina operacional para controlar o ciclo de vida do código-fonte com rastreabilidade, reversibilidade e colaboração segura em equipa:

* **Parte 0 — Configuração do Ambiente & Autenticação no GitHub:** Instalação do Git, configuração de identidade (`user.name`, `user.email`) e autenticação criptográfica segura com o GitHub via chave SSH `ed25519`.
* **Parte 1 — Aspetos Funcionais do Git & Ciclo de Vida Local:** Inicialização de repositórios (`git init`), transição entre as três zonas operacionais (*Working Tree*, *Staging Area* e *Repositório Local*) e os quatro estados dos ficheiros, boas práticas (regra 50/72) e padronização com *Conventional Commits*, inspeção detalhada com `git log`, marcação local de versões com `git tag` ([SemVer](https://semver.org/)) e exclusão de artefactos com `.gitignore`.
* **Parte 2 — Ramificação, Integração & Resolução de Conflitos:** O paradigma de ramos como ponteiros leves ($O(1)$) e o ponteiro simbólico `HEAD`, comandos de gestão (`git branch`, `git switch`, `git switch -c`, `git branch -d`), estratégias de integração com `git merge` (*Fast-Forward* vs. *3-Way Merge*), linearização do histórico com `git rebase` e resolução manual de conflitos de *merge*.
* **Parte 3 — Colaboração Distribuída, Workflows & GitHub Releases:** Gestão de repositórios remotos (`origin`), sincronização com `fetch`, `pull` e `push`, execução *end-to-end* do modelo **Scaled Trunk-Based Development** (com *Short-Lived Feature Branches* e *Pull Requests* com *Code Review*) e publicação oficial de versões com **GitHub Releases**.

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Antes de iniciar os exercícios, crie e aceda à pasta de trabalho dedicada para esta sessão laboratorial:

```bash
$ mkdir -p ~/IEI/aula06
$ cd ~/IEI/aula06
```

Todos os repositórios locais e ficheiros criados durante a aula deverão ser organizados dentro deste diretório de trabalho.

> **Nota sobre caminhos de ficheiros:**
> Os comandos deste guião assumem que o terminal está posicionado no diretório de trabalho `~/IEI/aula06`.

-----

## Parte 0: Configuração do Ambiente & Autenticação no GitHub

Antes de iniciar o desenvolvimento, é necessário preparar o cliente Git local e estabelecer a autenticação segura com a plataforma GitHub.

### Passo 1: Instalação e Verificação do Git

Em sistemas baseados em Debian/Ubuntu, verifique se o Git se encontra instalado ou proceda à sua instalação:

```bash
$ sudo apt update && sudo apt install -y git
$ git --version
```

### Passo 2: Configuração Global de Identidade

O Git incorpora a identidade do autor de forma imutável em cada *commit* criado. Configure o seu nome completo, o seu endereço de correio eletrónico institucional da Universidade de Aveiro e o nome padrão do ramo principal (`main`):

```bash
$ git config --global user.name "O Seu Nome Completo"
$ git config --global user.email "o.seu.email@ua.pt"
$ git config --global init.defaultBranch main
```

Pode consultar a configuração gravada em `~/.gitconfig` executando:

```bash
$ git config --global --list
```

### Passo 3: Autenticação Segura com o GitHub

Para sincronizar código com o GitHub (`git push`), a plataforma exige autenticação por chave SSH (recomendada) ou *Personal Access Token* (PAT).

#### Método Recomendado: Par de Chaves SSH (ed25519)

1. Gere um novo par de chaves SSH utilizando o algoritmo `ed25519`:
   ```bash
   $ ssh-keygen -t ed25519 -C "o.seu.email@ua.pt" -f ~/.ssh/id_ed25519 -N ""
   ```
2. Visualize e copie o conteúdo integral da sua **chave pública** (`.pub`):
   ```bash
   $ cat ~/.ssh/id_ed25519.pub
   ```
   *(O conteúdo deve começar por `ssh-ed25519 AAAAC3...` e terminar no seu email).*
3. Registe a chave pública na sua conta GitHub:
   * Aceda a [GitHub.com](https://github.com/) e inicie sessão.
   * No canto superior direito, clique na fotografia de perfil $\rightarrow$ **Settings**.
   * Na barra lateral esquerda (secção *Access*), selecione **SSH and GPG keys**.
   * Clique no botão verde **New SSH key**.
   * Preencha o campo **Title** com um identificador da máquina (ex.: `Portátil Ubuntu IEI`).
   * No campo **Key**, cole exatamente o texto copiado da chave pública e clique em **Add SSH key**.
4. Teste a ligação segura a partir do terminal:
   ```bash
   $ ssh -T git@github.com
   ```
   > Na primeira ligação, confirme a impressão digital (*fingerprint*) do servidor digitando `yes`. Deverá receber a confirmação:
   > `Hi <utilizador>! You've successfully authenticated, but GitHub does not provide shell access.`

#### Método Alternativo: Personal Access Token (PAT)

Caso não disponha de acesso SSH na rede onde se encontra:
1. No GitHub, aceda a **Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** $\rightarrow$ **Fine-grained tokens**.
2. Clique em **Generate new token**, defina um nome descritivo (ex.: `IEI-Token-Aula06`), escolha a validade e conceda permissão **Read and write** em **Repository permissions $\rightarrow$ Contents**.
3. Copie imediatamente o token gerado (`github_pat_...`) e utilize-o como palavra-passe nas operações HTTPS.

-----

## Parte 1: Aspetos Funcionais do Git & Ciclo de Vida Local

Nesta parte (correspondente à **Parte II** dos slides teóricos), irá operar localmente sobre as três zonas do Git (**Working Tree**, **Staging Area** e **Repositório Local**), sem depender de qualquer ligação à Internet.

### Exercício 1: Inicialização do Repositório (`git init`) e Estrutura `.git/`

1. Crie uma pasta para o seu projeto e inicialize-a como repositório Git:
   ```bash
   $ mkdir ~/IEI/aula06/meu-projeto && cd ~/IEI/aula06/meu-projeto
   $ git init
   ```
2. Inspecione a diretoria oculta `.git/` criada automaticamente:
   ```bash
   $ ls -la .git/
   $ cat .git/HEAD
   ```
   > **Compreensão Arquitetural:**
   > A diretoria `.git/` é a base de dados local que armazena todo o grafo do histórico, objetos comprimidos (`objects/`), ponteiros de ramos (`refs/heads/`) e a referência simbólica `HEAD` (`ref: refs/heads/main`).

### Exercício 2: As Três Zonas, Estados dos Ficheiros (`status`, `add`, `commit`)

Ao transitar entre o **Working Tree**, a **Staging Area** e o **Repositório Local**, cada ficheiro assume um de quatro estados: **Untracked**, **Modified**, **Staged** ou **Unmodified**.

1. Crie um ficheiro `index.html` no seu *Working Tree*:
   ```html
   <!DOCTYPE html>
   <html lang="pt">
   <head>
       <meta charset="UTF-8">
       <title>Portal IEI - Universidade de Aveiro</title>
   </head>
   <body>
       <h1>Bem-vindo ao Projeto de IEI</h1>
       <p>Controlo de versões distribuído com Git e GitHub.</p>
   </body>
   </html>
   ```
2. Inspecione o estado com `git status`:
   ```bash
   $ git status
   ```
   O ficheiro surge a vermelho como **Untracked** (o Git ainda não o monitoriza).
3. Promova o ficheiro para a **Staging Area / Index** com `git add`:
   ```bash
   $ git add index.html
   $ git status
   ```
   O ficheiro surge agora a verde no estado **Staged** (*Changes to be committed*).
4. Consolide o conteúdo da *Staging Area* num snapshot permanente no **Repositório Local** usando `git commit`:
   ```bash
   $ git commit -m "feat: adiciona estrutura HTML inicial da página principal"
   $ git status
   ```
   O ficheiro encontra-se agora no estado **Unmodified** (*nothing to commit, working tree clean*).
5. Edite o ficheiro `index.html` acrescentando um rodapé antes de `</body>`:
   ```html
       <footer>DETI - Universidade de Aveiro</footer>
   ```
   Execute `git status` e verifique que o ficheiro já rastreado passou ao estado **Modified** (a vermelho, *Changes not staged for commit*).
6. **Teste de Desindexação (`git restore --staged`):**
   Se preparar um ficheiro modificado por engano (`git add`), pode retirá-lo da *Staging Area* de volta para o estado *Modified* no *Working Tree* sem perder as edições em disco:
   ```bash
   $ git add index.html
   $ git restore --staged index.html
   $ git status
   ```

### Exercício 3: Boas Práticas (50/72), Conventional Commits e Retificação (`--amend`)

Como abordado nos slides teóricos, mensagens de commit estruturadas segundo a especificação [Conventional Commits](https://www.conventionalcommits.org/) (`<tipo>[âmbito opcional]: <descrição>`) viabilizam auditorias rápidas, geração automática de *changelogs* e cálculo automático de versões SemVer.

1. Indexe a alteração efetuada no `index.html` e simule um commit com uma mensagem descuidada (anti-padrão):
   ```bash
   $ git add index.html
   $ git commit -m "mudancas no html"
   $ git log --oneline
   ```
2. Corrija o último commit utilizando `git commit --amend`, substituindo-o por uma mensagem que respeita a **convenção 50/72** (assunto conciso no modo imperativo $\le 50$ caracteres, seguido de corpo explicativo separado por linha em branco):
   ```bash
   $ git commit --amend -m "feat(ui): adiciona rodapé institucional" \
   -m "Inclui identificação oficial do departamento segundo o guia de estilo."
   $ git log --oneline
   ```
   > **Nota Técnica:** O comando `--amend` substitui o último commit por um novo objeto com novo hash SHA-1. Apenas deve ser utilizado em commits locais que **ainda não tenham sido partilhados** via `push`.
3. Crie um ficheiro de documentação `README.md` e registe um commit do tipo `docs:`:
   ```bash
   $ cat << 'EOF' > README.md
   # Portal IEI
   Projeto laboratorial da Aula 06 de Introdução à Engenharia Informática.
   EOF
   $ git add README.md
   $ git commit -m "docs: adiciona documentação inicial no ficheiro README"
   ```

### Exercício 4: Inspeção do Histórico (`git log`) e Marcação de Versões (`git tag`)

1. Pratique as cinco variantes de inspeção do histórico estudadas nos slides teóricos:
   ```bash
   # 1. Apresentação detalhada padrão (autor, data, hash SHA completo e corpo)
   $ git log

   # 2. Visão compacta de uma linha por commit (Hash curto + Assunto)
   $ git log --oneline

   # 3. Representação visual da topologia em ASCII
   $ git log --graph --oneline --all

   # 4. Exibição das diferenças de código (diff) introduzidas nos últimos 2 commits
   $ git log -p -2

   # 5. Resumo estatístico de ficheiros alterados, inserções e deleções
   $ git log --stat
   ```
2. **Marcação de Versões com `git tag` e Versionamento Semântico ([SemVer](https://semver.org/)):**
   Ao contrário de um *branch*, uma **tag** é um ponteiro fixo e imutável para um commit específico (`vMAJOR.MINOR.PATCH`):
   ```bash
   # 1. Criar uma tag leve no commit atual (HEAD)
   $ git tag v0.1.0

   # 2. Listar todas as tags existentes no repositório
   $ git tag

   # 3. Visualizar os commits com as respetivas tags e ponteiros associados
   $ git log --oneline --decorate
   ```

### Exercício 5: Exclusão de Ficheiros Não-Rastreados (`.gitignore`)

Binários compilados (`*.o`), dependências (`node_modules/`, `.venv/`), segredos locais (`.env`) e metadados do sistema (`.DS_Store`) nunca devem ser versionados.

1. Simule a presença de um ficheiro de credenciais sensíveis e de um binário compilado no *Working Tree*:
   ```bash
   $ echo "API_SECRET_KEY=9988776655" > .env
   $ touch modulo.o
   $ git status
   ```
2. Crie o ficheiro `.gitignore` com as regras de exclusão estudadas:
   ```bash
   $ cat << 'EOF' > .gitignore
   # Binários e diretórios de compilação
   bin/
   build/
   *.o

   # Ambientes virtuais Python
   .venv/
   __pycache__/

   # Ficheiros sensíveis e de configuração local
   .env
   .DS_Store
   EOF
   ```
3. Verifique com `git status` que `.env` e `modulo.o` deixaram de ser listados como *Untracked*:
   ```bash
   $ git status
   ```
4. Indexe e consolide o `.gitignore` com o tipo `chore:`:
   ```bash
   $ git add .gitignore
   $ git commit -m "chore: configura regras de exclusão no .gitignore"
   ```

-----

## Parte 2: Ramificação, Integração & Resolução de Conflitos

Nesta parte (correspondente à **Parte III** dos slides teóricos), irá explorar o modelo de ramificação em $O(1)$ do Git, comparar os dois tipos de `git merge` (*Fast-Forward* vs. *3-Way Merge*), linearizar o histórico com `git rebase` e resolver conflitos de fusão.

### Exercício 6: Paradigma de Branches ($O(1)$) e Comandos de Gestão

No Git, um ramo é apenas um ficheiro de **41 bytes** (40 caracteres do hash SHA-1 + `\n`) guardado em `.git/refs/heads/`.

1. Crie e mude para um novo ramo `feature-login` num único passo utilizando a sintaxe moderna recomendada (`git switch -c`):
   ```bash
   $ git switch -c feature-login
   ```
   *(Nota: Na sintaxe clássica equivalente utilizava-se `git checkout -b feature-login`).*
2. Verifique como o Git representa este ramo internamente em `.git/`:
   ```bash
   $ cat .git/HEAD
   $ cat .git/refs/heads/feature-login
   $ wc -c .git/refs/heads/feature-login
   ```
   > **Confirmação Experimental:** O ficheiro `.git/refs/heads/feature-login` tem exatamente **41 bytes**! E o `.git/HEAD` aponta simbolicamente para `ref: refs/heads/feature-login`.
3. Liste todos os ramos existentes:
   ```bash
   $ git branch -a
   ```
4. Crie um ficheiro `login.html` para desenvolver esta funcionalidade isoladamente:
   ```html
   <!DOCTYPE html>
   <html lang="pt">
   <head>
       <meta charset="UTF-8">
       <title>Autenticação - Portal IEI</title>
   </head>
   <body>
       <h1>Iniciar Sessão</h1>
   </body>
   </html>
   ```
5. Indexe e faça commit no ramo `feature-login`:
   ```bash
   $ git add login.html
   $ git commit -m "feat(auth): cria página de autenticação de utilizadores"
   ```
6. Comute de volta para `main` e observe o *Working Tree*:
   ```bash
   $ git switch main
   $ ls -la
   ```
   O ficheiro `login.html` desapareceu do diretório de trabalho, pois pertence exclusivamente ao ramo `feature-login`.

### Exercício 7: Estratégias de Integração com `git merge` (*Fast-Forward* vs. *3-Way*)

1. **Cenário 1 — Fusão *Fast-Forward* (Linear):**
   Como o ramo `main` não recebeu novos commits desde a criação de `feature-login`, integre o ramo executando a sequência de comandos estudada:
   ```bash
   $ git switch main
   $ git merge feature-login
   ```
   Observe a mensagem `Fast-forward`: o ponteiro `main` simplesmente deslizou em $O(1)$ para o commit de `feature-login`, **sem criar nenhum commit de fusão**.
2. Elimine com segurança o ramo `feature-login` já integrado:
   ```bash
   $ git branch -d feature-login
   ```
3. **Cenário 2 — Fusão *3-Way Merge* (Ramos Divergentes):**
   Vamos agora criar uma divergência real entre `main` e um novo ramo `feature-estilos`:
   ```bash
   # 1. Criar e comutar para o ramo feature-estilos
   $ git switch -c feature-estilos
   $ echo "body { font-family: Arial, sans-serif; }" > style.css
   $ git add style.css
   $ git commit -m "feat(ui): adiciona folha de estilos CSS"

   # 2. Regressar ao main e realizar um commit independente noutro ficheiro
   $ git switch main
   $ echo "Licença MIT - 2026" > LICENSE
   $ git add LICENSE
   $ git commit -m "docs: adiciona ficheiro de licença MIT"
   ```
4. Agora as duas histórias divergiram a partir do seu ancestral comum. Integre `feature-estilos` em `main`:
   ```bash
   $ git merge feature-estilos -m "Merge branch 'feature-estilos' into main"
   ```
5. Visualize o grafo resultante e elimine o ramo temporário:
   ```bash
   $ git log --graph --oneline --all
   $ git branch -d feature-estilos
   ```
   > **Observação:** Como os ramos tinham divergido, o Git executou um **3-Way Merge**, criando um novo **Commit de Fusão (*Merge Commit*)** com dois pais!

### Exercício 8: Linearização do Histórico com `git rebase`

Como vimos nos slides teóricos, sincronizações repetidas via *3-Way Merge* geram históricos complexos ("grafo *spaghetti*"). O `git rebase` resolve este problema reaplicando os commits do ramo de funcionalidade sobre o topo atualizado de `main`.

1. Crie um novo ramo `feature-perfil` e registe um commit:
   ```bash
   $ git switch -c feature-perfil
   $ echo "<h1>Perfil do Estudante</h1>" > perfil.html
   $ git add perfil.html
   $ git commit -m "feat(perfil): adiciona página de perfil do estudante"
   ```
2. Regresse ao `main` e simule uma atualização concorrente na linha principal:
   ```bash
   $ git switch main
   $ echo "Versão: 0.2.0" >> README.md
   $ git add README.md
   $ git commit -m "docs: regista número de versão no README"
   ```
3. Os ramos `main` e `feature-perfil` voltaram a divergir! Em vez de usar `git merge` (que criaria uma nova bifurcação), comute para `feature-perfil` e linearize-o sobre `main` com `git rebase`:
   ```bash
   $ git switch feature-perfil
   $ git rebase main
   ```
   > **Mecanismo Interno:** O Git "desprendeu" o commit de `feature-perfil` e reaplicou-o sobre o topo mais recente de `main`, gerando um novo commit (`E'`) com novo hash SHA.
4. Agora regresse ao `main` e integre `feature-perfil`:
   ```bash
   $ git switch main
   $ git merge feature-perfil
   $ git branch -d feature-perfil
   ```
5. Inspecione o histórico com `git log --graph --oneline`:
   ```bash
   $ git log --graph --oneline
   ```
   Repare que a integração ocorreu por **Fast-Forward** e o topo do histórico manteve-se **estritamente linear**!
   > **Regra de Ouro do Rebase:** **NUNCA** execute `git rebase` sobre ramos públicos partilhados com colegas, pois a reescrita de hashes SHA quebra a sincronização da equipa.

### Exercício 9: Deteção e Resolução de Conflitos de Merge

Um conflito ocorre quando dois ramos alteram **as mesmas linhas no mesmo ficheiro** de forma contraditória.

1. Em `main`, crie um ficheiro de configuração `config.txt`:
   ```bash
   $ echo "timeout_ms = 5000" > config.txt
   $ git add config.txt
   $ git commit -m "chore(config): define timeout padrão de 5000ms"
   ```
2. Crie um ramo `feature-timeout` e altere o valor para `10000`:
   ```bash
   $ git switch -c feature-timeout
   $ echo "timeout_ms = 10000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): aumenta timeout para 10000ms em redes lentas"
   ```
3. Volte ao `main` e altere a **mesma linha** de `config.txt` para `3000`:
   ```bash
   $ git switch main
   $ echo "timeout_ms = 3000" > config.txt
   $ git add config.txt
   $ git commit -m "perf(config): reduz timeout para 3000ms no ramo principal"
   ```
4. Tente integrar `feature-timeout` em `main`:
   ```bash
   $ git merge feature-timeout
   ```
   O Git suspende o merge e emite o aviso:
   ```text
   Auto-merging config.txt
   CONFLICT (content): Merge conflict in config.txt
   Automatic merge failed; fix conflicts and then commit the result.
   ```
5. Inspecione o conteúdo de `config.txt` para observar os marcadores visuais injetados pelo Git:
   ```bash
   $ cat config.txt
   ```
   ```text
   <<<<<<< HEAD
   timeout_ms = 3000
   =======
   timeout_ms = 10000
   >>>>>>> feature-timeout
   ```
6. **Protocolo de Resolução (4 passos dos slides teóricos):**
   * **Passo 1 & 2:** Decida o valor final (ex.: `8000`) e substitua o conteúdo do ficheiro **eliminando todos os marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`):
     ```bash
     $ echo "timeout_ms = 8000" > config.txt
     ```
   * **Passo 3:** Adicione o ficheiro resolvido à *Staging Area*:
     ```bash
     $ git add config.txt
     ```
   * **Passo 4:** Conclua o merge commit:
     ```bash
     $ git commit -m "fix(config): resolve conflito de merge com timeout 8000"
     $ git branch -d feature-timeout
     ```

-----

## Parte 3: Colaboração Distribuída, Workflows & GitHub Releases

Nesta parte final (correspondente à **Parte IV** dos slides teóricos), irá publicar o projeto no GitHub, sincronizar alterações remotas (`fetch`, `pull`, `push`), executar o modelo colaborativo proposto (**Scaled Trunk-Based Development com Feature Branches e Pull Requests**) e lançar uma **GitHub Release**.

### Exercício 10: Repositórios Remotos (`origin`) e Sincronização (`push`, `fetch`, `pull`)

1. No seu browser, aceda a [GitHub.com](https://github.com/) e crie um **novo repositório vazio**:
   * **Repository name:** `iei-projeto-git`
   * **Visibility:** Public
   * **Importante:** **NÃO** selecione *Add a README file*, `.gitignore` ou *license*. Clique em **Create repository**.
2. No seu terminal local (`~/IEI/aula06/meu-projeto`), associe o repositório remoto sob o nome convencional `origin`:
   ```bash
   # Substitua <UTILIZADOR> pelo seu username do GitHub
   $ git remote add origin git@github.com:<UTILIZADOR>/iei-projeto-git.git
   $ git remote -v
   ```
   *(Se utilizar HTTPS/PAT, use `https://github.com/<UTILIZADOR>/iei-projeto-git.git`).*
3. **Publicar o ramo local (`git push`):**
   ```bash
   $ git push -u origin main
   ```
   Atualize a página do GitHub no browser e confirme que todo o código e histórico estão agora alojados na nuvem.
4. **Diferença prática entre `git fetch` e `git pull`:**
   * Na interface web do GitHub, clique no ficheiro `README.md`, clique no ícone de lápis (**Edit this file**), adicione uma linha no final (`## Equipa de Desenvolvimento`) e clique em **Commit changes...** diretamente no browser.
   * O servidor remoto (`origin/main`) tem agora um commit novo que o seu computador desconhece!
   * No terminal local, execute primeiro `git fetch origin`:
     ```bash
     $ git fetch origin
     $ cat README.md
     $ git log --graph --oneline --all
     ```
     > **Verificação:** Como estudado nos slides, o `git fetch` descarregou o novo commit do servidor (visível em `origin/main` no `git log`), mas **não alterou os ficheiros do seu Working Tree**!
   * Agora integre as alterações descarregadas no seu ramo `main` local:
     ```bash
     $ git pull --rebase origin main
     $ cat README.md
     ```

### Exercício 11: Modelo Proposto — Workflow Trunk-Based com Feature Branches & Pull Requests

Nos projetos em equipa, adotamos o **Scaled Trunk-Based Development**: criamos *Short-Lived Feature Branches* a partir de `main`, mantemo-los atualizados com `rebase` e integramo-los através de **Pull Requests (PR)** com **Revisão de Código (*Code Review*)**.

Execute a sequência completa passo a passo (idêntica ao exemplo prático dos slides teóricos):

```bash
# 1. Garantir que o ramo 'main' local está sincronizado
# e criar o feature branch de curta duração
$ git switch main && git pull --rebase
$ git switch -c feat/autenticacao-oauth
```

2. **Desenvolver de forma iterativa com commits pequenos e atómicos (Conventional Commits):**
   ```bash
   $ echo "<h2>Autenticação Segura via OAuth2</h2>" >> login.html
   $ git add login.html
   $ git commit -m "feat(auth): adiciona suporte a autenticação OAuth2"
   ```
3. **Antes de submeter, atualizar o `main` e linearizar o feature branch (prevenir conflitos):**
   ```bash
   $ git switch main && git pull --rebase
   $ git switch feat/autenticacao-oauth && git rebase main
   ```
4. **Publicar o ramo no repositório remoto:**
   ```bash
   $ git push -u origin feat/autenticacao-oauth
   ```
5. **Abrir o Pull Request e realizar *Code Review* no GitHub:**
   * Aceda à página do seu repositório no GitHub e clique no botão verde **Compare & pull request**.
   * Confirme a direção da fusão: `base: main` $\leftarrow$ `compare: feat/autenticacao-oauth`.
   * Preencha a descrição explicando o objetivo da funcionalidade e clique em **Create pull request**.
   * Na página do Pull Request, clique no separador **Files changed**, passe o cursor sobre a linha adicionada em `login.html`, clique no botão `+` e adicione um comentário de revisão (*Code Review*).
   * Regresse ao separador **Conversation** e conclua a integração clicando em **Merge pull request** $\rightarrow$ **Confirm merge**.
6. **Após aprovação e merge do PR no GitHub, atualizar o `main` local e remover o ramo temporário:**
   ```bash
   $ git switch main && git pull --rebase
   $ git branch -d feat/autenticacao-oauth
   $ git log --oneline -5
   ```

### Exercício 12: Publicação de Versões e GitHub Releases

Para encerrar o ciclo de desenvolvimento, vamos etiquetar a versão estável `v1.0.0` (após o merge do Pull Request) e publicar uma **GitHub Release** oficial:

1. No terminal (no ramo `main` atualizado), crie a tag leve `v1.0.0`:
   ```bash
   $ git tag v1.0.0
   ```
2. Como o `git push` padrão não transfere etiquetas para o servidor, publique a tag explicitamente no remoto `origin`:
   ```bash
   $ git push origin v1.0.0
   ```
   *(Nota: Para enviar todas as tags locais de uma só vez, pode também utilizar `git push origin --tags`).*
3. **Criar a Release na plataforma GitHub:**
   * Na página principal do repositório no GitHub, localize a secção **Releases** (barra lateral direita) e clique em **Create a new release** (ou **Draft a new release**).
   * Em **Choose a tag**, selecione `v1.0.0`.
   * Em **Release title**, escreva `v1.0.0 — Primeira Versão Estável`.
   * Clique no botão **Generate release notes** (para ver como o GitHub gera automaticamente o *changelog* a partir dos seus *Conventional Commits* e *Pull Requests*!) e clique em **Publish release**.

-----

## Parte 4: Desafios Autónomos de Consolidação

Para consolidar as suas competências, experimente os seguintes desafios autónomos:

### Desafio A: A "Máquina do Tempo" e o Estado *Detached HEAD*
1. Consulte o histórico compacto: `git log --oneline`.
2. Escolha o hash SHA do seu primeiro commit (ex.: `98ca9c2`) e execute:
   ```bash
   $ git checkout <HASH_DO_PRIMEIRO_COMMIT>
   ```
3. Execute `git status` e verifique que o Git avisa que está em **Detached HEAD** (o ponteiro `HEAD` aponta diretamente para um commit em vez de apontar simbolicamente para um ramo).
4. Verifique com `ls` que todos os ficheiros criados depois desse commit desapareceram temporariamente do *Working Tree*.
5. Regresse imediatamente ao presente em segurança com:
   ```bash
   $ git switch main
   ```

### Desafio B: Localização Rápida de Alterações com `git log -S`
1. Suponha que pretende descobrir exatamente em que commit foi introduzida a expressão `"OAuth2"` no projeto:
   ```bash
   $ git log -S "OAuth2" -p
   ```
2. Observe como a opção `-S` (*pickaxe*) pesquisa na história os commits que adicionaram ou removeram ocorrências dessa string.

-----

## Síntese dos Comandos Essenciais Abordados

| Comando | Descrição Operacional |
| :--- | :--- |
| `git init` | Inicializa um novo repositório Git local (`.git/`). |
| `git clone <url>` | Clona um repositório remoto completo para a máquina local. |
| `git status` | Inspeciona o estado dos ficheiros no *Working Tree* e *Staging Area*. |
| `git add <ficheiro>` | Promove alterações do *Working Tree* para a *Staging Area*. |
| `git restore --staged <fich>` | Retira um ficheiro da *Staging Area* sem alterar o *Working Tree*. |
| `git commit -m "<msg>"` | Grava o conteúdo da *Staging Area* num novo snapshot imutável. |
| `git commit --amend` | Substitui o último commit local corrigindo a mensagem ou conteúdo. |
| `git log --oneline --graph` | Visualiza o histórico e a topologia de ramos de forma compacta. |
| `git tag v1.0.0` | Cria uma etiqueta leve (*lightweight tag*) no commit atual (`HEAD`). |
| `git branch -a` | Lista todos os ramos locais e remotos conhecidos. |
| `git switch <ramo>` | Comuta para um ramo existente atualizando o *Working Tree*. |
| `git switch -c <novo-ramo>` | Cria um novo ramo e comuta imediatamente para ele. |
| `git merge <ramo>` | Integra o ramo especificado no ramo ativo (*Fast-Forward* ou *3-Way*). |
| `git rebase main` | Lineariza o ramo atual reaplicando os seus commits sobre o topo de `main`. |
| `git branch -d <ramo>` | Elimina com segurança um ramo local já integrado. |
| `git remote add origin <url>` | Regista um servidor remoto sob o identificador padrão `origin`. |
| `git fetch origin` | Descarrega novidades do remoto sem alterar o *Working Tree* local. |
| `git pull --rebase` | Sincroniza o ramo local linearizando-o sobre o topo do servidor remoto. |
| `git push -u origin <ramo>` | Publica os commits do ramo local no repositório remoto. |
| `git push origin v1.0.0` | Publica explicitamente uma etiqueta de versão no servidor remoto. |
