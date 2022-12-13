# dev-microservices-architecture

## 開発の目的  
マイクロサービスでの認証・認可を実装することで理解を深める

## 認証・認可構成図  

![image](https://user-images.githubusercontent.com/79680980/206892749-ff7004ef-68fb-4f2a-9b5e-7b79e1de8950.png)


## 概要
./mainserviceにてある個人サイトが動いていると仮定。  
./micro-todo下、すなわちtodoアプリを既存アプリから切り離しマイクロサービス化  

### 認証・認可
・認証はFastAPIのOAuth2ライブラリをちょっといじってcookieヘッダにjwtをのせた。(期限は一時間)  
・フロントはSPAなのでcookieの値を読み取らず、http通信のheaderを介してauth検証  
・mainserviceもmicro-todoもauthサーバにて認証認可を行う  
・クライアントがcookieをバケツリレーする形でmicro-todoでcookieをauthサーバに検証  

### API
・main-serviceで認可が取れてれば、micro-todoのリソースを読み取れる。（ここでは最新のtodoを読める）  
・user_idに紐付いたmicro_idを外部キーとしてmicro-todoリソースを読み取る

### 課題
・micro-todoにてセッションが切れたあと、ログインし直すのだが、micro-todoへリダイレクトできない。  
　ー　　プロキシを作る？　SPA外の動的ルーティングがわからん。nginxでやりたい  
・EC2などのサーバにのせてさらに環境をわけたい  
　ー　開発環境でのOAuthはつかめてきたので、本版環境との統合  

# 参考文献
1. https://fabeee.co.jp/column/employee-blog/mattsun01/
2. https://zenn.dev/mryhryki/articles/2020-12-28-oauth2-flow
3. https://qiita.com/sand/items/990afc5d49a37b026acc
4. https://zenn.dev/iroristudio/articles/0bc4729fefbc41
5. https://www.fastapitutorial.com/blog/fastapi-jwt-httponly-cookie/
