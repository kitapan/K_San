import PySimpleGUI as sg
import pyperclip
import datetime
import os
import sys
import time
import threading
import pygame
from java_courses import java_course_options
from programming_courses import programming_course_options
from office_courses import office_course_options
from creative_courses import creative_course_options
from cad_courses import cad_course_options
from google_courses import google_course_options
from school_number import school_options

# ウィンドウテーマ
sg.theme('TealMono')

java_course = ['', 'ベーシック', 'スタンダード', 'アドバンスド']
font = ('Helvetica', 12)
bold_font = ('Helvetica', 13, 'bold')

# today
now = datetime.date.today()
now = "{0:%m%d}".format(now)

# タイマーの初期化
timer_running = False
start_time = 0
alarm_playing = False

# pygameの初期化
pygame.mixer.init()

# 1~70
lis = ['{:02d}'.format(i + 1) for i in range(70)]

# 1~8
period = [str(p + 1) for p in range(8)]

# 1on1
one_on_one_numbers = ['', '1', '2', '3', '4', '5', '6', '7']

# アクションタブ
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

# Javaタブ
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
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='javaDetail', font=font)]
]

# プログラミングタブ
tabProgramming = [
    [sg.Radio('PHPﾍﾞｰｼｯｸ', '1', key='php_basic', enable_events=True),
     sg.Radio('PHPｱﾄﾞﾊﾞﾝｽ', '1', key='php_advance', enable_events=True),
     sg.Radio('WordPress', '1', key='wordpress', enable_events=True),
     sg.Radio('SQL1-2', '1', key='sql', enable_events=True),
     sg.Radio('Pythonﾍﾞｰｼｯｸ', '1', key='python_basic', enable_events=True)],
    [sg.Radio('Android入門', '1', key='java_android_trial', enable_events=True),
     sg.Radio('Android基礎編', '1', key='java_android', enable_events=True),
     sg.Radio('RPA', '1', key='rpa', enable_events=True)],        
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='programmingDetail', font=font)]
]

# オフィスタブ
tabOffice = [
    [sg.Radio('W1-2', '1', key='word_basic', enable_events=True),
     sg.Radio('W3-4', '1', key='word_advance', enable_events=True),
     sg.Radio('E1-2', '1', key='excel_basic', enable_events=True),
     sg.Radio('E3-4', '1', key='excel_advance', enable_events=True),
     sg.Radio('PP1-2', '1', key='powerpoint_basic', enable_events=True),
     sg.Radio('PP3-4', '1', key='powerpoint_advance', enable_events=True),
     sg.Radio('AC1-2', '1', key='access_basic', enable_events=True),
     sg.Radio('AC3-4', '1', key='access_advance', enable_events=True)],
    [sg.Radio('ACｸｴﾘ活用', '1', key='access_query_utilization', enable_events=True),
     sg.Radio('ACﾋﾞｼﾞﾈｽ活用', '1', key='access_business', enable_events=True)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetail', font=font)]
]

# オフィスタブ2
tabOfficePlus = [
    [sg.Radio('ﾋﾟﾎﾞｯﾄ実践', '1', key='pivot_tables', enable_events=True),
     sg.Radio('Eﾏｽﾀｰﾌﾞｯｸ', '1', key='excel_master_book', enable_events=True),
     sg.Radio('VBA', '1', key='skills_up_vba', enable_events=True),
     sg.Radio('VBAｱﾄﾞ', '1', key='vba_advanced', enable_events=True),
     sg.Radio('ﾏｸﾛ実践', '1', key='macro_practice', enable_events=True),
     sg.Radio('VBA実践', '1', key='vba_practice', enable_events=True)],
    [sg.Radio('Eﾊﾟﾜｰｸｴﾘ', '1', key='excel_power_query', enable_events=True),
     sg.Radio('Eﾊﾟﾜｰﾋﾟﾎﾞｯﾄ', '1', key='excel_power_pivot', enable_events=True),
     sg.Radio('ﾍﾞｰｼｯｸ関数', '1', key='basic_function', enable_events=True),
     sg.Radio('ｱﾄﾞﾊﾞﾝｽ関数', '1', key='advance_function', enable_events=True),
     sg.Radio('ｽｷﾙｱｯﾌﾟ関数', '1', key='skill_function', enable_events=True)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetailPlus', font=font)]
]

# クリエイティブタブ
tabCreative = [
    [sg.Radio('HTMLﾍﾞｰｼｯｸ', '1', key='html_css_basic', enable_events=True),
     sg.Radio('MEB1', '1', key='web_coding', enable_events=True),
     sg.Radio('MEB2', '1', key='responsive_web_design', enable_events=True),
     sg.Radio('HTMLﾄﾚｰﾆﾝｸﾞ', '1', key='html_css_training', enable_events=True),
     sg.Radio('JSB', '1', key='java_script', enable_events=True),
     sg.Radio('MEA', '1', key='web_coding_advance', enable_events=True)],
    [sg.Radio('Ai1', '1', key='illustrator_cc2021_basic1', enable_events=True),
     sg.Radio('Ai2', '1', key='illustrator_cc2021_basic2', enable_events=True),
     sg.Radio('Ai3', '1', key='illustrator_cc2021_advance', enable_events=True),
     sg.Radio('Ps1', '1', key='photoshop_cc2021_basic1', enable_events=True),
     sg.Radio('Ps2', '1', key='photoshop_cc2021_basic2', enable_events=True),
     sg.Radio('Ps3', '1', key='photoshop_cc2021_advanced', enable_events=True),
     sg.Radio('ﾄﾞｷｭﾒﾝﾄ作成', '1', key='design_document', enable_events=True),
     sg.Radio('WEB素材', '1', key='parts_web', enable_events=True)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='creativeDetail', font=font)]
]

# クリエイティブタブ2
tabCreativePlus = [
    [sg.Radio('Prﾍﾞｰｼｯｸ', '1', key='premiere_pro_basic', enable_events=True),
     sg.Radio('Aeﾍﾞｰｼｯｸ', '1', key='after_effects_basic', enable_events=True),
     sg.Radio('Prｽﾀﾝﾀﾞｰﾄﾞ', '1', key='premiere_pro_standard', enable_events=True),
     sg.Radio('Prｴﾌｪｸﾄﾊﾞﾘｴｰｼｮﾝ', '1', key='effect_variations', enable_events=True),
     sg.Radio('FireFly', '1', key='firefly', enable_events=True),],
    [sg.Radio('Ai1(2024)', '1', key='illustrator_cc2024_basic1', enable_events=True),
     sg.Radio('Ai2(2024)', '1', key='illustrator_cc2024_basic2', enable_events=True),
     sg.Radio('Ps1(2024)', '1', key='photoshop_cc2024_basic1', enable_events=True),
     sg.Radio('Ps2(2024)', '1', key='photoshop_cc2024_basic2', enable_events=True),
     sg.Radio('ﾃﾞｻﾞｲﾝ', '1', key='create_design', enable_events=True),
     sg.Radio('ﾚﾀｯﾁ', '1', key='retouching_processing', enable_events=True)],         
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='creativeDetailPlus', font=font)]
]

# CADタブ
tabCad = [
    [sg.Radio('Auto1-2', '1', key='auto_cad_basic', enable_events=True),
     sg.Radio('Auto3-4(建)', '1', key='auto_cad_advanced_architecture', enable_events=True),
     sg.Radio('Auto3-4(機)', '1', key='auto_cad_advanced_mechanical', enable_events=True),
     sg.Radio('Jw1-2', '1', key='jw_cad_basic', enable_events=True),
     sg.Radio('Jw3-4', '1', key='jw_cad_advanced', enable_events=True),
     sg.Radio('Fusionﾍﾞｰｼｯｸ', '1', key='fusion_basic', enable_events=True)],
    [sg.Radio('Fusionｱﾄﾞﾊﾞﾝｽ', '1', key='fusion_advance', enable_events=True),
     sg.Radio('AutoCAD建築製図編', '1', key='architectural_draft', enable_events=True),
     sg.Radio('AutoCAD土木編', '1', key='civil_engineering', enable_events=True)],    
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='cadDetail', font=font)]
]

# googleタブ
tabGoogle = [
    
    [sg.Radio('ChatGPT', '1', key='chatgpt_trial', enable_events=True),
     sg.Radio('GAT', '1', key='gat', enable_events=True),
     sg.Radio('GSS', '1', key='gss', enable_events=True), 
     sg.Radio('GASﾄﾗｲｱﾙ', '1', key='gas_trial', enable_events=True),
     sg.Radio('GASﾍﾞｰｼｯｸ', '1', key='gas_basic', enable_events=True),
     sg.Radio('GASｽﾀﾝﾀﾞｰﾄﾞ', '1', key='gas_standard', enable_events=True)],
    [sg.Radio('AppSheet', '1', key='appsheet_trial', enable_events=True)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='googleDetail', font=font)]
]

# トラブルタブ
tabTrouble = [
    [sg.Text('校舎名', size=(5, 1)),
     sg.Combo([], size=(27, 1), key='schoolDetail')],
    [sg.Text('ID', size=(2, 1)),
     sg.InputText(size=(12, 1), font=font, key='studentId'),
     sg.Text('名前', size=(3, 1)),
     sg.InputText(size=(17, 1), font=font, key='studentName'),
     sg.Text('科目', size=(3, 1)),
     sg.InputText(size=(17, 1), font=font, key='studentCourse')],
    [sg.Radio('Room移動', '1', key='roomChange', enable_events=True),
     sg.Radio('音声つながらない', '1', key='audioFollow', enable_events=True),
     sg.Radio('Roomにいない', '1', key='notRoom', enable_events=True),
     sg.Radio('助けてください', '1', key='helpMe', enable_events=True)]
]

col1 = [
    [sg.Checkbox('わかばROOM', key='wakaba', default=False),
    sg.Checkbox('初VU期間サポート対象', key='subject', default=False),
    sg.Spin(period, size=(2, 1), font=font, key='seven')],
    [sg.Text('授業', size=(4, 1), font=font),
    sg.Spin(lis, size=(2, 1), font=font, key='jyugyou'),
    sg.Text('時限', size=(4, 1), font=font),
    sg.Spin(period, size=(2, 1), font=font, key='jigen'),
    sg.Text('Room', size=(5, 1), font=font),
    sg.Spin(lis, size=(2, 1), font=font, key='room')],
    [sg.Checkbox('受講促進○', key='promotionTrue', default=False, size=(9, 1), font=font),
     sg.Checkbox('受講促進×', key='promotionFalse', default=False, size=(9, 1), font=font),
     sg.Checkbox('巡回不要', key='noFollow', default=False, size=(9, 1), font=font)],
]

col2 =[
    sg.Button('COPY', size=(10, 1), key='COPY', button_color=('white', '#001480')),
    sg.Button('CODE', size=(10, 1), key='CODE', button_color=('white', '#001480')),
    sg.Button('CLEAR', size=(10, 1), key='CLEAR', button_color=('white', '#dc143c')),
    sg.Button('START', key='start_stop', size=(10, 1)),
    sg.Text('所要時間：', size=(8, 1), font=font),
    sg.Text('00:00', size=(10, 1), font=font, key='timer')
]

# Main tabs
layout = [
    [col1],
    [sg.TabGroup([[sg.Tab('AC', tabAction), sg.Tab('JV', tabJava), sg.Tab('PG', tabProgramming), 
                   sg.Tab('CR', tabCreative), sg.Tab('CR+', tabCreativePlus), sg.Tab('GO', tabGoogle), sg.Tab('OF', tabOffice),
                   sg.Tab('OF+', tabOfficePlus), sg.Tab('CD', tabCad),sg.Tab('TR', tabTrouble)]],
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
window = sg.Window('K_San', layout, keep_on_top=True, size=(595, 305), resizable=True, icon=icon_path)

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
    data += f"挨拶:{course_name}　{values[detail]}\n注意事項:"
    if values['noFollow']:
        data += '★巡回不要　'
    if values['promotionTrue']:
        data += f'受講促進○ {now} {values["jigen"]}限'
    if values['promotionFalse']:
        data += '受講促進×'
        
    data += f"\n{values['remarks']}" if values['noFollow'] or values['promotionTrue'] or values['promotionFalse'] else values['remarks']

    return data

def play_alarm():
    absolute_path = os.path.abspath('alarm.wav')
    pygame.mixer.music.load(absolute_path)
    pygame.mixer.music.set_volume(0.1)  # 音量を10%に設定
    pygame.mixer.music.play(loops=-1)  # ループ再生


def stop_alarm():
    pygame.mixer.music.stop()

# メイン処理
while True:
    event, values = window.read(timeout=10)
    
    # タブの選択イベント処理
    if event == 'tabgroup':
        selected_tab = window['tabgroup'].get()
        if selected_tab == 'AC':
            window['fast'].update(value=True)
            
    # Java コースの選択イベント
    if event in ('java_basic', 'java_standard', 'java_advance'):
        selected_type = event
        window['javaDetail'].update(values=java_course_options[selected_type])
        
    # プログラミング コースの選択イベント
    if event in ('php_basic', 'php_advance', 'wordpress', 'python_basic','java_android',
                 'java_android_trial','sql', 'rpa'):
        selected_type = event
        window['programmingDetail'].update(values=programming_course_options[selected_type])
        
    # オフィス コースの選択イベント
    if event in ('word_basic', 'word_advance', 'excel_basic', 'excel_advance', 'powerpoint_basic', 'powerpoint_advance',
                 'access_basic', 'access_advance', 'pivot_tables', 'excel_master_book', 'skills_up_vba', 'vba_advanced',
                 'macro_practice', 'vba_practice', 'excel_power_query', 'excel_power_pivot', 'access_query_utilization',
                 'access_business', 'basic_function', 'advance_function', 'skill_function'):
        selected_type = event
        window['officeDetail'].update(values=office_course_options[selected_type])
        window['officeDetailPlus'].update(values=office_course_options[selected_type])
    
    # クリエイティブ コースの選択イベント
    if event in ('html_css_basic', 'web_coding', 'responsive_web_design', 'html_css_training', 'java_script', 'web_coding_advance', 'parts_web',
                 'illustrator_cc2021_basic1', 'illustrator_cc2021_basic2', 'illustrator_cc2021_advance', 'photoshop_cc2021_basic1',
                 'photoshop_cc2021_basic2', 'photoshop_cc2021_advanced', 'firefly', 'design_document', 'premiere_pro_basic',
                 'after_effects_basic', 'premiere_pro_standard', 'effect_variations', 'illustrator_cc2024_basic1', 'illustrator_cc2024_basic2',
                 'photoshop_cc2024_basic1', 'photoshop_cc2024_basic2', 'create_design', 'retouching_processing'):
        selected_type = event
        window['creativeDetail'].update(values=creative_course_options[selected_type])
        window['creativeDetailPlus'].update(values=creative_course_options[selected_type])
        
    # CAD コースの選択イベント
    if event in ('auto_cad_basic', 'auto_cad_advanced_architecture', 'auto_cad_advanced_mechanical', 'jw_cad_basic', 'jw_cad_advanced',
                 'fusion_basic', 'fusion_advance', 'architectural_draft', 'civil_engineering'):
        selected_type = event
        window['cadDetail'].update(values=cad_course_options[selected_type])
        
    # Google コースの選択イベント
    if event in ('chatgpt_trial','gat', 'gss', 'gas_trial', 'gas_basic', 'gas_standard','appsheet_trial'):
        selected_type = event
        window['googleDetail'].update(values=google_course_options[selected_type])
    
    # トラブル 校舎選択イベント
    if event == 'tabgroup':
        selected_tab = window['tabgroup'].get()
        if selected_tab == 'TR':
            window['schoolDetail'].update(values=school_options['schools'])   


    # COPY ボタンの処理
    if event == 'COPY':
        data = ""
        if values['fast']:
            data = get_greeting_data(values)
        elif values['help']:
            data = f"ヘルプ対応:{values['remarks']} 所要時間：{window['timer'].get()}"
        elif values['follow']:
            data = f"フォロー対応:{values['remarks']} 所要時間：{window['timer'].get()}"
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
        elif values['java_android']:
            data = get_course_data(values, 'Android基礎開発講座', 'programmingDetail')
        elif values['java_android_trial']:
            data = get_course_data(values, 'Androidアプリ入門', 'programmingDetail')
        elif values['sql']:
            data = get_course_data(values, 'SQL1-2', 'programmingDetail')
        elif values['rpa']:
            data = get_course_data(values, 'RPA講座ベーシックforSynchRoid', 'programmingDetail')
               
        # オフィスタブ作成    
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
        elif values['access_query_utilization']:
            data = get_course_data(values, 'Accessクエリ活用', 'officeDetail')
        elif values['access_business']:
            data = get_course_data(values, 'Accessビジネス活用', 'officeDetail')
            
        # オフィス+タブ作成     
        elif values['pivot_tables']:
            data = get_course_data(values, 'ピボット実践', 'officeDetailPlus')            
        elif values['excel_master_book']:
            data = get_course_data(values, 'Excelマスターブック', 'officeDetailPlus')
        elif values['skills_up_vba']:
            data = get_course_data(values, 'スキルアップVBA', 'officeDetailPlus')                  
        elif values['vba_advanced']:
            data = get_course_data(values, 'VBAアドバンスド', 'officeDetailPlus')                  
        elif values['macro_practice']:
            data = get_course_data(values, 'マクロ実践', 'officeDetailPlus')                  
        elif values['vba_practice']:
            data = get_course_data(values, 'VBA実践', 'officeDetailPlus')                  
        elif values['excel_power_query']:
            data = get_course_data(values, 'Excelパワークエリ', 'officeDetailPlus')                              
        elif values['excel_power_pivot']:
            data = get_course_data(values, 'Excelパワーピボット', 'officeDetailPlus')
        elif values['basic_function']:
            data = get_course_data(values, 'ベーシックExcel関数実践', 'officeDetailPlus')                  
        elif values['advance_function']:
            data = get_course_data(values, 'アドバンスExcel関数実践', 'officeDetailPlus')                              
        elif values['skill_function']:
            data = get_course_data(values, 'スキルアップExcel関数実践', 'officeDetailPlus')            
                        
        #　クリエイティブタブ作成    
        elif values['html_css_basic']:
            data = get_course_data(values, 'HTML/CSSベーシック', 'creativeDetail')
        elif values['web_coding']:
            data = get_course_data(values, 'マークアップEB パート1(WEB)', 'creativeDetail')
        elif values['responsive_web_design']:
            data = get_course_data(values, 'マークアップEB パート2(レスポンシブ)', 'creativeDetail')
        elif values['html_css_training']:
            data = get_course_data(values, 'HTML/CSSトレーニングブック～運用・更新編～', 'creativeDetail')
        elif values['java_script']:
            data = get_course_data(values, 'JavaScriptベーシック', 'creativeDetail')
        elif values['web_coding_advance']:
            data = get_course_data(values, 'マークアップエンジニア アドバンス', 'creativeDetail')             
        elif values['illustrator_cc2021_basic1']:
            data = get_course_data(values, 'Illustrator ベーシック1', 'creativeDetail')
        elif values['illustrator_cc2021_basic2']:
            data = get_course_data(values, 'Illustrator ベーシック2', 'creativeDetail')
        elif values['illustrator_cc2021_advance']:
            data = get_course_data(values, 'Illustrator アドバンス', 'creativeDetail')
        elif values['photoshop_cc2021_basic1']:
            data = get_course_data(values, 'Photoshop ベーシック1', 'creativeDetail')
        elif values['photoshop_cc2021_basic2']:
            data = get_course_data(values, 'Photoshop ベーシック2', 'creativeDetail')
        elif values['photoshop_cc2021_advanced']:
            data = get_course_data(values, 'Photoshop アドバンス', 'creativeDetail')            
        elif values['design_document']:
            data = get_course_data(values, 'デザインで差をつけるドキュメント作成講座', 'creativeDetail')
        elif values['parts_web']:
            data = get_course_data(values, 'パーツで魅せるWEB素材作成講座', 'creativeDetail')                 
                 
        #　クリエイティブ+タブ作成 
        elif values['premiere_pro_basic']:
            data = get_course_data(values, 'PremierePro ベーシック', 'creativeDetailPlus')
        elif values['after_effects_basic']:
            data = get_course_data(values, 'AfterEffects ベーシック', 'creativeDetailPlus')
        elif values['premiere_pro_standard']:
            data = get_course_data(values, 'PremierePro スタンダード', 'creativeDetailPlus')
        elif values['effect_variations']:
            data = get_course_data(values, 'PremierePro スタンダード～エフェクトバリエーション～', 'creativeDetailPlus')
        elif values['firefly']:
            data = get_course_data(values, 'AdobeFirefly トライアル', 'creativeDetailPlus')
        elif values['illustrator_cc2024_basic1']:
            data = get_course_data(values, 'Illustrator(2024) ベーシック1', 'creativeDetailPlus')
        elif values['illustrator_cc2024_basic2']:
            data = get_course_data(values, 'Illustrator(2024) ベーシック2', 'creativeDetailPlus')
        elif values['photoshop_cc2024_basic1']:
            data = get_course_data(values, 'Photoshop(2024) ベーシック1', 'creativeDetailPlus')
        elif values['photoshop_cc2024_basic2']:
            data = get_course_data(values, 'Photoshop(2024) ベーシック2', 'creativeDetailPlus')            
        elif values['create_design']:
            data = get_course_data(values, 'Illustrator & Photoshop デザインの作り方', 'creativeDetailPlus')
        elif values['retouching_processing']:
            data = get_course_data(values, 'Photoshop レタッチ・加工', 'creativeDetailPlus')                      
   
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
            data = get_course_data(values, 'JwCADアドバンス', 'cadDetail')
        elif values['fusion_basic']:
            data = get_course_data(values, 'Fusionベーシック', 'cadDetail')
        elif values['fusion_advance']:
            data = get_course_data(values, 'Fusionアドバンス', 'cadDetail')
        elif values['architectural_draft']:
            data = get_course_data(values, 'AutoCAD建築製図編', 'cadDetail')                       
        elif values['civil_engineering']:
            data = get_course_data(values, 'AutoCAD土木編', 'cadDetail')                  
            
        #　googleタブ作成
        elif values['chatgpt_trial']:
            data = get_course_data(values, 'ChatGPT トライアル', 'googleDetail')        
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
        elif values['appsheet_trial']:
            data = get_course_data(values, 'AppSheetトライアル', 'googleDetail')
            
        #　トラブルタブ作成
        elif values['roomChange']:
            data = f"{values['studentId']}　{values['studentName']} 様、\n科目が{values['studentCourse']}です。Room移動許可をお願いします。"
        elif values['audioFollow']:
            data = f"{values['studentId']}　{values['studentName']} 様、\n音声がつながりません。フォローお願いします。"
        elif values['notRoom']:
            data = f"{values['studentId']}　{values['studentName']} 様、\nステータスが出席ですがRoomにいません。フォローお願いします。"
        elif values['helpMe']:
            data = f"Room{values['jyugyou']}、ヘルプなどでROOMが回っていません。助けてください！"         
                     
        pyperclip.copy(data)

    # CODEボタン
    if event == 'CODE':
        data = f"{now}_{values['jyugyou']}_{values['jigen']}限_Room00"
        pyperclip.copy(data)
    
    # タイマー実装
    if event == 'start_stop':
        if not timer_running:
            start_time = time.time() - (start_time if start_time else 0)
            timer_running = True
            window['start_stop'].update('STOP')
        else:
            stop_alarm()
            
    # アラーム停止
    elif event == 'CLEAR':
        timer_running = False
        start_time = 0
        window['timer'].update('00:00')
        window['start_stop'].update('START')
        window['timer'].update(font=font, text_color='black')  # テキストの色とフォントをリセット
        stop_alarm()
        alarm_playing = False
        
    # アラーム再生
    if timer_running:
        elapsed_time = time.time() - start_time
        window['timer'].update(time.strftime('%M:%S', time.gmtime(elapsed_time)))
        if elapsed_time >= 1 * 60 and not alarm_playing:  # 3分 = 3 * 60秒
            threading.Thread(target=play_alarm).start()
            window['timer'].update(font=bold_font, text_color='red')  # 3分経過でフォントを太字、色を赤に
            alarm_playing = True  # アラームが再生中であることを記録

    # CLEARボタン
    if event == 'CLEAR':
        window['greeting'].update('')
        window['remarks'].update('')
        window['noFollow'].update(False)
        window['promotionTrue'].update(False)
        window['promotionFalse'].update(False)
        
        if values['wakaba']:
            window['javaDetail'].update('')
            window['programmingDetail'].update('')
            window['creativeDetail'].update('')
            window['creativeDetailPlus'].update('')
            window['googleDetail'].update('')
            window['officeDetail'].update('')
            window['officeDetailPlus'].update('')
            window['cadDetail'].update('')
            window['schoolDetail'].update('')
            window['studentId'].update('')
            window['studentName'].update('')
            window['studentCourse'].update('')            
            window['DiscordInput'].update('')
            window['1on1Input'].update('')
            window['1on1Course'].update('')
            
        else:
            window['javaDetail'].update('')
            window['programmingDetail'].update('')
            window['creativeDetail'].update('')
            window['creativeDetailPlus'].update('')
            window['googleDetail'].update('')
            window['officeDetail'].update('')
            window['officeDetailPlus'].update('')
            window['cadDetail'].update('')
            window['schoolDetail'].update('')
            window['studentId'].update('')
            window['studentName'].update('')
            window['studentCourse'].update('')            
            window['DiscordInput'].update('')
            window['1on1Input'].update('')
            window['1on1Course'].update('')
            window['subject'].update(False)

        if any(values[key] for key in ('java_basic', 'java_standard', 'java_advance', 'BuildUp', '1on1', 'Discord',
                                       'php_basic', 'php_advance', 'wordpress', 'python_basic',
                                       'java_android', 'java_android_trial','sql', 'rpa', 'word_basic', 'word_advance', 'excel_basic',
                                       'excel_advance', 'powerpoint_basic', 'powerpoint_advance', 'access_basic', 'access_advance',
                                       'pivot_tables', 'excel_master_book', 'skills_up_vba', 'vba_advanced', 'macro_practice',
                                       'vba_practice', 'excel_power_query', 'excel_power_pivot', 'access_query_utilization',
                                       'access_business', 'basic_function', 'advance_function', 'skill_function', 'html_css_basic',
                                       'web_coding', 'responsive_web_design', 'html_css_training', 'java_script', 'web_coding_advance', 'parts_web',
                                       'illustrator_cc2021_basic1', 'illustrator_cc2021_basic2', 'illustrator_cc2021_advance',
                                       'photoshop_cc2021_basic1', 'photoshop_cc2021_basic2', 'photoshop_cc2021_advanced', 'firefly',
                                       'design_document', 'premiere_pro_basic', 'after_effects_basic', 'premiere_pro_standard',
                                       'effect_variations', 'illustrator_cc2024_basic1', 'illustrator_cc2024_basic2', 'photoshop_cc2024_basic1',
                                       'photoshop_cc2024_basic2', 'create_design', 'retouching_processing', 'auto_cad_basic',
                                       'auto_cad_advanced_architecture', 'auto_cad_advanced_mechanical', 'jw_cad_basic', 'jw_cad_advanced',
                                       'fusion_basic', 'fusion_advance', 'architectural_draft', 'civil_engineering', 'chatgpt_trial', 'gat',
                                       'gss', 'gas_trial', 'gas_basic', 'gas_standard','appsheet_trial')):
            window['fast'].update(True)
            window['tabgroup'].Widget.select(0)

    # ウィンドウ終了処理
    if event == sg.WINDOW_CLOSED:
        break

window.close()
pygame.mixer.quit()
