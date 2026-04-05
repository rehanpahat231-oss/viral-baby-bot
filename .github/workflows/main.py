import os
import random
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import imageio.v3 as iio
from datetime import datetime
import sys

# Setup folders
os.makedirs('outputs', exist_ok=True)

print("🚀 Baby Bot Starting...")

# Viral prompts
BABY_PROMPTS = [
    "cute newborn baby smiling, soft lighting, photorealistic",
    "adorable baby laughing with chubby cheeks, pastel background",
    "sleeping baby angelic pose, cinematic lighting",
    "baby with funny surprised expression, viral meme potential",
    "twin babies hugging, adorable moment"
]

VIRAL_TITLES = [
    "This smile will make your day! 😍",
    "Wait for the laugh! 🤣",
    "Cutest baby ever? 💕",
    "Pure happiness ✨",
    "Cuteness overload! 🥺"
]

def generate_image(filename):
    """Generate AI Image"""
    try:
        prompt = random.choice(BABY_PROMPTS)
        print(f"🎨 Generating: {prompt[:40]}...")
        
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&nologo=true&seed={random.randint(1,9999)}"
        
        r = requests.get(url, timeout=60)
        print(f"📥 Image download status: {r.status_code}")
        
        if r.status_code == 200 and len(r.content) > 1000:
            path = f"outputs/{filename}"
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"✅ Image saved: {path} ({len(r.content)} bytes)")
            return path
        else:
            print(f"❌ Image download failed: Status {r.status_code}, Size {len(r.content)}")
            return None
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None

def create_video(img1_path, img2_path):
    """Create video with error handling"""
    try:
        print("🎬 Creating video...")
        frames = []
        fps = 30
        duration = 3.5
        
        for idx, img_path in enumerate([img1_path, img2_path]):
            print(f"📸 Processing image {idx+1}...")
            
            # Open image
            img = Image.open(img_path).convert('RGB')
            img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            
            # Enhance
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)
            
            # Add text
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
            except:
                font = ImageFont.load_default()
            
            text = random.choice(VIRAL_TITLES)
            bbox = draw.textbbox((0,0), text, font=font)
            x = (1080 - (bbox[2]-bbox[0]))//2
            y = 1600
            
            draw.rectangle([x-20, y-10, x+(bbox[2]-bbox[0])+20, y+100], fill='black')
            draw.text((x, y), text, fill='white', font=font)
            
            # Generate frames (Ken Burns)
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
            
            print(f"✅ Image {idx+1} processed")
        
        # Save video
        output = "outputs/baby_short.mp4"
        print(f"💾 Saving video ({len(frames)} frames)...")
        iio.imwrite(output, frames, fps=fps, codec="libx264", quality=8)
        
        print(f"✅ Video saved: {output}")
        return output
        
    except Exception as e:
        print(f"❌ Video creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    try:
        print("🍼 Starting process...")
        
        # Generate images
        img1 = generate_image("img1.jpg")
        if not img1:
            print("❌ First image failed, exiting")
            sys.exit(1)
            
        img2 = generate_image("img2.jpg")
        if not img2:
            print("❌ Second image failed, exiting")
            sys.exit(1)
        
        # Create video
        video = create_video(img1, img2)
        if not video:
            print("❌ Video creation failed")
            sys.exit(1)
        
        # Save metadata
        title = random.choice(VIRAL_TITLES)
        with open("outputs/metadata.txt", "w") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Tags: #Shorts #Baby #Cute #Viral\n")
        
        print("🎉 SUCCESS! Video created.")
        return 0
        
    except Exception as e:
        print(f"❌ Main error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
