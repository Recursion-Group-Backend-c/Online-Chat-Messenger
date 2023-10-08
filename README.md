# Online-Chat-Messenger
RecursionCSのBackendProject2_Online-Chat-Messengerのリポジトリーになります。

## 概要
クライアントとサーバー間でTCP/UDP通信を行い、オンラインチャットメッセンジャーというアプリを実現しています。

このアプリは、リアルタイムでのグループチャットを手軽に行うことができます。

TCPとUDPの役割は下記になります。

- TCP : 新規チャットルームの作成または既存のチャットルームへ参加します
- UDP : チャットルーム内のユーザー同士でメッセージを送受信しやり取りを行います

### TCP
- headerについて
  
  下記バイト表のような、TCPR(カスタムプロトコル)をクライアントとサーバで送受信しています
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/4b4d1b4b-6f44-4cc9-b9e8-a5eb51ad23b6)

![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/5e64ee4f-0de0-4a62-b0d8-d4128ecf64f7)

- 取りうるパターン

  クライアントとサーバ間では下記のようなパターンを想定しプログラムを作成しています
  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/09958ce5-7c35-46d3-bbd5-e8573ece3eb6)

- パターン図
  
  "取りうるパターン"のクライアントとサーバ間のイメージは下記のようになります
  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/dbdbb58f-ccab-432b-b56c-a13d189f12c7)

  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/3b21b51d-8826-4734-a168-7e06db81b269)

  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/5ae0fbd8-6667-4f22-8cea-1c7467b45533)

### UDP
- クライアントからサーバに送信するパケット

  仕様をもとに必要なデータを整理した結果、下記のデータをパケットとして送信することとしました
  - 4096バイト(↓内訳)
    - token : 32byte
    - user_name : 255byte
    - message : 3,809byte
      
  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/f2c21db9-7f2c-4163-9db5-707f19f1dd83)

- サーバからクライアントに送信するパケット

  仕様をもとに必要なデータを整理した結果、下記のデータをパケットとして送信することとしました
  - 4092バイト(↓内訳)
    - user_name : 255byte
    - message : 3,839byte

- リレーシステム削除

  リレーシステムから削除されるパターンは2通りあり、下記イメージの灰色を削除する形になります

  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/68230232-8fd6-400a-883f-05cc453c912a)  

- チャットルームの有効期間
  
  チャットルームはホストが退出することにより自動的に閉じられます

  パターンは2通りあります

  ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/f8eb2b56-6173-41ba-a1bb-29d606dbb446)
  
## 使用方法
### client
>python3 client.py

### server
>python3 server.py

### 手順
1. このリポジトリをクローンする
2. ターミナルを起動し"server"のコマンドを入力する
   ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/e982a01d-2a6a-48db-a0ec-fc82dab61b7f)
3. ターミナルを起動し"client"のコマンドを入力する
   ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/e65e456a-0e38-40f9-8a30-0468c1a12205)
4. client側のターミナルの指示に従い入力していく
   ![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/1d3e217a-3527-40f7-9204-7485c956f074)
5. ターミナルに"Chat start!"と表示されたらメッセージを入力する
6. 手順3~手順6をチャットしたいuserの数だけ繰り返しルームの作成またはルームに参加する
