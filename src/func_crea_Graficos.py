#funcion para crear el grafico 
import plotly.express as px


def crear_grafico_pie(df, filtrarPor, my_dropdown, name,names,title):
    # filtrar el dataframe por la unidad seleccionada
    dff = df[df[filtrarPor]==my_dropdown]
    
    # contar el número de elementos por rama
    dff = dff.groupby([names]).size().reset_index(name=name)
    
    # crear el gráfico de tarta
    fig_pie = px.pie(
        data_frame=dff,
        names=names,
        values=name,
        color_discrete_sequence=px.colors.sequential.RdBu,
        title=title,
        
    )                   
    # Modifica el tamaño de la letra de los porcentajes
    fig_pie.update_layout(
        
        title_font={"size": 15, "family": "Arial Black, sans-serif"}
    )
    return fig_pie
