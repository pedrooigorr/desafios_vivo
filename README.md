# 🚚 Dashboard Logístico Inteligente

Dashboard interativo desenvolvido com **Streamlit** para monitoramento de atrasos logísticos e desempenho operacional em tempo real.

## 📊 Funcionalidades

- **5 KPIs** em tempo real: total de entregas, atrasadas, % de atraso, transportadora crítica e média de dias de atraso
- **Alertas visuais automáticos** por nível de criticidade (verde / amarelo / vermelho)
- **Insight automático** com identificação da transportadora mais problemática e recomendação de ação
- **6 gráficos interativos:**
  - Comparação de atrasos por transportadora
  - Análise por região (todas as regiões, incluindo zeradas)
  - Pontualidade por transportadora (barras empilhadas)
  - Ranking numerado de dias totais de atraso
  - Proporção de dias de atraso (pizza)
  - Mapa de bolhas do Brasil por região
- **Filtros dinâmicos** por região e transportadora com botão de limpar
- **Tabela com destaque visual** — linhas atrasadas em vermelho, no prazo em verde
- **Exportar CSV** com os dados filtrados

## 🗂️ Estrutura do Projeto

```
├── app.py                  # Aplicação principal
├── dados.csv               # Base de dados de entregas
├── requirements.txt        # Dependências
├── assets/
│   └── style.css           # Estilos customizados
└── utils/
    ├── data.py             # Carregamento e processamento dos dados
    ├── kpis.py             # Cálculo e exibição dos KPIs
    └── charts.py           # Geração dos gráficos
```

## 🚀 Como executar localmente

1. Clone o repositório:
```bash
git clone https://github.com/pedroigorr/desafios_vivo.git
cd desafios_vivo
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o app:
```bash
streamlit run app.py
```

## 🛠️ Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) — framework para dashboards em Python
- [Pandas](https://pandas.pydata.org/) — manipulação de dados
- [Plotly](https://plotly.com/) — gráficos interativos

## 📦 Desafio

Desenvolvido como solução para o desafio **AMT01 — Visualização de dados: dashboards**, com foco em:
- Organização lógica e clareza analítica
- Usabilidade e recursos de interação
- Interpretação dos dados e apoio à tomada de decisão