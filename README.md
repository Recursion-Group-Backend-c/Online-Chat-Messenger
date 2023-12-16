# Online-Chat-Messenger

## 🌱概要
グループチャットができるアプリケーション

## ✨デモ
![output](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/ac773301-d79c-4e7b-9ca3-df7c9fb2f0e3)

## 📝説明
このアプリケーションは、グループチャットができるアプリケーションです。

グループチャットができるアプリケーションと言えば、日本ではLINEやKakaoTalkなどが有名ですね。

このアプリケーションでは、例に挙げたアプリケーションのメイン機能であるリアルタイムでのグループチャットを楽しむことができます!

アプリケーションは簡単に起動でき、友達を招待してすぐにグループチャットを始めることができます。

アプリケーションの実行には、ターミナルという黒い画面にコマンドを入力します。

基本的な機能として、チャットルームの作成/ユーザー同士でのグループチャットができます。

### 補足
#### 用語集
[説明](#説明)で登場する用語について補足します。

用語の意味がわからない時は、下記表を確認してください。

| 用語 | 意味 |
| ------- | ------- |
| ターミナル | コンピュータに対してテキストベースのコマンド入力と出力を行うインターフェースのことです。<br>このインターフェースは、コマンドラインインターフェース（CLI）とも呼ばれます。<br>[デモ](#デモ)で表示されている黒い画面のことです。 |
| コマンド | コンピュータに対して特定の操作を実行するよう指示するテキストベースの命令です。<br>コマンドを入力することで、コンピュータは、コマンドの意味を読み取りアクションをおこします。 |

## 🧰前提条件
このアプリケーションを実行するには、下記ソフトウェアを事前にインストールしておく必要があります。

インストールされていない場合は、[インストール](#インストール)/[使用方法](#使用方法)/[使用例](#使用例)で記載されているコマンドが実行できませんので

必ずインストールしてから進めてください。

### Git
Gitがインストールされていない場合は、下記手順でインストールしてください。

1. ターミナルを起動する。<br>使用するOSによりターミナルの名称が異なりますので注意してください。<br>(例. Windows:コマンドプロンプト,mac:ターミナル)

2. Gitがインストールされているか確認する。<br>`git version 2.34.1` のように表示された場合は、Gitがインストールされています。<br>以降の手順はスキップしてください。<br>**また、ターミナルは引き続き使用しますので開いたままにしてください!**
```
git --version
```

3. システムを更新する
```
sudo apt-get update
```

4. Gitをインストールする
```
sudo apt install git
```

5. Gitがインストールされたことを確認する。<br>`git version 2.34.1` のように表示されていれば、Gitのインストールは完了です!
```
git --version
```

### Python 3.x
[Python](https://www.python.org/downloads/)の公式サイトからあなたのPCのOSに合わせて、ダウンロードしてください。

ダウンロードしたファイルを使用してインストールできます。

Pythonがインストールされているかは、下記コマンドで確認することができます。

`Python 3.10.12`のように表示されていれば、Pythonはインストールされています。

```
python3 --version
```

## 🍴インストール
### クローン
このアプリケーションをあなたのPCで実行するために、クローンします。

クローンとは、このアプリケーションの実行に必要なファイル(リポジトリのコンテンツ)をあなたのPCのローカル環境へコピーすることです。

下記手順でクローンしてください。

1. リポジトリをクローンする
```
git clone https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger.git
```

2. クローンしたリポジトリへ移動する
```
cd Online-Chat-Messenger
```

## 🚀使用方法
1. ターミナルを3つ起動します。<br>起動した3つのターミナルについては、以降の手順では下記名称で呼ぶこととします。

| ターミナル | 名称 |
| ------- | ------- |
| ターミナル1 | サーバ用ターミナル |
| ターミナル2 | クライアント用ターミナル1 |
| ターミナル3 | クライアント用ターミナル2 |

2. サーバ用ターミナルに下記コマンドを入力する
```
python3 server.py
```
3. クライアント用ターミナル1に下記コマンドを入力する
```
python3 client.py
```
4. クライアント用ターミナルに表示される指示に従い、チャットルームを作成する
5. クライアント用ターミナル2に下記コマンドを入力する
```
python3 client.py
```
6. クライアント用ターミナルに表示される指示に従い、手順4.で作成したチャットルームに参加する
7. ユーザー同士でグループチャットを楽しむ
8. グループチャットを終了したい場合は、クライアント用ターミナル1に`exit`と入力して終了する

## 🙋使用例
一通りの手順のイメージは[デモ](#デモ)を参考にしてください。

1. ターミナルを3つ起動します。<br>起動した3つのターミナルについては、以降の手順では下記名称で呼ぶこととします。

| ターミナル | 名称 |
| ------- | ------- |
| ターミナル1 | サーバ用ターミナル |
| ターミナル2 | クライアント用ターミナル1 |
| ターミナル3 | クライアント用ターミナル2 |

2. サーバ用ターミナルに下記コマンドを入力する
```
python3 server.py
```
3. クライアント用ターミナル1に下記コマンドを入力する
```
python3 client.py
```
4. クライアント用ターミナルに表示される指示に従い、チャットルームを作成する。<br>チャットルームの作成に必要な入力は、下記のように入力しました。<br>表示される指示については、[ユーザー入力について](#ユーザー入力について)を確認してください。<br>`Input user name(Up to 10 characters) :` user1<br>`Input operation(choose 1 or 2) :` 1<br>`Input room name(Up to 8 characters) :` room1<br>`Password conditions.`<br>`Must be between 6 and 11 characters and include the following characters.`<br>`・Uppercase letters`<br>`・Lowercase letters`<br>`・NumbersInput`<br>`Input password :` Abc123<br>`Input room name size (Range 0 to 255):` 2<br>入力が完了すると、`room created!`と表示されたので、チャットルームの作成に成功しました。
5. クライアント用ターミナル2に下記コマンドを入力する
```
python3 client.py
```
6. クライアント用ターミナルに表示される指示に従い、手順4.で作成したチャットルームに参加する。<br>チャットルームの参加に必要な入力は、下記のように入力しました。<br>表示される指示については、[ユーザー入力について](#ユーザー入力について)を確認してください。<br>`Input user name(Up to 10 characters) :` user2<br>`Input operation(choose 1 or 2) :` 2<br>`Input room name(Up to 8 characters) :` room1<br>`Password conditions.`<br>`Must be between 6 and 11 characters and include the following characters.`<br>`・Uppercase letters`<br>`・Lowercase letters`<br>`・NumbersInput`<br>`Input password : `Abc123<br>`Input host token : `858e85fc-6143-4086-99d2-4205135ae259<br>入力が完了すると、`Chat room: room1 successfully created`と表示されたので、チャットルームに参加することができました。
7. ユーザー同士でグループチャットを楽しむ。<br>クライアント用ターミナル1とクライアント用ターミナル2でグループチャットができる状態になりました。<br>試しにグループチャットを利用してみます。<br>クライアント用ターミナル2(user2) : `Hello!`<br>クライアント用ターミナル1(user1) : `Nice to meet you!`<br>どちらのクライアント用ターミナルも入力したメッセージが共有されています!
8. グループチャットを終了したい場合は、クライアント用ターミナル1に`exit`と入力して終了する。<br>終了したいので、クライアント用ターミナル1に`exit`と入力しました。<br>以降に何か入力してもメッセージが共有されなくなりました。<br>グループチャットが利用できなくなったのがわかります。

### ユーザー入力について
| 用語 | 意味 |
| ------- | ------- |
| `Input user name(Up to 10 characters) :` | ユーザー名を入力して下さい。<br>文字数は、最大10文字までです。<br>入力例. user1 |
| `Input operation(choose 1 or 2) :` | チャットルームを作成するか参加するか選択してください。<br>・1 : チャットルームを作成する<br>・2 : チャットムールに参加する<br>入力例. 1 |
| `Input room name(Up to 8 characters) :` room1 | チャットルーム名を入力してください。<br>文字数は、最大8文字までです。<br>入力例. room1 |
| `Password conditions.`<br>`Must be between 6 and 11 characters and include the following characters.`<br>`・Uppercase letters`<br>`・Lowercase letters`<br>`・NumbersInput`<br>`Input password :`| パスワードを設定してください。<br>6~11文字で下記の文字を含めてください。<br>・アルファベットの大文字<br>・アルファベットの小文字<br>・数字<br>入力例. Abc123 |
| `Input room name size (Range 0 to 255):` | チャットルームの最大人数を入力してください。<br>人数は、0~255人です。<br>入力例. 2 |
| `Input host token : ` | ホストトークンを入力してください。<br>この指示は、`Input operation(choose 1 or 2) :`で2を入力した後に、表示されます。<br>チャットルームが作成された時に、トークンが表示されているはずなのでコピーして貼り付けてください。<br>入力例. 858e85fc-6143-4086-99d2-4205135ae259 |

## 💾使用技術
<table>
<tr>
  <th>カテゴリ</th>
  <th>技術スタック</th>
</tr>
<tr>
  <td>開発言語</td>
  <td>Python</td>
</tr>
<tr>
  <td rowspan=2>インフラ</td>
  <td>Ubuntu</td>
</tr>
<tr>
  <td>VirtualBox</td>
</tr>
</table>

## 👀機能一覧
### サーバ用ターミナル
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/9e5667e1-7333-41ae-9081-2615424d374e)

### クライアント用ターミナル1(user1)
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/d850f3f5-51ba-495e-9681-7bc7611f473c)

### クライアント用ターミナル2(user2)
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/56ed2c38-2a2a-4366-a10b-d11ae5595a95)


<table>
<tr>
  <th colspan=2>機能</th>
  <th>内容</th>
</tr>
<tr>
  <td colspan=2>メッセージの表示</td>
  <td>アプリケーションの進行に必要なメッセージを表示します。</td>
</tr>
<tr>
  <td rowspan=8>TCP</td>
  <td>チャットルームの作成と参加について</td>
  <td>
    チャットルームの作成と参加については、パターン図を作成しました。<br>
    <a href="#チャットルーム作成と参加で取りうるパターン">チャットルーム作成と参加で取りうるパターン</a>を確認してください。
  </td>
</tr>
<tr>
  <td>チャットルームの作成に必要な入力の要求</td>
  <td>チャットルームの作成に必要な入力をユーザーに求めます。</td>
</tr>
<tr>
  <td>チャットルームの参加に必要な入力の要求</td>
  <td>チャットルームの参加に必要な入力をユーザーに求めます。</td>
</tr>
<tr>
  <td>チャットルームの作成</td>
  <td>
    チャットルームの作成に必要な入力が完了すると、クライアントはサーバへTCPR(カスタムプロトコル)を送信します。<br>
    TCPRの構成については、<a href="#headerについて">headerについて</a>を確認してください。<br>
    サーバは、TCPRからデータを取得し、チャットルームを作成します。<br>
    チャットルームが作成中ということがわかるように処理が進むごとにチャットルームの作成状況(state)をクライアントへ送信します。<br>
    stateの内容は、下記のようになります。<br>
    0 : ルーム作成要求<br>
    1 : ルーム作成中<br>
    2 : ルーム作成完了<br>
    チャットルームの作成が完了すると、クライアントへ完了通知を送信します。<br>
    クライアントは、サーバから完了通知を受け取ると、ターミナルに<strong>room created!</strong>と表示します。</td>
</tr>
<tr>
  <td>ホストトークンの発行</td>
  <td>
    チャットルームの作成が完了すると、サーバは、ホストトークンを発行します。<br>
    ホストトークンの発行が完了すると、クライアントへ通知を送信します。<br>
    クライアントは、サーバから通知を受け取ると、ターミナルにホストトークンと注記を表示します。
  </td>
</tr>
<tr>
  <td>チャットルームの参加</td>
  <td>
    チャットルームの参加に必要な入力が完了すると、クライアントはサーバへTCPR(カスタムプロトコル)を送信します。<br>
    サーバは、TCPRからデータを取得し、チャットルームに参加できるかチェックします。<br>
    チャットルームの参加が完了すると、クライアントへ完了通知を送信します。<br>
    クライアントは、サーバから完了通知を受け取ると、ターミナルに<strong>Chat room: [roomname] successfully created</strong>と表示します。<br>
    また、下記の場合は、チャットルームに参加することができません。<br>
    1.ユーザーが入力した、ホストトークンが存在しない<br>
    2.チャットルームの許容人数に達している<br>
    3.ユーザーが入力した、パスワードが正しくない
  </td>
</tr>
<tr>
  <td>メンバートークンの発行</td>
  <td>
    チャットルームの参加が完了すると、サーバは、メンバートークンを発行します。<br>
    メンバートークンの発行が完了すると、クライアントへ通知を送信します。
  </td>
</tr>
<tr>
  <td>TCPコネクションの終了</td>
  <td>
    <strong>チャットルームの作成とホストトークンの発行</strong>または<strong>チャットルームの参加とメンバートークンの発行</strong>が完了すると、TCPコネクションは終了します。
  </td>
</tr>
<tr>
  <td rowspan=3>UDP</td>
  <td>グループチャットでの会話</td>
  <td>
    グループチャットには、UDPを利用しています。<br>
    チャットルーム内のユーザー同士でメッセージを送受信しやり取りを行います。<br>
    例えば、ユーザーが4人いた時、ユーザー1がメッセージが送信すると、メンバー全員のターミナルにユーザー1が送信したメッセージが共有されます。<br>
    送受信には、クライアントとサーバでデータをパケットとして共有しています。<br>
    パケットの構成については、下記を確認してください。<br>
    ・<a href="#クライアントからサーバに送信するパケット">クライアントからサーバに送信するパケット</a><br>
    ・<a href="#サーバからクライアントに送信するパケット">サーバからクライアントに送信するパケット</a>
  </td>
</tr>
<tr>
  <td>リレーシステムの削除</td>
  <td>
    チャットルーム内のユーザーはリストで管理しています。<br>
    メッセージの共有は、リレー形式になっており、ユーザーが退出すると、退出したユーザーにはメッセージが共有されなくなります。<br>
    リレーシステムの削除されるパターンは、下記の2通りがあります。<br>
    1.一定時間メッセージを送信していない<br>
    2.ユーザーが自ら退出したい
  </td>
</tr>
<tr>
  <td>チャットルームの有効期間</td>
  <td>
    チャットルームはホストが退出することにより自動的に閉じられます。<br>
    閉じられたチャットルームには参加することはできません。
  </td>
</tr>
</table>

### TCP
TCPは、新規チャットルームの作成または既存のチャットルームの参加という機能に利用しています。

#### headerについて
クライアントとサーバ間では、下記バイト表のような、TCPR(カスタムプロトコル)を送受信して共有しています。

![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/4b4d1b4b-6f44-4cc9-b9e8-a5eb51ad23b6)

バイト表の各バイトの情報は、下記のようになります。

![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/5e64ee4f-0de0-4a62-b0d8-d4128ecf64f7)

#### チャットルーム作成と参加で取りうるパターン
クライアントとサーバ間で取りうるパターンは下記のようになります。

![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/09958ce5-7c35-46d3-bbd5-e8573ece3eb6)

取りうるパターンをもとに作成したパターン図は下記のようになります。

パターン図には、下記のような情報を記載しています。

- クラインアントとサーバ間でやりとりされるヘッダーの情報
- TCP通信接続要求、許可、確率のタイミング
- クライアントからサーバへのリクエストの内容
- サーバからクライアントへのレスポンスの内容
- サーバが実行する処理
- TCPコネクション終了のタイミング
- UDPの切り替えのタイミング

##### パターン1.チャットルームの作成
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/dbdbb58f-ccab-432b-b56c-a13d189f12c7)

##### パターン2.チャットルームの参加_成功時
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/3b21b51d-8826-4734-a168-7e06db81b269)

##### パターン3.チャットルームの参加_失敗時
![image](https://github.com/Recursion-Group-Backend-c/Online-Chat-Messenger/assets/119317071/5ae0fbd8-6667-4f22-8cea-1c7467b45533)

### UDP
UDPは、グループチャットでの会話やリレーシステムの削除、チャットルームの有効期間の管理に利用しています。

#### クライアントからサーバに送信するパケット
グループチャットでの会話には、クライアントとサーバ間で、データをパケットとして共有しています。

クライアントからサーバに送信するパケットは、仕様をもとに必要なデータを整理した結果、下記のようなデータサイズの配分でパケットとして送信することとしました。

| データ | データサイズ(全体:4096バイト) |
| ------- | ------- |
| token | 32byte |
| user_name | 255byte |
| message | 3,809byte |

#### サーバからクライアントに送信するパケット
グループチャットでの会話には、クライアントとサーバ間で、データをパケットとして共有しています。

サーバからクライアントに送信するパケットは、仕様をもとに必要なデータを整理した結果、下記のようなデータサイズの配分でパケットとして送信することとしました。

| データ | データサイズ(全体:4092バイト) |
| ------- | ------- |
| user_name | 255byte |
| message | 3,839byte |

## 📜作成の経緯
⭐️後で記載する!!!

作成した理由を記載する。

## ⭐️こだわった点
⭐️後で記載する!!!

テキストや参考にした記事などを再度読み返して技術の理解を深めてから書く。

ここがエンジニアに一番読んでもらいたい箇所なのでできるだけ詳細に書く。

## 📮今後の実装したいもの
- [ ] デスクトップアプリケーションとして利用できるようにする

## 📑参考文献
### 公式ドキュメント
- [Python](https://docs.python.org/ja/3/)

### 参考にしたサイト
- [Python_Download](https://www.python.org/downloads/)
