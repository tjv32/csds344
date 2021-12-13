import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
from dash_extensions import Download
import plotly.graph_objects as go

import pathlib
import io
import base64
import datetime
from make_app import app
import string
import binascii

from DES.DES_encrypt import DES_decrypt_adj, DES_encrypt_adj

default_message = 'This is the default message'

txt_encrpyt_options = [{'label': i, 'value': i} for i in ['RSA', 'DES', 'VIG']]
video_encrpyt_options = [{'label': i, 'value': i} for i in ['RSA', 'DES']]
method_options = [{'label': i, 'value': i} for i in ['Encrypt', 'Decrypt']]
method_d_options = [{'label': i, 'value': i} for i in ['Text', 'JPG']]
   

tab_title = html.H1(
    children='DES',
    style={
        'textAlign': 'center',
        'color': 'black'
        }
    )

file_input_label = html.Label(
    children = 'Enter Text Message Below to be Encrypted or Decrypted or Input a File (txt)',
    style={
        'textAlign': 'left',
        'color': 'black',
    }
)

method_dd = dcc.Dropdown(
        id='method_dd',
        options=method_options,
        multi=False,
        value='Encrypt'
    )
method_label = html.Label(
    children = 'Select Method',
    style={
        'textAlign': 'left',
        'color': 'black',
    }
)

method_dd_o = dcc.Dropdown(
        id='output_dd_o',
        options=method_d_options,
        multi=False,
        value='Text'
    )
method_label_o = html.Label(
    children = 'Select Output',
    style={
        'textAlign': 'left',
        'color': 'black',
    }
)


plaintext_input = dcc.Input(
            id='plaintext_input',
            type='text',
            placeholder='Name',
            style={
                'height': 54,
                'width':'100%',
                'display': 'inline-block'
            }
        )
plaintext_upload = html.Div(
    [
        dcc.Upload(
            id='plaintext_upload',
            children=html.Div(
                [
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]
            ),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        )
    ]
)

key_title = html.Label(
    children = 'Enter Text Key or Input a File (txt) if not entered, default key will be used',
    style={
        'textAlign': 'left',
        'color': 'black',
    }
)

plain_msg = html.Div(id='plain_msg')
key_msg = html.Div(id='key_msg')
overall_msg = html.Div(id='overall_msg')

result_orig_msg = html.Div(id='result_orig_msg')
result_changed_msg = html.Div(id='result_changed_msg')

key_input = dcc.Input(
            id='key_input',
            type='text',
            placeholder='Name',
            style={
                'height': 54,
                'width':'100%',
                'display': 'inline-block'
            }
        )





key_upload = html.Div(
    [
        dcc.Upload(
            id='key_upload',
            children=html.Div(
                [
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]
            ),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        )
    ]
)


update_button = html.Button(
    'Update', 
    id='update_button_main',
)

result_layout = go.Layout(
    title='',
)

result_fig = go.Figure(
    data = None,
    layout = result_layout
)

result_graph = dcc.Graph(
    id='result',
    figure=result_fig,
)

download_button = html.Div(
    [
        html.Button(
            "Download Result", 
            id="btn_1"
        ), 
        dcc.Download(id="download_des_but")
    ]
)


body_1 = html.Div(
	[
		dbc.Container(
 			[
            	dbc.Row(
                	[
                    	dbc.Col(
                        	[
                            	tab_title
                        	]
                    	)
                	]
            	),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                file_input_label,
                                plaintext_input,
                                plaintext_upload,
                                plain_msg,
                                key_title,
                                key_input,
                                key_upload,
                                key_msg,
                                method_label,
                                method_dd,
                                method_label_o,
                                method_dd_o,
                                update_button,
                                overall_msg,
                                download_button,
                            ],
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                result_orig_msg
                            ]
                        ),
                        dbc.Col(
                            [
                                result_changed_msg
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                
                            ]
                        )
                    ]
                )

        	],
        	fluid = True
    	)
    ]
)
 
tab_1 = dcc.Tab(
	label='DES', 
	children=[
        body_1
    ]
)

def adjust_hex(lines):
    print('begin hex check', lines)
    hex_v = True
    for c in lines:
        try:
            tmp = int(c[2:], 16)
        except:
            hex_v = False
    if(hex_v):
        print('NOT CONVERTING TO HEX')
    else:
        print('CONVERTING TO HEX')
        lines = " ".join(lines)
        lines = [hex(ord(val)) for val in lines]
    return " ".join(lines)

def save_jpg(final_cipher):
    
    byte_array = bytes([int(x, 0) for x in final_cipher])
    #print(byte_array)
    #print(len(final_cipher))
    decode = base64.decodebytes(byte_array)
    decrypted_image = open('DES/decrypted.jpg', 'wb')
    decrypted_image.write(decode)
    decrypted_image.close()


def inputKey(key):
    key = [eval(x) for x in key]
    key = ['{:08b}'.format(x) for x in key]
    key = "".join(key)
    return key


@app.callback(  
            [
                Output('key_msg', 'children'),
                Output('temp_key', 'data'),
            ],
            [
                Input('key_upload', 'contents'),
            ],
            [
                State('key_upload', 'filename'),
                State('key_upload', 'last_modified'),
                State('temp_upload', 'data')
            ])
def create_upload_display_key(contents, filename, last_modified, mem_obj):
    if(contents is None):
        raise PreventUpdate
    try:
        if(mem_obj is None):
            mem_obj = {}
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
            
        lines = io.StringIO(decoded.decode('utf-8')).read()
        lines = lines.split('\n')
        lines = " ".join(lines)
        mem_obj['upload'] = lines
        mem_obj['file_name'] = filename.split('.')[-1]

        update_msg = html.Div([
            f'{filename} successfully uploaded'
        ])
    except:
        mem_obj = None
        update_msg = html.Div([
            'There was an error processing this file.'
        ])
    return update_msg, mem_obj

@app.callback(  
            [
                Output('plain_msg', 'children'),
                Output('temp_upload', 'data'),
            ],
            [
                Input('plaintext_upload', 'contents'),
            ],
            [
                State('plaintext_upload', 'filename'),
                State('plaintext_upload', 'last_modified'),
                State('temp_upload', 'data')
            ])
def create_upload_display_plain(contents, filename, last_modified, mem_obj):
    if(contents is None):
        raise PreventUpdate
    if(1==1):
        if(mem_obj is None):
            mem_obj = {}
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        file_ext = filename.split('.')[-1]
        mem_obj['ext'] = file_ext


        if(file_ext == 'txt'):
            
            lines = io.StringIO(decoded.decode('utf-8')).read().split(" ")
            #lines = " ".join(lines)
            #print(lines)
            
            lines = adjust_hex(lines)



        elif(file_ext == 'jpg'):

            lines = bytes(content_string, 'utf-8')
            final_lines = []
            for val in lines:
                final_lines.append(str(hex(val)))
            #print('length', len(final_lines))
            lines = " ".join(final_lines)
            #print('This is the length', len(lines))

            #print('original string', decoded.hex())
            #print()
            #print('encode bytes', base64.encodebytes(decoded))
            #print()
            #print('hex method' , base64.encodebytes(decoded).hex())
            #lines = " ".join(lines[1:5])
            #print(lines)
            #base64.encodebytes(decoded).decode("ascii")
            #print(eval(lines))
            #b = bytearray()
            #b.extend(map(ord, lines))
            #print(lines)
            #lines = bytes(bytearray.fromhex(lines))
            #print(lines)
            #b=[ord(x) for x in s]
            #mem_obj['upload'] = b
            #mem_obj['display'] = b
            
        #lines = io.StringIO(decoded.decode('utf-8')).read()
        #lines = lines.split('\n')
        #lines = " ".join(lines)
        #print(lines)
        mem_obj['display'] = lines
        mem_obj['upload'] = lines
        #print(mem_obj['upload'])
        #mem_obj['display'] = lines

        update_msg = html.Div([
            f'{filename} successfully uploaded'
        ])
    else:
        mem_obj = None
        update_msg = html.Div([
            'There was an error processing this file.'
        ])
    return update_msg, mem_obj


@app.callback(
    [
        Output('result_orig_msg', 'children'),
        Output('result_changed_msg', 'children'),
        Output('overall_msg', 'children'),
        Output('download_des', 'data'),

    ],
    [
        Input('update_button_main', 'n_clicks'),
    ],
    [
        State('method_dd', 'value'),
        State('plaintext_input', 'value'),
        State('key_input', 'value'),

        State('temp_upload', 'data'),
        State('temp_key', 'data'),
        State('output_dd_o', 'value')

        
    ]
)
def update_main_view(n_clicks, method_dd, plaintext_free_input, key_free_input,
      upload_plain, upload_key, output_dd):
    #print('hello')
    #print('success', (plaintext_free_input is None and upload_plain is None) or (key_free_input == None and upload_key == None))
    if((plaintext_free_input is None and upload_plain is None) or (key_free_input == None and upload_key == None)):

        raise PreventUpdate
    final_key, final_plain, display_plain = '', '', ''
    if(key_free_input is not None):
        final_key = key_free_input.split(' ')
    else:
        final_key = upload_key['upload'].split(' ')

    if(plaintext_free_input is not None):
        final_plain = adjust_hex(plaintext_free_input.split(' '))
    else:
        final_plain = upload_plain['upload']
        display_plain = final_plain
    #print(final_plain)

    plain_key = " ".join(final_key)

    #if(not isinstance(str, final_plain)):
    #    final_plain = " ".join(final_plain)


    final_key = inputKey(final_key)

    time_elapsed = 1

    orig_update, adj_update = '', ''
    final_output = []
    if(method_dd == 'Encrypt'):
        tmp = final_plain.split(" ")
        #print(tmp)
        chunks = [tmp[x: x + 8] for x in range(0, len(tmp), 8)]
        while(len(chunks[-1]) < 8):
            chunks[-1].append('0x0')
        final_cipher = []
        begin_time = datetime.datetime.now() 
        for chunk in chunks:
            cipher = DES_encrypt_adj(" ".join(chunk), final_key, 'cipher.txt')
            final_cipher.extend(cipher)
        time_elapsed = datetime.datetime.now() - begin_time
        
        orig_update = html.Div(
            [
                f'Plaintext: {final_plain}',
                html.Br(),
                f'Key: {plain_key}',
                html.Br(),
                f'Time Elapsed: {time_elapsed.total_seconds()} seconds'
            ]
        )
        adj_update = html.Div(
            [
                f'Encrypted Cipher: {" ".join(final_cipher)}'
            ]
        )
        final_output = " ".join(final_cipher)
    elif(method_dd == 'Decrypt'):
        tmp = final_plain.split(" ")
        chunks = [tmp[x: x + 8] for x in range(0, len(tmp), 8)]
        while(len(chunks[-1]) < 8):
            chunks[-1].append('0x0')
        final_cipher = []
        begin_time = datetime.datetime.now() 
        for chunk in chunks:
            cipher = DES_decrypt_adj(" ".join(chunk), final_key, 'cipher.txt')
            final_cipher.extend(cipher)
        time_elapsed = datetime.datetime.now() - begin_time
        while(final_cipher[-1] == '0x0'):
            final_cipher.pop()

        orig_update = html.Div(
            [
                f'Cipher: {final_plain}',
                html.Br(),
                f'Key: {plain_key}',
                html.Br(),
                f'Time Elapsed: {time_elapsed.total_seconds()} seconds'
            ]
        )
        print('before', final_cipher[:5])
        tmp = []
        for x in final_cipher:
            print(x)
            tmp.append(bytearray.fromhex(x[2:]).decode())
        adj_update = html.Div(
            [
                f'Decrypted Plaintext: {"".join(tmp)}'
            ]
        )
        if(output_dd == 'JPG'):
            save_jpg(final_cipher)
        final_output = " ".join(final_cipher)
    update_msg = html.Div([
            f'Success!'
        ])
    return orig_update, adj_update, update_msg, {'method' : method_dd, 'format' : output_dd, 'output' : final_output}

@app.callback(
        Output("download_des_but", "data"),
        [
            Input("btn_1", "n_clicks"),
        ],
        [
            State('download_des', 'data'),
        ],
        prevent_initial_call=True,
)
def generate_csv(n_nlicks, download):
    if(download is None):
        raise PreventUpdate
    # Convert data to a string.
    s = io.StringIO()
    o_format = '.txt'
    if(download['format'] == 'Text'):
        return dict(filename=f"{download['method']}.txt", content=download['output'], type="text/txt")  

    else:
        return dcc.send_file(
        pathlib.Path("DES/decrypted.jpg")
    )

