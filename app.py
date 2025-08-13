import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Pattern Analyzer",
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
        return "green"
    elif number in RED_NUMBERS:
        return "red"
    else:
        return "black"

def get_parity(number):
    if number == 0:
        return "zero"
    elif number % 2 == 0:
        return "even"
    else:
        return "odd"

def get_dozen(number):
    if number == 0:
        return "zero"
    elif 1 <= number <= 12:
        return "first"
    elif 13 <= number <= 24:
        return "second"
    else:
        return "third"

def get_diagonal(number):
    if number == 0:
        return "zero"
    elif number in DIAGONAL_1 and number in DIAGONAL_2:
        return "both"
    elif number in DIAGONAL_1:
        return "diagonal_1"
    elif number in DIAGONAL_2:
        return "diagonal_2"
    else:
        return "none"

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
    if current_dozen in st.session_state.dozen_types:
        st.session_state.dozen_count += 1
        st.session_state.dozen_types.add(current_dozen)
    else:
        st.session_state.dozen_types = {current_dozen}
        st.session_state.dozen_count = 1
    
    # Actualizar contador de diagonales
    current_diagonal = get_diagonal(number)
    if current_diagonal == "both":
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
        st.session_state.diagonal_count = 1 if current_diagonal != "none" else 0

# Título principal
st.title("🎯 Pattern Analyzer")

# Sidebar para configuración
st.sidebar.header("⚙️ Configuration")
color_threshold = st.sidebar.number_input("Color/Parity Threshold", min_value=1, max_value=20, value=5)
dozen_threshold = st.sidebar.number_input("Dozen Threshold", min_value=1, max_value=50, value=20)
diagonal_threshold = st.sidebar.number_input("Diagonal Threshold", min_value=1, max_value=20, value=7)

# Sección principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Number Entry")
    
    with st.form("number_form", clear_on_submit=True):
        col_input, col_add = st.columns([3, 1])
        
        with col_input:
            new_number = st.number_input("Enter number (0-36)", min_value=0, max_value=36, value=0, key="number_input")
        
        with col_add:
            submitted = st.form_submit_button("➕ Add", use_container_width=True)
        
        if submitted:
            st.session_state.numbers.append(new_number)
            update_counters(new_number)
            st.rerun()
    
    col_delete_container = st.columns([1, 2])
    with col_delete_container[0]:
        if st.button("🗑️ Delete Last", use_container_width=True) and st.session_state.numbers:
            st.session_state.numbers.pop()
            # Recalcular todos los contadores
            reset_all_counters()
            for num in st.session_state.numbers:
                update_counters(num)
            st.rerun()

    # Mostrar últimos números
    if st.session_state.numbers:
        st.subheader("📊 Recent Numbers")
        recent_numbers = st.session_state.numbers[-10:]  # Últimos 10 números
        
        cols = st.columns(min(len(recent_numbers), 10))
        for i, num in enumerate(recent_numbers):
            color = get_color(num)
            if color == "red":
                cols[i].markdown(f"<div style='background-color: #ff4444; color: white; padding: 10px; text-align: center; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{num}</div>", unsafe_allow_html=True)
            elif color == "black":
                cols[i].markdown(f"<div style='background-color: #333333; color: white; padding: 10px; text-align: center; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{num}</div>", unsafe_allow_html=True)
            else:  # green (0)
                cols[i].markdown(f"<div style='background-color: #00aa00; color: white; padding: 10px; text-align: center; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold;'>{num}</div>", unsafe_allow_html=True)

with col2:
    st.header("📈 Current Patterns")
    
    # Mostrar contadores actuales
    st.metric("Color Streak", f"{st.session_state.color_count} {st.session_state.color_type or 'None'}")
    st.metric("Parity Streak", f"{st.session_state.parity_count} {st.session_state.parity_type or 'None'}")
    st.metric("Dozen Streak", f"{st.session_state.dozen_count} ({len(st.session_state.dozen_types)} dozens)")
    st.metric("Diagonal Streak", f"{st.session_state.diagonal_count} {st.session_state.diagonal_type or 'None'}")

# Sección de recomendaciones
st.header("🎯 Recommendations")

recommendations = []

# Recomendación de color
if st.session_state.color_count >= color_threshold and st.session_state.color_type:
    opposite_color = "black" if st.session_state.color_type == "red" else "red"
    recommendations.append(f"🔴⚫ **Color Pattern Detected**: {st.session_state.color_count} consecutive {st.session_state.color_type}s. Consider betting on **{opposite_color}**.")

# Recomendación de paridad
if st.session_state.parity_count >= color_threshold and st.session_state.parity_type:
    opposite_parity = "even" if st.session_state.parity_type == "odd" else "odd"
    recommendations.append(f"🔢 **Parity Pattern Detected**: {st.session_state.parity_count} consecutive {st.session_state.parity_type}s. Consider betting on **{opposite_parity}**.")

# Recomendación de docenas
if st.session_state.dozen_count >= dozen_threshold and len(st.session_state.dozen_types) == 2:
    all_dozens = {"first", "second", "third"}
    missing_dozen = all_dozens - st.session_state.dozen_types
    if missing_dozen:
        dozen_name = list(missing_dozen)[0]
        dozen_ranges = {"first": "1-12", "second": "13-24", "third": "25-36"}
        recommendations.append(f"📦 **Dozen Pattern Detected**: {st.session_state.dozen_count} numbers from 2 dozens. Consider betting on **{dozen_name} dozen ({dozen_ranges[dozen_name]})**.")

# Recomendación de diagonales
if st.session_state.diagonal_count >= diagonal_threshold and st.session_state.diagonal_type in ["diagonal_1", "diagonal_2"]:
    if st.session_state.diagonal_type == "diagonal_1":
        opposite_diagonal = "diagonal_2"
        numbers_to_bet = sorted(list(DIAGONAL_2 - DIAGONAL_1))
    else:
        opposite_diagonal = "diagonal_1"
        numbers_to_bet = sorted(list(DIAGONAL_1 - DIAGONAL_2))
    
    recommendations.append(f"🔷 **Diagonal Pattern Detected**: {st.session_state.diagonal_count} consecutive numbers from {st.session_state.diagonal_type}. Consider betting on **{opposite_diagonal}**: {numbers_to_bet}")

# Mostrar recomendaciones
if recommendations:
    for rec in recommendations:
        st.success(rec)
else:
    st.info("No patterns detected yet. Keep adding numbers!")

# Estadísticas generales
if st.session_state.numbers:
    st.header("📊 Statistics")
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        total_numbers = len(st.session_state.numbers)
        red_count = sum(1 for n in st.session_state.numbers if get_color(n) == "red")
        black_count = sum(1 for n in st.session_state.numbers if get_color(n) == "black")
        zero_count = sum(1 for n in st.session_state.numbers if n == 0)
        
        st.subheader("Colors")
        st.write(f"🔴 Red: {red_count} ({red_count/total_numbers*100:.1f}%)")
        st.write(f"⚫ Black: {black_count} ({black_count/total_numbers*100:.1f}%)")
        st.write(f"🟢 Zero: {zero_count} ({zero_count/total_numbers*100:.1f}%)")
    
    with col_stats2:
        even_count = sum(1 for n in st.session_state.numbers if n != 0 and n % 2 == 0)
        odd_count = sum(1 for n in st.session_state.numbers if n != 0 and n % 2 == 1)
        
        st.subheader("Parity")
        st.write(f"Even: {even_count} ({even_count/(total_numbers-zero_count)*100:.1f}%)" if total_numbers > zero_count else "Even: 0")
        st.write(f"Odd: {odd_count} ({odd_count/(total_numbers-zero_count)*100:.1f}%)" if total_numbers > zero_count else "Odd: 0")
    
    with col_stats3:
        first_dozen = sum(1 for n in st.session_state.numbers if 1 <= n <= 12)
        second_dozen = sum(1 for n in st.session_state.numbers if 13 <= n <= 24)
        third_dozen = sum(1 for n in st.session_state.numbers if 25 <= n <= 36)
        
        st.subheader("Dozens")
        st.write(f"1st (1-12): {first_dozen}")
        st.write(f"2nd (13-24): {second_dozen}")
        st.write(f"3rd (25-36): {third_dozen}")

# Footer
st.markdown("---")
st.markdown("*Pattern Analyzer - Statistical tracking tool*")
