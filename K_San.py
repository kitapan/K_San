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
from experience_tickets import experience_ticket
from experience_supports import experience_support

# ウィンドウテーマ
sg.theme('TealMono')

font = ('Helvetica', 12)
curriculumFont = ('Helvetica', 9)
bold_font = ('Helvetica', 12, 'bold')

# today
now = datetime.date.today()
now = "{0:%m%d}".format(now)

# タイマーの初期化
timer_running = False
start_time = 0
alarm_playing = False

# pygameの初期化
def initialize_pygame():
    try:
        pygame.mixer.init()
        print("Pygame mixer initialized successfully.")
    except Exception as e:
        print(f"Error initializing pygame mixer: {e}")
        sg.popup_error('Pygameの初期化に失敗しました。プログラムを終了します。')
        sys.exit(1)  # 初期化に失敗した場合、プログラムを終了する

# 1~70
lis = ['{:02d}'.format(i + 1) for i in range(70)]

# 1~8
period = [str(p + 1) for p in range(8)]

# タイマー時間
timerSet = [1, 2, 3, 4, 5]

# アクションタブ
tabAction = [
    [sg.Radio('挨拶', '1', default=True, key='fast'),
     sg.Radio('ヘルプ', '1', key='help'),
     sg.Radio('フォロー', '1', key='follow'),
    #  sg.Radio('Aヘルプ', '1', key='adviceHelp'),
    #  sg.Radio('Aフォロー', '1', key='adviceFollow')
     ],
    [sg.Radio('面談', '1', key='cs'),
     sg.Radio('VUサポ', '1', key='vu'),
     sg.Radio('初VU期間サポ', '1', key='fastVu'),
     sg.Radio('次回テスト', '1', key='nextTest'),
     sg.Radio('テスト実施', '1', key='testExecution'),],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.InputText(size=(150, 1), key='greeting', font=font)]
]

# Javaタブ
tabJava = [
    [sg.Radio('Javaﾍﾞｰｼｯｸ', '1', key='java_basic', enable_events=True),
     sg.Radio('旧Javaﾍﾞｰｼｯｸ', '1', key='old_java_basic', enable_events=True),
     sg.Radio('Javaｽﾀﾝﾀﾞｰﾄﾞ', '1', key='java_standard', enable_events=True),
     sg.Radio('Javaｱﾄﾞﾊﾞﾝｽﾄﾞ', '1', key='java_advance', enable_events=True)],
    [sg.Radio('AWSﾍﾞｰｼｯｸ', '1', key='aws_basic', enable_events=True),
     sg.Radio('AWSｽﾀﾝﾀﾞｰﾄﾞ', '1', key='aws_standard', enable_events=True),
     sg.Radio('AWSｱﾄﾞﾊﾞﾝｽﾄﾞ', '1', key='aws_advanced', enable_events=True)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='javaDetail', font=font)]
]

# プログラミングタブ
tabProgramming = [
    [sg.Radio('PHPⒷ', '1', key='php_basic', enable_events=True, font=curriculumFont),
     sg.Radio('PHPⒶ', '1', key='php_advance', enable_events=True, font=curriculumFont),
     sg.Radio('WordPress', '1', key='wordpress', enable_events=True, font=curriculumFont),
     sg.Radio('SQL1-2', '1', key='sql', enable_events=True, font=curriculumFont),
     sg.Radio('Python', '1', key='python_basic', enable_events=True, font=curriculumFont),
     sg.Radio('RPA', '1', key='rpa', enable_events=True, font=curriculumFont)],
    [sg.Radio('Android入門', '1', key='java_android_trial', enable_events=True, font=curriculumFont),
     sg.Radio('Android基礎', '1', key='java_android', enable_events=True, font=curriculumFont),
     sg.Radio('実践Java', '1', key='java_specialist', enable_events=True, font=curriculumFont)],        
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='programmingDetail', font=font)]
]

# オフィスタブ1
tabOffice = [
    [sg.Radio('W1-2', '1', key='word_basic', enable_events=True, font=curriculumFont),
     sg.Radio('W3-4', '1', key='word_advance', enable_events=True, font=curriculumFont),
     sg.Radio('E1-2', '1', key='excel_basic', enable_events=True, font=curriculumFont),
     sg.Radio('E3-4', '1', key='excel_advance', enable_events=True, font=curriculumFont),
     sg.Radio('PP1-2', '1', key='powerpoint_basic', enable_events=True, font=curriculumFont),
     sg.Radio('PP3-4', '1', key='powerpoint_advance', enable_events=True, font=curriculumFont),
     sg.Radio('AC1-2', '1', key='access_basic', enable_events=True, font=curriculumFont)],
    [sg.Radio('AC3-4', '1', key='access_advance', enable_events=True, font=curriculumFont),
     sg.Radio('Wﾏｽﾀ', '1', key='word_master_book', enable_events=True, font=curriculumFont),
     sg.Radio('ACｸｴﾘ', '1', key='access_query_utilization', enable_events=True, font=curriculumFont),
     sg.Radio('ACﾋﾞｼﾞ', '1', key='access_business', enable_events=True, font=curriculumFont),
     sg.Radio('伝提', '1', key='proposal', enable_events=True, font=curriculumFont),
     sg.Radio('伝提ﾄﾞﾘ', '1', key='proposal_drill', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetail', font=font)]
]

# オフィスタブ2
tabOfficeSecond = [
    [sg.Radio('ﾋﾟﾎﾞ実践', '1', key='pivot_tables', enable_events=True, font=curriculumFont),
     sg.Radio('Eﾏｽﾀ', '1', key='excel_master_book', enable_events=True, font=curriculumFont),
     sg.Radio('VBA', '1', key='skills_up_vba', enable_events=True, font=curriculumFont),
     sg.Radio('VBAⒶ', '1', key='vba_advanced', enable_events=True, font=curriculumFont),
     sg.Radio('ﾏｸﾛ実践', '1', key='macro_practice', enable_events=True, font=curriculumFont),
     sg.Radio('VBA実践', '1', key='vba_practice', enable_events=True, font=curriculumFont)],
    [sg.Radio('ﾊﾟﾜｰｸｴﾘ', '1', key='excel_power_query', enable_events=True, font=curriculumFont),
     sg.Radio('ﾊﾟﾜｰﾋﾟﾎﾞｯﾄ', '1', key='excel_power_pivot', enable_events=True, font=curriculumFont),
     sg.Radio('関2', '1', key='basic_function', enable_events=True, font=curriculumFont),
     sg.Radio('関3', '1', key='advance_function', enable_events=True, font=curriculumFont),
     sg.Radio('ｽｷﾙ関', '1', key='skill_function', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetailSecond', font=font)]
]

# オフィスタブ3
tabOfficeThird = [
    [sg.Radio('ﾃﾞｰﾀ分析', '1', key='data_analysis', enable_events=True, font=curriculumFont),        
     sg.Radio('仕事術(基)', '1', key='work_basic', enable_events=True, font=curriculumFont),
     sg.Radio('仕事術(応)', '1', key='work_application', enable_events=True, font=curriculumFont),
     sg.Radio('仕事術(経)', '1', key='work_accounting', enable_events=True, font=curriculumFont),
     sg.Radio('仕事術(管)', '1', key='work_administrator', enable_events=True, font=curriculumFont)],    
    [sg.Radio('ﾅﾚｯｼﾞW', '1', key='business_knowledge_word', enable_events=True, font=curriculumFont),
     sg.Radio('ﾅﾚｯｼﾞE', '1', key='business_knowledge_excel', enable_events=True, font=curriculumFont),
     sg.Radio('ﾅﾚｯｼﾞP', '1', key='business_knowledge_powerpoint', enable_events=True, font=curriculumFont),
     sg.Radio('ﾜｰｸW', '1', key='business_drill_word', enable_events=True, font=curriculumFont),
     sg.Radio('ﾜｰｸE', '1', key='business_drill_excel', enable_events=True, font=curriculumFont),
     sg.Radio('ﾜｰｸP', '1', key='business_drill_powerpoint', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetailThird', font=font)]
]

# オフィスタブ4
tabOfficeFourth = [
    [sg.Radio('W1', '1', key='generate_ai_word_level1', enable_events=True, font=curriculumFont),
     sg.Radio('W2', '1', key='generate_ai_word_level2', enable_events=True, font=curriculumFont),
     sg.Radio('W3', '1', key='generate_ai_word_level3', enable_events=True, font=curriculumFont),
     sg.Radio('W4', '1', key='generate_ai_word_level4', enable_events=True, font=curriculumFont),
     sg.Radio('E1', '1', key='generate_ai_excel_level1', enable_events=True, font=curriculumFont),
     sg.Radio('E2', '1', key='generate_ai_excel_level2', enable_events=True, font=curriculumFont),
     sg.Radio('E3', '1', key='generate_ai_excel_level3', enable_events=True, font=curriculumFont),
     sg.Radio('E4', '1', key='generate_ai_excel_level4', enable_events=True, font=curriculumFont)],
     [sg.Radio('PP1', '1', key='generate_ai_powerpoint_level1', enable_events=True, font=curriculumFont),
     sg.Radio('PP2', '1', key='generate_ai_powerpoint_level2', enable_events=True, font=curriculumFont),
     sg.Radio('PP3', '1', key='generate_ai_powerpoint_level3', enable_events=True, font=curriculumFont),
     sg.Radio('PP4', '1', key='generate_ai_powerpoint_level4', enable_events=True, font=curriculumFont),
     sg.Radio('forE', '1', key='ai_sw_for_excel_pw', enable_events=True, font=curriculumFont)],    
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='officeDetailFourth', font=font)]
]

# クリエイティブタブ1
tabCreative = [
    [sg.Radio('HTMLⒷ', '1', key='html_css_basic', enable_events=True, font=curriculumFont),
     sg.Radio('MEB1', '1', key='web_coding', enable_events=True, font=curriculumFont),
     sg.Radio('MEB2', '1', key='responsive_web_design', enable_events=True, font=curriculumFont),
     sg.Radio('HTMLﾄﾚｰﾆﾝｸﾞ', '1', key='html_css_training', enable_events=True, font=curriculumFont),
     sg.Radio('JSB', '1', key='java_script', enable_events=True, font=curriculumFont),
     sg.Radio('MEA', '1', key='web_coding_advance', enable_events=True, font=curriculumFont)],
    [sg.Radio('Ai1', '1', key='illustrator_cc2021_basic1', enable_events=True, font=curriculumFont),
     sg.Radio('Ai2', '1', key='illustrator_cc2021_basic2', enable_events=True, font=curriculumFont),
     sg.Radio('Ai3', '1', key='illustrator_cc2021_advance', enable_events=True, font=curriculumFont),
     sg.Radio('Ps1', '1', key='photoshop_cc2021_basic1', enable_events=True, font=curriculumFont),
     sg.Radio('Ps2', '1', key='photoshop_cc2021_basic2', enable_events=True, font=curriculumFont),
     sg.Radio('Ps3', '1', key='photoshop_cc2021_advanced', enable_events=True, font=curriculumFont),
     sg.Radio('ﾄﾞｷｭ', '1', key='design_document', enable_events=True, font=curriculumFont),
     sg.Radio('ﾊﾟｰﾂ', '1', key='parts_web', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='creativeDetail', font=font)]
]

# クリエイティブタブ2
tabCreativeSecond = [
    [sg.Radio('PrⒷ', '1', key='premiere_pro_basic', enable_events=True, font=curriculumFont),
     sg.Radio('AeⒷ', '1', key='after_effects_basic', enable_events=True, font=curriculumFont),
     sg.Radio('PrⓈ', '1', key='premiere_pro_standard', enable_events=True, font=curriculumFont),
     sg.Radio('PrⒺ', '1', key='effect_variations', enable_events=True, font=curriculumFont),
     sg.Radio('FireFly', '1', key='firefly', enable_events=True, font=curriculumFont),
     sg.Radio('ﾃﾞｻﾞｲﾝ', '1', key='create_design', enable_events=True, font=curriculumFont),
     sg.Radio('ﾚﾀｯﾁ', '1', key='retouching_processing', enable_events=True, font=curriculumFont)],
    [sg.Radio('Ai1(24)', '1', key='illustrator_cc2024_basic1', enable_events=True, font=curriculumFont),
     sg.Radio('Ai2(24)', '1', key='illustrator_cc2024_basic2', enable_events=True, font=curriculumFont),
     sg.Radio('Ai3(24)', '1', key='illustrator_cc2024_advanced', enable_events=True, font=curriculumFont),     
     sg.Radio('Ps1(24)', '1', key='photoshop_cc2024_basic1', enable_events=True, font=curriculumFont),
     sg.Radio('Ps2(24)', '1', key='photoshop_cc2024_basic2', enable_events=True, font=curriculumFont),
     sg.Radio('Ps3(24)', '1', key='photoshop_cc2024_advanced', enable_events=True, font=curriculumFont)],         
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='creativeDetailSecond', font=font)]
]

# クリエイティブタブ3
tabCreativeThird = [
    [sg.Radio('ﾍﾞｰｼｯｸ', '1', key='web_production_professional_basic', enable_events=True),
     sg.Radio('ｽﾀﾝﾀﾞｰﾄﾞ', '1', key='web_production_professional_standard', enable_events=True),
     sg.Radio('ｱﾄﾞﾊﾞﾝｽﾄﾞ', '1', key='web_production_professional_advanced', enable_events=True)],    
    [sg.Text('', size=(4, 1), font=font)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='creativeDetailThird', font=font)]
]

# CADタブ1
tabCad = [
    [sg.Radio('Auto1-2', '1', key='auto_cad_basic', enable_events=True, font=curriculumFont),
     sg.Radio('Auto3-4(建)', '1', key='auto_cad_advanced_architecture', enable_events=True, font=curriculumFont),
     sg.Radio('Auto3-4(機)', '1', key='auto_cad_advanced_mechanical', enable_events=True, font=curriculumFont),
     sg.Radio('Jw1-2', '1', key='jw_cad_basic', enable_events=True, font=curriculumFont),
     sg.Radio('Jw3-4', '1', key='jw_cad_advanced', enable_events=True, font=curriculumFont)],
    [sg.Radio('FusionⒷ', '1', key='fusion_basic', enable_events=True, font=curriculumFont),
     sg.Radio('FusionⒶ', '1', key='fusion_advance', enable_events=True, font=curriculumFont),
     sg.Radio('Auto建築製図', '1', key='architectural_draft', enable_events=True, font=curriculumFont),
     sg.Radio('Auto土木', '1', key='civil_engineering', enable_events=True, font=curriculumFont),
     sg.Radio('Revit', '1', key='revit_basic', enable_events=True, font=curriculumFont)],    
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='cadDetail', font=font)]
]

# CADタブ2
tabCadSecond = [
    [sg.Radio('AutoCADﾄﾚ', '1', key='auto_cad_basic_training', enable_events=True, font=curriculumFont),
     sg.Radio('建CAD3級(Auto)', '1', key='architecture_cad3', enable_events=True, font=curriculumFont),
     sg.Radio('建CAD3級(Jw)', '1', key='architecture_jw_cad3', enable_events=True, font=curriculumFont),
     sg.Radio('ﾕｰｻﾞ試験', '1', key='auto_cad_user', enable_events=True, font=curriculumFont)],
    [sg.Radio('CAD利用2級', '1', key='cad_engineer_2', enable_events=True),
     sg.Radio('建CAD2級(Auto)', '1', key='architecture_cad2', enable_events=True, font=curriculumFont),
     sg.Radio('建CAD2級(Jw)', '1', key='architecture_jw_cad2', enable_events=True, font=curriculumFont)],   
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='cadDetailSecond', font=font)]
]

# googleタブ
tabGoogle = [
    [sg.Radio('ChatGPTⓉ', '1', key='chatgpt_trial', enable_events=True, font=curriculumFont),
     sg.Radio('ChatGPTⒷ', '1', key='chatgpt_basic', enable_events=True, font=curriculumFont),
     sg.Radio('GAT', '1', key='gat', enable_events=True, font=curriculumFont),
     sg.Radio('GSS', '1', key='gss', enable_events=True, font=curriculumFont)], 
    [sg.Radio('GASⓉ', '1', key='gas_trial', enable_events=True, font=curriculumFont),
     sg.Radio('GASⒷ', '1', key='gas_basic', enable_events=True, font=curriculumFont),
     sg.Radio('GASⓈ', '1', key='gas_standard', enable_events=True, font=curriculumFont),
     sg.Radio('AppSheet', '1', key='appsheet_trial', enable_events=True, font=curriculumFont),
     sg.Radio('SaaS', '1', key='dx_course_it_basics', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='googleDetail', font=font)]
]

# エクスペアリンスタブ
tabExperience = [
    [sg.Radio('Illustrator', '1', key='illustrator_ex', enable_events=True, font=curriculumFont),
     sg.Radio('PhotoShop', '1', key='photoshop_ex', enable_events=True, font=curriculumFont),
     sg.Radio('AutoCAD', '1', key='autocad_ex', enable_events=True, font=curriculumFont),
     sg.Radio('jw_cad', '1', key='jw_cad_ex', enable_events=True, font=curriculumFont), 
     sg.Radio('Javaエンジニア', '1', key='java_ex', enable_events=True, font=curriculumFont)],
     [sg.Radio('Web制作プロ', '1', key='web_ex', enable_events=True, font=curriculumFont),
     sg.Radio('Excel', '1', key='excel_ex', enable_events=True, font=curriculumFont)],
    [sg.Text('挨拶', size=(4, 1), font=font),
     sg.Combo([], size=(150, 1), key='experienceDetail', font=font)]
]

# トラブルタブ
tabTrouble = [
    [sg.Text('カンパニー', size=(9, 1)),
     sg.Combo(list(school_options.keys()),size=(10, 1), key='unit', enable_events=True),
     sg.Text('校舎名', size=(5, 1)),
     sg.Combo([], size=(27, 1), key='schoolDetail')],
    [sg.Text('ID', size=(2, 1)),
     sg.InputText(size=(11, 1), font=font, key='studentId'),
     sg.Text('名前', size=(3, 1)),
     sg.InputText(size=(11, 1), font=font, key='studentName'),
     sg.Text('科目', size=(3, 1)),
     sg.InputText(size=(17, 1), font=font, key='studentCourse')],
    [sg.Radio('移動', '1', key='roomChange', enable_events=True),
     sg.Radio('不通', '1', key='audioFollow', enable_events=True),
     sg.Radio('退出', '1', key='exitConfirmation', enable_events=True),
     sg.Radio('不在', '1', key='notRoom', enable_events=True),
     sg.Radio('助けて', '1', key='helpMe', enable_events=True),
     sg.Radio('5分前', '1', key='fiveMinutes', enable_events=True),
     sg.Radio('2分前', '1', key='twoMinutes', enable_events=True)]
]
# 設定
def createSettingLayout():
    return[
        [sg.Checkbox('ｸﾘｴｲﾃｨﾌﾞ', key='chk_CR', enable_events=True),
         sg.Checkbox('Webﾌﾟﾛ', key='chk_WEB', enable_events=True),
        sg.Checkbox('CAD', key='chk_CD', enable_events=True)],
        [sg.Checkbox('ﾌﾟﾛｸﾞﾗﾐﾝｸﾞ', key='chk_PG', enable_events=True),
         sg.Checkbox('RaiseTech', key='chk_RT', enable_events=True)],
        [sg.Checkbox('ｴｸｽﾍﾟﾘｴﾝｽ', key='chk_EX', enable_events=True)],
        [sg.Button('OK', size=(10, 1), button_color=('white', '#001480')),
         sg.Button('CLEAR', size=(10, 1), button_color=('white', '#dc143c'))], 
    ]

col1 = [
    [sg.Checkbox('わかばROOM', key='wakaba', default=False),
    sg.Checkbox('初VU期間サポート対象', key='subject', default=False),
    sg.Spin(period, size=(2, 1), font=font, key='seven'),
    sg.Text('', size=(10, 1), font=font),
    sg.Text('Setting', key='openSetting', enable_events=True, text_color=sg.theme_text_color(), background_color=sg.theme_background_color())],
    [sg.Text('授業', size=(4, 1), font=font),
    sg.Spin(lis, size=(2, 1), font=font, key='jyugyou'),
    sg.Text('時限', size=(4, 1), font=font),
    sg.Spin(period, size=(2, 1), font=font, key='jigen'),
    sg.Text('Room', size=(5, 1), font=font),
    sg.Spin(lis, size=(3, 1), font=font, key='room'),
    sg.Text('', size=(1, 1), font=font),
    sg.Checkbox('アラーム分', key='alarmCheck', default=True),
    sg.Spin(timerSet, size=(2, 1), font=font, key='alarmSet', initial_value=3)],
    [sg.Checkbox('受講促進○', key='promotionTrue', default=False, size=(8, 1), font=font),
     sg.Checkbox('受講促進×', key='promotionFalse', default=False, size=(8, 1), font=font),
     sg.Checkbox('巡回不要', key='noFollow', default=False, size=(7, 1), font=font),
     sg.Checkbox('VUサポ対象者', key='vuTarget', default=False, size=(9, 1), font=font),
     sg.Checkbox('ExpS', key='experienceSupport', default=False, size=(9, 1), font=font)],
]

col2 =[
    sg.Button('COPY', size=(10, 1), key='COPY', button_color=('white', '#001480')),
    sg.Button('CODE', size=(10, 1), key='CODE', button_color=('white', '#001480')),
    sg.Button('CLEAR', size=(10, 1), key='CLEAR', button_color=('white', '#dc143c')),
    sg.Button('START', key='start_stop', size=(9, 1)),
    sg.Text('所要時間：', size=(7, 1), font=font),
    sg.Text('00:00', size=(7, 1), font=font, key='timer'),
]

# メインタブ
layout = [
    [col1],
    [sg.TabGroup([
        [sg.Tab('ACTION', tabAction, key='ACTION'), 
        sg.Tab('OF①', tabOffice, key='OF1'), 
        sg.Tab('OF②', tabOfficeSecond, key='OF2'),
        sg.Tab('OF③', tabOfficeThird, key='OF3'),
        sg.Tab('AI+', tabOfficeFourth, key='OF4'),
        sg.Tab('CR①', tabCreative, key='CR1', visible=False),
        sg.Tab('CR②', tabCreativeSecond, key='CR2', visible=False),
        sg.Tab('WEB+', tabCreativeThird, key='CR3', visible=False),
        sg.Tab('CD①', tabCad, key='CD1', visible=False),
        sg.Tab('CD②', tabCadSecond, key='CD2', visible=False),
        sg.Tab('GO', tabGoogle, key='GO'),
        sg.Tab('PG', tabProgramming, key='PG', visible=False),
        sg.Tab('RT', tabJava, key='RT', visible=False),
        sg.Tab('EX', tabExperience, key='EX', visible=False),
        sg.Tab('TR', tabTrouble, key='TR'),
        ]],
        key="tabgroup", enable_events=True, font=('Helvetica', 9))],
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
window = sg.Window('K_San v2504.02', layout, keep_on_top=True, size=(534, 304), resizable=True, icon=icon_path)

def get_greeting_data(values):
    data = ""
    if values['wakaba']:
        data += '☆'
    if values['subject']:
        data += f"【初VU期間サポート対象】{values['seven']}回目\n"
    data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
    data += f"挨拶:{values['greeting']}/\n注意事項:"
    if values['noFollow']:
        data += '★巡回不要　'
    if values['promotionTrue']:
        data += f'受講促進○ {now} {values["jigen"]}限　'
    if values['promotionFalse']:
        data += '受講促進×　'
    if values['vuTarget']:
        data += '■VUサポート対象者　'  
 
    data += f"\n{values['remarks']}" if values['noFollow'] or values['promotionTrue'] or values['promotionFalse'] else values['remarks']
       
    return data

def get_course_data(values, course_name, detail):
    data = ""
    if values['wakaba']:
        data += '☆'
    if values['subject']:
        data += f"【初VU期間サポート対象】{values['seven']}回目\n"
    data += f"{now}_{values['jyugyou']}_{values['jigen']}限_Room{values['room']}\n"
    data += f"挨拶:{course_name}　{values[detail]}/\n注意事項:"
    if values['noFollow']:
        data += '★巡回不要　'
    if values['promotionTrue']:
        data += f'受講促進○ {now} {values["jigen"]}限　'
    if values['promotionFalse']:
        data += '受講促進×　'
    if values['vuTarget']:
        data += '■VUサポート対象者　'  
        
    data += f"\n{values['remarks']}" if values['noFollow'] or values['promotionTrue'] or values['promotionFalse'] else values['remarks']

    return data

def play_alarm():
    try:
        absolute_path = resource_path('alarm.wav')
        print(f"Attempting to play sound from: {absolute_path}")
        pygame.mixer.music.load(absolute_path)
        pygame.mixer.music.set_volume(0.3)  # 音量を30%に設定
        pygame.mixer.music.play(loops=-1)  # ループ再生
        print("Sound playing successfully.")
    except pygame.error as e:
        print(f"Error playing sound: {e}")
        sg.popup('アラーム音の再生に失敗しました。PCのサウンド機能を確認してください。', button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

def open_setting_window(window):
    """設定タブを別ウィンドウで開く関数"""
    window_x, window_y = window.current_location()
    tabSetting = createSettingLayout()
    setting_window = sg.Window('Setting', tabSetting, location=(window_x+137, window_y+100), modal=True, keep_on_top=True, finalize=True, size=(260, 138),
                               resizable=True, icon=icon_path)
    
    if window['CR1'].visible:
        setting_window['chk_CR'].update(True)
    if window['CR3'].visible:
        setting_window['chk_WEB'].update(True)        
    if window['CD1'].visible:
        setting_window['chk_CD'].update(True)
    if window['PG'].visible:
        setting_window['chk_PG'].update(True)
    if window['RT'].visible:
        setting_window['chk_RT'].update(True)
    if window['EX'].visible:
        setting_window['chk_EX'].update(True)

    while True:
        event, values = setting_window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            break
        # タブとチェックボックスの対応関係を辞書で定義
        tab_visibility_mapping = {
            'chk_CR': ['CR1', 'CR2'],
            'chk_WEB': ['CR3'],
            'chk_CD': ['CD1', 'CD2'],
            'chk_PG': ['PG'],
            'chk_RT': ['RT'],
            'chk_EX': ['EX']
        }

        # ループでタブの表示/非表示を更新
        for chk, tabs in tab_visibility_mapping.items():
            for tab in tabs:
                window[tab].update(visible=values[chk])

        # "CLEAR"ボタンがクリックされたとき
        if event == 'CLEAR':
            setting_window['chk_CR'].update(False)
            setting_window['chk_WEB'].update(False)
            setting_window['chk_CD'].update(False)
            setting_window['chk_PG'].update(False)
            setting_window['chk_RT'].update(False)
            setting_window['chk_EX'].update(False)
            
            # チェックボックスの状態に基づいて可視性を更新
            for key in ['CR1', 'CR2', 'CR3', 'CD1', 'CD2', 'PG', 'RT', 'EX']:
                window[key].update(visible=False)
   
    setting_window.close()

def stop_alarm():
    pygame.mixer.music.stop()
    
# Pygame初期化の呼び出し
initialize_pygame()

# メイン処理
while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'openSetting':
        open_setting_window(window)
    
    # タブの選択イベント処理
    if event == 'tabgroup':
        selected_tab = window['tabgroup'].get()
        if selected_tab == 'ACTION':
            window['fast'].update(value=True)
            
    # Java コースの選択イベント
    if event in ('java_basic', 'old_java_basic', 'java_standard', 'java_advance', 'aws_basic', 'aws_standard', 'aws_advanced'):
        selected_type = event
        window['javaDetail'].update(values=java_course_options[selected_type])
        
    # プログラミング コースの選択イベント
    if event in ('php_basic', 'php_advance', 'wordpress', 'python_basic','java_android',
                 'java_android_trial','sql', 'rpa', 'java_specialist'):
        selected_type = event
        window['programmingDetail'].update(values=programming_course_options[selected_type])
        
    # オフィス コースの選択イベント
    if event in ('word_basic', 'word_advance', 'excel_basic', 'excel_advance', 'powerpoint_basic', 'powerpoint_advance',
                 'access_basic', 'access_advance', 'word_master_book', 'pivot_tables', 'excel_master_book', 'skills_up_vba', 'vba_advanced',
                 'macro_practice', 'vba_practice', 'excel_power_query', 'excel_power_pivot', 'access_query_utilization',
                 'access_business', 'proposal', 'proposal_drill', 'basic_function', 'advance_function', 'skill_function',
                 'business_knowledge_word', 'business_knowledge_excel', 'business_knowledge_powerpoint', 'data_analysis',
                 'work_basic', 'work_application', 'work_accounting', 'work_administrator','business_drill_word',
                 'business_drill_excel', 'business_drill_powerpoint',
                 'generate_ai_excel_level1', 'generate_ai_excel_level2', 'generate_ai_excel_level3', 'generate_ai_excel_level4',
                 'generate_ai_word_level1', 'generate_ai_word_level2', 'generate_ai_word_level3', 'generate_ai_word_level4',
                 'generate_ai_powerpoint_level1', 'generate_ai_powerpoint_level2', 'generate_ai_powerpoint_level3', 'generate_ai_powerpoint_level4',
                 'ai_sw_for_excel_pw'):
        selected_type = event
        window['officeDetail'].update(values=office_course_options[selected_type])
        window['officeDetailSecond'].update(values=office_course_options[selected_type])
        window['officeDetailThird'].update(values=office_course_options[selected_type])
        window['officeDetailFourth'].update(values=office_course_options[selected_type])        
    
    # クリエイティブ コースの選択イベント
    if event in ('html_css_basic', 'web_coding', 'responsive_web_design', 'html_css_training', 'java_script', 'web_coding_advance', 'parts_web',
                 'illustrator_cc2021_basic1', 'illustrator_cc2021_basic2', 'illustrator_cc2021_advance', 'photoshop_cc2021_basic1',
                 'photoshop_cc2021_basic2', 'photoshop_cc2021_advanced', 'firefly', 'design_document', 'premiere_pro_basic',
                 'after_effects_basic', 'premiere_pro_standard', 'effect_variations', 'illustrator_cc2024_basic1', 'illustrator_cc2024_basic2',
                 'photoshop_cc2024_basic1', 'photoshop_cc2024_basic2', 'create_design', 'retouching_processing', 'illustrator_cc2024_advanced', 'photoshop_cc2024_advanced',
                 'web_production_professional_basic', 'web_production_professional_standard', 'web_production_professional_advanced'):
        selected_type = event
        window['creativeDetail'].update(values=creative_course_options[selected_type])
        window['creativeDetailSecond'].update(values=creative_course_options[selected_type])
        window['creativeDetailThird'].update(values=creative_course_options[selected_type])
        
    # CAD コースの選択イベント
    if event in ('auto_cad_basic', 'auto_cad_advanced_architecture', 'auto_cad_advanced_mechanical', 'jw_cad_basic', 'jw_cad_advanced',
                 'fusion_basic', 'fusion_advance', 'architectural_draft', 'civil_engineering', 'auto_cad_basic_training', 'architecture_cad3',
                 'architecture_cad2', 'architecture_jw_cad2', 'cad_engineer_2', 'auto_cad_user', 'architecture_jw_cad3', 'revit_basic'):
        selected_type = event
        window['cadDetail'].update(values=cad_course_options[selected_type])
        window['cadDetailSecond'].update(values=cad_course_options[selected_type])
        
    # Google コースの選択イベント
    if event in ('chatgpt_trial','gat', 'gss', 'gas_trial', 'gas_basic', 'gas_standard','appsheet_trial', 'dx_course_it_basics',
                 'chatgpt_basic'):
        selected_type = event
        window['googleDetail'].update(values=google_course_options[selected_type])
        
    # エクスペリエンスチケット コースの選択イベント
    if event in ('illustrator_ex', 'photoshop_ex', 'autocad_ex', 'jw_cad_ex', 'java_ex', 'web_ex', 'excel_ex'):
        selected_type = event
        window['experienceDetail'].update(values=experience_ticket[selected_type])        
    
    # トラブル 校舎選択イベント
    if event == 'unit':
        selected_type = values['unit']
        if selected_type in school_options:
            window['schoolDetail'].update(values=school_options[selected_type])


    # COPY ボタンの処理
    if event == 'COPY':
        data = ""
        if values['fast']:
            data = get_greeting_data(values)
        elif values['help'] and values['alarmCheck']:
            data = f"ヘルプ対応:所要時間：{window['timer'].get()} {values['remarks']}"
        elif values['help']:
            data = f"ヘルプ対応:{values['remarks']}"
        elif values['follow']:
            data = f"フォロー対応:{values['remarks']}"
            
            
        # G3専用アドバイスコマンド    
        # elif values['adviceHelp'] and values['alarmCheck']:
        #     data = f"ヘルプ対応:所要時間：{window['timer'].get()} !▲ {values['remarks']} ▲!"
        # elif values['adviceHelp']:
        #     data = f"ヘルプ対応:!▲ {values['remarks']} ▲!"               
        # elif values['adviceFollow']:
        #     data = f"フォロー対応:!▲ {values['remarks']} ▲!"
            
                        
        elif values['cs']:
            data = f"【面談依頼】\n内容：{values['remarks']}"
        elif values['vu']:
            data = f"【VUサポート】\n内容：{values['remarks']}"
        elif values['fastVu']:
            data = f"【初VU期間サポート】{values['seven']}回目\nヘルプ：0回　フォロー：0回\n内容：{values['remarks']}"
        elif values['nextTest']:
            data = "【次回定着テスト】"
        elif values['testExecution']:
            data = "【定着テスト実施】"              
            
        # Javaエンジニアタブ作成
        if values['java_basic']:
            data = get_course_data(values, 'Javaエンジニア ベーシック', 'javaDetail')
        elif values['old_java_basic']:
            data = get_course_data(values, 'Javaエンジニア 旧版_ベーシック', 'javaDetail')
        elif values['java_standard']:
            data = get_course_data(values, 'Javaエンジニア スタンダード', 'javaDetail')
        elif values['java_advance']:
            data = get_course_data(values, 'Javaエンジニア アドバンスド', 'javaDetail')
        elif values['aws_basic']:
            data = get_course_data(values, 'AWS ベーシック', 'javaDetail')
        elif values['aws_standard']:
            data = get_course_data(values, 'AWS スタンダード', 'javaDetail')
        elif values['aws_advanced']:
            data = get_course_data(values, 'AWS アドバンスド', 'javaDetail')                        
            
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
            data = get_course_data(values, 'RPA講座ベーシック', 'programmingDetail')
        elif values['java_specialist']:
            data = get_course_data(values, '実践Java技術者試験', 'programmingDetail')            

               
        # オフィスタブ1作成    
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
        elif values['word_master_book']:
            data = get_course_data(values, 'Wordマスターブック', 'officeDetail')    
        elif values['access_query_utilization']:
            data = get_course_data(values, 'Accessクエリ活用', 'officeDetail')
        elif values['access_business']:
            data = get_course_data(values, 'Accessビジネス活用', 'officeDetail')
        elif values['proposal']:
            data = get_course_data(values, '伝わる提案書', 'officeDetail')
        elif values['proposal_drill']:
            data = get_course_data(values, '伝わる提案書（ドリル）', 'officeDetail')
            
        # オフィスタブ2作成     
        elif values['pivot_tables']:
            data = get_course_data(values, 'ピボット実践', 'officeDetailSecond')            
        elif values['excel_master_book']:
            data = get_course_data(values, 'Excelマスターブック', 'officeDetailSecond')
        elif values['skills_up_vba']:
            data = get_course_data(values, 'スキルアップVBA', 'officeDetailSecond')                  
        elif values['vba_advanced']:
            data = get_course_data(values, 'VBAアドバンスド', 'officeDetailSecond')                  
        elif values['macro_practice']:
            data = get_course_data(values, 'マクロ実践', 'officeDetailSecond')                  
        elif values['vba_practice']:
            data = get_course_data(values, 'VBA実践', 'officeDetailSecond')                  
        elif values['excel_power_query']:
            data = get_course_data(values, 'Excelパワークエリ', 'officeDetailSecond')                              
        elif values['excel_power_pivot']:
            data = get_course_data(values, 'Excelパワーピボット', 'officeDetailSecond')
        elif values['basic_function']:
            data = get_course_data(values, 'ベーシックExcel関数実践', 'officeDetailSecond')                  
        elif values['advance_function']:
            data = get_course_data(values, 'アドバンスExcel関数実践', 'officeDetailSecond')                              
        elif values['skill_function']:
            data = get_course_data(values, 'スキルアップExcel関数実践', 'officeDetailSecond')
            
        # オフィスタブ3作成     
        elif values['business_knowledge_word']:
            data = get_course_data(values, 'ビジネスナレッジブックWord', 'officeDetailThird')            
        elif values['business_knowledge_excel']:
            data = get_course_data(values, 'ビジネスナレッジブックExcel', 'officeDetailThird')
        elif values['business_knowledge_powerpoint']:
            data = get_course_data(values, 'ビジネスナレッジブックPowerPoint', 'officeDetailThird')
        elif values['business_drill_word']:
            data = get_course_data(values, 'ビジネス活用ドリルWord', 'officeDetailThird')            
        elif values['business_drill_excel']:
            data = get_course_data(values, 'ビジネス活用ドリルExcel', 'officeDetailThird')
        elif values['business_drill_powerpoint']:
            data = get_course_data(values, 'ビジネス活用ドリルPowerPoint', 'officeDetailThird')                              
        elif values['data_analysis']:
            data = get_course_data(values, 'Excelデータ分析', 'officeDetailThird')                  
        elif values['work_basic']:
            data = get_course_data(values, 'Excel仕事術≪基本編≫', 'officeDetailThird')                  
        elif values['work_application']:
            data = get_course_data(values, 'Excel仕事術≪応用編≫', 'officeDetailThird')                  
        elif values['work_accounting']:
            data = get_course_data(values, 'Excel仕事術≪経理実務編≫', 'officeDetailThird')                
        elif values['work_administrator']:
            data = get_course_data(values, 'Excel仕事術≪管理者実務編≫', 'officeDetailThird')
            
        # AIタブ作成 
        elif values['generate_ai_word_level1']:
            data = get_course_data(values, '生成AI活用 Word Lv1', 'officeDetailFourth')            
        elif values['generate_ai_word_level2']:
            data = get_course_data(values, '生成AI活用 Word Lv2', 'officeDetailFourth')
        elif values['generate_ai_word_level3']:
            data = get_course_data(values, '生成AI活用 Word Lv3', 'officeDetailFourth')
        elif values['generate_ai_word_level4']:
            data = get_course_data(values, '生成AI活用 Word Lv4', 'officeDetailFourth')
        elif values['generate_ai_excel_level1']:
            data = get_course_data(values, '生成AI活用 Excel Lv1', 'officeDetailFourth')            
        elif values['generate_ai_excel_level2']:
            data = get_course_data(values, '生成AI活用 Excel Lv2', 'officeDetailFourth')
        elif values['generate_ai_excel_level3']:
            data = get_course_data(values, '生成AI活用 Excel Lv3', 'officeDetailFourth')
        elif values['generate_ai_excel_level4']:
            data = get_course_data(values, '生成AI活用 Excel Lv4', 'officeDetailFourth')                            
        elif values['generate_ai_powerpoint_level1']:
            data = get_course_data(values, '生成AI活用 PowerPoint Lv1', 'officeDetailFourth')            
        elif values['generate_ai_powerpoint_level2']:
            data = get_course_data(values, '生成AI活用 PowerPoint Lv2', 'officeDetailFourth')
        elif values['generate_ai_powerpoint_level3']:
            data = get_course_data(values, '生成AI活用 PowerPoint Lv3', 'officeDetailFourth')
        elif values['generate_ai_powerpoint_level4']:
            data = get_course_data(values, '生成AI活用 PowerPoint Lv4', 'officeDetailFourth')
        elif values['ai_sw_for_excel_pw']:
            data = get_course_data(values, 'AI for Excel＜プロワーカー編＞', 'officeDetailFourth')
                             
                        
        #　クリエイティブタブ1作成    
        elif values['html_css_basic']:
            data = get_course_data(values, 'HTML/CSSベーシック', 'creativeDetail')
        elif values['web_coding']:
            data = get_course_data(values, 'マークアップEBパート1(WEB)', 'creativeDetail')
        elif values['responsive_web_design']:
            data = get_course_data(values, 'マークアップEBパート2(レスポンシブ)', 'creativeDetail')
        elif values['html_css_training']:
            data = get_course_data(values, 'HTML/CSSトレーニングブック～運用・更新編～', 'creativeDetail')
        elif values['java_script']:
            data = get_course_data(values, 'JavaScriptベーシック', 'creativeDetail')
        elif values['web_coding_advance']:
            data = get_course_data(values, 'マークアップエンジニア アドバンス', 'creativeDetail')             
        elif values['illustrator_cc2021_basic1']:
            data = get_course_data(values, 'Illustratorベーシック1', 'creativeDetail')
        elif values['illustrator_cc2021_basic2']:
            data = get_course_data(values, 'Illustratorベーシック2', 'creativeDetail')
        elif values['illustrator_cc2021_advance']:
            data = get_course_data(values, 'Illustratorアドバンス', 'creativeDetail')
        elif values['photoshop_cc2021_basic1']:
            data = get_course_data(values, 'Photoshopベーシック1', 'creativeDetail')
        elif values['photoshop_cc2021_basic2']:
            data = get_course_data(values, 'Photoshopベーシック2', 'creativeDetail')
        elif values['photoshop_cc2021_advanced']:
            data = get_course_data(values, 'Photoshopアドバンス', 'creativeDetail')            
        elif values['design_document']:
            data = get_course_data(values, 'デザインで差をつけるドキュメント作成講座', 'creativeDetail')
        elif values['parts_web']:
            data = get_course_data(values, 'パーツで魅せるWEB素材作成講座', 'creativeDetail')                 
                 
        #　クリエイティブタブ2作成 
        elif values['premiere_pro_basic']:
            data = get_course_data(values, 'PremiereProベーシック', 'creativeDetailSecond')
        elif values['after_effects_basic']:
            data = get_course_data(values, 'AfterEffectsベーシック', 'creativeDetailSecond')
        elif values['premiere_pro_standard']:
            data = get_course_data(values, 'PremiereProスタンダード', 'creativeDetailSecond')
        elif values['effect_variations']:
            data = get_course_data(values, 'PremiereProスタンダード～エフェクトバリエーション～', 'creativeDetailSecond')
        elif values['firefly']:
            data = get_course_data(values, 'AdobeFireflyトライアル', 'creativeDetailSecond')
        elif values['illustrator_cc2024_basic1']:
            data = get_course_data(values, 'Illustrator(2024)ベーシック1', 'creativeDetailSecond')
        elif values['illustrator_cc2024_basic2']:
            data = get_course_data(values, 'Illustrator(2024)ベーシック2', 'creativeDetailSecond')
        elif values['illustrator_cc2024_advanced']:
            data = get_course_data(values, 'Illustrator(2024)アドバンス', 'creativeDetailSecond')                        
        elif values['photoshop_cc2024_basic1']:
            data = get_course_data(values, 'Photoshop(2024)ベーシック1', 'creativeDetailSecond')
        elif values['photoshop_cc2024_basic2']:
            data = get_course_data(values, 'Photoshop(2024)ベーシック2', 'creativeDetailSecond')
        elif values['photoshop_cc2024_advanced']:
            data = get_course_data(values, 'Photoshop(2024)アドバンス', 'creativeDetailSecond')                        
        elif values['create_design']:
            data = get_course_data(values, 'Illustrator & Photoshop デザインの作り方', 'creativeDetailSecond')
        elif values['retouching_processing']:
            data = get_course_data(values, 'Photoshop レタッチ・加工', 'creativeDetailSecond')
            
        #　クリエイティブタブ3作成 
        elif values['web_production_professional_basic']:
            data = get_course_data(values, 'Web制作プロフェッショナル ベーシック', 'creativeDetailThird')
        elif values['web_production_professional_standard']:
            data = get_course_data(values, 'Web制作プロフェッショナル スタンダード', 'creativeDetailThird')
        elif values['web_production_professional_advanced']:
            data = get_course_data(values, 'Web制作プロフェッショナル アドバンスド', 'creativeDetailThird')

        #　CADタブ1作成
        elif values['auto_cad_basic']:
            data = get_course_data(values, 'AutoCADベーシック', 'cadDetail')
        elif values['auto_cad_advanced_architecture']:
            data = get_course_data(values, 'AutoCADアドバンス（建築）', 'cadDetail')
        elif values['auto_cad_advanced_mechanical']:
            data = get_course_data(values, 'AutoCADアドバンス（機械）', 'cadDetail')
        elif values['jw_cad_basic']:
            data = get_course_data(values, 'Jw_cadベーシック', 'cadDetail')
        elif values['jw_cad_advanced']:
            data = get_course_data(values, 'Jw_cadアドバンス', 'cadDetail')
        elif values['fusion_basic']:
            data = get_course_data(values, 'Fusionベーシック', 'cadDetail')
        elif values['fusion_advance']:
            data = get_course_data(values, 'Fusionアドバンス', 'cadDetail')
        elif values['architectural_draft']:
            data = get_course_data(values, 'AutoCAD建築製図編', 'cadDetail')                       
        elif values['civil_engineering']:
            data = get_course_data(values, 'AutoCAD土木編', 'cadDetail')
        elif values['revit_basic']:
            data = get_course_data(values, 'Revitベーシック講座', 'cadDetail')

            
        #　CADタブ2作成
        elif values['auto_cad_basic_training']:
            data = get_course_data(values, 'AutoCAD版トレーニングプラス講座', 'cadDetailSecond')
        elif values['architecture_cad3']:
            data = get_course_data(values, '建築CAD検定3級(AutoCAD)', 'cadDetailSecond')
        elif values['architecture_jw_cad3']:
            data = get_course_data(values, '建築CAD検定3級(jw_cad)', 'cadDetailSecond')
        elif values['architecture_cad2']:
            data = get_course_data(values, '建築CAD検定2級(AutoCAD)', 'cadDetailSecond')
        elif values['architecture_jw_cad2']:
            data = get_course_data(values, '建築CAD検定2級(jw_cad)', 'cadDetailSecond')            
        elif values['cad_engineer_2']:
            data = get_course_data(values, 'CAD利用技術者試験2級対策', 'cadDetailSecond')
        elif values['auto_cad_user']:
            data = get_course_data(values, 'AutoCADユーザー対策講座', 'cadDetailSecond')
            
        #　googleタブ作成
        elif values['chatgpt_trial']:
            data = get_course_data(values, 'ChatGPTトライアル', 'googleDetail')
        elif values['chatgpt_basic']:
            data = get_course_data(values, 'ChatGPTベーシック', 'googleDetail')                
        elif values['gat']:
            data = get_course_data(values, 'Googleアプリトライアル', 'googleDetail')
        elif values['gss']:
            data = get_course_data(values, 'Googleスプレッドシートスタンダード', 'googleDetail')
        elif values['gas_trial']:
            data = get_course_data(values, 'GASトライアル', 'googleDetail')
        elif values['gas_basic']:
            data = get_course_data(values, 'GASベーシック', 'googleDetail')
        elif values['gas_standard']:
            data = get_course_data(values, 'GASスタンダード', 'googleDetail')
        elif values['appsheet_trial']:
            data = get_course_data(values, 'AppSheetトライアル', 'googleDetail')
        elif values['dx_course_it_basics']:
            data = get_course_data(values, 'DX推進講座～Salesforce IT基礎編～', 'googleDetail')
            
        # EXタブ作成    
        elif values['illustrator_ex']:
            data = get_course_data(values, 'Illustrator エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['illustrator_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['illustrator_ex'][selected_session]}"
                    
        elif values['photoshop_ex']:
            data = get_course_data(values, 'Photoshop エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['photoshop_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['photoshop_ex'][selected_session]}"
                    
        elif values['autocad_ex']:
            data = get_course_data(values, 'AutoCAD エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['autocad_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['autocad_ex'][selected_session]}"
                          
        elif values['jw_cad_ex']:
            data = get_course_data(values, 'Jw_cad エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['jw_cad_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['jw_cad_ex'][selected_session]}"
                    
        elif values['java_ex']:
            data = get_course_data(values, 'Javaエンジニア エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['java_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['java_ex'][selected_session]}"
                    
        elif values['web_ex']:
            data = get_course_data(values, 'Web制作プロフェッショナル エクスペリエンスチケット', 'experienceDetail')  
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['web_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['web_ex'][selected_session]}"
                    
        elif values['excel_ex']:
            data = get_course_data(values, 'Excel エクスペリエンスチケット', 'experienceDetail')
            if values['experienceSupport']:
                selected_session = values['experienceDetail']
                if selected_session and selected_session in experience_support['excel_ex']:
                    data = f"【VUサポート】\n内容：{experience_support['excel_ex'][selected_session]}" 
  
                   
        #　トラブルタブ作成
        elif values['roomChange']:
            data = f"【Room移動依頼】\n{values['studentId']}　{values['studentName']} 様\n科目が{values['studentCourse']}です。Room移動許可をお願いします。"
        elif values['audioFollow']:
            data = f"【音声確認依頼】\n{values['studentId']}　{values['studentName']} 様\n音声がつながりません。フォローお願いします。"
        elif values['exitConfirmation']:
            data = f"【退出確認依頼】\n{values['studentId']}　{values['studentName']} 様\nRoomから退出されています。フォローお願いします。"            
        elif values['notRoom']:
            data = f"【出席確認依頼】\n{values['studentId']}　{values['studentName']} 様\nステータスが出席ですがRoomにいません。フォローお願いします。"
        elif values['helpMe']:
            data = f"Room{values['jyugyou']}\nROOMが回っていません。助けてください！"
        elif values['fiveMinutes']:
            data = (
                "受講中の皆様へご連絡です。\n"
                "授業終了5分前となりました。\n"
                "終了2分前になりましたら、皆様をメインルームにお戻しします。\n"
                "キリの良いところで保存などの終了準備を行ってください。"
            )
        elif values['twoMinutes']:
            data = (
                "受講中に失礼いたします。\n"
                "授業終了2分前となりました。\n"
                "これより皆様をメインルームにお戻し致します。\n"
                "自動的にメインルームに戻りますので、そのままお待ちください。"
            )

                     
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
    if event == 'CLEAR':
        timer_running = False
        start_time = 0
        window['timer'].update('00:00')
        window['start_stop'].update('START')
        window['timer'].update(font=font, text_color='black')  # テキストの色とフォントをリセット
        stop_alarm()
        alarm_playing = False
        
    # アラーム再生
    if values is not None:
        if timer_running:
            elapsed_time = time.time() - start_time
            window['timer'].update(time.strftime('%M:%S', time.gmtime(elapsed_time)))
            if elapsed_time >= values['alarmSet'] * 60 and not alarm_playing and values['alarmCheck']:
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
        window['vuTarget'].update(False)
        window['experienceSupport'].update(False)
        
        if values['wakaba']:
            window['javaDetail'].update('')
            window['programmingDetail'].update('')
            window['creativeDetail'].update('')
            window['creativeDetailSecond'].update('')
            window['creativeDetailThird'].update('')
            window['googleDetail'].update('')
            window['officeDetail'].update('')
            window['officeDetailSecond'].update('')
            window['officeDetailThird'].update('')            
            window['cadDetail'].update('')
            window['cadDetailSecond'].update('')
            window['schoolDetail'].update('')
            window['unit'].update('')            
            window['studentId'].update('')
            window['studentName'].update('')
            window['studentCourse'].update('')            

            
        else:
            window['javaDetail'].update('')
            window['programmingDetail'].update('')
            window['creativeDetail'].update('')
            window['creativeDetailSecond'].update('')
            window['creativeDetailThird'].update('')            
            window['googleDetail'].update('')
            window['officeDetail'].update('')
            window['officeDetailSecond'].update('')
            window['officeDetailThird'].update('')            
            window['cadDetail'].update('')
            window['cadDetailSecond'].update('')
            window['schoolDetail'].update('')
            window['unit'].update('')
            window['studentId'].update('')
            window['studentName'].update('')
            window['studentCourse'].update('')            
            window['subject'].update(False)

        if any(values[key] for key in (
            'java_basic', 'old_java_basic', 'java_standard', 'java_advance',
            'php_basic', 'php_advance', 'wordpress', 'python_basic', 'java_android', 
            'java_android_trial', 'sql', 'rpa', 'java_specialist', 'word_basic', 
            'word_advance', 'excel_basic', 'excel_advance', 'powerpoint_basic', 
            'powerpoint_advance', 'access_basic', 'access_advance', 'pivot_tables', 
            'excel_master_book', 'skills_up_vba', 'vba_advanced', 'macro_practice', 
            'vba_practice', 'excel_power_query', 'excel_power_pivot', 
            'access_query_utilization', 'access_business', 'proposal', 
            'proposal_drill', 'basic_function', 'advance_function', 
            'skill_function', 'business_knowledge_word', 
            'business_knowledge_excel', 'business_knowledge_powerpoint', 
            'business_drill_word', 'business_drill_excel', 
            'business_drill_powerpoint', 'data_analysis', 'work_basic', 
            'work_application', 'work_accounting', 'work_administrator', 
            'html_css_basic', 'web_coding', 'responsive_web_design', 
            'html_css_training', 'java_script', 'web_coding_advance', 'parts_web', 
            'illustrator_cc2021_basic1', 'illustrator_cc2021_basic2', 
            'illustrator_cc2021_advance', 'photoshop_cc2021_basic1', 
            'photoshop_cc2021_basic2', 'photoshop_cc2021_advanced', 'firefly', 
            'design_document', 'premiere_pro_basic', 'after_effects_basic', 
            'premiere_pro_standard', 'effect_variations', 'illustrator_cc2024_basic1', 
            'illustrator_cc2024_basic2', 'photoshop_cc2024_basic1', 
            'photoshop_cc2024_basic2', 'create_design', 'retouching_processing', 
            'auto_cad_basic', 'auto_cad_advanced_architecture', 
            'auto_cad_advanced_mechanical', 'jw_cad_basic', 'jw_cad_advanced', 
            'fusion_basic', 'fusion_advance', 'architectural_draft', 
            'civil_engineering', 'auto_cad_basic_training', 'architecture_cad3', 
            'architecture_cad2', 'architecture_jw_cad2', 'cad_engineer_2', 
            'auto_cad_user', 'chatgpt_trial', 'gat', 'gss', 'gas_trial', 
            'gas_basic', 'gas_standard', 'appsheet_trial','word_master_book', 
            'illustrator_cc2024_advanced', 'photoshop_cc2024_advanced', 'web_production_professional_basic',
            'dx_course_it_basics', 'chatgpt_basic', 'web_production_professional_standard', 'architecture_jw_cad3',
            'revit_basic', 'web_production_professional_advanced',
            'generate_ai_excel_level1', 'generate_ai_excel_level2', 'generate_ai_excel_level3', 'generate_ai_excel_level4',
            'generate_ai_word_level1', 'generate_ai_word_level2', 'generate_ai_word_level3', 'generate_ai_word_level4',
            'generate_ai_powerpoint_level1', 'generate_ai_powerpoint_level2', 'generate_ai_powerpoint_level3', 'generate_ai_powerpoint_level4',
            'illustrator_ex', 'photoshop_ex', 'autocad_ex', 'jw_cad_ex', 'java_ex', 'web_ex', 'excel_ex', 'aws_basic', 'aws_standard', 'aws_advanced',
            'ai_sw_for_excel_pw'
        )):

            window['fast'].update(True)
            window['tabgroup'].Widget.select(0)

window.close()
pygame.mixer.quit()
