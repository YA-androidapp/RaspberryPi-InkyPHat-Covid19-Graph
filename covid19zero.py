#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.


# pipからパッケージをインストールするとビルドが走って時間がかかってしまうのでaptからインストールする
# python3 -m pip install -U pip
# sudo apt update && sudo apt upgrade -y
# sudo apt install -y python3-matplotlib python3-pandas python3-pil libatlas-base-dev
# curl https://get.pimoroni.com/inky | bash
# python3 -m pip install inkyphat

# python3 covid19.py black
# crontab:
#   @reboot python3 /home/pi/RaspberryPi-InkyPHat-Covid19-Graph-main/covid19zero.py && sleep 600 && shutdown -h now


from PIL import Image, ImageDraw, ImageFont
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sys


# 定数
IMAGE_DPI = 96
INKY_HEIGHT = 104
INKY_WIDTH = 212
CSV_PATH = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'


# 引数
USAGE = 'Usage: {} <colour: red, yellow or black>'.format(sys.argv[0])
if len(sys.argv) < 2:
    print(USAGE)
    sys.exit(1)


# データ取得
df = pd.read_csv(CSV_PATH)
df['Datetime'] = pd.to_datetime(df['Date'])
df1 = df.loc[:, ['Datetime', 'ALL']]


# Matplotlib
fig = plt.figure(figsize=(INKY_WIDTH/IMAGE_DPI, INKY_HEIGHT/IMAGE_DPI), dpi=IMAGE_DPI)
plt.plot(df1['Datetime'], df1['ALL'], color = "red")
plt.axis('off')
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.savefig('plt.png', bbox_inches='tight', pad_inches=0, dpi=IMAGE_DPI)

# date
dtstr = df1.iloc[-1]["Datetime"].strftime('%m/%d')
label = f'{dtstr}: {df1.iloc[-1]["ALL"]:,}'
# font = ImageFont.load_default()
font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 24)

# Pillow
img = Image.open('plt.png')
draw = ImageDraw.Draw(img)
draw.text((0, 0), label, fill="red", font=font)

pal_img = Image.new('P', (1, 1))
pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
inky_img = img.convert('RGB').quantize(palette=pal_img)
inky_img = inky_img.resize((INKY_WIDTH, INKY_HEIGHT))

inky_img.save('inky.png')


# on Raspberry Pi
try:
    import inkyphat
    inkyphat.set_colour(sys.argv[1])
    inkyphat.set_image(inky_img)
    inkyphat.show()
except ModuleNotFoundError:
    pass
except ValueError:
    print(USAGE)
    sys.exit(1)
