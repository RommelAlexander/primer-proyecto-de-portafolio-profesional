import site
import streamlit as st
import pandas as pd
import sys
import os


# Acoplamos la ruta del directorio actual al path de Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Ahora la importación funcionará sin importar el contexto de ejecución
from srcprocessor import DataProcessor

# Configuracion de la pagina
st.set_page_config(
    page_title="Telco Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)

# Inicializacion del Estado de la Aplicacion
# Esto nos permite guardar el dataframe en memoria entre cambios de menu
if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "processor" not in st.session_state:
    st.session_state.processor = None

# Menu de Navegacion principal
st.sidebar.title("Navegación")
opcion_menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Modulo 1: Home", "Modulo 2: Carga de Datos", "Modulo 3: EDA (Analisis)"]
)

# Controles de modulo
# Modulo 1: Home
if opcion_menu == "Modulo 1: Home":
    st.title("📊 Análisis de Fuga de Clientes - Telco")
    st.subheader("Especialización en Python for Analytics - Caso de Estudio N°2")
    st.write("---")

    # Layout de dos columnas: Una para el contexto del negocio y otra para la ficha tecnica/autor
    col_contexto, col_autor = st.columns([2, 1])

    with col_contexto:
        st.markdown("### 🎯 Objetivo del Proyecto")
        st.write(
            "El objetivo principal de esta aplicacion es realizar un **análisis exploratorio de datos (EDA)** "
            "exhaustivo sobre el dataset historico de la empresa de telecomunicaciones, atraves de esta interfaz"
            "interactiva. Se busca limpiar, transformar y visualizar los datos para **identificar patrones de comportamiento "
            "y factores clave asociados a la fuga de clientes**, sirviendo como una herramienta funcional "
            "para la toma de decisiones estrategicas."
        )
        st.warning(
            "🛑 **Nota de alcance:** El enfoque de este producto analitico es 100% exploratorio y descriptivo. "
            "**NO tiene como objetivo el desarrollo de modelos predictivos de Machine Learning.**"
        )

        st.markdown("### 📈 Contexto de Negocio e Impacto Financiero")
        st.write(
            "En el periodo reciente, bajo la coyuntura global generada por el **COVID-19**, la empresa experimento "
            "un incremento critico en su tasa de desercion de clientes, elevandose del **2.0% al 2.5%** (+0.5 puntos porcentuales). "
            "Este escenario representa una amenaza financiera severa para la organizacion debido a una regla fundamental de la industria:"
        )
        
        # Resaltado visual del costo financiero utilizando un bloque de informacion
        st.info(
            "💡 **Metrica Clave:** El costo de adquirir un nuevo cliente (CAC) es entre **6 y 7 veces mayor** "
            "que el costo de retener a un cliente existente. Por lo tanto, mitigar la fuga mediante el analisis "
            "de datos historicos es la estrategia mas rentable para asegurar la estabilidad operativa."
        )

    with col_autor:
        # Tarjeta de presentacion del Autor
        st.markdown("### 👤 Datos del Autor")
        with st.container(border=True):
            st.markdown("**Nombre Completo:**\n*Rommel Alexander Picon Silva*")
            st.markdown("**Especialización:**\n*Python for Analytics*")
            st.markdown("**Año de Ejecución:**\n*2026*")
        
        st.markdown("### 🛠️ Tecnologías Utilizadas")
        st.markdown("- **Lenguaje:** `Python`")
        st.markdown("- **Framework Web:** `Streamlit`")
        st.markdown("- **Procesamiento de Datos:** `Pandas` & `NumPy`")
        st.markdown("- **Visualizacion:** `Matplotlib` & `Seaborn`")
        st.markdown("- **Paradigma:** `Programación Orientada a Objetos`")

    # Seccion inferior
    st.write("---")
    st.markdown("### 📋 Acerca del Dataset (`TelcoCustomerChurn.csv`)")
    st.write(
        "Los datos provienen de los registros historicos de la compañia y abarcan multiples dimensiones del cliente, "
        "clasificadas en tres grandes pilares: información demografica (genero, dependientes), caracteristicas "
        "de las cuentas y servicios contratados (tipo de internet, streaming, seguridad, contrato) y métricas "
        "financieras (cargos mensuales y cargos totales acumulados)."
    )

# Modulo 2: Carga de datos
elif opcion_menu == "Modulo 2: Carga de Datos":
    st.title("Carga y Validación del Dataset")
    st.write("---")

    # Carga de archivo CSV
    archivo_cargado = st.file_uploader(
        "Selecciona el archivo", 
        type=["csv"]
    )

    if archivo_cargado is not None:
        try:
            # Leer el archivo utilizando
            df_inicial = pd.read_csv(archivo_cargado)
            
            # Guardar el DataFrame en el estado de la sesion
            st.session_state.dataset = df_inicial
            
            # Inicializar la clase POO con el DataFrame cargado
            st.session_state.processor = DataProcessor(df_inicial)
            
            st.success("Archivo cargado y procesado exitosamente")
            
            # Despliegue de metricas basicas
            col_filas, col_columnas = st.columns(2)
            
            # Consumimos los metodos de la clase DataProcessor
            num_filas, num_columnas = st.session_state.processor.obtener_dimensiones()
            
            with col_filas:
                st.metric(label="Total de Registros (Filas)", value=f"{num_filas:,}")
            with col_columnas:
                st.metric(label="Total de Variables (Columnas)", value=num_columnas)
                
            st.write("---")
            st.markdown("### Vista Previa de los Datos (Primeros 5 registros)")
            
            # Mostramos la vista previa del DataFrame
            vista_previa = st.session_state.processor.obtener_vista_previa()
            st.dataframe(vista_previa, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error al procesar el archivo CSV: {str(e)}")
            
    else:
        # Mensaje en caso de que no se haya subido ningun archivo
        st.info("Por favor, suba el archivo CSV del proyecto para activar las funciones de analisis.")
        
        # Si el usuario remueve el archivo, limpiamos el estado de la sesion para mantener la seguridad
        st.session_state.dataset = None
        st.session_state.processor = None

# Modulo 3: EDA 
elif opcion_menu == "Modulo 3: EDA (Analisis)":
    st.title("🎛️ Nucleo Análitico - EDA")
    st.write("---")
    
    # Compuerta de seguridad: Validacion obligatoria
    if st.session_state.dataset is None:
        st.error("⚠️ Acceso denegado: Archivo pendientes de carga")
    else:
        # Pestañas
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "Información General", 
            "Clasificación de Variables", 
            "Estadísticas Descriptivas",
            "Valores Faltantes",
            "Distribución Númerica",
            "Análisis Categorico",
            "Bivariado (Númerica vs Categórico)",
            "Bivariado (Categórico vs Categórico)",
            "Análisis Dinamico",
            "Hallazgos Claves"
        ])
        
        # ---------------------------------------------------------------------
        # Pestaña 1: Informacion general
        # ---------------------------------------------------------------------
        with tab1:
            st.markdown("### 📋 Información General del Dataset")
            st.write(
                "A continuacion se presenta un resumen técnico de la estructura del dataset, "
                "identificando los tipos de datos asignados por columna y la presencia de valores faltantes."
            )
            
            # Llamamos al metodo de nuestra clase POO
            df_info = st.session_state.processor.obtener_informacion_general()
            
            # Usamos columnas para colocar la tabla y una tarjeta de interpretacion al lado
            col_tabla, col_interpretacion = st.columns([3, 2])
            
            with col_tabla:
                st.dataframe(df_info, use_container_width=True)
                
            with col_interpretacion:
                st.markdown("💡 **Análisis Preliminar:**")
                st.write(
                    "Este panel permite verificar si Pandas ha interpretado correctamente las variables. "
                    "Es de especial importancia revisar columnas como TotalCharges, la cual podria requerir "
                    "una conversion de tipo de dato si se detectan anomalias o espacios en blanco."
                )
        
        # ---------------------------------------------------------------------
        # Pestaña 2: Clasificacion de variables
        # ---------------------------------------------------------------------
     
        with tab2:
            st.markdown("### 🗂️ Clasificación de Variables")
            st.write(
                "A traves de una funcion personalizada basada en tipos de datos nativos, "
                "el sistema ha segmentado las variables del dataset."
            )
            
            # Ejecutamos la funcion desde nuestro objeto
            clasificacion = st.session_state.processor.clasificar_variables()
            
            # Layout de dos columnas para mostrar los resultados
            col_num, col_cat = st.columns(2)
            
            with col_num:
                st.metric(
                    label="Variables Numericas", 
                    value=int(clasificacion["conteo_numericas"])
                )
                with st.container(border=True):
                    st.write("**Lista de columnas:**")
                    for col in clasificacion["numericas"]:
                        st.code(col, language="text")                        
            with col_cat:
                st.metric(
                    label="Variables Categoricas", 
                    value=int(clasificacion["conteo_categoricas"])
                )
                with st.container(border=True):
                    st.write("**Lista de columnas:**")
                    for col in clasificacion["categoricas"]:
                        st.code(col, language="text")

        # ---------------------------------------------------------------------
        # Pestaña 3: Estadistica descriptiva
        # ---------------------------------------------------------------------
      
        with tab3:
            st.markdown("### 🔢 Estadísticas Descriptivas")
            st.write(
                "Resumen análitico de las variables númericas del dataset. "
                "Este panel permite evaluar las tendencias centrales y la dispersión de los datos:"
            )
            
            # Ejecutamos el metodo descriptivo
            df_descriptivo = st.session_state.processor.obtener_estadisticas_descriptivas()
            
            # Desplegamos la tabla estadistica
            st.dataframe(df_descriptivo, use_container_width=True)
            
            st.write("---")
            
            # Contenedor para la interpretacion
            st.markdown("💡 **Interpretación Análitica de Tendencias:**")
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.info(
                    "📌 **Analisis de Centralidad (Media vs Mediana):**\n\n"
                    "Al comparar la Media y la Mediana (Percentil 50) de variables como tenure o MonthlyCharges, "
                    "podemos identificar si la distribución presenta sesgos significativos. Una cercania entre "
                    "ambos valores sugiere una distribución relativamente símetrica."
                )
                
            with col_info2:
                st.info(
                    "📌 **Análisis de Dispersión (Desviación Estandar):**\n\n"
                    "La Desviación Estandar nos indica que tan alejados estan los datos respecto a su promedio. "
                    "Un valor elevado en TotalCharges denota una alta variabilidad en el comportamiento "
                    "de facturación acumulada dentro de la cartera de clientes de la compania."
                )

        # ---------------------------------------------------------------------
        # Pestaña 4: Valores faltantes
        # ---------------------------------------------------------------------
        with tab4:
            st.markdown("### 🔍 Análisis de Valores Faltantes (Nulos)")
            st.write(
                "Evaluación del estado de completitud de los datos para identificar "
                "registros ausentes que puedan afectar la calidad del análisis estadistico:"
            )
            
            # Ejecutamos el metodo
            df_faltantes = st.session_state.processor.analizar_valores_faltantes()
            
            col_tabla_nulos, col_discusion = st.columns([3, 2])
            
            with col_tabla_nulos:                
                st.dataframe(df_faltantes, use_container_width=True)
                
            with col_discusion:
                st.markdown("💡 **Discusión Breve de Calidad de Datos:**")
                st.warning(
                    "📌 **Estado de la Integridad:**\n\n"
                    "El dataset actual muestra un 0% de valores faltantes en la gran mayoria de variables "
                    "debido a la limpieza preventiva realizada en el constructor de datos. "
                    "Es importante recordar que la variable TotalCharges originalmente contenia espacios vacios "
                    "asociados a clientes con tiempo de permanencia igual a 0 meses (usuarios nuevos que aun "
                    "no han completado su primer ciclo de facturacion)."
                )
                st.info(
                    "🎯 **Impacto en Toma de Decisiones:**\n\n"
                    "Mantener un control estricto sobre los valores faltantes evita sesgos en el calculo de la "
                    "media de cargos mensuales y asegura que las estrategias de retención se basen en registros validos."
                )

        # ---------------------------------------------------------------------
        # Pestaña 5: Distribucion numerica
        # ---------------------------------------------------------------------
        with tab5:
            st.markdown("### 📊 Distribución de Variables Númericas")
            st.write(
                "Selecciona una variable númerica para analizar su comportamiento, "
                "tendencias de agrupación y la presencia de asimetrías en su distribución:"
            )
            
            # Obtenemos la clasificacion para conocer las columnas numericas disponibles
            listas_variables = st.session_state.processor.clasificar_variables()
            variables_numericas = listas_variables["numericas"]
            
            # Layout de columnas: Izquierda para seleccion y analisis, Derecha para el grafico
            col_controles, col_grafico = st.columns([2, 3])
            
            with col_controles:
                # Widget interativo para seleccionar la variable (selectbox)
                var_seleccionada = st.selectbox(
                    "Selecciona la variable a graficar:",
                    options=variables_numericas,
                    key="sb_histograma"
                )
                
                st.write("---")
                st.markdown("💡 **Guia de Interpretación Visual:**")
                if var_seleccionada == "tenure":
                    st.info(
                        "📌 **Variable Tenure (Permanencia):**\n\n"
                        "Suele mostrar altas concentraciones en los extremos (clientes muy nuevos o "
                        "clientes con mucha antiguedad). Los picos en los primeros meses representan "
                        "la zona critica de fuga de clientes vinculada al problema de negocio."
                    )
                elif var_seleccionada == "MonthlyCharges":
                    st.info(
                        "📌 **Variable MonthlyCharges (Cargos Mensuales):**\n\n"
                        "Permite identificar que rangos de tarifas son los mas comunes. "
                        "Un pico alto en tarifas bajas podria indicar una gran base de clientes con planes basicos."
                    )
                else:
                    st.info(
                        "📌 **Análisis Estadistico:**\n\n"
                        "Evalua si la curva de densidad (KDE) tiene una campana simetríca o si "
                        "el sesgo se inclina hacia la izquierda o derecha, lo cual ayuda a comprender "
                        "el valor promedio real de facturacion o permanencia."
                    )
                    
            with col_grafico:
                # Generamos el grafico
                fig_hist = st.session_state.processor.generar_histograma(var_seleccionada)
                
                # Renderizamos la figura de Matplotlib de forma nativa en Streamlit
                st.pyplot(fig_hist, use_container_width=True)

        # ---------------------------------------------------------------------
        # Pestaña 6: Analisis de variables categoricas
        # ---------------------------------------------------------------------
        with tab6:
            st.markdown("### 🗂️ Análisis de Variables Categoricas")
            st.write(
                "Explora la distribución, conteos y proporciones porcentuales de las "
                "variables cualitativas del dataset para entender el perfil de los clientes:"
            )
            
            # Obtenemos la lista de variables categoricas
            listas_variables = st.session_state.processor.clasificar_variables()
            variables_categoricas = listas_variables["categoricas"]
            
            # Removemos de las opciones de graficado por no aportar valor visual
            if "customerID" in variables_categoricas:
                variables_categoricas.remove("customerID")
                
            # Diseño en columnas para controles y visualizaciones
            col_controles_cat, col_tabla_cat, col_grafico_cat = st.columns([1.5, 1.5, 2])
            
            with col_controles_cat:
                var_cat_seleccionada = st.selectbox(
                    "Selecciona una variable categorica:",
                    options=variables_categoricas,
                    key="sb_categorico"
                )
                
                st.write("---")
                st.markdown("💡 **Contexto del Negocio:**")
                st.write(
                    "Analizar variables como Contract o InternetService permite mapear "
                    "que porcentaje de la cartera esta expuesto a contratos de mes a mes, "
                    "los cuales representan historicamente el mayor riesgo de fuga."
                )
                
            with col_tabla_cat:
                # Ejecutamos el metodo estadistico
                df_frec, fig_barras = st.session_state.processor.analizar_variable_categorica(var_cat_seleccionada)
                
                st.write("**Tabla de Frecuencias:**")
                st.dataframe(df_frec, use_container_width=True)
                
            with col_grafico_cat:
                # Renderizamos el grafico de barras
                st.pyplot(fig_barras, use_container_width=True)

        # ---------------------------------------------------------------------
        # Pestaña 7: Analisis Bivariado numerico vs categorico
        # ---------------------------------------------------------------------
        with tab7:
            st.markdown("### 📊 Análisis Bivariado (Numerico vs Churn)")
            st.write(
                "Compara las distribuciones de las variables númericas agrupadas por "
                "el estado de fuga de los clientes para identificar patrones de comportamiento:"
            )
            
            listas_variables = st.session_state.processor.clasificar_variables()
            variables_numericas = listas_variables["numericas"]
            
            col_ctrl7, col_graf7 = st.columns([2, 3])
            
            with col_ctrl7:
                var_num_bi = st.selectbox(
                    "Selecciona una variable numerica para el cruce:",
                    options=variables_numericas,
                    key="sb_bivariado_num"
                )
                st.write("---")
                st.markdown("💡 **Interpretación Estadistica:**")
                st.info(
                    "El grafico de cajas permite comparar visualmente la Mediana (linea central de la caja) "
                    "y la dispersión entre el grupo que permanece (No) y el que abandona (Yes).\n\n"
                    "Por ejemplo, una mediana de tenure mas baja en el grupo Yes confirmaria que "
                    "los clientes mas nuevos tienen mayor tendencia a la fuga."
                )
                
            with col_graf7:
                fig_box = st.session_state.processor.generar_boxplot_bivariado(var_num_bi)
                st.pyplot(fig_box, use_container_width=True)

        # ---------------------------------------------------------------------
        # Pestaña 8: Analisis categorico vs categorico
        # ---------------------------------------------------------------------
        with tab8:
            st.markdown("### 🗂️ Análisis Bivariado (Categorico vs Churn)")
            st.write(
                "Analiza como influyen las caracteristicas contractuales y los servicios "
                "contratados en las tasas de desercion de los clientes:"
            )
            
            variables_categoricas = listas_variables["categoricas"]
            exclusiones = ["customerID", "Churn"]
            opciones_cat_bi = [v for v in variables_categoricas if v not in exclusiones]
            
            col_ctrl8, col_graf8 = st.columns([2, 3])
            
            with col_ctrl8:
                var_cat_bi = st.selectbox(
                    "Selecciona una variable categorica para el cruce:",
                    options=opciones_cat_bi,
                    key="sb_bivariado_cat"
                )
                st.write("---")
                st.markdown("💡 **Foco del Análisis de Negocio:**")
                st.info(
                    "Compara la proporcion de barras en cada categoria. Si en una opcion "
                    "especifica (como contrato Month-to-month) la barra de Yes es proporcionalmente "
                    "muy alta en comparacion con las otras, se identifica un factor de riesgo directo."
                )
                
            with col_graf8:
                fig_barras_bi = st.session_state.processor.generar_barras_bivariado(var_cat_bi)
                st.pyplot(fig_barras_bi, use_container_width=True)

        # ---------------------------------------------------------------------
        # Pestaña 9: Analisis dinamico
        # ---------------------------------------------------------------------
        with tab9:
            st.markdown("### 🎛️ Análisis Dinamico Basado en Parametros")
            st.write(
                "Utiliza el selector multiple para construir tu propia vista del dataset. "
                "Debes seleccionar dos o mas variables númericas y el sistema calculara de forma "
                "automatica su matriz de correlación lineal:"
            )
            
            # Obtenemos todas las columnas disponibles
            todas_columnas = [col for col in st.session_state.dataset.columns if col != "customerID"]
            
            # Widget interactivo
            columnas_seleccionadas = st.multiselect(
                "Selecciona las columnas que deseas analizar:",
                options=todas_columnas,
                default=["tenure", "MonthlyCharges", "TotalCharges"],
                key="ms_dinamico"
            )
            
            if columnas_seleccionadas:
                # Ejecutamos la logica
                df_fil, fig_corr = st.session_state.processor.analizar_columnas_dinamicas(columnas_seleccionadas)
                
                col_tab_din, col_graf_din = st.columns([3, 2])
                
                with col_tab_din:
                    st.write("**Vista parcial de la seleccion (Primeros 10 registros):**")
                    st.dataframe(df_fil.head(10), use_container_width=True)
                    
                with col_graf_din:
                    if fig_corr is not None:
                        st.write("**Relacion Lineal (Heatmap):**")
                        st.pyplot(fig_corr, use_container_width=True)
                    else:
                        st.info(
                            "💡 **Nota automatica:** Selecciona al menos dos variables númericas "
                            "(por ejemplo, 'tenure' y 'MonthlyCharges') para desplegar el mapa de correlación."
                        )
            else:
                st.warning("⚠️ Selecciona al menos una columna para mostrar los datos en pantalla.")

        # ---------------------------------------------------------------------
        # Pestaña 10: Hallazgos claves
        # ---------------------------------------------------------------------
        with tab10:
            st.markdown("### 🎯 Hallazgos Clave e Insights de Negocio")
            st.write(
                "A traves del análisis exploratorio integrado, se han mapeado los principales "
                "detonantes y caracteristicas correlacionadas con la perdida de clientes:"
            )
            
            col_insights, col_graf_resumen = st.columns([2, 2])
            
            with col_insights:
                st.markdown("💡 **Insights Principales del EDA:**")
                st.warning(
                    "🔥 **1. Vulnerabilidad Contractual:**\n\n"
                    "Los clientes con contratos Month-to-month (mes a mes) exhiben una tasa de deserción "
                    "drasticamente superior al promedio de la cartera, representando el principal foco de alerta."
                )
                st.error(
                    "⚡ **2. El Paradoxo de la Fibra Optica:**\n\n"
                    "A pesar de ser un servicio de alta velocidad, los usuarios con internet de fibra optica "
                    "registran indices de abandono mas elevados. Esto podria indicar insatisfaccion con el precio, "
                    "problemas de estabilidad en la infraestructura o deficiencias en el soporte tecnico."
                )
                st.info(
                    "📉 **3. Periodo Critico de Retencion:**\n\n"
                    "El analisis de permanencia (tenure) demuestra que el riesgo maximo de fuga se concentra "
                    "en los primeros 6 meses de relacion comercial. Superado el primer año, la lealtad se incrementa notablemente."
                )
                
            with col_graf_resumen:
                fig_resumen = st.session_state.processor.generar_grafico_resumen_insights()
                st.pyplot(fig_resumen, use_container_width=True)

        # ---------------------------------------------------------------------
        # Concluciones finales
        # ---------------------------------------------------------------------
                st.write("---")
                st.markdown("## 🏁 Conclusiones Finales del Proyecto")
                st.write(
                    "Basado en el Análisis Exploratorio de Datos (EDA) desarrollado en este producto analitico, "
                    "se plantean 5 lineas de accion estrategicas orientadas a la toma de decisiones corporativas:"
                )
                
                conclusiones = [
                    "**Incentivar la migración contractual:** Diseñar politicas de descuento u otorgar beneficios de valor agregado (como servicios de streaming complementarios) para motivar a los usuarios de contratos Month-to-month a transicionar hacia planes anuales o bianuales, estabilizando los flujos de ingresos.",
                    "**Auditoria tecnica al servicio de Fibra Optica:** Establecer un comite de control de calidad e ingenieria para evaluar el servicio de internet por fibra optica, investigando si el alto churn responde a caidas del servicio, tarifas elevadas o una lenta respuesta del soporte de asistencia automatizada.",
                    "**Plan de contingencia para Clientes Nuevos:** Implementar un programa de acompañamiento intensivo (Onboarding program) enfocado en los clientes durante sus primeros 3 a 6 meses de antiguedad, aplicando encuestas proactivas de satisfaccion para mitigar la zona de maximo riesgo de desercion.",
                    "**Optimizacion de la estructura financiera de cargos:** Revisar la relacion entre MonthlyCharges y la retencion, estructurando paquetes modulares que permitan a los clientes de alta facturacion reducir componentes secundarios de su plan antes de optar por la cancelacion total del servicio.",
                    "**Rentabilizacion mediante estrategias de retencion focalizada:** Sabiendo que el costo de adquisicion (CAC) supera entre 6 y 7 veces al de retencion, reasignar el 15% del presupuesto de marketing de adquisicion global hacia campañas de fidelizacion de cuentas existentes identificadas dentro de los segmentos de riesgo estructural."
                ]
                
                for idx, conclusion in enumerate(conclusiones, 1):
                    st.markdown(f"> **{idx}.** {conclusion}")
                