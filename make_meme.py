from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''         
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word, 
            # add the line to the lines array
            lines.append(line)    
    return lines


img = Image.open('data/memes/0.jpeg')
image_size = img.size
draw = ImageDraw.Draw(img)
font_file_path = 'data/impact.ttf'
font = ImageFont.truetype(font_file_path, size=30, encoding="unic")
line_height = font.getsize('hg')[1]
color = 'rgb(255, 255, 255)'


# upper_text = "meme generator users hitkul"
upper_text = "IIIT D"
lower_text = "y u no give less work?"


upper_lines = text_wrap(upper_text, font, image_size[0])
y = 0
for line in upper_lines:
    width_space_left = image_size[0]-font.getsize(line)[0]
    x = int(width_space_left/2)
    draw.text((x, y), line, fill=color, font=font)
    y = y + line_height

lower_lines = text_wrap(lower_text, font, image_size[0])

y = image_size[1]-line_height-10
for line in lower_lines[::-1]:
    width_space_left = image_size[0]-font.getsize(line)[0]
    x = int(width_space_left/2)
    draw.text((x, y), line, fill=color, font=font)
    y = y - line_height

img.save('data/test.jpeg')