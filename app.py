import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Patrones",
    page_icon="📊",
    layout="wide"
)

# Inicializar session state
if 'numbers' not in st.session_state:
    st.session_state.numbers = []
if 'color_count' not in st.session_state:
    st.session_state.color_count = 0
if 'color_type' not in st.session_state:
    st.session_state.color_type = None
if 'parity_count' not in st.session_state:
    st.session_state.parity_count = 0
if 'parity_type' not in st.session_state:
    st.session_state.parity_type = None
if 'dozen_count' not in st.session_state:
    st.session_state.dozen_count = 0
if 'dozen_types' not in st.session_state:
    st.session_state.dozen_types = set()
if 'diagonal_count' not in st.session_state:
    st.session_state.diagonal_count = 0
if 'diagonal_type' not in st.session_state:
    st.session_state.diagonal_type = None

# Definiciones de la ruleta francesa
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# Diagonales
DIAGONAL_1 = {1, 2, 4, 5, 8, 9, 11, 12, 13, 14, 16, 17, 20, 21, 23, 24, 25, 26, 28, 29, 32, 33, 35, 36}
DIAGONAL_2 = {2, 3, 5, 6, 7, 8, 10, 11, 14, 15, 17, 18, 19, 20, 22, 23, 26, 27, 29, 30, 31, 32, 34, 35}

def get_color(number):
    if number == 0:
        return "verde"
    elif number in RED_NUMBERS:
        return "rojo"
    else:
        return "negro"

def get_parity(number):
    if number == 0:
        return "cero"
    elif number % 2 == 0:
        return "par"
    else:
        return "impar"

def get_dozen(number):
    if number == 0:
        return "cero"
    elif 1 <= number <= 12:
        return "primera"
    elif 13 <= number <= 24:
        return "segunda"
    else:
        return "tercera"

def get_diagonal(number):
    if number == 0:
        return "cero"
    elif number in DIAGONAL_1 and number in DIAGONAL_2:
        return "ambas"
    elif number in DIAGONAL_1:
        return "diagonal_1"
    elif number in DIAGONAL_2:
        return "diagonal_2"
    else:
        return "ninguna"

def reset_all_counters():
    st.session_state.color_count = 0
    st.session_state.color_type = None
    st.session_state.parity_count = 0
    st.session_state.parity_type = None
    st.session_state.dozen_count = 0
    st.session_state.dozen_types = set()
    st.session_state.diagonal_count = 0
    st.session_state.diagonal_type = None

def update_counters(number):
    # Si es 0, resetear todos los contadores
    if number == 0:
        reset_all_counters()
        return
    
    # Actualizar contador de color
    current_color = get_color(number)
    if st.session_state.color_type == current_color:
        st.session_state.color_count += 1
    else:
        st.session_state.color_type = current_color
        st.session_state.color_count = 1
    
    # Actualizar contador de paridad
    current_parity = get_parity(number)
    if st.session_state.parity_type == current_parity:
        st.session_state.parity_count += 1
    else:
        st.session_state.parity_type = current_parity
        st.session_state.parity_count = 1
    
    # Actualizar contador de docenas
    current_dozen = get_dozen(number)
    
    # Si es el primer número o no hay docenas registradas
    if not st.session_state.dozen_types:
        st.session_state.dozen_types = {current_dozen}
        st.session_state.dozen_count = 1
    # Si la docena actual ya está en el set (continúa el patrón)
    elif current_dozen in st.session_state.dozen_types:
        st.session_state.dozen_count += 1
    # Si es una nueva docena
    else:
        # Si ya tenemos 2 docenas y llega una tercera, resetear
        if len(st.session_state.dozen_types) >= 2:
            st.session_state.dozen_types = {current_dozen}
            st.session_state.dozen_count = 1
        # Si tenemos 1 docena y llega una segunda, agregarla
        else:
            st.session_state.dozen_types.add(current_dozen)
            st.session_state.dozen_count += 1
    
    # Actualizar contador de diagonales
    current_diagonal = get_diagonal(number)
    if current_diagonal == "ambas":
        # Si está en ambas diagonales, mantener el patrón actual si existe
        if st.session_state.diagonal_type in ["diagonal_1", "diagonal_2"]:
            st.session_state.diagonal_count += 1
        else:
            st.session_state.diagonal_type = "diagonal_1"  # Por defecto
            st.session_state.diagonal_count = 1
    elif st.session_state.diagonal_type == current_diagonal:
        st.session_state.diagonal_count += 1
    else:
        st.session_state.diagonal_type = current_diagonal
        st.session_state.diagonal_count = 1 if current_diagonal != "ninguna" else 0

# Título principal
st.title("🎯 Analizador de Patrones")

# Sidebar para configuración
st.sidebar.header("⚙️ Configuración")
color_threshold = st.sidebar.number_input("Umbral Color/Paridad", min_value=1, max_value=20, value=5)
dozen_threshold = st.sidebar.number_input("Umbral Docenas", min_value=1, max_value=50, value=20)
diagonal_threshold = st.sidebar.number_input("Umbral Diagonales", min_value=1, max_value=20, value=7)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("📝 Ingreso de Números")
    
    with st.form("number_form", clear_on_submit=True):
        new_number = st.number_input("Ingresa número (0-36)", min_value=0, max_value=36, value=0, key="number_input")
        submitted = st.form_submit_button("➕ Agregar", use_container_width=True)
        
        if submitted:
            st.session_state.numbers.append(new_number)
            update_counters(new_number)
            st.rerun()
    
    if st.button("🗑️ Borrar Último", use_container_width=True) and st.session_state.numbers:
        st.session_state.numbers.pop()
        # Recalcular todos los contadores
        reset_all_counters()
        for num in st.session_state.numbers:
            update_counters(num)
        st.rerun()

    if st.session_state.numbers:
        st.subheader("📊 Últimos Números")
        recent_numbers = st.session_state.numbers[-10:]  # Últimos 10 números
        recent_numbers.reverse()  # Mostrar el más reciente arriba
        
        for num in recent_numbers:
            color = get_color(num)
            if color == "rojo":
                st.markdown(f"<div style='background-color: #ff4444; color: white; padding: 8px; text-align: center; border-radius: 8px; margin: 2px 0; font-weight: bold; font-size: 18px;'>{num}</div>", unsafe_allow_html=True)
            elif color == "negro":
                st.markdown(f"<div style='background-color: #333333; color: white; padding: 8px; text-align: center; border-radius: 8px; margin: 2px 0; font-weight: bold; font-size: 18px;'>{num}</div>", unsafe_allow_html=True)
            else:  # verde (0)
                st.markdown(f"<div style='background-color: #00aa00; color: white; padding: 8px; text-align: center; border-radius: 8px; margin: 2px 0; font-weight: bold; font-size: 18px;'>{num}</div>", unsafe_allow_html=True)

with col2:
    st.header("📋 Historial Completo")
    
    if st.session_state.numbers:
        # Crear DataFrame con información detallada
        history_data = []
        for i, num in enumerate(reversed(st.session_state.numbers), 1):
            color = get_color(num)
            parity = get_parity(num)
            dozen = get_dozen(num)
            
            history_data.append({
                "#": i,
                "Número": num,
                "Color": color,
                "Paridad": parity,
                "Docena": dozen
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        st.write(f"**Total de números:** {len(st.session_state.numbers)}")
    else:
        st.info("No hay números registrados aún.")

with col3:
    st.header("📈 Patrones Actuales")
    
    # Mostrar contadores actuales
    st.metric("Racha de Color", f"{st.session_state.color_count} {st.session_state.color_type or 'Ninguno'}")
    st.metric("Racha de Paridad", f"{st.session_state.parity_count} {st.session_state.parity_type or 'Ninguno'}")
    st.metric("Racha de Docenas", f"{st.session_state.dozen_count} ({len(st.session_state.dozen_types)} docenas)")
    st.metric("Racha de Diagonales", f"{st.session_state.diagonal_count} {st.session_state.diagonal_type or 'Ninguno'}")

    st.header("🎯 Recomendaciones")

    recommendations = []

    # Recomendación de color
    if st.session_state.color_count >= color_threshold and st.session_state.color_type:
        opposite_color = "negro" if st.session_state.color_type == "rojo" else "rojo"
        recommendations.append(f"🔴⚫ **Patrón de Color Detectado**: {st.session_state.color_count} {st.session_state.color_type}s consecutivos. Considera apostar al **{opposite_color}**.")

    # Recomendación de paridad
    if st.session_state.parity_count >= color_threshold and st.session_state.parity_type:
        opposite_parity = "par" if st.session_state.parity_type == "impar" else "impar"
        recommendations.append(f"🔢 **Patrón de Paridad Detectado**: {st.session_state.parity_count} {st.session_state.parity_type}s consecutivos. Considera apostar al **{opposite_parity}**.")

    # Recomendación de docenas
    if st.session_state.dozen_count >= dozen_threshold and len(st.session_state.dozen_types) == 2:
        all_dozens = {"primera", "segunda", "tercera"}
        missing_dozen = all_dozens - st.session_state.dozen_types
        if missing_dozen:
            dozen_name = list(missing_dozen)[0]
            dozen_ranges = {"primera": "1-12", "segunda": "13-24", "tercera": "25-36"}
            recommendations.append(f"📦 **Patrón de Docenas Detectado**: {st.session_state.dozen_count} números de 2 docenas. Considera apostar a la **{dozen_name} docena ({dozen_ranges[dozen_name]})**.")

    # Recomendación de diagonales
    if st.session_state.diagonal_count >= diagonal_threshold and st.session_state.diagonal_type in ["diagonal_1", "diagonal_2"]:
        if st.session_state.diagonal_type == "diagonal_1":
            opposite_diagonal = "diagonal_2"
            numbers_to_bet = sorted(list(DIAGONAL_2 - DIAGONAL_1))
        else:
            opposite_diagonal = "diagonal_1"
            numbers_to_bet = sorted(list(DIAGONAL_1 - DIAGONAL_2))
        
        recommendations.append(f"🔷 **Patrón de Diagonal Detectado**: {st.session_state.diagonal_count} números consecutivos de {st.session_state.diagonal_type}. Considera apostar a **{opposite_diagonal}**: {numbers_to_bet}")

    # Mostrar recomendaciones
    if recommendations:
        for rec in recommendations:
            st.success(rec)
    else:
        st.info("No se han detectado patrones aún. ¡Sigue agregando números!")

if st.session_state.numbers:
    st.header("📊 Estadísticas Generales")
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        total_numbers = len(st.session_state.numbers)
        red_count = sum(1 for n in st.session_state.numbers if get_color(n) == "rojo")
        black_count = sum(1 for n in st.session_state.numbers if get_color(n) == "negro")
        zero_count = sum(1 for n in st.session_state.numbers if n == 0)
        
        st.subheader("Colores")
        st.write(f"🔴 Rojo: {red_count} ({red_count/total_numbers*100:.1f}%)")
        st.write(f"⚫ Negro: {black_count} ({black_count/total_numbers*100:.1f}%)")
        st.write(f"🟢 Cero: {zero_count} ({zero_count/total_numbers*100:.1f}%)")
    
    with col_stats2:
        even_count = sum(1 for n in st.session_state.numbers if n != 0 and n % 2 == 0)
        odd_count = sum(1 for n in st.session_state.numbers if n != 0 and n % 2 == 1)
        
        st.subheader("Paridad")
        st.write(f"Par: {even_count} ({even_count/(total_numbers-zero_count)*100:.1f}%)" if total_numbers > zero_count else "Par: 0")
        st.write(f"Impar: {odd_count} ({odd_count/(total_numbers-zero_count)*100:.1f}%)" if total_numbers > zero_count else "Impar: 0")
    
    with col_stats3:
        first_dozen = sum(1 for n in st.session_state.numbers if 1 <= n <= 12)
        second_dozen = sum(1 for n in st.session_state.numbers if 13 <= n <= 24)
        third_dozen = sum(1 for n in st.session_state.numbers if 25 <= n <= 36)
        
        st.subheader("Docenas")
        st.write(f"1ª (1-12): {first_dozen}")
        st.write(f"2ª (13-24): {second_dozen}")
        st.write(f"3ª (25-36): {third_dozen}")

# Footer
st.markdown("---")
st.markdown("*Analizador de Patrones - Herramienta de seguimiento estadístico*")
