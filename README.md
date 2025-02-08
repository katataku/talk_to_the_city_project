## 🛠 セットアップ

# Dockerコンテナのビルドと起動
docker compose up --build

# Pythonコンテナに接続
docker exec -it new_city_report-reports-python-1 /bin/bash

# PDFデータの取り込み
python ingestPdf.py

# アプリケーションの実行
python main.py configs/ai01.json

# アクセス
http://localhost:3000
