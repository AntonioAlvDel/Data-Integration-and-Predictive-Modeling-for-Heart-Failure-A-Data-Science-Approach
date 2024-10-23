import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import ttk

df=pd.read_csv("DatosCancer/heart.csv")
string_col = df.select_dtypes(include="object").columns
df[string_col]=df[string_col].astype("string")
df[string_col].head()
df_numerical=pd.get_dummies(df,columns=string_col,drop_first=False)
df_numerical.head()


scaler = MinMaxScaler()
data = pd.DataFrame(scaler.fit_transform(df_numerical), columns=df_numerical.columns)


# Variables predictoras (X): todas las columnas excepto 'HeartDisease'
x = data.drop('HeartDisease', axis=1)

# Variable objetivo (Y): 'HeartDisease'
y = data['HeartDisease']

# Division
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 1)

# Ajuste del modelo
classifier = SVC(C=10,gamma=0.01,kernel='rbf').fit(x_train, y_train)
y_train_pred = classifier.predict(x_train)
y_test_pred = classifier.predict(x_test)


def prediccion():
    try:
        # Obtener los valores ingresados por el usuario
        datos = {
            'Age': int(entradas_variables[0].get()),
            'Sex': str(entradas_variables[1].get()),
            'ChestPainType': str(entradas_variables[2].get()),
            'RestingBP': int(entradas_variables[3].get()),
            'Cholesterol': int(entradas_variables[4].get()),
            'FastingBS': int(entradas_variables[5].get()),
            'RestingECG': str(entradas_variables[6].get()),
            'MaxHR': int(entradas_variables[7].get()),
            'ExerciseAngina': str(entradas_variables[8].get()),
            'Oldpeak': int(entradas_variables[9].get()),
            'ST_Slope': str(entradas_variables[10].get()),
        }
        data_input = pd.DataFrame(datos, index=[0])
        # Añadir la nueva fila al principio del DataFrame original
        df_input = pd.concat([data_input, df], ignore_index=True)
        df_input = df_input.drop(columns=['HeartDisease'])
        string_col = df_input.select_dtypes(include="object").columns
        df_input[string_col]=df_input[string_col].astype("string")
        df_numerical_input=pd.get_dummies(df_input,columns=string_col,drop_first=False)
        scaler_input = MinMaxScaler()
        data = pd.DataFrame(scaler_input.fit_transform(df_numerical_input), columns=df_numerical_input.columns)
        y_output = classifier.predict(data.head(1))
        resultado_var.set(f"Resultado clínico: {int(y_output)}")

    except Exception as e:
        resultado_var.set(f"Error: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de fallo cardíaco")

# Crear etiquetas y entradas para las variables
etiquetas_variables = []
entradas_variables = []
nombre_variables = ["Edad","Género","Dolor en el pecho","Presion arterial en reposo","Colesterol","Glucemia en ayunas","Electrocardiograma en reposo","Frecuencia cardiaca máxima","Angina","Oldpeak","ST_Slope"]

for i in range(0, 11):
    etiqueta = ttk.Label(ventana, text=f"  {nombre_variables[i]}:", anchor="w")
    etiqueta.grid(row=i, column=0, padx=10, pady=5)
    etiquetas_variables.append(etiqueta)

    entry_variable = ttk.Entry(ventana)
    entry_variable.grid(row=i, column=1, padx=10, pady=5)
    entradas_variables.append(entry_variable)

# Etiqueta de informacion aidicional
precision_label = ttk.Label(ventana, text="Mínimo rendimiento obtenido del modelo", anchor="w")
precision_label.grid(row=0, column=2, padx=10, pady=5)

exhaustividad_label = ttk.Label(ventana, text="Precisión: 0.881", anchor="w")
exhaustividad_label.grid(row=1, column=2, padx=10, pady=5)

generosidad_label = ttk.Label(ventana, text="Exactitud: 0.892", anchor="w")
generosidad_label.grid(row=2, column=2, padx=10, pady=5)

generosidad_label = ttk.Label(ventana, text="Exhaustividad: 0.899", anchor="w")
generosidad_label.grid(row=3, column=2, padx=10, pady=5)

# Botón para calcular la suma
boton_calcular = ttk.Button(ventana, text="Calculadora", command=prediccion)
boton_calcular.grid(row=13, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado
resultado_var = tk.StringVar()
etiqueta_resultado = ttk.Label(ventana, textvariable=resultado_var)
etiqueta_resultado.grid(row=14, column=0, columnspan=2, pady=5)

# Iniciar el bucle principal
ventana.mainloop()
