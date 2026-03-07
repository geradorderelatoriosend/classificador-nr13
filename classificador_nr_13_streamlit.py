from __future__ import annotations

import streamlit as st


# ---------------------------------
# Base interna de fluidos
# ---------------------------------
FLUIDOS = {
    "ar comprimido": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "ar comprimido",
    },
    "vapor de água": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 150.0,
        "tipo_especial": "vapor de água",
    },
    "nitrogênio": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "gases asfixiantes simples",
    },
    "oxigênio": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "outro",
    },
    "hidrogênio": {
        "inflamavel": True,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "hidrogênio",
    },
    "acetileno": {
        "inflamavel": True,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "acetileno",
    },
    "glp": {
        "inflamavel": True,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "outro",
    },
    "amônia": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": True,
        "temperatura_c": 25.0,
        "tipo_especial": "outro",
    },
    "diesel": {
        "inflamavel": False,
        "combustivel": True,
        "toxico": False,
        "temperatura_c": 130.0,
        "tipo_especial": "outro",
    },
    "óleo combustível": {
        "inflamavel": False,
        "combustivel": True,
        "toxico": False,
        "temperatura_c": 220.0,
        "tipo_especial": "outro",
    },
    "água": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "outro",
    },
    "outro": {
        "inflamavel": False,
        "combustivel": False,
        "toxico": False,
        "temperatura_c": 25.0,
        "tipo_especial": "outro",
    },
}


# ---------------------------------
# Regras de classificação NR-13
# ---------------------------------
def normalizar_numero_br(valor_texto: str) -> float:
    texto = str(valor_texto).strip()
    if not texto:
        raise ValueError("Campo vazio")

    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")

    return float(texto)


def litros_para_m3(volume_litros: float) -> float:
    return volume_litros / 1000


def kgf_cm2_para_mpa(pressao_kgf_cm2: float) -> float:
    return pressao_kgf_cm2 * 0.0980665


def kgf_cm2_para_kpa(pressao_kgf_cm2: float) -> float:
    return pressao_kgf_cm2 * 98.0665


def calcular_pv(pressao_kgf_cm2: float, volume_litros: float) -> tuple[float, float, float, float]:
    pressao_mpa = kgf_cm2_para_mpa(pressao_kgf_cm2)
    pressao_kpa = kgf_cm2_para_kpa(pressao_kgf_cm2)
    volume_m3 = litros_para_m3(volume_litros)
    pv_categoria = pressao_mpa * volume_m3
    pv_enquadramento = pressao_kpa * volume_m3
    return pressao_mpa, pressao_kpa, volume_m3, pv_categoria, pv_enquadramento


def formatar_numero_br(valor: float, casas: int = 2) -> str:
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "#").replace(".", ",").replace("#", ".")


def classificar_grupo_potencial_risco(pv: float) -> str:
    if pv > 100:
        return "Grupo 1"
    if 30 < pv <= 100:
        return "Grupo 2"
    if 2.5 < pv <= 30:
        return "Grupo 3"
    if 1 < pv <= 2.5:
        return "Grupo 4"
    return "Grupo 5"


def classificar_fluido(
    inflamavel: bool,
    combustivel: bool,
    temperatura_c: float,
    toxico: bool,
    fluido_especial: str,
) -> str:
    fluido_especial = fluido_especial.strip().lower()

    if inflamavel:
        return "Classe A"
    if combustivel and temperatura_c >= 200:
        return "Classe A"
    if toxico:
        return "Classe A"
    if fluido_especial in {"hidrogenio", "hidrogênio", "acetileno"}:
        return "Classe A"

    if combustivel and temperatura_c < 200:
        return "Classe B"

    if fluido_especial in {
        "vapor de agua",
        "vapor de água",
        "gases asfixiantes simples",
        "gas asfixiante simples",
        "gás asfixiante simples",
        "ar comprimido",
    }:
        return "Classe C"

    return "Classe D"


def classificar_categoria(classe_fluido: str, grupo: str) -> str:
    tabela = {
        "Classe A": {
            "Grupo 1": "Categoria I",
            "Grupo 2": "Categoria I",
            "Grupo 3": "Categoria II",
            "Grupo 4": "Categoria III",
            "Grupo 5": "Categoria III",
        },
        "Classe B": {
            "Grupo 1": "Categoria I",
            "Grupo 2": "Categoria II",
            "Grupo 3": "Categoria III",
            "Grupo 4": "Categoria IV",
            "Grupo 5": "Categoria IV",
        },
        "Classe C": {
            "Grupo 1": "Categoria I",
            "Grupo 2": "Categoria II",
            "Grupo 3": "Categoria III",
            "Grupo 4": "Categoria IV",
            "Grupo 5": "Categoria V",
        },
        "Classe D": {
            "Grupo 1": "Categoria II",
            "Grupo 2": "Categoria III",
            "Grupo 3": "Categoria IV",
            "Grupo 4": "Categoria V",
            "Grupo 5": "Categoria V",
        },
    }
    return tabela[classe_fluido][grupo]


def obter_dados_fluido(nome_fluido: str) -> dict:
    return FLUIDOS.get(nome_fluido.strip().lower(), FLUIDOS["outro"])


# ---------------------------------
# Interface Streamlit
# ---------------------------------
st.set_page_config(page_title="Classificador NR-13", page_icon="🧪", layout="centered")

st.title("Classificação de Vaso de Pressão - NR-13")
st.caption("Versão web para uso no celular e computador")

with st.form("form_nr13"):
    st.subheader("Dados do equipamento")
    pressao_txt = st.text_input("Pressão máxima de operação (kgf/cm²)", value="15,29")
    volume_txt = st.text_input("Volume interno (litros)", value="30")

    st.subheader("Fluido")
    fluido_nome = st.selectbox("Fluido especial", options=list(FLUIDOS.keys()), index=0)
    dados_fluido = obter_dados_fluido(fluido_nome)

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Inflamável", value="Sim" if dados_fluido["inflamavel"] else "Não", disabled=True)
        st.text_input("Combustível", value="Sim" if dados_fluido["combustivel"] else "Não", disabled=True)
    with col2:
        st.text_input("Tóxico", value="Sim" if dados_fluido["toxico"] else "Não", disabled=True)
        st.text_input("Temperatura do fluido (°C)", value=formatar_numero_br(dados_fluido["temperatura_c"], 2), disabled=True)

    submitted = st.form_submit_button("Classificar")

if submitted:
    try:
        pressao = normalizar_numero_br(pressao_txt)
        volume = normalizar_numero_br(volume_txt)
        if pressao <= 0 or volume <= 0:
            raise ValueError
    except ValueError:
        st.error("Preencha pressão e volume com números válidos. Ambos devem ser maiores que zero.")
    else:
        temperatura = float(dados_fluido["temperatura_c"])
        inflamavel = bool(dados_fluido["inflamavel"])
        combustivel = bool(dados_fluido["combustivel"])
        toxico = bool(dados_fluido["toxico"])
        tipo_especial = str(dados_fluido["tipo_especial"])

        classe = classificar_fluido(
            inflamavel=inflamavel,
            combustivel=combustivel,
            temperatura_c=temperatura,
            toxico=toxico,
            fluido_especial=tipo_especial,
        )

        pressao_mpa, pressao_kpa, volume_m3, pv_categoria, pv_enquadramento = calcular_pv(pressao, volume)
        enquadrado_nr13 = pv_enquadramento > 8 or classe == "Classe A"
        grupo = classificar_grupo_potencial_risco(pv_categoria)
        categoria = classificar_categoria(classe, grupo) if enquadrado_nr13 else "Não aplicável"

        st.subheader("Resultado")
        if enquadrado_nr13:
            st.success(f"Enquadrado na NR-13 | {classe} | {grupo} | {categoria}")
        else:
            st.warning(f"Não enquadrado na NR-13 | {classe} | Grupo/Categoria não aplicáveis")

        st.markdown("### Resumo")
        st.write(f"**Fluido selecionado:** {fluido_nome}")
        st.write(f"**Pressão máxima de operação:** {formatar_numero_br(pressao, 2)} kgf/cm²")
        st.write(f"**Volume interno:** {formatar_numero_br(volume, 2)} litros")
        st.write(f"**Pressão convertida para grupo/categoria:** {formatar_numero_br(pressao_mpa, 6)} MPa")
        st.write(f"**Pressão convertida para enquadramento NR-13:** {formatar_numero_br(pressao_kpa, 2)} kPa")
        st.write(f"**Volume convertido:** {formatar_numero_br(volume_m3, 6)} m³")
        st.write(f"**P.V para enquadramento NR-13:** {formatar_numero_br(pv_enquadramento, 6)} kPa·m³")
        st.write(f"**P.V para grupo/categoria:** {formatar_numero_br(pv_categoria, 6)} MPa·m³")
        st.write(f"**Enquadrado na NR-13:** {'Sim' if enquadrado_nr13 else 'Não'}")

        st.markdown("### Critérios automáticos")
        st.write(f"**Inflamável:** {'Sim' if inflamavel else 'Não'}")
        st.write(f"**Combustível:** {'Sim' if combustivel else 'Não'}")
        st.write(f"**Tóxico:** {'Sim' if toxico else 'Não'}")
        st.write(f"**Temperatura do fluido:** {formatar_numero_br(temperatura, 2)} °C")
        st.write(f"**Tipo especial considerado:** {tipo_especial}")

st.divider()
st.caption("Para publicar grátis: GitHub + Streamlit Community Cloud")
