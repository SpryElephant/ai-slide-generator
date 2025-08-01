import openai, io, requests, json, sys, os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

STYLE = ("Modern, futuristic, minimalistic; palette deep‑indigo #2D2F92, violet #6F3EDD, "
         "electric‑teal #15D4C8 highlights; soft volumetric glow; cinematic lighting; "
         "ultra‑sharp; 8‑K render; no text or watermark; avoid clutter; "
         "high contrast between subject and transparent areas.")

assets = {
  # filename                text                                                     size        final       alpha
  "BG-Simple.png":        ("Clean minimal gradient background; subtle deep indigo to violet fade; very low contrast texture; designed for text overlay compatibility.",      "1792x1024",(1920,1080),False),
  "OL-TechTimeline.png":  ("Right-side vertical tech timeline; floating holographic icons: cloud, mobile, AI brain, blockchain; positioned on right third of image; left side solid dark indigo for text space.", "1024x1024",(750,900),False),
  "OL-AIModels.png":      ("Horizontal banner across top; glowing AI model logos GPT-4, Claude, Gemini in electric teal; bottom two-thirds solid dark background for content.","1792x1024",(1920,420),False),
  "OL-DevWorkflow.png":   ("Left-side developer silhouette with code streams; AI assistant hologram; positioned on left third; right side dark gradient for text placement.","1024x1024",(750,900),False),
  "OL-ProcessFlow.png":   ("Right-aligned 3D flowchart with neon connections; code to AI to deployment; positioned on right third; left side clean dark background.","1024x1024",(750,900),False),
  "OL-CycleBreaker.png":  ("Center floating curved arrow with particle effects; designed with clear space around edges for text; subtle glow effect.","1024x1024",(600,600),False),
  "OL-DevTools.png":      ("Bottom banner of floating holographic screens showing dev tools; top two-thirds reserved for text with dark overlay.","1792x1024",(1920,420),False),
  "OL-Connections.png":   ("Top banner with connected platform logos; clean geometric design; bottom space kept minimal for content overlay.","1792x1024",(1920,420),False),
  "OL-Productivity.png":  ("Left-side developer with neural interface and floating productivity icons; right side gradient fade to dark for text content.","1024x1024",(750,900),False),
  "OL-Architecture.png":  ("Right-side architect figure with holographic microservices blueprint; left side clean dark space for text positioning.","1024x1024",(750,900),False),
  "BG-Culture.png":       ("Full transformation scene: left skeptical developer in grayscale dissolving, right vibrant AI-empowered developer emerging; central space darkened for text overlay.","1792x1024",(1920,1080),False),
  "IC-Bolt.png":          ("Minimalist neon‑teal outline lightning‑bolt icon, inner glow, transparent.","1024x1024",(350,350),True),
  "IC-Arrow.png":         ("Minimalist neon‑teal outline upward‑arrow icon, inner glow, transparent.","1024x1024",(350,350),True),
  "IC-Chat.png":          ("Minimalist neon‑teal outline chat‑bubble icon, inner glow, transparent.","1024x1024",(350,350),True),
  "IC-Compass.png":       ("Minimalist neon‑teal outline compass icon, inner glow, transparent.","1024x1024",(350,350),True),
  "BG-Wave.png":          ("Epic code wave background; flowing lines of code forming ocean wave; sunrise gradient indigo to teal; darker upper and lower bands for text positioning.","1792x1024",(1920,1080),False)
}

out_dir = Path("assets")
out_dir.mkdir(exist_ok=True)

def dalle(prompt,size):
    try:
        resp=client.images.generate(model="dall-e-3",prompt=prompt,size=size,n=1,response_format="url")
        return resp.data[0].url
    except Exception as e:
        print("Generation error:",e)
        sys.exit(1)

for fname,(scene,size,final,alpha) in tqdm(assets.items(),desc="Images"):
    fp=out_dir/fname
    if fp.exists(): 
        print(f"{fname} exists, skipping."); continue
    url=dalle(f"{STYLE} — {scene}",size)
    raw=requests.get(url).content
    img=Image.open(io.BytesIO(raw)).convert("RGBA")
    img=img.resize(final,Image.LANCZOS)
    img.save(fp)
    print("saved",fp)
