import PySimpleGUI as sg
import pyperclip
import datetime
import os
import sys
from java_courses import java_course_options
from programming_courses import programming_course_options
from office_courses import office_course_options
from creative_courses import creative_course_options
from cad_courses import cad_course_options
from google_courses import google_course_options

# ウィンドウテーマ
sg.theme('TealMono')

java_course = ['', 'ベーシック', 'スタンダード', 'アドバンスド']
font = ('Helvetica', 12)

# today
now = datetime.date.today()
now = "{0:%m%d}".format(now)

# 1~70
lis = ['{:02d}'.format(i + 1) for i in range(70)]

# 1~8
period = [str(p + 1) for p in range(8)]

# 1on1
one_on_one_numbers = ['', '1', '2', '3', '4', '5', '6', '7']

# 通常
tabAction = [
    [sg.Radio('挨拶', '1', default=True, key='fast'),
     sg.Radio('ヘルプ', '1', key='help'),
     sg.Radio('フォロー', '1', key='follow')],
    [sg.Radio('面談依頼', '1', key='cs'),
     sg.Radio('VUサポート', '1', key='vu'),
     sg.Radio('初VU期間サポート', '1', key='fastVu')],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.InputText(size=(150, 1), key='greeting', font=font)]
]

# Javaエンジニアタブ
tabJava = [
    [sg.Radio('ベーシック', '1', key='java_basic', enable_events=True),
     sg.Radio('スタンダード', '1', key='java_standard', enable_events=True),
     sg.Radio('アドバンスド', '1', key='java_advance', enable_events=True)],
    [sg.Radio('Discord', '1', key='Discord', enable_events=True, size=(5, 1)),
     sg.InputText(size=(9, 1), font=font, key='DiscordInput'),
     sg.Radio('1on1', '1', key='1on1', enable_events=True, size=(3, 1)),
     sg.Spin(java_course, size=(11, 1), key='1on1Course', font=font),
     sg.Spin(one_on_one_numbers, size=(2, 1), key='1on1Input', font=font),
     sg.Radio('BuildUp', '1', key='BuildUp', enable_events=True)],
    [sg.Combo([], size=(150, 1), key='javaDetail', font=font)]
]

# プログラミングタブ
tabProgramming = [
    [sg.Radio('PHPベーシック', '1', key='php_basic', enable_events=True),
     sg.Radio('PHPアドバンス', '1', key='php_advance', enable_events=True),
     sg.Radio('WordPress', '1', key='wordpress', enable_events=True),
     sg.Radio('実践Java技術者試験', '1', key='java_specialist', enable_events=True)],
    [sg.Radio('Pythonベーシック', '1', key='python_basic', enable_events=True),
     sg.Radio('android入門', '1', key='java_android_trial', enable_events=True),
     sg.Radio('android基礎編', '1', key='java_android', enable_events=True),
     sg.Radio('SQL1-2', '1', key='sql', enable_events=True)],
    [sg.Radio('AppSheet', '1', key='appsheet_trial', enable_events=True)],    
    [sg.Combo([], size=(150, 1), key='programmingDetail', font=font)]
]

# officeタブ
tabOffice = [
    [sg.Radio('Word1-2', '1', key='word_basic', enable_events=True),
     sg.Radio('Word3-4', '1', key='word_advance', enable_events=True),
     sg.Radio('Excel1-2', '1', key='excel_basic', enable_events=True),
     sg.Radio('Excel3-4', '1', key='excel_advance', enable_events=True)],
    [sg.Radio('PowerPoint1-2', '1', key='powerpoint_basic', enable_events=True),
     sg.Radio('PowerPoint3-4', '1', key='powerpoint_advance', enable_events=True),
     sg.Radio('Access1-2', '1', key='access_basic', enable_events=True),
     sg.Radio('Access3-4', '1', key='access_advance', enable_events=True)],
    [sg.Combo([], size=(150, 1), key='officeDetail', font=font)]
]

# クリエイティブタブ
tabCreative = [
    [sg.Radio('HTML/CSSﾍﾞｰｼｯｸ', '1', key='html_css_basic', enable_events=True),
     sg.Radio('MEB P1', '1', key='web_coding', enable_events=True),
     sg.Radio('MEB P2', '1', key='responsive_web_design', enable_events=True),
     sg.Radio('HTML/CSSﾄﾚｰﾆﾝｸﾞ', '1', key='html_css_training', enable_events=True)],
    [sg.Radio('JSB', '1', key='java_script', enable_events=True)],
    [sg.Combo([], size=(150, 1), key='creativeDetail', font=font)]
]

# CADタブ
tabCad = [
    [sg.Radio('AutoCAD1-2', '1', key='auto_cad_basic', enable_events=True),
     sg.Radio('AutoCAD3-4(建築)', '1', key='auto_cad_advanced_architecture', enable_events=True),
     sg.Radio('AutoCAD3-4(機械)', '1', key='auto_cad_advanced_mechanical', enable_events=True),
     sg.Radio('JwCAD1-2', '1', key='jw_cad_basic', enable_events=True)],
    [sg.Radio('JwCAD3-4', '1', key='jw_cad_advanced', enable_events=True)],
    [sg.Combo([], size=(150, 1), key='cadDetail', font=font)]
]

# googleタブ
tabGoogle = [
    [sg.Radio('GAT', '1', key='gat', enable_events=True),
     sg.Radio('GSS', '1', key='gss', enable_events=True),
     sg.Radio('GASトライアル', '1', key='gas_trial', enable_events=True),
     sg.Radio('GASベーシック', '1', key='gas_basic', enable_events=True)],
    [sg.Radio('GASスタンダード', '1', key='gas_standard', enable_events=True)],
    [sg.Combo([], size=(150, 1), key='googleDetail', font=font)]
]

col1 = [
    [sg.Checkbox('わかばROOM', key='wakaba', default=False),
    sg.Checkbox('初VU期間サポート対象', key='subject', default=False),
    sg.Spin(period, size=(2, 1), font=font, key='seven')],
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

col2 =[
    sg.Button('COPY', size=(10, 1), key='COPY', button_color=('white', '#001480')),
    sg.Button('CODE', size=(10, 1), key='CODE', button_color=('white', '#001480')),
    sg.Button('CLEAR', size=(10, 1), key='CLEAR', button_color=('white', '#dc143c'))
]

# Main tabs
layout = [
    [col1],
    [sg.TabGroup([[sg.Tab('ｱｸｼｮﾝ', tabAction), sg.Tab('Java', tabJava), sg.Tab('ﾌﾟﾛｸﾞﾗﾐﾝｸﾞ', tabProgramming), 
                   sg.Tab('ｸﾘｴｲﾃｨﾌﾞ', tabCreative), sg.Tab('Google', tabGoogle), sg.Tab('ｵﾌｨｽ', tabOffice),
                   sg.Tab('CAD', tabCad)]],
                 key="tabgroup", enable_events=True)],
    [sg.Text('備考', size=(4, 1), font=font),sg.Multiline(size=(150, 2), key='remarks', font=font)],
    [col2]
]

# アイコンのパス設定
def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath('.'), relative)

icon_path = resource_path("128_04.ico")

# ウィンドウの生成
window = sg.Window('K_3', layout, keep_on_top=True, size=(560, 305), resizable=True, icon=icon_path)

def get_greeting_data(values):
    data = ""
    if values['wakaba']:
        data += '☆'
    if values['subject']:
        data += f"【初VU期間サポート対象】{values['seven']}回目\n"
    data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
    data += f"挨拶:{values['greeting']}\n注意事項:"
    if values['noFollow']:
        data += '★巡回不要　'
    if values['promotionTrue']:
        data += f'受講促進○ {now} {values["jigen"]}限'
    if values['promotionFalse']:
        data += '受講促進×'
 
    data += f"\n{values['remarks']}" if values['noFollow'] or values['promotionTrue'] or values['promotionFalse'] else values['remarks']
       
    return data

def get_course_data(values, course_name, detail):
    data = ""
    if values['wakaba']:
        data += '☆'
    if values['subject']:
        data += f"【初VU期間サポート対象】{values['seven']}回目\n"
    data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
    data += f"挨拶:{course_name}\n{values[detail]}\n注意事項:"
    if values['noFollow']:
        data += '★巡回不要　'
    if values['promotionTrue']:
        data += f'受講促進○ {now} {values["jigen"]}限'
    if values['promotionFalse']:
        data += '受講促進×'
        
    data += f"\n{values['remarks']}" if values['noFollow'] or values['promotionTrue'] or values['promotionFalse'] else values['remarks']

    return data

# メイン処理
while True:
    event, values = window.read()
    
    # タブの選択イベント処理
    if event == 'tabgroup':
        selected_tab = window['tabgroup'].get()
        if selected_tab == 'アクション':
            window['fast'].update(value=True)
            
    # Java コースの選択イベント
    if event in ('java_basic', 'java_standard', 'java_advance'):
        selected_type = event
        window['javaDetail'].update(values=java_course_options[selected_type])
        
    # programming コースの選択イベント
    if event in ('php_basic', 'php_advance', 'wordpress', 'java_specialist', 'python_basic','java_android','java_android_trial','sql','appsheet_trial'):
        selected_type = event
        window['programmingDetail'].update(values=programming_course_options[selected_type])
        
    # office コースの選択イベント
    if event in ('word_basic', 'word_advance', 'excel_basic', 'excel_advance', 'powerpoint_basic', 'powerpoint_advance', 'access_basic', 'access_advance'):
        selected_type = event
        window['officeDetail'].update(values=office_course_options[selected_type])
    
    # クリエイティブ コースの選択イベント
    if event in ('html_css_basic', 'web_coding', 'responsive_web_design', 'html_css_training', 'java_script'):
        selected_type = event
        window['creativeDetail'].update(values=creative_course_options[selected_type])
        
    # CAD コースの選択イベント
    if event in ('auto_cad_basic', 'auto_cad_advanced_architecture', 'auto_cad_advanced_mechanical', 'jw_cad_basic', 'jw_cad_advanced'):
        selected_type = event
        window['cadDetail'].update(values=cad_course_options[selected_type])
        
    # Google コースの選択イベント
    if event in ('gat', 'gss', 'gas_trial', 'gas_basic', 'gas_standard'):
        selected_type = event
        window['googleDetail'].update(values=google_course_options[selected_type])

    # COPY ボタンの処理
    if event == 'COPY':
        data = ""
        if values['fast']:
            data = get_greeting_data(values)
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
            data = f"1on1:{values['1on1Course']} {values['1on1Input']}回"
            
        # Javaエンジニアタブ作成
        if values['java_basic']:
            data = get_course_data(values, 'Javaエンジニア ベーシック', 'javaDetail')
        elif values['java_standard']:
            data = get_course_data(values, 'Javaエンジニア スタンダード', 'javaDetail')
        elif values['java_advance']:
            data = get_course_data(values, 'Javaエンジニア アドバンスド', 'javaDetail')
            
        # プログラミングタブ作成    
        elif values['php_basic']:
            data = get_course_data(values, 'PHPベーシック', 'programmingDetail')
        elif values['php_advance']:
            data = get_course_data(values, 'PHPアドバンス', 'programmingDetail')
        elif values['wordpress']:
            data = get_course_data(values, 'WordPress', 'programmingDetail')
        elif values['python_basic']:
            data = get_course_data(values, 'Pythonベーシック', 'programmingDetail')
        elif values['java_specialist']:
            data = get_course_data(values, '実践Java技術者試験', 'programmingDetail')
        elif values['java_android']:
            data = get_course_data(values, 'Android基礎開発講座', 'programmingDetail')
        elif values['java_android_trial']:
            data = get_course_data(values, 'Androidアプリ入門', 'programmingDetail')
        elif values['sql']:
            data = get_course_data(values, 'SQL1-2', 'programmingDetail')
        elif values['appsheet_trial']:
            data = get_course_data(values, 'AppSheetトライアル', 'programmingDetail')         
            
        # Officeタブ作成    
        elif values['word_basic']:
            data = get_course_data(values, 'Wordベーシック', 'officeDetail')
        elif values['word_advance']:
            data = get_course_data(values, 'Wordアドバンス', 'officeDetail')
        elif values['excel_basic']:
            data = get_course_data(values, 'Excelベーシック', 'officeDetail')
        elif values['excel_advance']:
            data = get_course_data(values, 'Excelアドバンス', 'officeDetail')
        elif values['powerpoint_basic']:
            data = get_course_data(values, 'PowerPointベーシック', 'officeDetail')
        elif values['powerpoint_advance']:
            data = get_course_data(values, 'PowerPointアドバンス', 'officeDetail')
        elif values['access_basic']:
            data = get_course_data(values, 'Accessベーシック', 'officeDetail')
        elif values['access_advance']:
            data = get_course_data(values, 'Accessアドバンス', 'officeDetail')
            
        #　クリエイティブタブ作成    
        elif values['html_css_basic']:
            data = get_course_data(values, 'HTML/CSSベーシック', 'creativeDetail')
        elif values['web_coding']:
            data = get_course_data(values, 'MEB コーティングベーシック', 'creativeDetail')
        elif values['responsive_web_design']:
            data = get_course_data(values, 'MEB レスポンシブWebデザインベーシック', 'creativeDetail')
        elif values['html_css_training']:
            data = get_course_data(values, 'HTML/CSSトレーニングブック', 'creativeDetail')
        elif values['java_script']:
            data = get_course_data(values, 'JSB', 'creativeDetail')
            
        #　CADタブ作成
        elif values['auto_cad_basic']:
            data = get_course_data(values, 'AutoCADベーシック', 'cadDetail')
        elif values['auto_cad_advanced_architecture']:
            data = get_course_data(values, 'AutoCADアドバンス（建築）', 'cadDetail')
        elif values['auto_cad_advanced_mechanical']:
            data = get_course_data(values, 'AutoCADアドバンス（機械）', 'cadDetail')
        elif values['jw_cad_basic']:
            data = get_course_data(values, 'JwCADベーシック', 'cadDetail')
        elif values['jw_cad_advanced']:
            data = get_course_data(values, 'JwCADベーシック', 'cadDetail')
            
        #　googleタブ作成
        elif values['gat']:
            data = get_course_data(values, 'Googleアプリ トライアル', 'googleDetail')
        elif values['gss']:
            data = get_course_data(values, 'Googleスプレッドシート スタンダード', 'googleDetail')
        elif values['gas_trial']:
            data = get_course_data(values, 'GASトライアル', 'googleDetail')
        elif values['gas_basic']:
            data = get_course_data(values, 'GASベーシック', 'googleDetail')
        elif values['gas_standard']:
            data = get_course_data(values, 'GASスタンダード', 'googleDetail')
                     
        pyperclip.copy(data)

    # CODEボタン
    if event == 'CODE':
        data = f"{now}_{values['jyugyou']}_{values['jigen']}限_Room00"
        pyperclip.copy(data)

    # CLEARボタン
    if event == 'CLEAR':
        window['greeting'].update('')
        window['remarks'].update('')
        window['noFollow'].update(False)
        window['promotionTrue'].update(False)
        window['promotionFalse'].update(False)
        
        if values['wakaba']:
            window['seven'].update('1')
            
        else:
            window['javaDetail'].update('')
            window['DiscordInput'].update('')
            window['1on1Input'].update('')
            window['1on1Course'].update('')
            window['subject'].update(False)

        if any(values[key] for key in ('java_basic', 'java_standard', 'java_advance', 'BuildUp', '1on1', 'Discord')):
            window['fast'].update(True)
            window['tabgroup'].Widget.select(0)

    # ウィンドウ終了処理
    if event == sg.WINDOW_CLOSED:
        break

window.close()
