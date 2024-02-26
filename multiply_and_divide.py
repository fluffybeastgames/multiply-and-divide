import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output, State
import numpy as np
import time
import dash_bootstrap_components as dbc

NUM_QUESTIONS = 5 # Number of questions to ask - currently this is hard-coded below but could be made a user input if the callbacks' logic is changed to use list comprehensions in the params
NUM_SPLASH_IMAGES = 4 # Number of splash images to choose from - should match the number of correctly named images in the assets folder
STARTING_POINTS = 5 # Max points per question - each incorrect response deducts 1 point
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    title='Multiply and Divide and Conquer',
    suppress_callback_exceptions=True
)

# Photo by <a href="https://unsplash.com/@jrkorpa?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Jr Korpa</a> on <a href="https://unsplash.com/photos/pink-and-black-wallpaper-9XngoIpxcEo?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
# Photo by <a href="https://unsplash.com/@lukechesser?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Luke Chesser</a> on <a href="https://unsplash.com/photos/blue-to-purple-gradient-eICUFSeirc0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
  

# Layout of the app
app.layout = html.Div([
    html.H1("Multiply and Divide and Conquer", style={'margin':'auto', 'text-align': 'center', 'color': 'white'}),
    
    dbc.Card(
        [
            
            html.Button('score-board', id='view-score-board-button', n_clicks=0, style={'margin': 'auto', 'display': 'inline-block'}),    
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
            dcc.Input(id=f'min-number', type='number', debounce=True, min=1, max=100, step=1, value=1, style={'width':'25%', 'margin':'auto'}), 
            html.Label(" to ", style={'width':'25%', 'margin':'auto'}),
            dcc.Input(id=f'max-number', type='number', debounce=True, min=1, max=100, step=1, value=10, style={'width':'25%', 'margin':'auto'}),

            html.Button('New Game', id='new-game-button', n_clicks=0, style={'margin-top': '20px', 'margin':'auto', 'display': 'block'}),
        ],
        id='card_input',
        style={'width': '33%', 'margin-top': '20px', 'margin':'auto','text-align': 'center'}
    ),
    dbc.Card(
        [
            html.Button('Back', id='game-back-button', n_clicks=0, style={'margin': 'auto', 'display': 'inline-block'}),
            # Display area for questions and user input
            dbc.ListGroup(id='question-display'),
            
            # Feedback area for correct/incorrect answers
            html.Div(id='feedback'),
        ],
        id='card_game_board',
        style={'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'}
    ),
    dbc.Card(
        [
            html.Label('score-board'),
            html.Button('Home', id='score-board-back-button', n_clicks=0, style={'margin': 'auto', 'display': 'inline-block'}),
        ],
        id='card_score-board',
        style={'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'}
    ),
    # Store the correct answers and user scores
    dcc.Store(id='correct-answers'),
    dcc.Store(id='user-scores'),

    # Flashing image after correct answers
    html.Div(id='success-message', style={'text-align': 'center'}),
    html.Img(id='flash-image', style={'display': 'none'}),
],
# style={'background-color': '#f2f2f2',}
style = {'background-image': 'url("assets/bg.jpg")', 'height': '100%'}


)


@app.callback(
    [Output('question-display', 'children'),
     Output('correct-answers', 'data'),
     Output('user-scores', 'data')],
    Input('new-game-button', 'n_clicks'),
    [State('operation-selector', 'value'),
     State('min-number', 'value'),
     State('max-number', 'value'),
     State('player-name', 'value')
    ],
    prevent_initial_call=False
)
def generate_questions(n_clicks, operation, min_num, max_num, player_name):
    questions = []
    correct_answers = []
    user_scores = []
    questions.append(dbc.ListGroupItem(html.Label(f"OK {player_name}! Answer the following {NUM_QUESTIONS} questions:")))
    questions.append(dbc.ListGroupItem(html.Label(f"Points", style={'float': 'right'})))
    
    for i in range(NUM_QUESTIONS):
        if operation == 'multiply':
            num1, num2 = np.random.randint(min_num, max_num + 1, size=2)
            
            question = dbc.ListGroupItem(
                [   html.Label(f"{num1} x {num2} = ", style={'width':'100px', 'margin-left': '50px', 'float': 'left'}),
                    dcc.Input(id=f'input-{i}', type='number', debounce=True, min=0, max=max(100, max_num*max_num+max_num), step=1, style={'width': '100px', 'float': 'left'}),
                    html.Button(f'Check', id=f'submit-button-{i}', n_clicks=0, style={'margin-left': '25px', 'float': 'left'}),
                    html.Label(id=f'feedback-{i}', children=''),
                    html.Label(id=f'points-{i}', children='0', style={'float': 'right'}),
                    
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
                    html.Label(id=f'points-{i}', children='0', style={'float': 'right'}),
                    
                ], style={'margin-bottom': '10px'},
            )

            answer = num2

        questions.append(question)
        correct_answers.append(answer)
        user_scores.append(STARTING_POINTS)

     
    return questions, correct_answers, user_scores


@app.callback(
    [
        Output('card_input', 'style'),
        Output('card_game_board', 'style'),
        Output('card_score-board', 'style')
        # Output('card_beast', 'style')
    ],
    [
        Input('new-game-button', 'n_clicks'),
        Input('game-back-button', 'n_clicks'),
        Input('score-board-back-button', 'n_clicks'),
        Input('view-score-board-button', 'n_clicks')
    ],
    prevent_initial_call=False
)
def toggle_visibility(n_clicks_ng, n_clicks_gb, n_clicks_sb, n_clicks_vs):
    print(ctx.triggered_id)
    if ctx.triggered_id == 'game-back-button':
        return {'width': '33%', 'margin-top': '20px', 'margin':'auto','text-align': 'center'}, {'display': 'none'},  {'display': 'none'}
    elif ctx.triggered_id == 'new-game-button':
        return {'display': 'none'}, {'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'},  {'display': 'none'}
    elif ctx.triggered_id == 'score-board-back-button':
        return {'display': 'none'}, {'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'},  {'display': 'none'}
    elif ctx.triggered_id == 'view-score-board-button':
        return {'display': 'none'},  {'display': 'none'}, {'width': '33%', 'margin-left':'20px', 'margin-top': '20px', 'margin':'auto', 'text-align': 'center'}
    


    else:
        return {'width': '33%', 'margin':'auto', 'margin-bottom': '20px', 'text-align': 'center'}, {'display': 'none'}, {'display': 'none'}
    
    # style={'width': '33%', 'margin':'auto', 'margin-bottom': '20px', 'text-align': 'left'}
    #     style={'width': '33%', 'margin-top': '20px', 'margin':'auto','text-align': 'center'}
    # ),

@app.callback(
    [Output('feedback-0', 'children'),
     Output('feedback-1', 'children'),
     Output('feedback-2', 'children'),
     Output('feedback-3', 'children'),
     Output('feedback-4', 'children'),
     Output('flash-image', 'src'),
     Output('flash-image', 'style'),
     Output('success-message', 'children'),
     Output('points-0', 'children'),
     Output('points-1', 'children'),
     Output('points-2', 'children'),
     Output('points-3', 'children'),
     Output('points-4', 'children')
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
     State('player-name', 'value'),
     State('max-number', 'value')
    ],
    prevent_initial_call=True
    
)
def check_answer(*args):

    button_clicked = ctx.triggered_id
    # print(button_clicked)
    num_correct = 0
    total_points = 0 # sum of points

    output = []
    points_list = [] # also output, but at the end, so we'll extend the list after the loop

    
    for i in range(NUM_QUESTIONS):
        # if button_clicked == f'submit-button-{i}':
            user_answer = args[i+5]
            correct_answer = args[10][i]
            if user_answer == correct_answer:
               
                output.append(html.Div("Correct!", style={'color': 'green'}))
                num_correct += 1

                #args[12] is the state of the max number
                points = max(STARTING_POINTS + int(args[12]/5) - args[i] + 1, 1)
                total_points += points
                points_list.append(points)

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
                
                points_list.append(0)

    if num_correct < NUM_QUESTIONS:
        output.append(None)
        output.append({'display': 'none'})
        output.append(None)
    else:
        splash_image_id = np.random.randint(0, NUM_SPLASH_IMAGES)
        output.append(f'assets/success_splash_{splash_image_id}.jpg')
        output.append({'display': 'block'})
        output.append(html.Div(f"Congratulations {args[11]}! You got all the answers correct and scored {total_points} points!", style={'color': 'white', 'font-size': '40px'}))

    # my_list.extend(another_list)
    output.extend(points_list)

    return output


if __name__ == '__main__':
    print('test')
    app.run_server(debug=True)
