from flask import Flask, jsonify, render_template  # Agregar render_template
import pandas as pd

app = Flask(__name__)

# Ruta del archivo Excel
excel_file = 'data/datos.xlsx'

# Función para cargar y limpiar las hojas de Excel en DataFrames
def load_data():
    df_fact = pd.read_excel(excel_file, sheet_name='HECHOS')
    df_dim1 = pd.read_excel(excel_file, sheet_name='Maestro Deportistas')
    df_dim2 = pd.read_excel(excel_file, sheet_name='Maestro Bares')
    df_dim3 = pd.read_excel(excel_file, sheet_name='Maestro Gasto')
    
    # Limpieza de datos: remplazar NaN por None
    df_fact = df_fact.where(pd.notnull(df_fact), None)
    df_dim1 = df_dim1.where(pd.notnull(df_dim1), None)
    df_dim2 = df_dim2.where(pd.notnull(df_dim2), None)
    df_dim3 = df_dim3.where(pd.notnull(df_dim3), None)
    
    return df_fact, df_dim1, df_dim2, df_dim3

df_fact, df_dim1, df_dim2, df_dim3 = load_data()

# Endpoint para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Endpoints para devolver los datos en formato JSON
@app.route('/data/fact')
def get_fact_data():
    # Calcular el "Gasto Total" multiplicando el precio por la cantidad
    df_fact['Gasto Total'] = df_fact['Precio'] * df_fact['Cantidad']

    # Agrupar por deportista y sumar el "Gasto Total" por cada deportista
    fact_data = df_fact.groupby('Deportista ID')['Gasto Total'].sum().reset_index()

    # Unir los datos con la tabla de Maestro Deportistas para obtener los nombres de los deportistas
    fact_data = pd.merge(fact_data, df_dim1[['Deportista ID', 'Deportista']], on='Deportista ID', how='left')

    # Convertir los datos a un formato adecuado para JSON
    data = fact_data.to_dict(orient='records')

    return jsonify(data)


@app.route('/data/dimension1')
def get_dimension1_data():
    return jsonify(df_dim1.to_dict(orient='records'))

@app.route('/data/dimension2')
def get_dimension2_data():
    return jsonify(df_dim2.to_dict(orient='records'))

@app.route('/data/dimension3')
def get_dimension3_data():
    return jsonify(df_dim3.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)



