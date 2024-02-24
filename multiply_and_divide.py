import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output, State
import numpy as np
import time
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    title='Multiplication and Division Game',
    suppress_callback_exceptions=True
)

# Layout of the app
app.layout = html.Div([
    html.H1("Multiplication and Division Game", style={'margin':'auto', 'text-align': 'center'}),
    
    dbc.Card(
        [
            html.Label('Your Name:'),
            dcc.Input(id='player-name', type='text', debounce=True, style={'width':'50%', 'margin':'auto'}),

            dcc.RadioItems(
                id='operation-selector',
                options=[
                    {'label': 'Multiplication', 'value': 'multiply'},
                    {'label': 'Division', 'value': 'divide'}
                ],
                value='multiply',
                labelStyle={'display': 'block'},
                style={'width': '33%', 'margin':'auto', 'margin-bottom': '20px', 'text-align': 'left'}
            ),
            # Dropdowns for selecting minimum and maximum numbers
            html.Label("Select minimum and maximum numbers: "),
            dcc.Input(id=f'min-number', type='number', debounce=True, min=0, max=100, step=1, value=1, style={'width':'25%', 'margin':'auto'}), 
            html.Label(" to ", style={'width':'25%', 'margin':'auto'}),
            dcc.Input(id=f'max-number', type='number', debounce=True, min=0, max=100, step=1, value=10, style={'width':'25%', 'margin':'auto'}),
        ],
        style={'width': '33%', 'margin-top': '20px', 'margin':'auto','text-align': 'center'}
    ),
    dbc.Card(
        [
            # Display area for questions and user input
            dbc.ListGroup(id='question-display'),
            
            # Feedback area for correct/incorrect answers
            html.Div(id='feedback'),
        ],
        style={'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'}
    ),
    
    # Store the correct answers and user scores
    dcc.Store(id='correct-answers'),
    dcc.Store(id='user-scores'),

    # Flashing image after correct answers
    html.Div(id='success-message', style={'text-align': 'center'}),
    html.Img(id='flash-image', style={'display': 'none'}),
])


@app.callback(
    [Output('question-display', 'children'),
     Output('correct-answers', 'data'),
     Output('user-scores', 'data')],
    [Input('operation-selector', 'value'),
     Input('min-number', 'value'),
     Input('max-number', 'value')],
    prevent_initial_call=False
)
def generate_questions(operation, min_num, max_num):
    num_questions = 5
    questions = []
    correct_answers = []
    user_scores = []
    questions.append(dbc.ListGroupItem(html.Label(f"Answer the following {num_questions} questions:")))
    questions.append(dbc.ListGroupItem(html.Label(f"Points", style={'float': 'right'})))
    
    for i in range(num_questions):
        if operation == 'multiply':
            num1, num2 = np.random.randint(min_num, max_num + 1, size=2)
            
            question = dbc.ListGroupItem(
                [   html.Label(f"{num1} x {num2} = ", style={'width':'100px', 'margin-left': '50px', 'float': 'left'}),
                    dcc.Input(id=f'input-{i}', type='number', debounce=True, min=0, max=max(100, max_num*max_num+max_num), step=1, style={'width': '100px', 'float': 'left'}),
                    html.Button(f'Check', id=f'submit-button-{i}', n_clicks=0, style={'margin-left': '25px', 'float': 'left'}),
                    html.Label(id=f'feedback-{i}', children=''),
                    html.Label(id=f'points-{i}', children='1', style={'float': 'right'}),
                    
                ], style={'margin-bottom': '10px'},
            )

            answer = num1 * num2
        else:  # operation is 'divide'
            num1, num2 = np.random.randint(min_num, max_num + 1, size=2)
            question = dbc.ListGroupItem(
                [   html.Label(f"{num1 * num2} / {num1} = ", style={'width':'100px', 'margin-left': '50px', 'float': 'left'}),
                    dcc.Input(id=f'input-{i}', type='number', debounce=True, min=0, max=max(100, max_num*max_num+max_num), step=1, style={'width': '100px', 'float': 'left'}),
                    html.Button(f'Check', id=f'submit-button-{i}', n_clicks=0, style={'margin-left': '25px', 'float': 'left'}),
                    html.Label(id=f'feedback-{i}', children=''),
                    html.Label(id=f'points-{i}', children='1', style={'float': 'right'}),
                    
                ], style={'margin-bottom': '10px'},
            )

            answer = num2

        questions.append(question)
        correct_answers.append(answer)
        user_scores.append(0)

     
    return questions, correct_answers, user_scores

@app.callback(
    [Output('feedback-0', 'children'),
     Output('feedback-1', 'children'),
     Output('feedback-2', 'children'),
     Output('feedback-3', 'children'),
     Output('feedback-4', 'children'),
     Output('flash-image', 'src'),
     Output('flash-image', 'style'),
     Output('success-message', 'children'),
    ],
    [Input('submit-button-0', 'n_clicks'),
     Input('submit-button-1', 'n_clicks'),
     Input('submit-button-2', 'n_clicks'),
     Input('submit-button-3', 'n_clicks'),
     Input('submit-button-4', 'n_clicks')
    ],
    [State('input-0', 'value'),
     State('input-1', 'value'),
     State('input-2', 'value'),
     State('input-3', 'value'),
     State('input-4', 'value'),
     State('correct-answers', 'data'),
     State('player-name', 'value')],
    prevent_initial_call=True
    
)
def check_answer(*args):

    button_clicked = ctx.triggered_id
    print(button_clicked)
    num_questions = 5
    num_correct = 0

    output = []
    for i in range(num_questions):
        # if button_clicked == f'submit-button-{i}':
            user_answer = args[i+5]
            correct_answer = args[10][i]
            if user_answer == correct_answer:
               
                output.append(html.Div("Correct!", style={'color': 'green'}))
                num_correct += 1

            else:
                if user_answer is None:
                    if button_clicked == f'submit-button-{i}' and args[i] >0:
                        output.append(html.Div("Please enter an answer.", style={'color': 'red'}))
                    else:
                        output.append('')
                elif user_answer < correct_answer:
                    output.append(html.Div("Incorrect! Answer is too low.", style={'color': 'red'}))
                else:
                    output.append(html.Div("Incorrect! Answer is too high.", style={'color': 'red'}))

    if num_correct < num_questions:
        output.append(None)
        output.append({'display': 'none'})
        output.append(None)
    else:
        output.append('assets/success_splash_0.jpg')
        output.append({'display': 'block'})
        output.append(html.Div(f"Congratulations {args[11]}! You got all the answers correct!", style={'color': 'green'}))

    return output


if __name__ == '__main__':
    print('test')
    app.run_server(debug=True)
