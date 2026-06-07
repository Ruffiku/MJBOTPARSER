import os
import time
import requests
import xml.etree.ElementTree as ET

# Ссылка на нужный раздел форума Majestic RP
RSS_URL = "https://forum.majestic-rp.ru/forums/zhaloby-na-igrokov.37/index.rss"
# Твой вебхук из Дискорда (Railway подтянет его автоматически)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Юзер-агент, чтобы прикинуться обычным браузером в обход Cloudflare
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

sent_links = set()

def check_forum():
    try:
        response = requests.get(RSS_URL, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return
        
        root = ET.fromstring(response.content)
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            
            if link not in sent_links:
                # Если это первый запуск, просто запоминаем старые темы
                if len(sent_links) > 0:
                    payload = {"content": f"📢 **Новая тема на форуме Majestic!**\n**{title}**\n🔗 {link}"}
                    requests.post(DISCORD_WEBHOOK, json=payload)
                sent_links.add(link)
    except Exception as e:
        print(f"Ошибка: {e}")

# Бесконечный цикл проверки каждые 5 минут
check_forum()
while True:
    time.sleep(300)
    check_forum()
