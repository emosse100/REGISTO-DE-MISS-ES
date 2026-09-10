import pandas as pd
import streamlit as st
from datetime import date

# Configuração da Página
st.set_page_config(
    page_title="Registo de Missões - Saudigitus",
    page_icon="🌍",
    layout="wide",
)

# Base de Dados em Memória (Simulada com session_state para persistência na sessão)
if "missoes" not in st.session_state:
    st.session_state.missoes = [
        {
            "id": 1,
            "colaborador": "Emílio Mosse",
            "parceiro": "Ministério da Saúde (MISAU)",
            "destino": "Província de Nampula",
            "data_inicio": date(2026, 8, 10),
            "data_fim": date(2026, 8, 14),
            "atividade": "Implementação e supervisão do sistema DHIS2 e integração com dados climáticos.",
            "destaques": "Formação de 25 técnicos locais e alinhamento de fluxos de interoperabilidade.",
        },
        {
            "id": 2,
            "colaborador": "Equipa Técnica",
            "parceiro": "INASA (Guiné-Bissau)",
            "destino": "Bissau",
            "data_inicio": date(2026, 6, 5),
            "data_fim": date(2026, 6, 12),
            "atividade": "Alinhamento de acordos de partilha de dados para o projeto TA2 de Clima e Saúde.",
            "destaques": "Assinatura do memorando preliminar e mapeamento de fontes de dados.",
        },
    ]

st.title("🌍 Plataforma de Gestão de Missões e Relatórios — Saudigitus")
st.markdown(
    "Registe as suas missões de serviço com parceiros e filtre os dados para alimentar a nossa Newsletter institucional."
)

# Menu Lateral de Navegação
menu = st.sidebar.selectbox(
    "Navegação", ["Registar Nova Missão", "Consultar Missões", "Gerador de Relatório para Newsletter"]
)

# -------------------------------------------------------------
# 1. REGISTAR NOVA MISSÃO
# -------------------------------------------------------------
if menu == "Registar Nova Missão":
    st.header("📝 Registar Apanhado de Missão")
    st.markdown("Preencha os dados da missão realizada em representação da Saudigitus.")

    with st.form("form_missao"):
        col1, col2 = st.columns(2)

        with col1:
            colaborador = st.text_input("Nome do Colaborador / Responsável")
            parceiro = st.text_input(
                "Instituição Parceira", placeholder="Ex: MISAU, INASA, Universidade..."
            )
            destino = st.text_input(
                "Local de Destino", placeholder="Ex: Província de Gaza, Maputo, Bissau"
            )

        with col2:
            data_inicio = st.date_input("Data de Início", value=date.today())
            data_fim = st.date_input("Data de Término", value=date.today())

        atividade = st.text_area(
            "Resumo da Atividade Realizada",
            placeholder="Descreva o que foi feito durante a missão...",
        )
        destaques = st.text_area(
            "Principais Resultados / Destaques",
            placeholder="Resultados alcançados, reuniões chave, impacto gerado...",
        )

        enviado = st.form_submit_button("Submeter Registo de Missão")

        if enviado:
            if not colaborador or not parceiro or not destino or not atividade:
                st.error("Por favor, preencha todos os campos obrigatórios.")
            else:
                nova_missao = {
                    "id": len(st.session_state.missoes) + 1,
                    "colaborador": colaborador,
                    "parceiro": parceiro,
                    "destino": destino,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "atividade": atividade,
                    "destaques": destaques,
                }
                st.session_state.missoes.append(nova_missao)
                st.success("Missão registada com sucesso! O apanhado já está disponível para a equipa.")

# -------------------------------------------------------------
# 2. CONSULTAR MISSÕES
# -------------------------------------------------------------
elif menu == "Consultar Missões":
    st.header("📊 Histórico de Missões Registadas")

    if not st.session_state.missoes:
        st.info("Ainda não existem missões registadas.")
    else:
        df = pd.DataFrame(st.session_state.missoes)
        
        # Filtros de visualização
        parceiro_filtro = st.selectbox(
            "Filtrar por Parceiro", ["Todos"] + list(df["parceiro"].unique())
        )

        if parceiro_filtro != "Todos":
            df_filtrado = df[df["parceiro"] == parceiro_filtro]
        else:
            df_filtrado = df

        st.dataframe(df_filtrado, use_container_width=True)

# -------------------------------------------------------------
# 3. GERADOR DE RELATÓRIO PARA NEWSLETTER
# -------------------------------------------------------------
elif menu == "Gerador de Relatório para Newsletter":
    st.header("📰 Gerador de Relatório Agregado (Newsletter Saudigitus)")
    st.markdown(
        "Selecione o intervalo de datas ou parceiros para gerar automaticamente o resumo formatado para a nossa comunicação institucional."
    )

    if not st.session_state.missoes:
        st.warning("Não há dados suficientes para gerar o relatório.")
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            mes_referencia = st.selectbox(
                "Filtrar por Mês de Referência",
                ["Todos", "Junho 2026", "Agosto 2026", "Setembro 2026"],
            )
        with col_f2:
            formato_saida = st.radio(
                "Formato de Saída", ["Texto Formatado (Pronto a Copiar)", "Tabela Resumo"]
            )

        st.divider()

        st.subheader("📄 Pré-visualização do Conteúdo para a Newsletter")

        # Gerar o texto agregado
        relatorio_texto = "### 🌍 Em Missão: Destaques das Atividades com os Nossos Parceiros\n\n"
        relatorio_texto += "Nos últimos tempos, a equipa da Saudigitus tem estado no terreno a fortalecer parcerias estratégicas e a impulsionar a inovação em saúde digital:\n\n"

        for m in st.session_state.missoes:
            relatorio_texto += f"* **{m['parceiro']} ({m['destino']}):** O colega *{m['colaborador']}* realizou uma missão entre {m['data_inicio'].strftime('%d/%m/%Y')} e {m['data_fim'].strftime('%d/%m/%Y')}. **Atividade:** {m['atividade']} **Destaque:** {m['destaques']}\n\n"

        if formato_saida == "Texto Formatado (Pronto a Copiar)":
            st.text_area(
                "Copie o texto abaixo para utilizar diretamente no editor da Newsletter:",
                value=relatorio_texto,
                height=300,
            )
            st.download_button(
                label="📥 Descarregar Relatório em Formato de Texto (.txt)",
                data=relatorio_texto,
                file_name="relatorio_newsletter_saudigitus.txt",
                mime="text/plain",
            )
        else:
            df_report = pd.DataFrame(st.session_state.missoes)[
                ["colaborador", "parceiro", "destino", "atividade", "destaques"]
            ]
            st.table(df_report)
            st.download_button(
                label="📥 Descarregar Dados em CSV",
                data=df_report.to_csv(index=False).encode("utf-8"),
                file_name="missoes_saudigitus.csv",
                mime="text/csv",
            )
