import os
import random
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import imageio.v3 as iio
from datetime import datetime

# Setup folders
os.makedirs('outputs', exist_ok=True)

# Viral baby prompts (AI generation ke liye)
BABY_PROMPTS = [
    "cute newborn baby smiling, soft lighting, photorealistic, 8k",
    "adorable baby laughing with chubby cheeks, pastel background, professional",
    "sleeping baby angelic pose, cinematic lighting, 4k",
    "baby with funny surprised expression, viral meme potential",
    "twin babies hugging, adorable moment, soft focus"
]

VIRAL_TITLES = [
    "This smile will make your day! 😍",
    "Wait for the laugh! 🤣",
    "Cutest baby ever? 💕",
    "Pure happiness ✨",
    "Cuteness overload! 🥺"
]

def generate_image(filename):
    """FREE AI Image Generator - Pollinations"""
    prompt = random.choice(BABY_PROMPTS)
    print(f"🎨 Creating: {prompt[:40]}...")
    
    # Pollinations AI (100% Free, Unlimited)
    encoded = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&nologo=true&seed={random.randint(1,9999)}"
    
    try:
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            path = f"outputs/{filename}"
            with open(path, 'wb') as f:
                f.write(r.content)
            return path
    except Exception as e:
        print(f"Error: {e}")
    return None

def create_video(img1_path, img2_path):
    """Create 7 second viral short"""
    print("🎬 Making video...")
    
    frames = []
    fps = 30
    duration = 3.5  # seconds per image
    
    for img_path in [img1_path, img2_path]:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((1080, 1920))
        
        # Enhance colors (viral look)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # Add text overlay
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        except:
            font = ImageFont.load_default()
        
        text = random.choice(VIRAL_TITLES)
        bbox = draw.textbbox((0,0), text, font=font)
        x = (1080 - (bbox[2]-bbox[0]))//2
        y = 1600
        
        # Black background for text
        draw.rectangle([x-20, y-10, x+(bbox[2]-bbox[0])+20, y+100], fill='black')
        draw.text((x, y), text, fill='white', font=font)
        
        # Ken Burns effect (slow zoom)
        for i in range(int(fps * duration)):
            progress = i / (fps * duration)
            scale = 1.0 + (0.1 * progress)
            
            new_w = int(1080 / scale)
            new_h = int(1920 / scale)
            left = (1080 - new_w)//2
            top = (1920 - new_h)//2
            
            cropped = img.crop((left, top, left+new_w, top+new_h))
            cropped = cropped.resize((1080, 1920))
            frames.append(np.array(cropped))
    
    # Save video
    output = "outputs/baby_short.mp4"
    iio.imwrite(output, frames, fps=fps, codec="libx264", quality=8)
    print(f"✅ Video ready: {output}")
    return output

def main():
    print("🍼 Baby Bot Starting...")
    
    # Generate 2 images
    img1 = generate_image("img1.jpg")
    img2 = generate_image("img2.jpg")
    
    if not img1 or not img2:
        print("❌ Image failed")
        return
    
    # Make video
    video = create_video(img1, img2)
    
    # Save metadata
    title = random.choice(VIRAL_TITLES)
    with open("outputs/metadata.txt", "w") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Tags: #Shorts #Baby #Cute #Viral\n")
    
    print(f"🎉 Done! Title: {title}")
    print("📥 Download video from Actions tab")

if __name__ == "__main__":
    main()
