# Painel de Controle - IrrigaPro

Dashboard para visualização de dados de sensores de EC e PH, e tempo de funcionamento de bombas de irrigação.

## Requisitos

- Python 3
- Bibliotecas listadas no arquivo `requirements.txt`

## Como Executar

1.  **Clone ou copie os arquivos do projeto.**

2.  **Navegue até o diretório do projeto:**

    Use o comando `cd` para entrar na pasta onde os arquivos do projeto estão.

    ```bash
    # Exemplo:
    cd Caminho/Para/Sua/Pasta/Do/Projeto
    ```

3.  **Crie e Ative o Ambiente Virtual**

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

4.  **Instale as Dependências**

    Instale todas as bibliotecas necessárias com o seguinte comando:

    ```bash
    pip3 install -r requirements.txt
    ```

5.  **Inicie o Painel de Controle**

    Execute o script principal do dashboard:

    ```bash
    python3 dashboard.py
    ```

## Acessando o Painel

Após o último comando, o terminal exibirá uma mensagem informando que o servidor está rodando, junto com um endereço local.

1.  Copie o endereço (geralmente `http://127.0.0.1:8050`).
2.  Cole-o na barra de endereços do seu navegador de internet.
3.  O painel de controle será carregado.