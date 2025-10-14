# Painel de Controle de Irrigação

Este projeto exibe um painel de controle (dashboard) web que monitora o tempo de funcionamento de bombas de irrigação e visualiza dados de sensores de EC (Condutividade Elétrica) e PH da água.

## Pré-requisitos

- [Python 3](https://www.python.org/downloads/) instalado.
  - **Importante (para usuários Windows):** Durante a instalação do Python, certifique-se de marcar a caixa **"Add Python to PATH"**.

## Como Executar o Projeto

Siga os passos abaixo para configurar e iniciar o painel de controle.

**1. Baixe o Projeto**

Se você recebeu os arquivos em um `.zip`, extraia-os para uma pasta no seu computador.

**2. Abra o Terminal**

Abra o seu terminal ou prompt de comando:
- **Windows:** Pesquise por `cmd` ou `PowerShell` no menu Iniciar.
- **macOS/Linux:** Pesquise por `Terminal`.

**3. Navegue até a Pasta do Projeto**

Use o comando `cd` para entrar na pasta onde os arquivos do projeto estão.

```bash
# Exemplo:
cd Caminho/Para/Sua/Pasta/Do/Projeto
```

**4. Crie e Ative o Ambiente Virtual**

Este passo cria um ambiente isolado para as dependências do projeto.

```bash
# Crie o ambiente
python -m venv venv

# Ative o ambiente
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```
*Após ativar, você verá `(venv)` no início da linha do seu terminal.*

**5. Instale as Dependências**

Instale todas as bibliotecas necessárias com o seguinte comando:

```bash
pip3 install -r requirements.txt
```

**6. Inicie o Painel de Controle**

Execute o script principal do dashboard:

```bash
python3 dashboard.py
```

## Acessando o Painel

Após o último comando, o terminal exibirá uma mensagem informando que o servidor está rodando, junto com um endereço local.

1.  Copie o endereço (geralmente `http://127.0.0.1:8050`).
2.  Cole-o na barra de endereços do seu navegador de internet.
3.  O painel de controle será carregado.
# Verdureira_IrrigaPro_DashBoard
