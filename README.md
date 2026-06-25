# Dashboard Logístico Inteligente

Dashboard interativo desenvolvido com **Streamlit** para monitoramento de atrasos logísticos e desempenho operacional em tempo real. Projeto desenvolvido como solução para o desafio **AMT01 — Visualização de dados: dashboards**.

---

## Objetivo

A solução foi criada para resolver um problema real enfrentado por empresas de logística: a dependência de planilhas extensas e relatórios manuais para monitorar entregas. O dashboard centraliza todas as informações operacionais em um único lugar, permitindo que gestores identifiquem rapidamente transportadoras problemáticas, regiões críticas e tomem decisões em tempo real — sem precisar cruzar dados manualmente.

---

## Funcionalidades

### Indicadores (KPIs)
- Total de entregas no período
- Quantidade de entregas atrasadas
- Percentual de atraso
- Transportadora mais crítica
- Média de dias de atraso

### Alertas Visuais Automáticos
- Alerta **vermelho** quando o percentual de atraso é igual ou maior que 50%
- Alerta **amarelo** entre 30% e 49%
- Alerta **verde** abaixo de 30%

### Insight Automático
Texto gerado automaticamente identificando a transportadora com mais dias acumulados de atraso, seu percentual sobre o total e a região mais crítica — com recomendação direta de ação para o gestor.

### Gráficos Interativos
- **Comparação entre transportadoras** — barras horizontais com quantidade de entregas atrasadas
- **Análise por região** — barras verticais mostrando todas as regiões, incluindo as sem atrasos
- **Pontualidade por transportadora** — barras empilhadas comparando entregas no prazo vs atrasadas
- **Ranking de atrasos** — ranking numerado (#1, #2, #3) por dias totais de atraso acumulados
- **Proporção de dias de atraso** — gráfico de pizza com a fatia de responsabilidade de cada transportadora
- **Mapa do Brasil** — mapa de bolhas mostrando a concentração de atrasos por região geográfica

### Filtros Dinâmicos
- Filtro por região
- Filtro por transportadora
- Botão de limpar filtros
- Contador dinâmico exibindo quantas entregas estão sendo analisadas

### Base de Dados
- Tabela com destaque visual automático — linhas atrasadas em **vermelho**, no prazo em **verde**
- Coluna de status com ícones ❌ / ✅
- Botão de exportação em **CSV** com os dados filtrados

### CRUD — Gerenciar Entregas
- **Adicionar** — cadastro de novas entregas com transportadora, região, prazo e dias reais
- **Editar** — atualização de qualquer campo de uma entrega existente
- **Remover** — exclusão de entregas com confirmação
- Todas as alterações são salvas automaticamente no `dados.csv` e refletidas em tempo real nos gráficos

---

## Estrutura do Projeto

```
├── app.py                  # Aplicação principal
├── dados.csv               # Base de dados de entregas
├── requirements.txt        # Dependências
├── assets/
│   └── style.css           # Estilos customizados
└── utils/
    ├── __init__.py
    ├── data.py             # Carregamento, processamento e funções CRUD
    ├── kpis.py             # Cálculo, exibição dos KPIs e geração de insights
    └── charts.py           # Geração de todos os gráficos
```

---

## Como executar localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/pedrooigorr/desafios_vivo.git
cd desafios_vivo
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Execute o app:**
```bash
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`

---

## Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| [Streamlit](https://streamlit.io/) | Framework principal do dashboard |
| [Pandas](https://pandas.pydata.org/) | Manipulação e processamento dos dados |
| [Plotly](https://plotly.com/) | Gráficos interativos |
| CSS customizado | Estilização e tema visual |
| GitHub + Streamlit Cloud | Versionamento e deploy |

---

## Lógica de construção

### Como os atrasos foram identificados
Para cada entrega, o sistema compara o `prazo_dias` com o `dias_reais`. Se o tempo real for maior que o prazo, a entrega é marcada como atrasada. Uma segunda coluna (`dias_atraso`) registra exatamente quantos dias cada entrega ultrapassou o prazo — permitindo não apenas saber *se* houve atraso, mas *o quanto* cada caso impactou a operação.

### Como os cálculos foram realizados
Todos os cálculos são feitos com Pandas sobre a base de dados em tempo real. O critério principal do ranking é o total de dias de atraso acumulados por transportadora — e não apenas a quantidade de entregas atrasadas — pois uma transportadora com 2 entregas atrasando 10 dias cada é mais crítica do que outra com 3 entregas atrasando 1 dia cada.

### Como as informações foram priorizadas
A organização segue a lógica **do geral para o específico**: o gestor entra no dashboard e em segundos já tem o diagnóstico da operação pelos KPIs e o alerta de criticidade. O insight automático aponta imediatamente o problema principal e recomenda uma ação. Os gráficos aprofundam a análise por transportadora e região, e a tabela oferece o detalhamento completo com opção de exportação.

---

## Deploy

O dashboard está disponível publicamente via **Streamlit Community Cloud**.
