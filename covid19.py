from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


# 定数
IMAGE_DPI = 96
INKY_HEIGHT = 122
INKY_WIDTH = 250
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
# plt.grid(True)
# plt.xlabel('Date')
# plt.ylabel('Cases')
# plt.xticks([i for i in df1['Datetime'] if i.strftime('%m%d') == '0101' or i.strftime('%m%d') == '0701'], fontsize=6)
# plt.title('Newly confirmed cases (daily)')
plt.axis('off')
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.savefig('plt.png', bbox_inches='tight', pad_inches=0, dpi=IMAGE_DPI)


# Pillow
fig.canvas.draw()
im = np.array(fig.canvas.renderer.buffer_rgba())
img = Image.fromarray(im)
img.save('pillow.png')

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
