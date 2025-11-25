from flask import Flask, render_template,request,jsonify,make_response,redirect
import json
import requests
from flask_cors import CORS
import logging

import jwt
import time

import os # 增加 os 套件的功能

app = Flask(__name__, static_folder="main/static", template_folder="main", static_url_path="/static")
# CORS 設定 - 使用前端 URL 並加入開發用的 localhost:3000
cors_origins = []

# 加入 localhost:3000 以便開發使用
cors_origins.append("http://localhost:3000")
CORS(app, supports_credentials=True, origins=cors_origins)

@app.route("/")
def index():
    return "服務運行中 - Flask Backend is running successfully!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5567, debug=True)
