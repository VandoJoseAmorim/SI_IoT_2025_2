# Roteiro e Material de Aula: Construindo Dashboards com Flask e Dash para ESP32

## Introdução

Este material didático tem como objetivo guiar o aprendizado na criação de dashboards interativos utilizando Python, com foco na integração com dispositivos embarcados como o ESP32. Abordaremos os conceitos fundamentais do Flask e Dash, comunicação HTTP e visualização de dados, utilizando como base o exemplo `dashboardESP32_v1.py`.

## Módulo 1: Fundamentos de Dashboards e Comunicação com ESP32

### 1.1. O que é um Dashboard e Por que Usar Python?

Um **dashboard** é uma interface gráfica que apresenta visualmente indicadores chave de desempenho (KPIs), métricas e dados relevantes, permitindo o monitoramento e a análise rápida de um sistema ou processo. Sua importância reside na capacidade de consolidar informações complexas em um formato de fácil compreensão, auxiliando na tomada de decisões e no controle de operações. No contexto de sistemas embarcados, dashboards são cruciais para monitorar sensores, controlar atuadores e visualizar o estado do hardware em tempo real [1].

A escolha do **Python** para o desenvolvimento de dashboards é justificada por seu vasto ecossistema de bibliotecas, que simplificam tarefas como manipulação de dados, criação de interfaces web e visualização gráfica. A linguagem é conhecida por sua sintaxe clara e facilidade de uso, o que acelera o desenvolvimento. A combinação de frameworks como Flask e Dash em Python oferece uma solução robusta e flexível para construir aplicações web interativas e analíticas.

Neste projeto, a arquitetura geral envolve um **dispositivo ESP32** atuando como a camada de hardware, responsável pela coleta de dados de sensores e pelo controle de atuadores. Um **dashboard web** desenvolvido em Python (com Flask e Dash) serve como a camada de software, que se comunica com o ESP32 para obter e exibir dados, além de enviar comandos de controle.

### 1.2. Comunicação HTTP com ESP32

O **ESP32** é um microcontrolador popular para projetos de IoT (Internet das Coisas) devido à sua capacidade de conectividade Wi-Fi e Bluetooth. Ele pode ser programado para atuar como um **servidor web**, expondo dados de sensores e funcionalidades de controle através de **endpoints HTTP**. Isso significa que outros dispositivos na rede, como o nosso dashboard Python, podem enviar requisições HTTP para o ESP32 para solicitar informações ou enviar comandos, estabelecendo uma comunicação bidirecional [2].

O **Protocolo HTTP (Hypertext Transfer Protocol)** é a base da comunicação de dados na World Wide Web, definindo um conjunto de regras para a troca de mensagens entre clientes (o dashboard Python) e servidores (o ESP32). As requisições HTTP mais comuns incluem:

*   **GET:** Utilizada para solicitar dados de um recurso específico no servidor. No exemplo do `dashboardESP32_v1.py`, o dashboard usa requisições `GET` para obter dados de temperatura, umidade e o status de componentes como botões, motores e alarmes do ESP32.
*   **POST:** Embora o exemplo utilize `GET` para enviar comandos de controle, o método `POST` é geralmente mais apropriado para enviar dados ao servidor com o intuito de criar ou atualizar um recurso, seguindo as boas práticas de design de APIs RESTful.

Os **códigos de status HTTP** são respostas numéricas enviadas pelo servidor para indicar o resultado de uma requisição. Por exemplo, um `200 OK` significa que a requisição foi bem-sucedida, enquanto um `404 Not Found` indica que o recurso solicitado não foi encontrado.

A **biblioteca `requests`** em Python é uma ferramenta amplamente utilizada para simplificar a interação com APIs web e fazer requisições HTTP. Ela abstrai a complexidade da comunicação de rede, tornando o envio e recebimento de dados via HTTP muito mais fácil e intuitivo. No `dashboardESP32_v1.py`, a classe `ESP32Controller` faz uso extensivo da biblioteca `requests` para interagir com o ESP32.

#### Objeto `ESP32Controller`

A classe `ESP32Controller` (linhas 23-49 do `dashboardESP32_v1.py`) é projetada para encapsular toda a lógica de comunicação com o dispositivo ESP32. Ela centraliza as operações de requisição HTTP, tornando o código mais organizado e reutilizável. Seus métodos são:

*   **`__init__(self, ip_address)`:** O construtor inicializa o objeto com o endereço IP do ESP32, que é então utilizado para formar a `base_url` para todas as requisições subsequentes. Isso permite que o endereço do ESP32 seja facilmente configurado e alterado.

    ```python
    class ESP32Controller:
        def __init__(self, ip_address):
            self.ip = ip_address
            self.base_url = f"http://{ip_address}"
    ```

*   **`get_sensor_data(self)`:** Este método realiza uma requisição HTTP `GET` para a `base_url` do ESP32. Ele espera que o ESP32 retorne uma resposta no formato JSON contendo os dados dos sensores. Um `timeout` de 5 segundos é configurado para evitar que a aplicação fique bloqueada indefinidamente caso o ESP32 não responda. Em caso de sucesso (status `200 OK`), o método extrai os dados JSON e retorna o primeiro item da lista de dados (assumindo que o ESP32 envia uma lista de dicionários, onde o primeiro contém os dados mais recentes). Se a requisição falhar ou os dados estiverem vazios, `None` é retornado.

    ```python
    def get_sensor_data(self):
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else None
            return None
        except requests.exceptions.RequestException:
            return None
    ```

*   **`control_motor(self, action)`:** Este método é responsável por enviar comandos ao ESP32 para controlar o motor. Ele aceita uma `action` (string, como "ligar" ou "desligar") e constrói o endpoint HTTP apropriado (`/motor1_h` para ligar, `/motor1_l` para desligar). Uma requisição `GET` é então enviada ao ESP32. O método retorna `True` se a requisição for bem-sucedida (código de status `200`), e `False` em caso de falha. Um `timeout` mais curto (2 segundos) é usado aqui, refletindo a expectativa de uma resposta rápida para operações de controle.

    ```python
    def control_motor(self, action):
        try:
            endpoint = "/motor1_h" if action == "ligar" else "/motor1_l"
            r = requests.get(f"{self.base_url}{endpoint}", timeout=2)
            return r.status_code == 200
        except:
            return False
    ```

*   **`control_alarm(self, action)`:** Este método funciona de maneira análoga ao `control_motor`, mas é dedicado ao controle do alarme, utilizando os endpoints `/alarme_h` e `/alarme_l`. É crucial notar que o código original contém um erro de digitação na condição de retorno (`return r.status_code == 2002`), que deveria ser `return r.status_code == 200` para verificar corretamente o sucesso da requisição HTTP. Este erro deve ser corrigido para garantir o funcionamento adequado do controle do alarme.

    ```python
    def control_alarm(self, action):
        try:
            endpoint = "/alarme_h" if action == "ligar" else "/alarme_l"
            r = requests.get(f"{self.base_url}{endpoint}", timeout=2)
            return r.status_code == 200 # CORREÇÃO: Era 2002 no original
        except:
            return False
    ```

## Módulo 2: Construindo o Backend com Flask e Dash

### 2.1. Introdução ao Flask

**Flask** é um **microframework web** para Python, valorizado por sua simplicidade e flexibilidade. Ele fornece as ferramentas essenciais para o desenvolvimento de aplicações web, permitindo que os desenvolvedores escolham as bibliotecas e componentes adicionais que melhor se adequam às necessidades de cada projeto. No contexto do nosso dashboard, o Flask atua como o servidor web subjacente que hospeda a aplicação Dash. Sua função principal é gerenciar as requisições HTTP recebidas e servir as páginas web geradas pelo Dash [3].

A inicialização de uma aplicação Flask é um processo direto:

```python
from flask import Flask
server = Flask(__name__)
```

Neste trecho, `from flask import Flask` importa a classe `Flask` da biblioteca homônima. Em seguida, `server = Flask(__name__)` cria uma instância da aplicação Flask. O argumento `__name__` é uma variável especial do Python que contém o nome do módulo atual, o que auxilia o Flask a localizar recursos como templates e arquivos estáticos de forma eficiente.

### 2.2. Introdução ao Dash

**Dash** é um framework de código aberto desenvolvido pela Plotly, projetado especificamente para a construção de **aplicações analíticas interativas** em Python. Ele permite que desenvolvedores criem interfaces de usuário complexas e ricas em dados utilizando exclusivamente Python, eliminando a necessidade de escrever código JavaScript, HTML ou CSS diretamente. O Dash é construído sobre tecnologias web robustas como Flask (para o backend), React.js (para o frontend) e Plotly.js (para visualização de gráficos), combinando a força do Python com a interatividade das bibliotecas JavaScript modernas [4].

A integração do Dash com uma aplicação Flask existente é uma de suas características mais poderosas, como demonstrado no `dashboardESP32_v1.py`:

```python
import dash
app = dash.Dash(__name__, server=server, url_base_pathname="/")
```

Aqui, `import dash` importa a biblioteca Dash. A linha `app = dash.Dash(__name__, server=server, url_base_pathname="/")` cria uma instância da aplicação Dash. O argumento `server=server` é fundamental, pois ele instrui o Dash a utilizar a instância do Flask (`server`) que já foi previamente criada. O parâmetro `url_base_pathname="/"` define que a aplicação Dash será acessível a partir da raiz do servidor Flask, ou seja, no endereço principal da aplicação web.

### 2.3. Layout da Aplicação Dash

O **layout** de uma aplicação Dash é a representação da estrutura visual da interface do usuário. Ele é construído como uma hierarquia de componentes Python que correspondem a elementos HTML. O Dash oferece dois tipos principais de componentes para a construção do layout:

*   **Componentes HTML (`dash.html`):** Estes componentes mapeiam diretamente para tags HTML padrão. Exemplos incluem `html.Div` para criar divisões lógicas na página, `html.H1` para títulos de nível 1, `html.P` para parágrafos, e `html.Button` para botões interativos. Eles são utilizados para estruturar o conteúdo e aplicar estilos básicos à interface.
*   **Componentes Core (`dash.dcc`):** São componentes interativos de nível superior que oferecem funcionalidades mais complexas. Entre eles, destacam-se `dcc.Graph` para exibir gráficos gerados pelo Plotly, `dcc.Dropdown` para menus suspensos, `dcc.Input` para campos de entrada de texto e `dcc.Interval` para disparar callbacks em intervalos de tempo regulares, permitindo atualizações automáticas.

No `dashboardESP32_v1.py`, o `app.layout` (linhas 100-134) é definido como um `html.Div` principal que engloba todos os elementos visuais do dashboard. Cada componente dentro do layout possui um `id` único, que é essencial para que os callbacks do Dash possam referenciá-los e gerenciar suas interações. A estrutura do layout é a seguinte:

```python
app.layout = html.Div([
    html.H1("🌡️ Painel de Controle ESP32"),
    html.Div(id="status-connection", style={"margin": "10px 0"}),
    html.Button("Atualizar Dados", id="btn-update", n_clicks=0),
    dcc.Interval(id="auto-update", interval=5000, n_intervals=0), # auto refresh a cada 5s
    html.Div([
        dcc.Graph(id="temp-hum-graph"),
    ]),
    html.Div([
        html.H3("📊 Dados Atuais"),
        html.Div(id="current-data")
    ]),
    html.Div([
        html.H3("🎛️ Controles"),
        html.Button("▶️ Ligar Motor", id="btn-motor-on"),
        html.Button("⏹️ Desligar Motor", id="btn-motor-off"),
        html.Button("🔔 Ativar Alarme", id="btn-alarm-on"),
        html.Button("🔕 Desativar Alarme", id="btn-alarm-off"),
    ], style={"marginTop": "20px"}),
    html.Div([
        html.H3("📋 Dados Recentes"),
        html.Div(id="recent-data-table")
    ])
])
```

Analisando os principais componentes do layout:

*   `html.H1("🌡️ Painel de Controle ESP32")`: Define o título principal do dashboard.
*   `html.Div(id="status-connection")`: Uma divisão HTML que será atualizada dinamicamente para exibir o status da conexão com o ESP32.
*   `html.Button("Atualizar Dados", id="btn-update")`: Um botão que, ao ser clicado, dispara um callback para realizar a atualização manual dos dados.
*   `dcc.Interval(id="auto-update", interval=5000)`: Um componente crucial para a interatividade em tempo real, que dispara um evento a cada 5000 milissegundos (5 segundos), permitindo a atualização automática do dashboard.
*   `dcc.Graph(id="temp-hum-graph")`: Onde o gráfico interativo de temperatura e umidade, gerado pelo Plotly, será renderizado.
*   `html.Div(id="current-data")`: Uma divisão destinada a exibir os dados mais recentes provenientes dos sensores e atuadores do ESP32.
*   Os botões com `id`s como `btn-motor-on`, `btn-motor-off`, `btn-alarm-on`, `btn-alarm-off` representam os controles para interagir diretamente com o ESP32, ligando ou desligando o motor e ativando ou desativando o alarme.
*   `html.Div(id="recent-data-table")`: Uma divisão para apresentar uma tabela com os dados históricos mais recentes coletados.

## Módulo 3: Interatividade e Visualização de Dados

### 3.1. Callbacks no Dash

Os **callbacks** são o mecanismo central que impulsiona a interatividade em aplicações Dash. Eles são funções Python que são automaticamente executadas em resposta a mudanças em propriedades de componentes de entrada (`Input`) e, por sua vez, atualizam propriedades de componentes de saída (`Output`). Essa arquitetura reativa permite a construção de dashboards dinâmicos e responsivos sem a necessidade de escrever código JavaScript diretamente [5].

O decorador `@app.callback` é utilizado para registrar uma função como um callback. Ele requer uma lista de `Output`s (os componentes e suas propriedades a serem atualizadas) e uma lista de `Input`s (os componentes e suas propriedades que, ao serem alteradas, disparam o callback). A sintaxe básica é a seguinte:

```python
@app.callback(
    Output("id-do-componente-saida", "propriedade-da-saida"),
    Input("id-do-componente-entrada", "propriedade-da-entrada")
)
def minha_funcao_callback(valor_da_entrada):
    # Lógica para processar o valor da entrada e gerar o novo valor para a saída
    return novo_valor_para_saida
```

No `dashboardESP32_v1.py`, a função `update_dashboard` (linhas 140-216) serve como o callback principal, gerenciando uma ampla gama de interações e atualizações no dashboard. Ela é acionada por diversos eventos, incluindo cliques nos botões de controle do motor e alarme, cliques no botão de atualização manual e os disparos periódicos do componente `dcc.Interval` para atualização automática.

Para identificar qual `Input` específico disparou o callback, o objeto `dash.callback_context` (acessado via `ctx`) é uma ferramenta poderosa. A propriedade `ctx.triggered` retorna uma lista de dicionários, onde cada dicionário descreve o componente que causou o disparo do callback. A informação `ctx.triggered[0]["prop_id"]` contém o `id` do componente e a propriedade que foi alterada (por exemplo, `btn-motor-on.n_clicks`). Essa capacidade permite que a função `update_dashboard` execute lógicas condicionais, adaptando seu comportamento com base na interação específica do usuário.

#### Análise do Callback Principal (`update_dashboard`)

Este callback multifuncional é responsável por coordenar as seguintes ações:

1.  **Detecção de Ações de Controle:** Primeiramente, ele verifica se um dos botões de controle (motor ou alarme) foi clicado. Se uma ação de controle for detectada, o método correspondente do `ESP32Controller` (`control_motor` ou `control_alarm`) é invocado para enviar o comando ao ESP32. O `connection_status` é então atualizado para refletir o resultado da operação.
2.  **Busca de Dados do ESP32:** Independentemente do evento que disparou o callback, a função sempre tenta obter os dados mais recentes do ESP32 através de `esp32.get_sensor_data()`. Isso garante que o dashboard esteja sempre exibindo informações atualizadas.
3.  **Atualização do Histórico:** Os dados recém-obtidos são processados e adicionados ao `data_history`, e o `connection_status` é atualizado pela função `update_data_history()`.
4.  **Geração do Gráfico:** O gráfico de temperatura e umidade é recriado com os dados mais recentes utilizando a função `create_temperature_humidity_chart()`, garantindo que a visualização esteja sempre atualizada.
5.  **Exibição de Dados Atuais:** Os dados mais recentes dos sensores e atuadores são formatados em elementos HTML (`html.P`) e preparados para serem exibidos na seção "Dados Atuais" do dashboard.
6.  **Atualização do Status da Conexão:** O status da conexão (indicando se o ESP32 está conectado ou desconectado) e a hora da última atualização são exibidos de forma clara, utilizando ícones visuais (círculo verde para conectado, vermelho para desconectado).
7.  **Exibição da Tabela de Dados Recentes:** Os últimos 10 registros do `data_history` são convertidos em um `pandas.DataFrame` e formatados como uma tabela HTML, proporcionando uma visão tabular dos dados históricos.
8.  **Retorno das Saídas:** Finalmente, a função retorna os quatro elementos de saída (o objeto do gráfico, os dados atuais formatados, a string de status da conexão e a tabela de dados recentes) na ordem exata especificada no decorador `@app.callback`. Estes valores são então utilizados pelo Dash para atualizar a interface do usuário.

### 3.2. Gerenciamento de Dados

Para um dashboard que monitora dados em tempo real, o gerenciamento eficiente do histórico de dados é fundamental. O `dashboardESP32_v1.py` emprega duas ferramentas principais para essa finalidade:

*   **`collections.deque`:** Uma `deque` (double-ended queue) é uma estrutura de dados que se assemelha a uma lista, mas é otimizada para operações de adição e remoção de elementos em ambas as extremidades de forma eficiente. Sua principal vantagem neste contexto é a capacidade de definir um `maxlen` (tamanho máximo). Quando a `deque` atinge seu limite de tamanho, a adição de um novo elemento automaticamente remove o elemento mais antigo. Essa característica a torna ideal para manter um histórico de dados de tamanho fixo, prevenindo o consumo excessivo de memória ao longo do tempo [6].

    ```python
    from collections import deque
    data_history = deque(maxlen=100) # Armazena os últimos 100 conjuntos de dados
    ```

*   **`pandas.DataFrame`:** A biblioteca **Pandas** é uma ferramenta indispensável para análise e manipulação de dados em Python. O `DataFrame` é sua estrutura de dados central, projetada para representar dados tabulares (organizados em linhas e colunas) de maneira eficiente e flexível. A conversão do `data_history` em um `DataFrame` simplifica significativamente tarefas como filtragem, ordenação e preparação dos dados para visualização, como é feito na função `create_temperature_humidity_chart()` e na geração da tabela de dados recentes [7].

    ```python
    import pandas as pd
    # ...
    df = pd.DataFrame(list(data_history))
    ```

#### Função `update_data_history(data)`

Esta função (linhas 52-67) é crucial para processar os dados brutos recebidos do ESP32 e integrá-los ao histórico do dashboard. Ela executa as seguintes etapas:

1.  **Verificação de Dados:** A função primeiro verifica se o parâmetro `data` não é `None`, garantindo que dados válidos foram efetivamente recebidos do ESP32.
2.  **Timestamp:** Um `timestamp` (`datetime.now()`) é adicionado ao conjunto de dados, registrando o momento exato da coleta da informação.
3.  **Formatação e Padronização:** É criado um dicionário `data_with_time`, que garante a presença de todas as chaves esperadas (`temperatura`, `umidade`, `botao`, `motor`, `alarme`). Valores padrão (por exemplo, `2` para temperatura/umidade, `0` para botão/motor/alarme) são atribuídos caso alguma chave esteja ausente nos dados recebidos, prevenindo erros e padronizando o formato.
4.  **Adição ao `deque`:** O dicionário `data_with_time` é então adicionado ao `data_history` utilizando o método `append()`. Devido à propriedade `maxlen` da `deque`, se ela já estiver cheia, o elemento mais antigo é automaticamente removido para dar lugar ao novo.
5.  **Atualização de Status:** As variáveis globais `last_update` e `connection_status` são atualizadas para refletir a conexão bem-sucedida e o momento da última atualização.
6.  **Tratamento de Desconexão:** Caso o parâmetro `data` seja `None` (indicando falha na obtenção de dados), o `connection_status` é definido como "Desconectado", informando o estado da comunicação.

### 3.3. Visualização de Dados com Plotly

**Plotly** é uma biblioteca de visualização de dados interativa e de código aberto para Python, amplamente utilizada para criar gráficos de alta qualidade que podem ser facilmente incorporados em aplicações web, como as construídas com Dash. Os gráficos gerados pelo Plotly são interativos por natureza, oferecendo funcionalidades como zoom, pan e a exibição de informações detalhadas ao passar o mouse sobre os elementos gráficos [8].

No `dashboardESP32_v1.py`, a função `create_temperature_humidity_chart()` (linhas 70-88) é responsável por construir o gráfico de linha que exibe o histórico de temperatura e umidade, utilizando os objetos de gráfico do Plotly (`plotly.graph_objects`).

#### Função `create_temperature_humidity_chart()`

Esta função orquestra a criação do gráfico interativo:

1.  **Verificação de Histórico:** Inicialmente, a função verifica se `data_history` está vazio. Se estiver, um objeto `go.Figure()` vazio é retornado para evitar erros de visualização em dashboards sem dados.
2.  **Conversão para `DataFrame`:** O `data_history` (que é uma `deque`) é convertido em um `pandas.DataFrame`. Essa conversão é fundamental, pois o `DataFrame` facilita a manipulação e o acesso aos dados de forma estruturada, o que é ideal para a criação de gráficos.
3.  **Criação da Figura:** Uma instância de `go.Figure()` é criada. Este é o objeto principal no Plotly para construir e configurar gráficos.
4.  **Adição de "Traces" (Séries de Dados):** As "traces" representam as séries de dados a serem plotadas no gráfico. Duas traces são adicionadas:
    *   Uma para a **temperatura**, utilizando os valores da coluna `temperatura` do `DataFrame` no eixo Y e os `timestamp`s no eixo X. A linha é configurada para ser vermelha e exibir tanto linhas quanto marcadores (`mode=\'lines+markers\'`).
    *   Outra para a **umidade**, de forma similar, utilizando os valores da coluna `umidade` no eixo Y, com uma linha azul e também exibindo linhas e marcadores.
5.  **Customização do Layout:** O método `fig.update_layout()` é utilizado para personalizar o layout do gráfico. Ele define o título do gráfico como "Histórico de Temperatura e Umidade" e o rótulo do eixo X como "Tempo".
6.  **Retorno:** Finalmente, o objeto `fig` do Plotly, contendo o gráfico configurado, é retornado. Este objeto será então renderizado pelo componente `dcc.Graph` no layout do Dash, tornando o gráfico visível e interativo na interface do usuário.

## Módulo 4: Execução e Considerações Finais

### 4.1. Rodando a Aplicação

Para que uma aplicação Python seja executada como um script principal, é uma prática comum utilizar o bloco `if __name__ == "__main__":`. Este bloco de código garante que o conteúdo dentro dele seja executado apenas quando o script é invocado diretamente, e não quando é importado como um módulo em outro script. No contexto do nosso dashboard, este bloco é essencial para iniciar o servidor Flask/Dash somente quando o `dashboardESP32_v1.py` é o programa principal [9].

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Dentro deste bloco, `app.run(debug=True)` inicia o servidor web. O argumento `debug=True` ativa o modo de depuração, que é extremamente valioso durante a fase de desenvolvimento. As vantagens do modo de depuração incluem:

*   **Recarregamento Automático:** O servidor reinicia automaticamente sempre que o código-fonte é modificado, eliminando a necessidade de parar e iniciar manualmente a aplicação a cada alteração.
*   **Depurador Interativo:** Em caso de erros ou exceções, um depurador interativo é exibido diretamente no navegador, permitindo ao desenvolvedor inspecionar variáveis, rastrear a pilha de chamadas e identificar a causa do problema de forma eficiente.

### 4.2. Pontos de Melhoria e Boas Práticas

Ao desenvolver sistemas como o dashboard para ESP32, é fundamental considerar aspectos que vão além da funcionalidade básica para garantir robustez, segurança e escalabilidade:

*   **Tratamento de Erros Robusto:** Embora o código já incorpore blocos `try-except` para lidar com falhas nas requisições HTTP, um sistema de produção exigiria um tratamento de erros mais sofisticado. Isso incluiria a exibição de mensagens de erro mais informativas para o usuário final (por exemplo, "ESP32 offline", "Erro ao enviar comando"), a implementação de um sistema de *logging* detalhado para facilitar a depuração e a criação de mecanismos de recuperação ou notificação em caso de falhas críticas do sistema.
*   **Segurança:** A comunicação HTTP simples (sem HTTPS) e a ausência de autenticação tornam o sistema vulnerável a ataques como interceptação de dados e controle não autorizado do dispositivo. Para ambientes de produção, é imperativo implementar medidas de segurança como:
    *   **HTTPS:** Para criptografar a comunicação entre o dashboard e o ESP32, protegendo a integridade e a confidencialidade dos dados.
    *   **Autenticação e Autorização:** Para garantir que apenas usuários ou sistemas devidamente autorizados possam acessar o dashboard e enviar comandos ao ESP32. Isso pode ser alcançado através de tokens de API, senhas, OAuth, ou outros métodos de segurança.
*   **Escalabilidade e Persistência de Dados:** O uso de `collections.deque` é uma solução excelente para manter um histórico de dados de curto prazo na memória. No entanto, para armazenar dados por períodos prolongados, realizar análises complexas ou suportar múltiplos usuários e grandes volumes de dados, a utilização de um **banco de dados** é a abordagem mais adequada. Bancos de dados relacionais (como PostgreSQL ou SQLite) ou não-relacionais (como MongoDB) permitiriam que os dados persistissem mesmo após o reinício da aplicação e facilitariam consultas e relatórios avançados.
*   **Configuração do ESP32:** O funcionamento correto do dashboard é intrinsecamente dependente do firmware carregado no ESP32. O microcontrolador deve ser programado para:
    *   Expor os endpoints HTTP corretos e esperados pelo dashboard (por exemplo, `/`, `/motor1_h`, `/alarme_l`).
    *   Responder às requisições com dados no formato JSON esperado pelo dashboard.
    *   Processar os comandos recebidos e controlar os atuadores (motor e alarme) de forma adequada.
    *   Lidar com múltiplas conexões e requisições de forma eficiente e robusta.
*   **Correção do Erro de Lógica:** Conforme identificado na análise técnica, o método `control_alarm` na classe `ESP32Controller` contém um erro de digitação na condição de retorno (`r.status_code == 2002`). Esta linha deve ser corrigida para `return r.status_code == 200` para que a verificação de sucesso da requisição HTTP funcione corretamente e o controle do alarme seja confiável.

## Referências

[1] Eckerson, W. W. (2010). *Performance Dashboards: Measuring, Monitoring, and Managing Your Business*. John Wiley & Sons.
[2] Deek, F. P., & McHugh, J. A. (2019). *Python for Programmers with Computer Science Applications*. Chapman and Hall/CRC.
[3] Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O\'Reilly Media.
[4] Plotly. (n.d.). *Dash by Plotly*. Retrieved from [https://dash.plotly.com/](https://dash.plotly.com/)
[5] Plotly. (n.d.). *Basic Callbacks*. Retrieved from [https://dash.plotly.com/basic-callbacks](https://dash.plotly.com/basic-callbacks)
[6] Python Software Foundation. (n.d.). *collections — Container datatypes*. Retrieved from [https://docs.python.org/3/library/collections.html#collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
[7] Pandas Development Team. (n.d.). *pandas: powerful Python data analysis toolkit*. Retrieved from [https://pandas.pydata.org/](https://pandas.pydata.org/)
[8] Plotly. (n.d.). *Plotly Python Open Source Graphing Library*. Retrieved from [https://plotly.com/python/](https://plotly.com/python/)
[9] Python Software Foundation. (n.d.). *The Python Tutorial - 6. Modules*. Retrieved from [https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts](https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts)

---

**Autor:** Manus AI
**Data:** 19 de Setembro de 2025
