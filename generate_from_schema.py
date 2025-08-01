#!/usr/bin/env python3
"""
Unified Presentation Generator
Generates all assets from a single presentation schema file.
"""

import openai
import io
import requests
import json
import sys
import os
import time
import shutil
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_presentation_schema(schema_path):
    """Load and validate presentation schema"""
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    required_keys = ['meta', 'visual_identity', 'layout_system', 'slides', 'asset_config']
    for key in required_keys:
        if key not in schema:
            raise ValueError(f"Missing required key in schema: {key}")
    
    return schema

def generate_image(prompt, size, max_retries=3):
    """Generate image using DALL-E with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1,
                response_format="url"
            )
            return response.data[0].url
        except (requests.exceptions.ConnectionError, ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                print(f"\n⚠️  Connection error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Connection failed after {max_retries} attempts: {e}")
                return None
        except Exception as e:
            print(f"\n❌ Generation error: {e}")
            return None

def process_asset(asset_info, style_prompt, asset_config, output_dir):
    """Process a single asset (background or icon)"""
    filename = asset_info['filename']
    filepath = output_dir / filename
    
    # Skip if exists
    if filepath.exists():
        return filepath  # Return silently, tqdm will show progress
    
    # Determine size and final dimensions
    if filename.startswith('IC-'):
        # Icon
        size = asset_config['dimensions']['icons']['generation_size']
        final_size = tuple(asset_config['dimensions']['icons']['final_size'])
    else:
        # Background
        size = asset_config['dimensions']['background']['generation_size'] 
        final_size = tuple(asset_config['dimensions']['background']['final_size'])
    
    # Generate image
    full_prompt = f"{style_prompt} — {asset_info['prompt']}"
    
    url = generate_image(full_prompt, size)
    
    if url is None:
        print(f"\n⚠️  Skipping {filename} due to generation failure")
        return None
    
    # Download and process with retry
    max_download_retries = 3
    for attempt in range(max_download_retries):
        try:
            raw_data = requests.get(url, timeout=30).content
            img = Image.open(io.BytesIO(raw_data)).convert("RGBA")
            img = img.resize(final_size, Image.LANCZOS)
            
            # Save
            img.save(filepath)
            return filepath
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_download_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"\n⚠️  Download error, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Download failed for {filename}: {e}")
                return None
        except Exception as e:
            print(f"\n❌ Processing error for {filename}: {e}")
            return None

def generate_presentation_assets(schema_path):
    """Generate all assets for a presentation from schema"""
    # Load schema
    schema = load_presentation_schema(schema_path)
    
    # Setup
    meta = schema['meta']
    visual_identity = schema['visual_identity'] 
    asset_config = schema['asset_config']
    
    print(f"🎬 Generating assets for: {meta['title']}")
    print(f"📋 Theme: {meta['theme']}")
    print(f"🎨 Style: {visual_identity['atmosphere']}")
    
    # Create output directory (standard name)
    output_dir = Path("assets_generated")
    output_dir.mkdir(exist_ok=True)
    
    # Extract style prompt
    style_prompt = visual_identity['style_prompt']
    
    # Generate slide backgrounds
    slide_assets = []
    for slide in schema['slides']:
        slide_assets.append({
            'filename': slide['background']['filename'],
            'prompt': slide['background']['prompt']
        })
    
    # Generate icons if present
    icon_assets = []
    if 'icons' in schema:
        for icon in schema['icons']:
            icon_assets.append({
                'filename': icon['filename'],
                'prompt': icon['prompt']
            })
    
    # Generate all assets
    all_assets = slide_assets + icon_assets
    
    # Count existing assets
    existing_count = sum(1 for asset in all_assets if (output_dir / asset['filename']).exists())
    new_count = len(all_assets) - existing_count
    
    if existing_count > 0:
        print(f"\n✓ Found {existing_count} existing assets")
    
    if new_count > 0:
        print(f"🚀 Generating {new_count} new assets...")
    else:
        print(f"✨ All assets already exist!")
    
    # Track generation results
    successful = 0
    failed = []
    
    for asset in tqdm(all_assets, desc="Processing assets"):
        result = process_asset(asset, style_prompt, asset_config, output_dir)
        if result is not None:
            successful += 1
        else:
            if not (output_dir / asset['filename']).exists():
                failed.append(asset['filename'])
    
    print(f"\n✅ Asset processing complete!")
    print(f"📁 Assets saved to: {output_dir}")
    print(f"📊 Successfully processed: {successful}/{len(all_assets)}")
    
    if failed:
        print(f"\n⚠️  Failed to generate {len(failed)} assets:")
        for filename in failed:
            print(f"   - {filename}")
        print("\nYou can run the generator again to retry failed assets.")
    
    return output_dir

def create_slides_json(schema_path, output_path):
    """Extract slide content from schema for runtime use"""
    schema = load_presentation_schema(schema_path)
    
    # Transform slides for runtime
    runtime_slides = []
    for slide in schema['slides']:
        runtime_slide = {
            'layout': slide['layout'],
            'bg': slide['background']['filename'],
            **slide['content']  # title, subtitle, bullets, text, etc.
        }
        runtime_slides.append(runtime_slide)
    
    # Save runtime slides
    with open(output_path, 'w') as f:
        json.dump(runtime_slides, f, indent=2)
    
    print(f"📄 Runtime slides saved to: {output_path}")
    return output_path

def get_next_version(presentation_dir):
    """Find the next available version number for a presentation"""
    version = 1
    while (presentation_dir / f"v{version}").exists():
        version += 1
    return version

def find_latest_version(presentation_dir):
    """Find the latest version directory for a presentation"""
    latest_version = None
    latest_dir = None
    
    if not presentation_dir.exists():
        return None
        
    for path in presentation_dir.glob("v*"):
        if path.is_dir():
            try:
                # Extract version number
                version_str = path.name[1:]  # Remove 'v' prefix
                version = int(version_str)
                if latest_version is None or version > latest_version:
                    latest_version = version
                    latest_dir = path
            except ValueError:
                continue
                
    return latest_dir

def copy_existing_assets(previous_dir, new_dir):
    """Copy assets from previous version to new version"""
    copied_count = 0
    
    # Copy assets_generated directory if it exists
    prev_assets = previous_dir / "assets_generated"
    new_assets = new_dir / "assets_generated"
    
    if prev_assets.exists():
        new_assets.mkdir(exist_ok=True)
        
        for asset_file in prev_assets.glob("*"):
            if asset_file.is_file():
                dest_file = new_assets / asset_file.name
                if not dest_file.exists():
                    shutil.copy2(asset_file, dest_file)
                    copied_count += 1
                    
    return copied_count

def migrate_unversioned_directory(old_dir, new_versioned_dir):
    """Migrate an old unversioned directory to the new versioned structure"""
    if not old_dir.exists():
        return False
        
    print(f"🔄 Migrating unversioned directory: {old_dir.name} → {new_versioned_dir}")
    
    # Create the versioned directory
    new_versioned_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all contents
    for item in old_dir.iterdir():
        dest = new_versioned_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    
    # Create version info for the migrated v1
    save_version_info(new_versioned_dir, 1, None)
    
    print(f"✅ Migration complete: {new_versioned_dir}")
    return True

def save_version_info(build_dir, version, previous_version=None):
    """Save version information to a metadata file"""
    version_info = {
        "version": version,
        "created_at": datetime.now().isoformat(),
        "previous_version": previous_version
    }
    
    version_file = build_dir / "version.json"
    with open(version_file, 'w') as f:
        json.dump(version_info, f, indent=2)

def copy_template_files(build_dir, script_dir):
    """Copy template HTML and other necessary files to build directory"""
    # Copy presentation HTML as index.html
    src_html = script_dir / "presentation_unified.html"
    if src_html.exists():
        dst_html = build_dir / "index.html"
        dst_html.write_text(src_html.read_text())
        print(f"📄 Copied presentation as: index.html")
    else:
        print(f"⚠️  Template not found: {src_html}")
    
    # Copy other template files
    template_files = ["README.md"]
    
    for filename in template_files:
        src = script_dir / filename
        if src.exists():
            dst = build_dir / filename
            dst.write_text(src.read_text())
            print(f"📄 Copied template: {filename}")
        else:
            print(f"⚠️  Template not found: {src}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate presentation from schema")
    parser.add_argument("schema_file", help="Path to presentation schema JSON file")
    parser.add_argument("--output", "-o", help="Output directory (default: build/[presentation-name]-v[version])")
    parser.add_argument("--no-version", action="store_true", help="Disable versioning (overwrite existing build)")
    args = parser.parse_args()
    
    schema_file = Path(args.schema_file)
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        sys.exit(1)
    
    # Load schema to get presentation name
    schema = load_presentation_schema(schema_file)
    short_name = schema['meta'].get('short_name', schema['meta']['theme'])
    
    # Create build directory with version
    if args.output:
        build_dir = Path(args.output)
        version = None
        previous_dir = None
    elif args.no_version:
        # Use old behavior without versioning
        build_dir = Path("build") / short_name
        version = None
        previous_dir = None
    else:
        # Use versioning: build/ai-dev/v1, build/ai-dev/v2, etc.
        # Keep original short_name for directory naming
        presentation_dir = Path("build") / short_name
        presentation_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for old unversioned directory and migrate if needed
        old_unversioned_dir = Path("build") / short_name  # e.g., build/ai-dev
        if old_unversioned_dir.exists() and not any(presentation_dir.glob("v*")):
            # Migrate old unversioned directory to v1
            v1_dir = presentation_dir / "v1"
            migrate_unversioned_directory(old_unversioned_dir, v1_dir)
        
        # Find previous version
        previous_dir = find_latest_version(presentation_dir)
        
        # Get next version
        version = get_next_version(presentation_dir)
        build_dir = presentation_dir / f"v{version}"
        
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy schema to build directory
    build_schema = build_dir / "presentation_schema.json"
    build_schema.write_text(schema_file.read_text())
    print(f"📋 Copied schema to: {build_schema}")
    
    print("🎭 Unified Presentation Generator")
    print("=" * 50)
    print(f"📂 Input: {schema_file}")
    print(f"📂 Output: {build_dir}")
    if version:
        print(f"📌 Version: v{version}")
        if previous_dir:
            print(f"📎 Previous version: {previous_dir.name}")
    
    # Copy assets from previous version if available
    copied_assets = 0
    if previous_dir and previous_dir.exists():
        copied_assets = copy_existing_assets(previous_dir, build_dir)
        if copied_assets > 0:
            print(f"♻️  Copied {copied_assets} existing assets from {previous_dir.name}")
    
    try:
        # Store script directory before changing working directory
        script_dir = Path(__file__).parent
        
        # Temporarily change working directory for generation
        original_cwd = Path.cwd()
        os.chdir(build_dir)
        
        # Generate assets
        asset_dir = generate_presentation_assets("presentation_schema.json")
        
        # Create runtime slides
        create_slides_json("presentation_schema.json", "slides_runtime.json")
        
        # Return to original directory for template copying
        os.chdir(original_cwd)
        
        # Copy template files with correct paths
        copy_template_files(build_dir, script_dir)
        
        # Save version info if using versioning
        if version:
            prev_version = None
            if previous_dir:
                try:
                    prev_version = int(previous_dir.name.split('-v')[-1])
                except ValueError:
                    pass
            save_version_info(build_dir, version, prev_version)
            print(f"📝 Saved version info: version.json")
            
            # Create or update "current" symlink
            presentation_dir = build_dir.parent
            current_link = presentation_dir / "current"
            
            # Remove existing symlink if it exists
            if current_link.exists() or current_link.is_symlink():
                current_link.unlink()
            
            # Create new symlink pointing to the latest version
            try:
                current_link.symlink_to(f"v{version}")
                print(f"🔗 Created symlink: current → v{version}")
            except OSError as e:
                # Fallback for Windows or systems that don't support symlinks
                print(f"⚠️  Could not create symlink (may not be supported on this system): {e}")
        
        print("\n🎉 Generation complete!")
        print(f"📁 Build directory: {build_dir.absolute()}")
        print(f"🖼️  Assets: {asset_dir}")
        print(f"📋 Runtime slides: slides_runtime.json")
        print(f"🎨 Schema: presentation_schema.json")
        print(f"🎬 Presentation: index.html")
        if version:
            print(f"📝 Version info: version.json")
        print(f"\n🚀 To view: python -m http.server 8000 (from {build_dir})")
        print(f"   Then open: http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        sys.exit(1)

if __name__ == "__main__":
    main()