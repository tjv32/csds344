import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
from dash_extensions import Download
import plotly.graph_objects as go

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util import number
from sympy.ntheory.factor_ import totient
import binascii
import struct
import random


import io
import base64
import datetime
from make_app import app


default_message = 'This is the default message'

txt_encrpyt_options = [{'label': i, 'value': i} for i in ['RSA', 'DES', 'VIG']]
video_encrpyt_options = [{'label': i, 'value': i} for i in ['RSA', 'DES']]
method_options = [{'label': i, 'value': i} for i in ['Encrypt', 'Decrypt']]

   

tab_title = html.H1(
    children='RSA',
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
        id='method_dd_r',
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

plaintext_input = dcc.Input(
            id='plaintext_input_r',
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
            id='plaintext_upload_r',
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

plain_msg = html.Div(id='plain_msg_r')
key_msg = html.Div(id='key_msg_r')
overall_msg = html.Div(id='overall_msg_r')

result_orig_msg = html.Div(id='result_orig_msg_r')
result_changed_msg = html.Div(id='result_changed_msg_r')

key_input = dcc.Input(
            id='key_input_r',
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
            id='key_upload_r',
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
    id='update_button_main_r',
)

result_layout = go.Layout(
    title='',
)

result_fig = go.Figure(
    data = None,
    layout = result_layout
)

result_graph = dcc.Graph(
    id='result_r',
    figure=result_fig,
)

body_2 = html.Div(
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
                                #key_title,
                                #key_input,
                                #key_upload,
                                #key_msg,
                                method_label,
                                method_dd,
                                update_button,
                                overall_msg,
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
 
tab_2 = dcc.Tab(
    label='RSA', 
    children=[
        body_2
    ]
)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
# Encryption for Strings
finding_key = True
p, q, n, e, n_tot, d = 0,0,0,0,0,0
while(finding_key):
    try:
        prime_base = 8
        p = number.getPrime(prime_base)
        q = number.getPrime(prime_base)
        n = p*q
        n_tot = totient(n)
        e = random.randint(3, 31)
        while n_tot % e == 0:
            e = random.randint(3, 31)

        d = modinv(e, n_tot)
        finding_key = False
    except:
        pass
    
# Modular multiplication inverse formula to calculate d, taken from internet.



#print("Prime base:",prime_base)
#print("P:",p)
#print("Q:",q)
#print("N:",n)
#print("E:",e)
#print("D:",d)
#print("Totient(N):",n_tot)
key1 = [n,e, prime_base]
key2 = [n,d, prime_base]

def encrypt(message, key):
    n = key[0]
    e = key[1]
    prime_base = key[2]
    enc_base = int(prime_base/2)
    dec_base = int(prime_base/4)

    # Step 1 - Converting the input into binary/ascii/hex
    msg_string = message
    msg_ascii = [ord(c) for c in msg_string]
    msg_hex = [intToHexFormatter(c,dec_base) for c in msg_ascii]

    # Step 2 - Hex to hex string
    msg_hex_string = "0x"
    for c in msg_hex:
        msg_hex_string += c[2:]

    # Step 3 - Taking the power of input so that enc_msg = (msg ^ e) % n
    enc_msg_int = []
    for c in msg_ascii:
        temp = pow(c,e) % n
        enc_msg_int.append(temp)

    # Step 4 - Converting the encrypted input into hex
    enc_msg_hex = []
    for c in enc_msg_int:
        temp = intToHexFormatter(c, enc_base)
        enc_msg_hex.append(temp)

    # Step 5 - Encrypted hex to encrypted hex string
    enc_msg_hex_string = "0x"
    for c in enc_msg_hex:
        enc_msg_hex_string += c[2:]

    # Step 6 - Output
    print("Original message information")
    print("\nMessage:",msg_string)
    print("\nMessage in ASCII format:",msg_ascii)
    print("\nMessage in Hex (ascii to hex) format:",msg_hex)
    print("\nMessage in complete hex string:",msg_hex_string)
    print("\n")
    print("\nEncrypted message information")
    print("\nEncrypted message in integer format:",enc_msg_int)
    print("\nEncrypted message in hex format:",enc_msg_hex)
    print("\nEncrypted messsage in complete hex string:",enc_msg_hex_string)
    
    return enc_msg_hex_string

def intToHexFormatter(entry, base):
    counter = 0
    temp = entry
    while temp >= 16:
        counter += 1
        temp = temp/16
    formattedHex = "0x"
    for i in range(int(base)-counter-1):
        formattedHex += "0"
    temp = hex(entry)
    formattedHex += temp[2:]
    return formattedHex

# Decryption for Strings

def decrypt(message, key):
    n = key[0]
    d = key[1]
    prime_base = key[2]
    enc_base = int(prime_base/2)
    dec_base = int(prime_base/4)
    # Step 1 - Converting the hex string into decryptable segments
    enc_msg_hex_string = message
    enc_msg_hex_length = len(enc_msg_hex_string[2:])
    enc_msg_received = []
    x = range(2,enc_msg_hex_length+1,enc_base)
    for c in x:
        temp = enc_msg_hex_string[c:c+enc_base]  #First two characters are 0x
        enc_msg_received.append(temp) 
    print(enc_msg_received)
    # Step 2 - Converting each encrypted hex segment into integers
    enc_msg_received_int = []
    for c in enc_msg_received:
        temp = int(c,16)
        enc_msg_received_int.append(temp)

    # Step 3 - Decrypting each integer segment
    dec_msg_int = []
    for c in enc_msg_received_int:
        temp = pow(c,d) % n
        dec_msg_int.append(temp)

    # Step 3 - Converting the decrypted segments into hex
    dec_msg_hex = []
    for c in dec_msg_int:
        dec_msg_hex.append(hex(c))

    # Step 4 - Decrypted hex to decrypted hex string
    dec_msg_hex_string = "0x"
    for c in dec_msg_hex:
        dec_msg_hex_string += c[2:]

    # Step 5 - Output
    print("\n\nBefore Decryption")
    print("\nEncrypted hex string received:",enc_msg_hex_string)
    print("\nEncrypted hex string converted divided into segments:",enc_msg_received)

    print("\n\nAfter Decryption")
    print("\nDecrypted message in integer format",dec_msg_int)
    print("\nDecrypted message in hex format",dec_msg_hex)
    print("\nDecrypted message in complete hex string:",dec_msg_hex_string)
    
    return dec_msg_hex_string







def inputKey(key):
    key = [eval(x) for x in key]
    key = ['{:08b}'.format(x) for x in key]
    key = "".join(key)
    return key

'''
@app.callback(  
            [
                Output('key_msg_r', 'children'),
                Output('temp_key_r', 'data'),
            ],
            [
                Input('key_upload_r', 'contents'),
            ],
            [
                State('key_upload_r', 'filename'),
                State('key_upload_r', 'last_modified'),
                State('temp_upload_r', 'data')
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
'''

@app.callback(  
            [
                Output('plain_msg_r', 'children'),
                Output('temp_upload_r', 'data'),
            ],
            [
                Input('plaintext_upload_r', 'contents'),
            ],
            [
                State('plaintext_upload_r', 'filename'),
                State('plaintext_upload_r', 'last_modified'),
                State('temp_upload_r', 'data')
            ])
def create_upload_display_plain(contents, filename, last_modified, mem_obj):
    if(contents is None):
        raise PreventUpdate
    try:
        if(mem_obj is None):
            mem_obj = {}
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
            
        lines = io.StringIO(decoded.decode('utf-8')).read()
        lines = lines.split('\n')

        mem_obj['upload'] = lines

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
        Output('result_orig_msg_r', 'children'),
        Output('result_changed_msg_r', 'children'),
        Output('overall_msg_r', 'children'),

    ],
    [
        Input('update_button_main_r', 'n_clicks'),
    ],
    [
        State('method_dd_r', 'value'),
        State('plaintext_input_r', 'value'),
        #State('key_input_r', 'value'),

        State('temp_upload_r', 'data'),
        State('temp_key_r', 'data'),

        
    ]
)
def update_main_view(n_clicks, method_dd, plaintext_free_input,
      upload_plain, upload_key):

    if(plaintext_free_input is None and
        upload_plain is None):
        raise PreventUpdate
    final_key, final_plain, display_plain = '', '', ''

    if(plaintext_free_input is not None):
        final_plain = plaintext_free_input
    else:
        display_plain = final_plain

    print(final_plain)

    #if(not isinstance(str, final_plain)):
    #    final_plain = " ".join(final_plain)



    time_elapsed = 1

    orig_update, adj_update = '', ''
    if(method_dd == 'Encrypt'):
        begin_time = datetime.datetime.now()
        cipher = encrypt(final_plain, key1)
        time_elapsed = datetime.datetime.now() - begin_time
        
        orig_update = html.Div(
            [
                f'Plaintext: {final_plain}',
                html.Br(),
                f'Private Key (n, d): {key1[:2]}',
                html.Br(),
                f'Time Elapsed: {time_elapsed.total_seconds()} seconds'
            ]
        )
        adj_update = html.Div(
            [
                f'Encrypted Cipher: {cipher}',
                html.Br(),
                f'Public Key (n, e): {key2[:2]}',
            ]
        )
    elif(method_dd == 'Decrypt'):
        begin_time = datetime.datetime.now()
        dec_message = decrypt(final_plain,key2)

        # File conversions
        dec_msg_hex_string = dec_message

        dec_msg_hex_length = len(dec_msg_hex_string[2:len(dec_msg_hex_string)])
        dec_msg_received = []

        x = range(2,dec_msg_hex_length+1,2)
        for c in x:
            temp = dec_msg_hex_string[c:c+2]  #First two characters are 0x
            dec_msg_received.append(temp)

        # 1 - Hex to proper text
        original_message = ""
        for c in dec_msg_received:
            temp = chr(int(c,16))
            original_message += temp
        time_elapsed = datetime.datetime.now() - begin_time

        orig_update = html.Div(
            [
                f'Cipher: {final_plain}',
                html.Br(),
                f'Public Key (n, e): {key2[:2]}',
                html.Br(),
                f'Time Elapsed: {time_elapsed.total_seconds()} seconds'
            ]
        )
        adj_update = html.Div(
            [
                f'Decrypted Plaintext: {original_message}',
                html.Br(),
                f'Private Key (n, d): {key1[:2]}',
            ]
        )
    update_msg = html.Div([
            f'Success!'
        ])
    return orig_update, adj_update, update_msg


