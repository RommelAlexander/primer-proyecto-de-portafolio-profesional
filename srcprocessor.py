import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataProcessor:
    """
    Clase encargada de encapsular el procesamiento
    """
    def __init__(self, dataframe: pd.DataFrame):
        # Realizamos una copia para no modificar el archivo original
        self.df = dataframe.copy()
        
        # Convertir 'TotalCharges' a decimal
        # Transforma los espacios en blanco o textos corruptos en NaN
        if "TotalCharges" in self.df.columns:
            self.df["TotalCharges"] = pd.to_numeric(self.df["TotalCharges"], errors="coerce")
            # Llenamos los NaN con 0.0 para mantener la integridad de los decimales
            self.df["TotalCharges"] = self.df["TotalCharges"].fillna(0.0)

    def obtener_dimensiones(self):
        """Retorna filas y columnas del dataframe."""
        return self.df.shape

    def obtener_vista_previa(self, n=5):
        """Retorna las primeras n filas"""
        return self.df.head(n)

    def obtener_informacion_general(self):
        """
        Retorna un DataFrame con los tipos de datos y la 
        cantidad de valores nulos por cada columna
        """
        info_df = pd.DataFrame({
            "Tipo de Dato": self.df.dtypes.astype(str),
            "Valores Nulos": self.df.isnull().sum()
        })
        return info_df

    def clasificar_variables(self):
        """
        Funcion personalizada para identificar y clasificar 
        las variables
        """
        # Seleccionamos las columnas numericas (int y float)
        columnas_numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Las demas columnas se consideran categoricas o de texto
        columnas_categoricas = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        
        resultado = {
            "numericas": columnas_numericas,
            "categoricas": columnas_categoricas,
            "conteo_numericas": len(columnas_numericas),
            "conteo_categoricas": len(columnas_categoricas)
        }
        
        return resultado
    
    def obtener_estadisticas_descriptivas(self):
        """
        Calcula las estadisticas descriptivas de las variables 
        numericas
        """
        # Seleccionamos las variables numericas
        df_numerico = self.df.select_dtypes(include=[np.number])
        
        # Resumen descriptivo transpuuesto
        resumen = df_numerico.describe().T
        
        # Renombramos las columnas
        resumen = resumen.rename(columns={
            "count": "Conteo",
            "mean": "Media",
            "std": "Desviacion Estandar",
            "min": "Minimo",
            "25%": "Percentil 25 (Q1)",
            "50%": "Mediana (Q2)",
            "75%": "Percentil 75 (Q3)",
            "max": "Maximo"
        })
        
        return resumen
    
    def analizar_valores_faltantes(self):
        """
        Calcula el conteo absoluto y el porcentaje de valores 
        faltantes para cada una de las columnas del dataset
        """
        conteo_nulos = self.df.isnull().sum()
        porcentaje_nulos = (conteo_nulos / len(self.df)) * 100
        
        df_nulos = pd.DataFrame({
            "Valores Faltantes": conteo_nulos,
            "Porcentaje (%)": porcentaje_nulos.round(2)
        })
        
        # Filtramos para mostrar principalmente las columnas bajo analisis
        return df_nulos
    
    def generar_histograma(self, columna: str):
        """
        Genera un grafico de distribucion (histograma con KDE) 
        para una variable numerica especifica.
        Retorna el objeto figure de matplotlib.
        """
        # Limpiamos figuras previas en memoria para evitar solapamientos
        plt.clf()
        
        # Creamos el contenedor del grafico
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Dibujamos el histograma con una linea de densidad estimador (KDE)
        sns.histplot(
            data=self.df, 
            x=columna, 
            kde=True, 
            ax=ax, 
            color="#1f77b4",
            bins=30
        )
        
        ax.set_title(f"Distribucion de la Variable: {columna}", fontsize=12, pad=10)
        ax.set_xlabel(columna, fontsize=10)
        ax.set_ylabel("Frecuencia (Conteo)", fontsize=10)
        plt.tight_layout()
        
        return fig
    
    def analizar_variable_categorica(self, columna: str):
        """
        Calcula el conteo de frecuencias y proporciones para una variable 
        categorica. Ademas genera un grafico de barras correspondiente.
        Retorna una tupla
        """
        # Calculo de frecuencias absolutas y porcentajes
        conteo = self.df[columna].value_counts()
        proporcion = self.df[columna].value_counts(normalize=True) * 100
        
        df_frecuencias = pd.DataFrame({
            "Frecuencia Absoluta": conteo,
            "Proporción (%)": proporcion.round(2)
        })
        
        # Generacion del grafico de barras
        plt.clf()
        fig, ax = plt.subplots(figsize=(7, 4))
        
        sns.countplot(
            data=self.df,
            y=columna,
            ax=ax,
            palette="viridis",
            order=conteo.index
        )
        
        ax.set_title(f"Distribucion de Frecuencias: {columna}", fontsize=12, pad=10)
        ax.set_xlabel("Cantidad de Clientes", fontsize=10)
        ax.set_ylabel(columna, fontsize=10)
        plt.tight_layout()
        
        return df_frecuencias, fig
    
    def generar_boxplot_bivariado(self, columna_num: str):
        """
        Genera un grafico de cajas (Boxplot) para comparar una variable 
        numerica en funcion de la variable objetivo Churn.
        Retorna el objeto figure de matplotlib.
        """
        plt.clf()
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Dibujamos el boxplot comparativo
        sns.boxplot(
            data=self.df,
            x="Churn",
            y=columna_num,
            ax=ax,
            palette="Set2"
        )
        
        ax.set_title(f"Analisis Bivariado: {columna_num} vs Churn", fontsize=12, pad=10)
        ax.set_xlabel("Fuga de Cliente (Churn)", fontsize=10)
        ax.set_ylabel(columna_num, fontsize=10)
        plt.tight_layout()
        
        return fig

    def generar_barras_bivariado(self, columna_cat: str):
        """
        Genera un grafico de barras agrupadas para analizar la relacion 
        entre una variable categorica y la variable objetivo Churn
        """
        plt.clf()
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Creamos el conteo cruzado
        sns.countplot(
            data=self.df,
            x=columna_cat,
            hue="Churn",
            ax=ax,
            palette="Dark2"
        )
        
        ax.set_title(f"Analisis Bivariado: {columna_cat} vs Churn", fontsize=12, pad=10)
        ax.set_xlabel(columna_cat, fontsize=10)
        ax.set_ylabel("Cantidad de Clientes", fontsize=10)
        plt.xticks(rotation=15)
        plt.tight_layout()
        
        return fig
    
    def analizar_columnas_dinamicas(self, columnas: list):
        """
        Genera un resumen estadistico personalizado o una matriz de 
        correlacion heatmap basada en las columnas seleccionadas por el usuario.
        Retorna una tupla
        """
        if not columnas:
            return None, None
            
        # Filtramos el dataframe con las columnas elegidas
        df_filtrado = self.df[columnas]
        
        # Si hay al menos dos variables numericas, generamos un heatmap de correlacion
        df_num = df_filtrado.select_dtypes(include=[np.number])
        fig = None
        
        if df_num.shape[1] >= 2:
            plt.clf()
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(
                df_num.corr(), 
                annot=True, 
                cmap="coolwarm", 
                fmt=".2f", 
                ax=ax,
                vmin=-1,
                vmax=1
            )
            ax.set_title("Matriz de Correlacion Dinamica", fontsize=11, pad=10)
            plt.tight_layout()
            
        return df_filtrado, fig
    
    def generar_grafico_resumen_insights(self):
        """
        Genera un grafico de barras resumen que consolida la tasa de 
        fuga (Churn) en los segmentos mas criticos identificados.
        Retorna el objeto figure de matplotlib.
        """
        plt.clf()
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Calculamos segmentos criticos para demostrar insights con datos reales
        # Proporcion de churn en contrato mes a mes
        m2m = self.df[self.df["Contract"] == "Month-to-month"]
        tasa_m2m = (m2m["Churn"] == "Yes").mean() * 100
        
        # Proporcion de churn en servicio de internet de Fibra Optica
        fo = self.df[self.df["InternetService"] == "Fiber optic"]
        tasa_fo = (fo["Churn"] == "Yes").mean() * 100
        
        # Proporcion de churn general como linea de base (promedio)
        tasa_general = (self.df["Churn"] == "Yes").mean() * 100
        
        categorias = ["Contrato Mes a Mes", "Internet Fibra Optica", "Promedio General"]
        tasas = [tasa_m2m, tasa_fo, tasa_general]
        colores = ["#d62728", "#ff7f0e", "#7f7f7f"]
        
        bars = ax.bar(categorias, tasas, color=colores, width=0.6)
        
        # Añadimos etiquetas de porcentaje sobre cada barra
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%", ha="center", va="bottom", fontweight="bold")
            
        ax.set_title("Tasas de Fuga (Churn) en Segmentos de Alto Riesgo", fontsize=11, pad=15)
        ax.set_ylabel("Porcentaje de Fuga (%)", fontsize=10)
        ax.set_ylim(0, max(tasas) + 10)
        plt.tight_layout()
        
        return fig