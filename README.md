# 一個簡單的縮址服務
https://flask-demo-project.herokuapp.com/
## 簡介

提供一個簡單的網頁讓使用者可以輸入將網址縮短，並且輸入該縮址後可以自動跳轉到原本的網址

## 系統架構
* 前端頁面 - templates/MainPage
* 後面API Service - main.py
* Heroku 平台設定檔 - Procfile requirements.txt
* Sqlite Datebase - test.db

## 前端介面
**由兩個表單構成**
* 一個將要縮的網址透過POST method 送至後端API - **/makeItShorte** 去產生縮址
* 另一個則是將輸入的縮址透過POST method 送至後端API - **/previewURL** 去查詢導向的網址

## 後端服務
**本服務後端API使用flask構成，負責處理前端送過來的需求**
**API 分為四部分**
* **"/"** - 負責將前端頁面透過Flask API render出來
* **"/previewURL"** - 查詢編碼出來的短網址
* **"/makeItShorter"** - 負責將網址編碼為短網址
* **"/<url_key>**" - 負責透過短網址從DB撈出原本的網址，並重新導向該網址

## 縮址的編碼原理

**將網址存進DB時會產生一個為一個數字ID，再將ID透過BASE62轉成62進位，再將每一位數字透過查表的方式轉換為[0-9|a-z|A-Z]某個字元**


**P.S. 本服務架設在Heroku平台，若此服務許久未使用，進入服務前會需要約30秒左右的時間讓平台重啟服務**
