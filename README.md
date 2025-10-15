# Painel de Controle - IrrigaPro

Dashboard para visualização de dados de sensores de EC e PH, e tempo de funcionamento de bombas de irrigação.

## Requisitos

- Python 3
- Bibliotecas listadas no arquivo `requirements.txt`

## Como Executar

1.  **Clone ou copie os arquivos do projeto.**

2.  **Crie e ative um ambiente virtual:**

    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o dashboard:**
    ```bash
    python3 dashboard.py
    ```

5.  Acesse o dashboard no seu navegador no endereço `http://127.0.0.1:8050/`.