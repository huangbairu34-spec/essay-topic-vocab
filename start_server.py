# -*- coding: utf-8 -*-
import http.server
import socketserver
import socket
import os
import webbrowser

PORT = 8083
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def get_lan_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith('127.') and not ip.startswith('169.254.') and not ip.startswith('192.168.56.'):
                ips.append(ip)
    except Exception:
        pass
    return ips

lan_ips = get_lan_ips()

# Try finding open port starting from 8083
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while PORT < 8090:
    try:
        s.bind(('', PORT))
        s.close()
        break
    except OSError:
        PORT += 1

print('=' * 65)
print('  考研英语作文主题词与拓展 (英一 / 英二) 手机背诵服务已启动！')
print('=' * 65)
print('\n 请确保手机与电脑连接在【同一个 Wi-Fi】下：')
for ip in lan_ips:
    print(f'    手机浏览器直接访问: http://{ip}:{PORT}/index.html')

print(f'\n 电脑本机直接访问: http://127.0.0.1:{PORT}/index.html')
print('\n 提示：按 Ctrl+C 可停止服务。')
print('=' * 65)

qr_urls = [f'http://{ip}:{PORT}/index.html' for ip in lan_ips]
primary_url = qr_urls[0] if qr_urls else f'http://127.0.0.1:{PORT}/index.html'

qr_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>手机扫码直接看 · 考研英语作文主题词</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 40px 20px; background: #0f172a; color: #f8fafc; }}
    .card {{ max-width: 460px; margin: 0 auto; background: #1e293b; padding: 32px 24px; border-radius: 24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); border: 1px solid #334155; }}
    h1 {{ color: #38bdf8; font-size: 22px; margin-bottom: 8px; font-weight: 700; }}
    .sub {{ color: #94a3b8; font-size: 14px; margin-bottom: 24px; line-height: 1.5; }}
    .qr-wrap {{ background: white; padding: 14px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
    img {{ width: 220px; height: 220px; display: block; border-radius: 8px; }}
    .url-box {{ background: #0f172a; padding: 14px; border-radius: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; color: #38bdf8; word-break: break-all; margin-top: 20px; border: 1px solid #334155; }}
    .tips {{ margin-top: 20px; font-size: 13px; color: #64748b; line-height: 1.6; }}
    .tag {{ display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 3px 8px; border-radius: 6px; font-size: 12px; margin: 2px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>📝 考研英语作文主题词</h1>
    <p class="sub">英一 2001-2026 · 英二 2010-2026 · 7大高分分类<br>请确保手机与电脑连接【同一 Wi-Fi】</p>
    <div class="qr-wrap">
      <img src="https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={primary_url}" alt="扫码打开">
    </div>
    <div class="url-box">{primary_url}</div>
    <div class="tips">
      <p>💡 手机相机 / 微信 / 夸克 / Safari 扫码即可直接全屏背诵</p>
      <div>
        <span class="tag">英一英二分流</span>
        <span class="tag">卡片速记</span>
        <span class="tag">划卡发音</span>
        <span class="tag">遮挡自测</span>
        <span class="tag">生词收藏</span>
      </div>
    </div>
  </div>
</body>
</html>'''

with open(os.path.join(DIRECTORY, '手机扫码访问.html'), 'w', encoding='utf-8') as f:
    f.write(qr_html)

try:
    webbrowser.open(f'http://127.0.0.1:{PORT}/手机扫码访问.html')
except Exception:
    pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务已安全退出。')
