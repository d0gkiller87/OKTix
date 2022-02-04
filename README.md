## Install
```bash
pip3 install -r requirements.txt
```

## Requirements
- Python 3.x
- Cookie-based authentication. Place your cookie(s) in the source code, i.e.:
```python
cookies = {
	'kktix_session_token_v2': 'xxxxx'
}
```

## Usage
```bash
python3 oktix.py [Event] [Ticket ID] [Ticket Quantity] [Sleep Seconds]
```

## Parameters
- Event - 活動名稱 (可透過活動 url 取得) / e.g. `https://kktix.com/events/sitcon2020` -> sitcon2020
- Ticket ID - 票卷資訊 ID (於能瀏覽票種的頁面，可嘗試 F12 選取票種 HTML，可能能在附近找到) / e.g. 234871
- Ticket Quantity - 票卷數量 / e.g. 1
- Sleep Seconds - 重新搶票間隔秒數 / e.g. 1.5

## Screenshots
![](/screenshots/1.png)
