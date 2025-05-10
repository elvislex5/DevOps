from PIL import Image, ImageDraw, ImageFont
import os

def create_default_avatar():
    # Créer une image carrée
    size = 200
    image = Image.new('RGB', (size, size), '#003366')
    draw = ImageDraw.Draw(image)
    
    # Dessiner un cercle
    draw.ellipse([10, 10, size-10, size-10], fill='#003366', outline='white', width=2)
    
    # Ajouter le texte "U" (pour User)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    text = "U"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    # Sauvegarder l'image
    os.makedirs('static/images', exist_ok=True)
    image.save('static/images/default-avatar.png')

def create_default_company():
    # Créer une image rectangulaire
    width = 600
    height = 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Dessiner un rectangle avec les couleurs de la marque
    draw.rectangle([0, 0, width, height], fill='#003366')
    
    # Ajouter le texte "LÔN-BTP"
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "LÔN-BTP"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Dessiner le texte avec deux couleurs
    draw.text((x, y), "LÔN-", fill='white', font=font)
    btp_bbox = draw.textbbox((0, 0), "LÔN-", font=font)
    btp_x = btp_bbox[2]
    draw.text((btp_x, y), "BTP", fill='#FFB400', font=font)
    
    # Sauvegarder l'image
    os.makedirs('static/images', exist_ok=True)
    image.save('static/images/default-company.png')

def create_logo_prototype():
    width, height = 600, 400
    bg = '#003366'
    yellow = '#FFB400'
    white = 'white'
    image = Image.new('RGB', (width, height), bg)
    draw = ImageDraw.Draw(image)

    # Immeuble stylisé
    building_x = width//4
    building_y = height//3
    building_w = width//2
    building_h = height//2
    draw.rectangle([building_x, building_y, building_x+building_w, building_y+building_h], fill=white, outline=yellow, width=4)
    # Fenêtres
    for i in range(3):
        for j in range(4):
            wx = building_x + 20 + i*60
            wy = building_y + 20 + j*40
            draw.rectangle([wx, wy, wx+30, wy+20], fill=bg)

    # Écran stylisé devant
    screen_x = building_x + building_w//4
    screen_y = building_y + building_h//2
    screen_w = building_w//2
    screen_h = building_h//3
    draw.rectangle([screen_x, screen_y, screen_x+screen_w, screen_y+screen_h], fill=yellow, outline=bg, width=3)
    # Graphique sur l'écran
    gx = screen_x + 20
    gy = screen_y + screen_h - 20
    for i, h in enumerate([30, 50, 20]):
        draw.rectangle([gx + i*40, gy-h, gx+20 + i*40, gy], fill=bg)

    # Pixels digitaux (effet tech)
    for i in range(10):
        px = building_x + building_w - 10 + i*8
        py = building_y - 10 - (i%3)*8
        draw.rectangle([px, py, px+6, py+6], fill=yellow)

    # Texte LÔN-BTP
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    text = "LÔN-"
    btp = "BTP"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x = (width - text_width - 100) // 2
    y = 40
    draw.text((x, y), text, fill=white, font=font)
    draw.text((x+text_width, y), btp, fill=yellow, font=font)

    image.save('static/images/lon-btp-logo-prototype.png')

if __name__ == '__main__':
    create_default_avatar()
    create_default_company()
    create_logo_prototype() 