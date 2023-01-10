import pandas as pd
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
import dash_table as dt
from flask import Flask
from dash_core_components import Graph
from dash import dash_table

from dash.dash_table.Format import Group
from dash import Dash, dash_table
from func_crea_Graficos import crear_grafico_pie
#from func_crea_tablas_simple import create_table_simple
# import dash_bootstrap_components as dbc


meta_tags= [{'name':'viewport','content': 'width=device-width'}]
external_stylesheets=[meta_tags,'assets/css.css','assets/normalize.css']
#https://necolas.github.io/normalize.css/

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = Flask(__name__)

# Read data from Excel file
df = pd.read_excel("Plantilla Qna 24.xlsx", sheet_name='Resultados')
df = df[["UM", "RFC", "A.Paterno", "A.Materno", "Nombre", "SUELDO TAB", "CÓDIGO", "ADSCRIPCION", "Area Hosp", "Sub-Area Hosp", "NUCLEOS", "RAMA", "UNIDAD", "TURNO", "EN_PLANTILLA", "NORMATIVA"]]

# Define colors for the app
colors = {
    'background': '#621132',
    'background2': '#b38e5d',
    'background3': '#000000',
    'text': '#b38e5d',
    'text1': '#621132',
    'text2': '#ffffff',
    'text3': '#000000',
}
 



#-------------Decorador que da iteractividad al segundo dropdown------------------
@app.callback(
  
    Output('seleccionaUnidades', 'options'),
    Input('seleccionaUnidad', 'value')
)

def set_cities_options(chosen_state):
       if (chosen_state)!= 'JURISDICCIONES':
            dff = df[df['UNIDAD']==(chosen_state)]   
            return [{'label': c, 'value': c} for c in sorted(dff.ADSCRIPCION.unique())]
       elif (chosen_state)== 'JURISDICCIONES':
            dff = df[df['UNIDAD']==(chosen_state)]  
            return [{'label': c, 'value': c} for c in sorted(dff.ADSCRIPCION.unique())]
          
#--------------- Decorador para mostrar una unidad al inicio del programa --------------------
@app.callback(
        Output('seleccionaUnidades', 'value'),
        Input('seleccionaUnidades', 'options')
)
def set_cities_options(chosen_state1):  
        return [k['value']for k in chosen_state1 ][0]



 #----------------Decorador grafico general por ramas -----------------------------------------
@app.callback(
    Output(component_id='the_graph1', component_property='figure'),
    
    Input(component_id='seleccionaUnidad', component_property='value')    
    )
def update_graph_pie(my_dropdown):
    return crear_grafico_pie(df, 'UNIDAD', my_dropdown,'numeroRama','RAMA','Distribución Global por Ramas')

    #--------------Decorador grafico general por Turnos -----------------------------------------
@app.callback(
     Output(component_id='the_graphTurnos', component_property='figure'),
     Input(component_id='seleccionaUnidad', component_property='value')      
    )
  
def update_graph_pie(my_dropdown):
    return crear_grafico_pie(df, 'UNIDAD',my_dropdown,'numeroTurno','TURNO','Distribución Global por Turnos')
 
#------------------Decorador grafico por unidad por Ramas -----------------------------------------
@app.callback(
     Output(component_id='theGraphUnidadRamas', component_property='figure'),
    Input(component_id='seleccionaUnidades', component_property='value')      
)

def update_graph_pie(my_dropdown):
    print(my_dropdown)
    return crear_grafico_pie(df,'ADSCRIPCION', my_dropdown, 'numeroRama','RAMA','Distribución por Unidad por Ramas')

#------------------Decorador grafico por unidad por Turnos -----------------------------------------
@app.callback(
     Output(component_id='theGraphUnidadTurnos', component_property='figure'),
    Input(component_id='seleccionaUnidades', component_property='value')      
)

def update_graph_pie(my_dropdown):
    print(my_dropdown)
    return crear_grafico_pie(df,'ADSCRIPCION', my_dropdown, 'numeroTurno','TURNO','Distribución por Unidad por Turnos')


#------------------Decorador tabla unidad rama---------------------
@app.callback(
  Output(component_id='tabla', component_property='data'),
  Input(component_id='seleccionaUnidad', component_property='value')
)
def update_table(seleccionaUnidad):
  dffTabla = df[df['UNIDAD']==(seleccionaUnidad)]
  dffTabla1= dffTabla.groupby(['RAMA']).size().reset_index(name='EN_PLANTILLA')

  # Calcula el total de la columna 'EN_PLANTILLA'
  TOTAL = dffTabla1['EN_PLANTILLA'].sum()

  # Agrega una fila al final de la tabla con el total
  dffTabla1 = dffTabla1.append({'RAMA': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

  return dffTabla1.to_dict('records')

#---------------Decorador tabla global turno-----------------
@app.callback(
 Output(component_id='tabla2', component_property='data'),   
Input(component_id='seleccionaUnidad', component_property='value')    
)

def update_table(seleccionaUnidad):
 
      
     dffTabla = df[df['UNIDAD']==(seleccionaUnidad)]
    
     dffTabla2= dffTabla.groupby(['TURNO']).size().reset_index(name='EN_PLANTILLA')
    
     # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla2['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla2 = dffTabla2.append({'TURNO': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)


    
     return dffTabla2.to_dict('records')
   


#------------decorador tabla global rama ----------------
@app.callback(
 Output(component_id='tabla3', component_property='data'),   
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
 
      
     dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
     dffTabla3= dffTabla.groupby(['RAMA']).size().reset_index(name='EN_PLANTILLA')
     
      # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla3['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla3 = dffTabla3.append({'RAMA': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)



     return dffTabla3.to_dict('records')
   
#------------Decorador tabla unidad turno ----------------
@app.callback(
 Output(component_id='tabla4', component_property='data'),   
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
 
      
     dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
     dffTabla4= dffTabla.groupby(['TURNO']).size().reset_index(name='EN_PLANTILLA')
     
     # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla4['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla4 = dffTabla4.append({'TURNO': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

     return dffTabla4.to_dict('records')


#----------------------------------------------------------------------------


#data table
@app.callback(
Output(component_id='table1X', component_property='data'),
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
   
    tipo_hospital={
        'C60':{"MATUTINA":123, "VESPERTINA":56, "VELADA A":31, "VELADA B":29, 
        "ESPECIAL DIURNA":30, "ESPECIAL NOCTURNA":0, "JORNADA ACUMULADA":0,"NO_DEFINIDO":0},

        'C50':{} 

        }
   
   
   
    # Inicializamos dffTabla1x como un DataFrame vacío
    dffTabla1x = pd.DataFrame()
 
    if seleccionaUnidades == 'HOSPITAL GENERAL DE APAN':
        print("lucatero")

        #C60={"MATUTINA":123, "VESPERTINA":56, "VELADA A":31, "VELADA B":29, "ESPECIAL DIURNA":30, "ESPECIAL NOCTURNA":0, "JORNADA ACUMULADA":0,"NO_DEFINIDO":0} 
        df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C60'][x] if not pd.isnull(x) else 0)


        # Aquí asignamos un valor a dffTabla1x
        dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
        dffTabla1x= dffTabla.groupby(['ADSCRIPCION','TURNO','NORMATIVA']).size().reset_index(name='EN_PLANTILLA')
       


        # Calcula el total de la columna 'EN_PLANTILLA'
        TOTAL = dffTabla1x['EN_PLANTILLA'].sum()
        TOTAL1= dffTabla1x['NORMATIVA'].sum()
    # Agrega una fila al final de la tabla con el total
        dffTabla1x =  dffTabla1x.append({'ADSCRIPCION': 'TOTAL', 'EN_PLANTILLA': TOTAL,  'NORMATIVA':TOTAL1}, ignore_index=True)
        
    # Aquí podemos utilizar dffTabla1x sin problema
    return dffTabla1x.to_dict('records')

   

 #----------------------app.layout-------------------------

app.layout= html.Div([
    
    html.Div([
                # Create marquee
                html.Marquee(id='marquee', children='Prueba rápida VIH, márcate un día y háztela.', style={'color': colors['text2']}),
                # Create logo
                html.Img(src='assets/logo.png'),
                    ],className='header'),
   
    html.Div([
                # Create header
                html.H1("DIRECCIÓN DE RECURSOS HUMANOS", className='title_text')
                ],className='header_title'),

                 
   
    html.Div([
                
        html.Label("Seleccione una Unidad:", style={'fontSize': 15, 'textAlign': 'center', 'font-weight': 'bold', 'color': colors['text']}),
        #-------------------Primer Dropdown-----------------------------------------
        dcc.Dropdown(
        id='seleccionaUnidad',
        options=[{'label': s, 'value': s} for s in sorted(df.UNIDAD.unique())],
        value='HOSPITALES',
        clearable=False,
        searchable=False,
        style={'backgroundColor': colors['background2'],'color': colors['text1'], 'font-size': 15, 'font-weight': 'bold'})

    ]),

   

    html.Div([
        #---------------------grafica ramas--------------------------------------------
         dcc.Graph(id='the_graph1'),
       
        
        #------------------- tabla unidades principal----------------------------------
        html.Label("Distribucion Global por Ramas:", style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}), 
        
        dash_table.DataTable(       
            id='tabla',        

            columns = [
            {"name": "RAMA", "id": "RAMA"},
            {"name": "EN_PLANTILLA","id": "EN_PLANTILLA",},
            ],

            
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
          
           
            selected_columns=[],
            selected_rows=[],
          
            page_action="native",
            page_current= 0,
            page_size= 10,
            
            style_data=   {'color':  '#ffffff',
                           'backgroundColor':'#621132'},

            fixed_rows =  {'headers':True},

            style_table = {'maxHeight':'px',
                           'backgroundColor':'#621132',                        
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_cell =  { 'textAlign':'left',
                            'border':'4px solid white',
                            'color':'#b38e5d',
                            'maxWidth':'10px',                           
                            'textOverflow':'ellipsis'

                }
                )




    ], className='container'),
    


    html.Div([

        #------------------tabla turnos------------------------
   # num_rows = len(dffTabla2)  # replace df with your dataframe
  html.Label("Distribucion Global por Turnos:", style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}),  
    #-------------------grafico rama por unidad------------------------
        dcc.Graph(id='the_graphTurnos'),
dash_table.DataTable(
    id='tabla2',
    columns = [
        {"name": "TURNO", "id": "TURNO"},
        {"name": "EN_PLANTILLA","id": "EN_PLANTILLA",}, 
    ],
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",         
    selected_columns=[],
    selected_rows=[],
    page_action="native",  # set this to 'none'
   # page_current= 0,
   # page_size= 10,  # set this to the total number of rows
    style_data=     {'color':  '#ffffff',
                     'backgroundColor':'#621132'},
    
    fixed_rows =    {'headers':True},
    
    style_table =   {'maxHeight':'350px',
                     'backgroundColor':'#621132',
                     'color':  '#ffffff',
                     'overflowY': 'none'},  # set this to 'none'
    
    style_header =  {'backgroundColor':'#000000',
                     'fontWeight':'bold',
                     'border':'4px solid white',
                     'textAlign':'center'},        
    
    style_cell =    {'textAlign':'left',
                     'border':'4px solid white',
                     'color':'#b38e5d',
                     'maxWidth':'10px',                           
                     'textOverflow':'ellipsis'
            }
)
 

    ]), 

html.Div([
        html.Label("Seleccione una Adscripción:", style={'fontSize':15, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}),
        #----------------------Segundo Dropdown--------------------------------------
        dcc.Dropdown(  
        id='seleccionaUnidades',   
        options=[],
        multi=False,
        style={'backgroundColor': colors['background2'],'color': colors['text1'], 'font-size': 15, 'font-weight': 'bold'})        
     ],style={'border-color': '#333', 'border-width': '2px', 'border-style': 'dashed'}),

html.Div([
    #--------------------grafico por unidad por ramas------------------------------------------
      dcc.Graph(id='theGraphUnidadRamas'),   
    #------------------- tabla Unidades rama  ----------------------------------
        html.Label("Distribucion por Unidad por Rama:", style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}),  
        dash_table.DataTable(       
            id='tabla3',        

            columns = [
            {"name": "RAMA", "id": "RAMA"},
            {"name": "EN_PLANTILLA","id": "EN_PLANTILLA",},
            ],

            
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
          
           
            selected_columns=[],
            selected_rows=[],
          
            page_action="native",
            page_current= 0,
            page_size= 10,
            
            style_data=   {'color':  '#ffffff',
                           'backgroundColor':'#621132'},

            fixed_rows =  {'headers':True},

            style_table = {'maxHeight':'px',
                           'backgroundColor':'#621132',                        
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_cell =  { 'textAlign':'left',
                            'border':'4px solid white',
                            'color':'#b38e5d',
                            'maxWidth':'10px',                           
                            'textOverflow':'ellipsis'

                }
                )

]),

 html.Div([
     
        #------------------tabla por unidad  turnos------------------------
 #--------------------grafico por unidad por ramas------------------------------------------
      dcc.Graph(id='theGraphUnidadTurnos'), 
 
 html.Label("Distribucion por Unidad por Turnos:", style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}),  

dash_table.DataTable(
    id='tabla4',
    columns = [
        {"name": "TURNO", "id": "TURNO"},
        {"name": "EN_PLANTILLA","id": "EN_PLANTILLA",}, 
    ],
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",         
    selected_columns=[],
    selected_rows=[],
    page_action="none",  # set this to 'none'
   # page_current= 0,
   # page_size= 10,  # set this to the total number of rows
    style_data=     {'color':  '#ffffff',
                     'backgroundColor':'#621132'},
    
    fixed_rows =    {'headers':True},
    
    style_table =   {'maxHeight':'350px',
                     'backgroundColor':'#621132',
                     'color':  '#ffffff',
                     'overflowY': 'none'},  # set this to 'none'
    
    style_header =  {'backgroundColor':'#000000',
                     'fontWeight':'bold',
                     'border':'4px solid white',
                     'textAlign':'center'},        
    
    style_cell =    {'textAlign':'left',
                     'border':'4px solid white',
                     'color':'#b38e5d',
                     'maxWidth':'10px',                           
                     'textOverflow':'ellipsis'
            }
)
 

    ]), 



html.Div([
    
html.Label("Comparación de Normativa VS Plantilla:", style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}),  
 # tabla nucleos
dash_table.DataTable(
        id='table1X',
        #data = dffTabla1.to_dict('records'),
        columns = [{'id':c, 'name':c} for c in 
                   df.loc[:,['ADSCRIPCION','TURNO','EN_PLANTILLA','NORMATIVA']]],
           #virtualization=True,
           
                style_data={
               # 'color':  '#b38e5d',
                'color':  '#ffffff',
                'backgroundColor':'#621132'
            },
            fixed_rows = {'headers':True},

            style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_data_conditional = [
                     {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  > {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'red',
                'fontWeight': 'bold',
                'textAlign':'center',         
            },
                
                  {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  < {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'yellow',
                'fontWeight': 'bold',
                 'textAlign':'center',     
            },
                
               {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  = {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'right',   
            },
                {
                'if': {
                    'filter_query': '{NORMATIVA} = {NORMATIVA}',
                    'column_id': 'NORMATIVA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'center',   
            }  



              ],

            style_cell = {
                'textAlign':'left',
                'border':'4px solid white',
                 'color':'#b38e5d',
                 
                'maxWidth':'50px',
                # 'whiteSpace':'normal'
                'textOverflow':'ellipsis'


                }


)





])

   



],className='row flex_display')










df.to_csv('modificado.csv')
if __name__  == "__main__":
       app.run_server(debug=True)