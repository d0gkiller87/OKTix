## Install
```bash
pip3 install -r requirements.txt
```

## Requirements
- Python 3.x
- Cookie-based authentication. Insert your cookie(s) in the source code, i.e.:
```
cookie = {
	'remember_user_token' : 'xxxxx',
	'kktix_session_token_v2': 'xxxxx'
}
```

## Usage
```bash
python3 oktix.py [Event] [Ticket ID] [Ticket Quantity] [Sleep Seconds]
```

## Parameters
- Event - 活動名稱 (可透過活動 url 取得) / e.g. sitcon2020
- Ticket ID - 票卷資訊ID (可透過 F12 選取票卷 HTML 找到) / e.g. 234871
- Ticket Quantity - 票卷數量 / e.g. 1
- Sleep Seconds - 失敗時重試前等待秒數 / e.g. 1.5

## Screenshots
![](https://github.com/vungsung/OkTix/blob/master/screenshots/1.png)
