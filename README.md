仮想環境作成
プロジェクト直下に移動後、以下のコマンドを実行するとプロジェクト内に指定した仮想環境名のフォルダが作成されます。
venvと命名されることがよくあるので、迷ったらpython -m venv venvで大丈夫です。

python -m venv [仮想環境名]


仮想環境のアクティベート
次に、以下のコマンドを使って仮想環境をアクティベートします。
Linux, MacとWindowsでディレクトリ構成とコマンドが若干違うため分けて紹介します。

.\[仮想環境名]\Scripts\activate







・仮想環境のアクティベート
C:\Users\R1912-C350001-0131\kita\Scripts\activate


pyinstaller K_San.py --noconsole --icon=128_04.ico

・PySimpleGUIがバージョン5から有償化されたため、バージョン4の最新版にダウングレード
pip install PySimpleGUI==4.60.5
