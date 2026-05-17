# 📊 Telco Customer Churn Analytics - Producto Análitico EDA

Este repositorio contiene un producto análitico interactivo desarrollado en Python utilizando **Streamlit**, orientado al **Análisis Exploratorio de Datos (EDA)** para la identificación de patrones criticos asociados a la fuga de clientes (Churn) en una compania de telecomunicaciones.

---

## 🎯 Objetivo del Proyecto
El proposito central de este desarrollo es limpiar, transformar, analizar y visualizar de manera dinamica el dataset economico e historico `TelcoCustomerChurn.csv`. 

El enfoque de esta herramienta es 100% descriptivo y exploratorio, diseñado estrategicamente para soportar la **toma de decisiones corporativas** y politicas de retención, mitigando el impacto financiero de la desercion incrementada tras la coyuntura del COVID-19 (donde la tasa de fuga se elevo del 2.0% al 2.5%).

---

## 🛠️ Tecnologías y Conceptos Aplicados
- **Framework Web:** Streamlit (Layouts, Widgets interactivos, Session State)
- **Procesamiento de Datos:** Pandas y NumPy
- **Visualizaciones Estructuradas:** Matplotlib y Seaborn
- **Paradigma de Programacion:** Programación Orientada a Objetos (POO) mediante una arquitectura limpia separando la logica del backend (`src/processor.py`) de la interfaz de usuario (`app.py`).

---

## 📦 Estructura del Repositorio
┣ 📂 .streamlit
 ┃ ┗ 📜 config.toml          # Personalizacion estetica y paleta corporativa
 ┣ 📜 app.py                 # Orquestador principal e interfaz de la app
 ┣ 📜 srcprocessor.py        # Clase POO DataProcessor (Nucleo análitico de logica)
 ┣ 📜 requirements.txt       # Dependencias y librerias del proyecto
 ┗ 📜 TelcoCustomerChurn.csv # Dataset historico de clientes