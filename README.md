# Debridge

Для запуску необхідно скачати та встановити Python. 
Качаєм тут - https://www.python.org/downloads/
При встановленні проставляєм всі галочки

Скрипт по Debridge

https://app.debridge.finance/

Ганяє ETH між мережами Arbitrum, Optimism, Base, Linea.

Можна виставити налаштування у файлі config.json

1) randomise_order - рандомізуєм гаманці (true\false)
2) max_gas - максимальний газ при якому працюватиме софт
3) network - вибираєм, звідки куди шлем ETH
4) amount - сума яку відправляєм. Якщо all=true - відправляє весь баланс
5) timeout - час очікування(в секундах) між гаманцями

wallet.txt - в цей файл закидуєм приватники

proxy.txt - закидуєм свої проксі у форматі (якщо хочете без проксі, просто видаліть цей файл)
http://login:pass@ip:port


ЗАПУСК

Відкриваєм термінал і пишем команди:

cd "напрямок папки"

pip install -r requirements.txt

py main.py
