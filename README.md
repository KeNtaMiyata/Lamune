# README
---
## News
- 2022/08/03 launch this project
- 2022/08/04 create db
-            create problem CRUD and boostrap


---
## About

- 自作問題を投稿して、自分で解く
- 忘却曲線に従って計画的に再度解く
- 以上の作業を効率化するためのアプリ


---
## Function

- ログイン機能
- 問題投稿機能（CRUD機能）
- 時間を記録
- 「今日の問題」ページ
- 忘却曲線に従って今日の問題を表示
- 正答したか誤答したか
- 自動ログアウト機能

- ログインしなかった時の対処（問題を解かなかった）


- 問題ごとにモード選択（暗記、記述）機能
- 暗記のときは指定した個所を黒く塗りつぶして表示


---
## Detail

---
## Security

---
## MileStone
- deadline: 2022/8/15(2week)

1. databaseの作成 (8/4)
1. 一覧ページの作成(index.html)(8/4)
1. 問題を入力して一覧ページに表示させる(8/4)
1. 問題を編集可能(8/4)
1. 問題を削除可能(8/4)
1. flask runの自動更新機能(8/5)
    ```
    terminal

    flask run --debugger --reload
    ```
    - or
    ```
    app.py

    # Ensure templates are auto-reloaded
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    ```
1. ログイン(8/6)
1. apologyの完成(8/10)
1. top ページ(8/10)
1. indexページの長い文章を少しだけ表示させる機能(8/10)
1. mypageページ 自分が作った問題だけを表示させる(8/10)
1. 問題の詳細ページ(show.html)(8/10)
1. showへのリンク　（8/10）
1. try ページ(問題を解く所)（showから飛べるように）
1. 忘却曲線の関数
1. nav bar
1. indexの行ごとにshowへのリンクをつけるjquery
1. passwordへのセキュリティ
    - ソルト、ハッシュ、ストレッチング
1. ...


---
## For

- 資格の勉強
- cs50 finalproject(personal)

---
## Language

- Flask
- python
- SQLite
- html/css
- javascript

---
this project is 
