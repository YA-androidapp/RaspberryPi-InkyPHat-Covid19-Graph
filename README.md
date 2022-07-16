# RaspberryPi-InkyPHat-Covid19-Graph

---

## Data

* 厚生労働省
  * [オープンデータ](https://www.mhlw.go.jp/stf/covid-19/open-data.html)
    * [新規陽性者数の推移（日別）](https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv)

## Env

```bash
python3 -m venv myenv
source myenv/bin/activate

python3 -m pip install -U pip
python3 -m pip install matplotlib numpy pandas pillow
sudo apt install -y libatlas-base-dev

curl https://get.pimoroni.com/inky | bash

python3 covid19.py yellow
```

---

Copyright (c) 2022 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
