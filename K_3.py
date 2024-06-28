import PySimpleGUI as sg
import pyperclip
import datetime
import os
import sys
from java_courses import java_course_options

# ウィンドウテーマ
sg.theme('TealMono')

java_course = [
    '',
    'ベーシック',
    'スタンダード',
    'アドバンスド'
]

font = (1)

# today
now = datetime.date.today()
now = "{0:%m%d}".format(now)

# 1~70
lis = ['{:02d}'.format(i + 1) for i in range(70)]

# 1~8
period = [str(p + 1) for p in range(8)]

# 1on1
Number7 = ['', '1', '2', '3', '4', '5', '6', '7']

# Tab A layout
tab_a_layout = [
    [sg.Radio('挨拶', '1', default=True, key='fast'),
     sg.Radio('ヘルプ', '1', key='help'),
     sg.Radio('フォロー', '1', key='follow')],
    [sg.Radio('面談依頼', '1', key='cs'),
     sg.Radio('VUサポート', '1', key='vu'),
     sg.Radio('初VU期間サポート', '1', key='fastVu')],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.InputText(size=(150, 1), key='greeting', font=font)]
]

# Tab B layout
tab_b_layout = [
    [sg.Radio('ベーシック', '1', key='JavaBasic', enable_events=True),
     sg.Radio('スタンダード', '1', key='JavaStandard', enable_events=True),
     sg.Radio('アドバンスド', '1', key='JavaAdvance', enable_events=True)],
    [sg.Radio('Discord', '1', key='Discord', enable_events=True, size=(5, 1)),
     sg.InputText(size=(9, 1), font=font, key='DiscordInput'),
     sg.Radio('1on1', '1', key='1on1', enable_events=True, size=(3, 1)),
     sg.Spin(java_course, size=(11, 1), key='1on1Course', font=font),
     sg.Spin(Number7, size=(2, 1), key='1on1Input', font=font),
     sg.Radio('BuildUp', '1', key='BuildUp', enable_events=True)],
    [sg.Text('Java', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='detail', font=font)]
]

col1 = [
    sg.Checkbox('わかばROOM', key='wakaba', default=False),
    sg.Checkbox('初VU期間サポート対象', key='subject', default=False),
    sg.Spin(period, size=(2, 1), font=font, key='seven'),
]

col2 = [
    [sg.Text('授業', size=(4, 1), font=font),
    sg.Spin(lis, size=(2, 1), font=font, key='jyugyou'),
    sg.Text('時限', size=(4, 1), font=font),
    sg.Spin(period, size=(2, 1), font=font, key='jigen'),
    sg.Text('Room', size=(4, 1), font=font),
    sg.Spin(lis, size=(2, 1), font=font, key='room')],
    [sg.Checkbox('受講促進○', key='promotionTrue', default=False, size=(9, 1), font=font),
     sg.Checkbox('受講促進×', key='promotionFalse', default=False, size=(9, 1), font=font),
     sg.Checkbox('巡回不要', key='noFollow', default=False, size=(9, 1), font=font)],
]



# Main layout with tabs
layout = [
    [col1],
    [col2],
    [sg.TabGroup([[sg.Tab('アクション', tab_a_layout), sg.Tab('Java', tab_b_layout)]], key="tabgroup")],
    [sg.Text('備考', size=(4, 1), font=font),sg.Multiline(size=(150, 2), key='remarks', font=font)],
    [sg.Button('COPY', size=(10, 1), key='COPY', button_color=('white', '#001480')),
     sg.Button('CODE', size=(10, 1), key='CODE', button_color=('white', '#001480')),
     sg.Button('CLEAR', size=(10, 1), key='CLEAR', button_color=('white', '#dc143c'))]
]

# アイコンのパス設定
def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath('.'), relative)

icon_path = resource_path("128_04.ico")

# ウィンドウの生成
window = sg.Window('K_3', layout, keep_on_top=True, size=(490, 330), resizable=True, icon=icon_path)

# メイン処理
while True:
    event, values = window.read()

    # Java コースの選択イベント
    if event in ('JavaBasic', 'JavaStandard', 'JavaAdvance'):
        selected_type = event
        window['detail'].update(values=java_course_options[selected_type])

    # COPY ボタンの処理
    if event == 'COPY':
        data = ""

        if values['fast']:
            if values['wakaba']:
                data += '☆'

            if values['subject']:
                data += f"【初VU期間サポート対象】{values['seven']}回目\n"

            data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
            data += f"挨拶:{values['greeting']}\n注意事項:"

            if values['noFollow']:
                data += '★巡回不要　'
            if values['promotionTrue']:
                data += '受講促進○' + ' ' + now + ' ' + values['jigen'] + '限'
            if values['promotionFalse']:
                data += '受講促進×'
                
            if values['noFollow'] or values['promotionTrue'] or values['promotionFalse']:
                data += f"\n{values['remarks']}"
            else:
                data += values['remarks']      

        elif values['help']:
            data = f"ヘルプ対応:{values['remarks']}"

        elif values['follow']:
            data = f"フォロー対応:{values['remarks']}"

        elif values['cs']:
            data = f"【面談依頼】\n内容：{values['remarks']}"

        elif values['vu']:
            data = f"【VUサポート】\n内容：{values['remarks']}"

        elif values['fastVu']:
            data = f"【初VU期間サポート】{values['seven']}回目\nヘルプ：0回　フォロー：0回\n内容：{values['remarks']}"

        elif values['BuildUp']:
            data = "BuildUp済"

        elif values['Discord']:
            data = f"Discord名：{values['DiscordInput']}"

        elif values['1on1']:
            data = f"1on1:{values['1on1Course']}　{values['1on1Input']}回"

        if values['JavaBasic']:
            
            if values['wakaba']:
                data += '☆'

            if values['subject']:
                data += f"【初VU期間サポート対象】{values['seven']}回目\n"

            data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
            data += f"挨拶:Javaエンジニア ベーシック\n{values['detail']}\n注意事項:"
            
            if values['noFollow']:
                data += '★巡回不要　'
            if values['promotionTrue']:
                data += '受講促進○' + ' ' + now + ' ' + values['jigen'] + '限'
            if values['promotionFalse']:
                data += '受講促進×'
            
            if values['noFollow'] or values['promotionTrue'] or values['promotionFalse']:
                data += f"\n{values['remarks']}"
            else:
                data += values['remarks']             

        elif values['JavaStandard']:
            
            if values['wakaba']:
                data += '☆'

            if values['subject']:
                data += f"【初VU期間サポート対象】{values['seven']}回目\n"

            data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
            data += f"挨拶:Javaエンジニア スタンダード\n{values['detail']}\n注意事項:"
            
            if values['noFollow']:
                data += '★巡回不要　'
            if values['promotionTrue']:
                data += '受講促進○' + ' ' + now + ' ' + values['jigen'] + '限'
            if values['promotionFalse']:
                data += '受講促進×'

            if values['noFollow'] or values['promotionTrue'] or values['promotionFalse']:
                data += f"\n{values['remarks']}"
            else:
                data += values['remarks']             

        elif values['JavaAdvance']:
            
            if values['wakaba']:
                data += '☆'

            if values['subject']:
                data += f"【初VU期間サポート対象】{values['seven']}回目\n"

            data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
            data += f"挨拶:Javaエンジニア アドバンスド\n{values['detail']}\n注意事項:"
            
            if values['noFollow']:
                data += '★巡回不要　'
            if values['promotionTrue']:
                data += '受講促進○' + ' ' + now + ' ' + values['jigen'] + '限'
            if values['promotionFalse']:
                data += '受講促進×'
            
            if values['noFollow'] or values['promotionTrue'] or values['promotionFalse']:
                data += f"\n{values['remarks']}"
            else:
                data += values['remarks']
                
        pyperclip.copy(data)     
            
    # CODEボタン
    if event == 'CODE':
        data = f"{now}_{values['jyugyou']}_{values['jigen']}限_Room00"

        pyperclip.copy(data)

    # CLEARボタン
    if event == 'CLEAR':
        if values['wakaba']:
            window['greeting'].update('')
            window['remarks'].update('')
            window['noFollow'].update(False)
            window['promotionTrue'].update(False)
            window['promotionFalse'].update(False)
        else:
            window['greeting'].update('')
            window['detail'].update('')
            window['DiscordInput'].update('')
            window['1on1Input'].update('')
            window['1on1Course'].update('')
            window['remarks'].update('')
            window['greeting'].update('')
            window['seven'].update('1')
            window['subject'].update(False)
            window['noFollow'].update(False)
            window['promotionTrue'].update(False)
            window['promotionFalse'].update(False)
            
        if values['JavaBasic'] or values['JavaStandard'] or values['JavaAdvance'] or values['BuildUp'] or values['1on1'] or values['Discord']:
            window['fast'].update(True)
            window['tabgroup'].Widget.select(0)
                        
    # ウィンドウ終了処理
    if event == sg.WINDOW_CLOSED:
        break

window.close()
