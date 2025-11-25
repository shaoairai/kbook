# KBook

全端網頁應用程式 - 會員系統

## 技術架構

| 層級 | 技術 | 版本 | 說明 |
|------|------|------|------|
| 前端 | Nuxt 4 (Vue 3) | 4.2.1 | SSR 模式 |
| 後端 | Flask | 2.2.2 | RESTful API |
| 資料庫 | PostgreSQL | 17 | Alpine 版本 |
| 容器化 | Docker Compose | - | 多容器編排 |

## 專案結構

```
kbook/
├── frontend/           # Nuxt 4 前端應用
│   ├── app/            # 應用程式檔案 (Nuxt 4 規範)
│   ├── server/         # Nitro API 路由
│   └── public/         # 靜態檔案
├── backend/            # Flask 後端 API
├── dockerfiles/        # Docker 建置檔案
├── db/                 # PostgreSQL 資料 (gitignore)
└── docker-compose.yaml # 容器編排設定
```

## 快速開始

### 環境需求

- Node.js 22+
- Python 3.13+
- Docker & Docker Compose

### 開發模式

**前端：**
```bash
cd frontend
npm install
npm run dev
```

**後端：**
```bash
cd backend
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 5000
```

### Docker 部署

```bash
# 建置前端（需先執行）
cd frontend && npm run build && cd ..

# 啟動所有服務
docker-compose up -d --build
```

## 服務端口

| 服務 | 本機端口 | 容器端口 |
|------|---------|---------|
| 前端 (Nuxt) | 5566 | 3000 |
| 後端 (Flask) | 5567 | 5000 |
| 資料庫 (PostgreSQL) | 5432 | 5432 |

## 開發連結

- 前端：http://localhost:5566（Docker）/ http://localhost:3000（開發）
- 後端 API：http://localhost:5567（Docker）/ http://localhost:5000（開發）
