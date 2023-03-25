---
title: 📄 RichText
description: 富文本段落
---

## 调用示例

```python
from PIL import Image, ImageDraw, ImageFont

from richtext import RichText, Paragraph


HYWH = ImageFont.truetype('./HYWenHei.ttf')

paragraph = Paragraph(
    '你说的对, 但是', RichText('原神', color='blue'),
    '是由', RichText('上海米哈游科技', size=60, font=HYWH),
    '开发的开放世界冒险游戏。'
 )
 
# 按字符分割，每行10个字：
paragraph.split(10)

# 按实际宽度分割，每行最大宽度为17*10 = 170
paragraph.wrap(170)

# 绘图
im = Image.new('RGB', (800, 600))
draw = ImageDraw.Draw(im)

paragraph.draw(draw, xy=(400, 300), anchor='mm')

# 也可以与html,bbcode,或者unity3d相互转换
p1 = paragraph.from_html(
    'I'm <span color="#ff0000">red!</span>'
)

p2 = paragraph.from_bbcode(
    'Sooo [size=60]Big![/color]'
)

p3 = paragraph.from_u3d_color(
    'I'm <color="#ff0000">red!</color>'
)

print(p1.to_u3d_color)
print(p2.to_html)
```