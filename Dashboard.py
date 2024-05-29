import dash
from dash import dcc, html
from dash import dash_table
import plotly.express as px
import pandas as pd

#Cargar el dataset
df = pd.read_excel('dataset.xlsx')
#Renombrar las variables para la visualización
df = df.rename(columns={'Edad': 'Edad', 'Género': 'Género', 'Estatus de relación': 'Estado Civil', 
                        'Tiempo en TikTok (horas)': 'TikTok(h)', 'Tiempo en Instagram (horas)': 'instagram(h)', 
                        'Tiempo en Twitter (horas)': 'Twitter(h)', 'Tiempo en Youtube (horas)': 
                        'Youtube(h)', 'Tiempo total en horas': 'Tiempo total(h)', 
                        'Tiempo de concentración (minutos)':'Concentración(min)', 
                        'Comparación en redes sociales (0-10)': 'Escala comparación', 
                        'Depresión (0-10)': 'Escala Depresión', 'Calidad del sueño (0-10)': 
                        'Escala Sueño', 'Estrés (0-10)': 'Escala Estrés', 
                        'Frecuencia de deporte a la semana': 'Frecuencia deporte(sem)'})


#Función para obtener df.info
def get_info(df):
    info_data = {
        'Variable': df.columns,
        'Tipo de dato': ['Numérico' if pd.api.types.is_numeric_dtype(df[col]) else 'Categórico' for col in df.columns],
        'Valores nulos': [df[col].isnull().sum() > 0 for col in df.columns]
    }
    info_df = pd.DataFrame(info_data)
    
    info_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in info_df.columns],
        data=info_df.to_dict('records'),
        style_header={
            'backgroundColor': '#343a40',
            'color': 'white',
            'font-family': 'Baghdad'
        },
        style_cell={
            'backgroundColor': '#21232C',
            'color': 'white',
            'textAlign': 'left',
            'font-family': 'Baghdad'
        },
        style_table={
            'height': 'auto'
        }
    )

    num_data = len(df) 

    return html.Div([
        html.H2('Información del DataFrame', style={'color': '#FFFFFF'}),
        info_table,
        html.P(f'Cantidad de datos: {num_data}', style={'color': '#FFFFFF'})
    ])

#Función para obtener df.describe
def get_describe(df):
    description = df.describe().transpose()
    description['std'] = description['std'].apply(lambda x: f"{x:.2f}")
    description.columns = ['Conteo', 'Promedio', 'Desviación estándar', 'Mínimo', '25%', 'Mediana', '75%', 'Máximo']
    description.reset_index(inplace=True)
    description.rename(columns={'index': 'Variable'}, inplace=True)
    
    describe_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in description.columns],
        data=description.to_dict('records'),
        style_header={
            'backgroundColor': '#343a40',
            'color': 'white',
            'font-family': 'Baghdad'
        },
        style_cell={
            'backgroundColor': '#21232C',
            'color': 'white',
            'textAlign': 'left',
            'font-family': 'Baghdad'
        },
        style_table={
            'height': '400px',
            'overflowY': 'auto'
        }
    )
    
    return html.Div([
        html.H2('Estadísticas Descriptivas', style={'color': '#FFFFFF'}),
        describe_table
    ])

#Gráficas

numeric_df = df.select_dtypes(include=int)

#Boxplot
box_fig = px.box(numeric_df, title='Distribución de las variables')
box_fig.update_layout(
    template='plotly_dark',
    xaxis_tickangle=-45, 
    xaxis_tickfont=dict(size=10), 
    yaxis_tickfont=dict(size=10),
    plot_bgcolor='#21232C',
    paper_bgcolor='#21232C'
)
box_fig = dcc.Graph(figure=box_fig)

#Mapa de calor
corr_fig = px.imshow(numeric_df.corr(), title='Correlación entre Variables', )
corr_fig.update_layout(
    template='plotly_dark',
    xaxis_tickangle=-45, 
    xaxis_tickfont=dict(size=10), 
    yaxis_tickfont=dict(size=10),
    plot_bgcolor='#21232C',
    paper_bgcolor='#21232C'
)
corr_div = dcc.Graph(figure=corr_fig)

#Usuarios mundiales de las redes sociales
#Cargar el dataset obtenido de Webscrapping
df_web = pd.read_excel('dataset_web_scraping.xlsx')
df_web_filtered = df_web[df_web['Characteristic'].isin(['YouTube', 'Instagram', 'TikTok', 'X/Twitter'])]
barras_usuarios_fig = px.bar(df_web_filtered, x='Number of active users in millions', y='Characteristic', 
                             title='Usuarios mundiales de las Redes Sociales',
                             labels={'Number of active users in millions': 'Usuarios Activos (mill)', 'Characteristic': 'Red Social'},
                             orientation='h')
barras_usuarios_fig.update_layout(
    template='plotly_dark',
    xaxis_tickangle=-45, 
    xaxis_tickfont=dict(size=10), 
    yaxis_tickfont=dict(size=10),
    plot_bgcolor='#21232C',
    paper_bgcolor='#21232C'
)
barras_usuarios_div = dcc.Graph(figure=barras_usuarios_fig)

#Gráfico de las horas de deporte a la semana relacionado al estrés
deporte_estres_fig = px.scatter(df, x='Frecuencia deporte(sem)', y='Escala Estrés', title='Estrés por frecuencia de deporte')
deporte_estres_fig.update_layout(
    title='Estrés por frecuencia de deporte',
    xaxis_title='Frecuencia deporte (sem)',
    yaxis_title='Escala de Estrés',
    plot_bgcolor='#21232C',
    paper_bgcolor='#21232C',
    font=dict(color='white')
)
deporte_estres_fig = dcc.Graph(figure=deporte_estres_fig)

#Gráfico de histograma para el tiempo total en redes sociales
total_instagram = df.groupby('Género')['instagram(h)'].sum().reset_index(name='Horas totales')
total_instagram['Redes Sociales'] = 'Instagram'
total_tiktok = df.groupby('Género')['TikTok(h)'].sum().reset_index(name='Horas totales')
total_tiktok['Redes Sociales'] = 'TikTok'
total_twitter = df.groupby('Género')['Twitter(h)'].sum().reset_index(name='Horas totales')
total_twitter['Redes Sociales'] = 'Twitter'
total_youtube = df.groupby('Género')['Youtube(h)'].sum().reset_index(name='Horas totales')
total_youtube['Redes Sociales'] = 'YouTube'

df_t_rs = pd.concat([total_instagram, total_tiktok, total_twitter, total_youtube], ignore_index=True)

tiempo_total_fig = px.bar(df_t_rs, x='Redes Sociales', y='Horas totales', labels={'Horas totales': 'Horas totales de los encuestados'},
             title='Total de las horas en redes sociales', color= 'Género', barmode='stack')
tiempo_total_fig.update_layout(template='plotly_dark', 
                                plot_bgcolor='#21232C', 
                                paper_bgcolor='#21232C',
                                font_color='#FFFFFF')
                                
tiempo_total_div = dcc.Graph(figure=tiempo_total_fig)

#Gráfica de estado civil y Escala de depresión
estatus_depresion_fig = px.box(df, x='Estado Civil', y='Escala Depresión', points="all", title='Depresión por Estatus de Relación')
estatus_depresion_fig.update_layout(
        title='Depresión con respecto al estado civil',
        xaxis_title='Estado civil',
        yaxis_title='Escala de depresión',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )

estatus_depresion_fig = dcc.Graph(figure=estatus_depresion_fig)


#Gráficas de barras percepción redes sociales
#Grafica de concentracion
counts_concentracion = df['Concentración(min)'].value_counts().sort_index()
bar_concentracion = px.bar(x=counts_concentracion.index, y=counts_concentracion.values, 
                 category_orders={'x': [str(i) for i in range(11)]})
bar_concentracion.update_layout(

        xaxis_title='Minutos de concetración',
        yaxis_title='Conteo personas',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )

#Grafica de comparacion
counts_comparation = df['Escala comparación'].value_counts().sort_index()
bar_comparation = px.bar(x=counts_comparation.index, y=counts_comparation.values, 
                 category_orders={'x': [str(i) for i in range(11)]})
bar_comparation.update_layout(
        xaxis_title='Escala de comparación (0-10)',
        yaxis_title='Conteo personas',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )

#Grafica de sueño
counts_sleep = df['Escala Sueño'].value_counts().sort_index()
bar_sleep = px.bar(x=counts_sleep.index, y=counts_sleep.values, 
                 category_orders={'x': [str(i) for i in range(11)]})
bar_sleep.update_layout(
        xaxis_title='Escala de Sueño (0-10)',
        yaxis_title='Conteo personas',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )

#Grafica de Depresión
counts_depression = df['Escala Depresión'].value_counts().sort_index()
bar_depression = px.bar(x=counts_depression.index, y=counts_depression.values, 
                 category_orders={'x': [str(i) for i in range(11)]})
bar_depression.update_layout(
        xaxis_title='Escala de Depresión (0-10)',
        yaxis_title='Conteo personas',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )

#Grafica de Estrés
counts_stress = df['Escala Estrés'].value_counts().sort_index()
bar_stress = px.bar(x=counts_stress.index, y=counts_stress.values, 
                 category_orders={'x': [str(i) for i in range(11)]})
bar_stress.update_layout(
        xaxis_title='Escala de Estrés (0-10)',
        yaxis_title='Conteo personas',
        plot_bgcolor='#21232C',
        paper_bgcolor='#21232C',
        font=dict(color='white')
    )


#Creación de app de Dash
app = dash.Dash(__name__)

#Diseño del Dashboard
app.layout = html.Div([
    html.H1('Dashboard de variables de la salud con respecto a las redes sociales', style={'textAlign': 'center', 'font-family': 'Baghdad', 'color': '#d4d4d4'}),
    
    #Primera fila
    html.Div([
        html.Div([
            html.Div(get_info(df), style={'color': '#FFFFFF', 'height': '100%'})
        ], style={'flex': 1, 'backgroundColor': '#21232C', 'height': '570px', 'margin-right': '10px', 'margin-bottom': '10px'}),
        
        html.Div([
            html.Div(get_describe(df), style={'color': '#FFFFFF', 'height': '100%'})
        ], style={'flex': 1, 'backgroundColor': '#21232C', 'height': '570px'})
    ], style={'display': 'flex', 'alignItems': 'flex-start', 'margin-bottom': '10px'}),
    
    # Segunda fila
    html.Div([
        html.Div([
            box_fig #Distribución de las variables
        ], id='histograma-div', style={'flex': 1, 'backgroundColor': '#21232C', 'margin-right': '10px', 'height':'510px'}),
        html.Div([
            corr_div #Gráfico de correlación
        ], id='correlacion-div', style={'flex': 1, 'backgroundColor': '#21232C', 'margin-right': '10px', 'height':'510px'}),
        html.Div([
            barras_usuarios_div,  #Usuarios mundiales de redes sociales
            html.P('*de un estudio realizado con KEPIOS en 2024 de estatista.com', style={'textAlign': 'right', 'color': 'white', 'margin-right': '10px'})
        ], id='barras-usuarios-div', style={'flex': 1, 'backgroundColor': '#21232C', 'height':'510px'})
    ], style={'display': 'flex', 'alignItems': 'flex-start', 'margin-bottom': '10px'}),
    
    # Tercera fila
    html.Div([
        html.Div([
            deporte_estres_fig #Estrés vs deporte
        ], id='barras-m-horas-div', style={'flex': 1, 'backgroundColor': '#21232C', 'height': '500px', 'margin-right': '10px'}),
        html.Div([
            tiempo_total_div #Tiempo total por género y por red social
        ], id='tiempo-total-div', style={'flex': 1, 'backgroundColor': '#21232C', 'height': '500px', 'margin-right': '10px'}),
        html.Div([
            estatus_depresion_fig #Depresión vs Estado Civil
        ], id='estres-redes-div', style={'flex': 1, 'backgroundColor': '#21232C', 'height': '500px'})
    ], style={'display': 'flex', 'alignItems': 'flex-start', 'margin-bottom': '10px'}),
    
    #Cuarta fila
    html.Div([
        html.H2('Percepción de variables de salud', style={'textAlign': 'center', 'font-family': 'Baghdad', 'color': 'white'})
    ], style={'display': 'flex', 'justifyContent': 'center', 'backgroundColor': '#21232C'}),
        
    html.Div([
        html.Div([
            dcc.Graph(figure=bar_concentracion)
        ], id='bar_concentracion', style={'backgroundColor': '#21232C', 'height': '500px', 'flex': 1}),
        
        html.Div([
            dcc.Graph(figure=bar_comparation)
        ], id='graph2-div', style={'backgroundColor': '#21232C', 'height': '500px', 'flex': 1}),
        
        html.Div([
            dcc.Graph(figure=bar_sleep)
        ], id='bar_comparation', style={'backgroundColor': '#21232C', 'height': '500px', 'flex': 1}),
    ], style={'display': 'flex', 'alignItems': 'flex-start'}),
    
    html.Div([
        html.Div([
            dcc.Graph(figure=bar_depression)
        ], id='bar_depression', style={'backgroundColor': '#21232C', 'height': '500px', 'flex': 1}),
        
        html.Div([
            dcc.Graph(figure=bar_stress)
        ], id='bar_stress', style={'backgroundColor': '#21232C', 'height': '500px', 'flex': 1}),
    ], style={'display': 'flex', 'alignItems': 'flex-start', 'margin-bottom': '10px'})
], style={'font-family': 'Baghdad', 'padding': '10px', 'background': '#282A35', 'height': '100vh', 'overflowY': 'scroll'})

if __name__ == '__main__':
    app.run_server(debug=True)