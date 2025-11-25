# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 重要規範

**Claude 回覆一律使用繁體中文。**

## 專案概述

這是一個全端網頁應用程式：
- **前端**: Nuxt 4 (Vue 3) 應用程式位於 `frontend/`
- **後端**: Flask API 位於 `backend/`
- **部署**: Docker Compose 容器編排

## 常用指令

### 前端 (在 `frontend/` 目錄下執行)

```bash
npm install          # 安裝依賴
npm run dev          # 啟動開發伺服器 http://localhost:3000
npm run build        # 建置生產版本
npm run preview      # 預覽生產版本
npm run generate     # 產生靜態網站
```

### Docker

```bash
docker-compose up -d              # 啟動所有服務
docker-compose up -d --build      # 重新建置並啟動
docker-compose down               # 停止所有服務
```

### 後端

Flask 後端透過 Docker 或直接執行：
```bash
flask run --host 0.0.0.0 --port 5000
```

## 架構

### 服務 (docker-compose.yaml)
- `project` (Nuxt 前端): Port 5566 → 內部 3000
- `projectapi` (Flask 後端): Port 5567 → 內部 5000
- `db` (PostgreSQL 17): Port 5432 → 內部 5432

### 資料庫
- PostgreSQL 17 Alpine
- 資料庫名稱: `postgresdb`
- 資料持久化: `./db/` 掛載至容器

## Nuxt 4 檔案架構規範

**重要：Nuxt 4 的所有應用程式檔案必須放在 `app/` 目錄下，這與舊版 Nuxt 不同。**

### 前端目錄結構 (`frontend/`)

```
frontend/
├── app/                    # 所有 Nuxt 應用程式檔案 (Nuxt 4 必須)
│   ├── app.vue             # 根元件
│   ├── pages/              # 頁面路由 (自動產生路由)
│   ├── components/         # Vue 元件 (自動匯入)
│   ├── composables/        # 組合式函數 (自動匯入)
│   ├── layouts/            # 版面配置
│   ├── middleware/         # 路由中介層
│   ├── plugins/            # Nuxt 插件
│   ├── assets/             # 靜態資源 (會被建置處理)
│   └── utils/              # 工具函數 (自動匯入)
├── public/                 # 靜態檔案 (直接複製到輸出)
├── server/                 # Nitro 伺服器 API 路由
│   ├── api/                # API 端點
│   └── middleware/         # 伺服器中介層
├── nuxt.config.ts          # Nuxt 設定檔
└── tsconfig.json           # TypeScript 設定
```

### Nuxt 4 檔案放置規則

建立新檔案時必須遵循以下規則：

| 檔案類型 | 正確路徑 | 錯誤路徑 |
|---------|---------|---------|
| 頁面 | `app/pages/` | `pages/` |
| 元件 | `app/components/` | `components/` |
| 組合式函數 | `app/composables/` | `composables/` |
| 版面配置 | `app/layouts/` | `layouts/` |
| 中介層 | `app/middleware/` | `middleware/` |
| 插件 | `app/plugins/` | `plugins/` |
| 靜態資源 | `app/assets/` | `assets/` |
| 工具函數 | `app/utils/` | `utils/` |
| 伺服器 API | `server/api/` | `app/server/` |

### 後端結構 (Flask)
- `backend/app.py` - Flask 主應用程式
- CORS 已啟用 `http://localhost:3000`
- 使用 Flask-CORS、PyJWT

### Dockerfiles
- `dockerfiles/Dockerfile.nuxt` - Node 22 Alpine，執行建置後的 Nuxt
- `dockerfiles/Dockerfile.python` - Python 3.13 slim bookworm，Flask 伺服器

## Docker 規範

### docker-compose.yaml 規範
- **不使用 `version` 屬性**：現代 Docker Compose 已棄用 `version` 欄位，直接以 `services:` 開頭
- 使用 Compose Specification 格式（Docker Compose 1.27.0+ 自動支援）

### Dockerfile 基礎映像規範

| 服務 | 基礎映像 | 說明 |
|------|---------|------|
| Nuxt 前端 | `node:22-alpine` | Node.js LTS，Alpine 輕量版 |
| Flask 後端 | `python:3.13-slim-bookworm` | Python 最新穩定版，Debian 12（支援至 2028） |
| PostgreSQL | `postgres:17-alpine` | PostgreSQL 17，Alpine 輕量版 |

### Dockerfile 最佳實踐

**Node.js (Nuxt):**
- 使用 `npm ci --omit=dev` 安裝生產依賴（取代已棄用的 `--production`）
- 只複製必要檔案：`package*.json`、`.output`、`public`

**Python (Flask):**
- 使用 `COPY` 取代 `ADD`（除非需要解壓縮功能）
- 使用 `pip install --no-cache-dir` 減少映像大小
- 合併 `apt-get update` 與清理指令，減少層數：
  ```dockerfile
  RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*
  ```

### 基礎映像選擇原則
- **避免使用 bullseye (Debian 11)**：將於 2026 年 6 月終止支援
- **推薦使用 bookworm (Debian 12)**：支援至 2028 年
- **Alpine 變體**：適合對映像大小敏感的場景，但需注意相容性
