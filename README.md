# AI-Powered Slide Presentation Generator

A sophisticated presentation system that transforms JSON schemas into stunning, AI-generated presentations with DALL-E 3 visuals and dynamic layouts.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Schema Structure](#schema-structure)
- [Build Process](#build-process)
- [Asset Generation](#asset-generation)
- [Layout System](#layout-system)
- [Link Navigation](#link-navigation)
- [Versioning System](#versioning-system)
- [File Structure](#file-structure)
- [Usage Guide](#usage-guide)
- [Advanced Features](#advanced-features)

## Overview

This presentation generator creates professional, visually stunning presentations by combining:
- **JSON Schema Definition**: Define your presentation structure, content, and visual style
- **AI-Generated Assets**: DALL-E 3 creates unique backgrounds and icons for each slide
- **Reveal.js Framework**: Powers the presentation with smooth transitions and navigation
- **Dynamic Layouts**: 8 different layout options for varied visual presentations
- **Smart Asset Management**: Reuses existing assets across versions to save time and API costs

## System Architecture

### Core Components

1. **`presentation_unified.html`**: The presentation template engine
   - Self-contained HTML file with embedded CSS and JavaScript
   - Dynamically loads presentation data from `presentation_schema.json`
   - Generates slides, styles, and navigation at runtime
   - Handles link navigation and layout positioning

2. **`generate_from_schema.py`**: The build orchestrator
   - Reads presentation schema files
   - Generates AI assets via DALL-E 3
   - Creates versioned build directories
   - Manages asset reuse across versions
   - Copies runtime files to build directory

3. **`validate_schema.py`**: Schema validation tool
   - Ensures JSON schemas conform to the expected structure
   - Validates required fields and data types
   - Helps catch errors before generation

## Schema Structure

The presentation schema is a comprehensive JSON file that defines every aspect of your presentation:

```json
{
  "meta": {
    "title": "Presentation Title",
    "author": "Your Name",
    "date": "2025-01-05",
    "version": "1.0.0",
    "theme": "theme_identifier",
    "short_name": "short-name-for-directories"
  },
  
  "visual_identity": {
    "colors": {
      "primary": "#15D4C8",
      "accent": "#FFD93D",
      "text_primary": "#FFFFFF",
      "text_secondary": "#B8B8B8",
      "bg_primary": "rgba(20,25,40,0.9)",
      "overlay_bg": "rgba(10,15,25,0.95)",
      "border": "rgba(21,212,200,0.3)"
    },
    "typography": {
      "font_family": "'Inter', -apple-system, sans-serif",
      "title_size": "3.5vw",
      "subtitle_size": "2.2vw",
      "body_size": "1.4vw",
      "small_size": "1.1vw"
    },
    "atmosphere": "Brief description for AI generation",
    "style_prompt": "Detailed style instructions for DALL-E 3"
  },
  
  "layout_system": {
    "layouts": {
      "title-slide": { "position": "center", "max_width": "60vw" },
      "lf": { "position": "left", "visual": "right", "max_width": "28vw" },
      "rf": { "position": "right", "visual": "left", "max_width": "28vw" },
      "tb": { "position": "bottom", "visual": "top", "max_width": "50vw" },
      "tl": { "position": "top-left", "max_width": "28vw" },
      "tr": { "position": "top-right", "max_width": "28vw" },
      "bl": { "position": "bottom-left", "max_width": "28vw" },
      "br": { "position": "bottom-right", "max_width": "28vw" }
    }
  },
  
  "slides": [
    {
      "id": "1",
      "layout": "title-slide",
      "background": {
        "filename": "BG-001_title.png",
        "prompt": "Specific prompt for this slide's background"
      },
      "content": {
        "title": "Slide Title",
        "subtitle": "Slide Subtitle",
        "bullets": ["Point 1", "Point 2"],
        "text": "Additional text content",
        "text_class": "normal|small",
        "icons": ["IC-001_icon.png"],
        "links": [
          {
            "text": "Link Text",
            "url": "https://example.com",
            "description": "Optional description"
          }
        ]
      }
    }
  ],
  
  "icons": [
    {
      "filename": "IC-001_icon.png",
      "prompt": "Icon generation prompt"
    }
  ],
  
  "asset_config": {
    "naming_convention": {
      "backgrounds": "BG-{number:03d}_{description}.png",
      "icons": "IC-{number:03d}_{description}.png"
    },
    "dimensions": {
      "background": {
        "generation_size": "1792x1024",
        "final_size": [1920, 1080]
      },
      "icons": {
        "generation_size": "1024x1024",
        "final_size": [512, 512]
      }
    }
  },
  
  "runtime_config": {
    "reveal_js": {
      "hash": true,
      "controls": true,
      "progress": true,
      "center": false,
      "transition": "slide"
    },
    "content_sizing": {
      "padding": "2vw",
      "corner_radius": "12px",
      "max_height": "80vh",
      "backdrop_blur": "12px",
      "border_radius": "16px"
    },
    "responsive_breakpoints": {
      "tablet": "1024px",
      "mobile": "768px"
    }
  }
}
```

## Build Process

### 1. Generation Command
```bash
python3 generate_from_schema.py your-presentation.json
```

### 2. Build Steps

1. **Schema Loading**: Reads and validates the JSON schema
2. **Version Management**: 
   - Creates next version number (v1, v2, v3...)
   - Sets up directory: `build/presentation-name/v{N}/`
3. **Asset Reuse**:
   - Copies existing assets from previous version
   - Only generates missing or new assets
4. **Asset Generation**:
   - Calls DALL-E 3 API for each missing asset
   - Downloads and resizes images to specified dimensions
   - Saves with schema-defined filenames
5. **Runtime Preparation**:
   - Copies `presentation_unified.html` as `index.html`
   - Generates `slides_runtime.json` with slide content
   - Copies schema as `presentation_schema.json`
   - Creates `version.json` with version metadata
6. **Symlink Creation**:
   - Creates/updates `current` symlink to latest version

### 3. Output Structure
```
build/
└── your-presentation-name/
    ├── current -> v3  (symlink to latest)
    ├── v1/
    ├── v2/
    └── v3/
        ├── index.html
        ├── presentation_schema.json
        ├── slides_runtime.json
        ├── version.json
        ├── README.md
        └── assets_generated/
            ├── BG-001_title.png
            ├── BG-002_overview.png
            └── IC-001_ai.png
```

## Asset Generation

### DALL-E 3 Integration

The system uses OpenAI's DALL-E 3 to generate:
- **Backgrounds**: 1792x1024 generated, resized to 1920x1080
- **Icons**: 1024x1024 generated, resized to 512x512

### Generation Process

1. **Prompt Construction**: 
   - Combines global `style_prompt` with slide-specific prompt
   - Example: `"{style_prompt} — {slide.background.prompt}"`

2. **Smart Retry Logic**:
   - 3 retry attempts for API failures
   - Exponential backoff (5s, 10s, 15s)
   - Graceful handling of network errors

3. **Asset Optimization**:
   - Downloads generated images
   - Resizes using high-quality Lanczos resampling
   - Saves as PNG with transparency support

### Asset Reuse

The versioning system intelligently reuses assets:
- Checks previous version for existing assets
- Copies unchanged assets to new version
- Only generates truly new/modified assets
- Significantly reduces API costs and generation time

## Layout System

### Available Layouts

1. **`title-slide`**: Centered content, ideal for title and section breaks
2. **`lf`** (Left Full): Content on left, visual space on right
3. **`rf`** (Right Full): Content on right, visual space on left
4. **`tb`** (Top/Bottom): Content at bottom, visual space above
5. **`tl`** (Top Left): Content in top-left corner
6. **`tr`** (Top Right): Content in top-right corner
7. **`bl`** (Bottom Left): Content in bottom-left corner
8. **`br`** (Bottom Right): Content in bottom-right corner

### Layout Features

- **Responsive Sizing**: Content boxes sized with viewport units (vw/vh)
- **Maximum Widths**: Each layout has configurable max-width
- **Backdrop Effects**: Blur and transparency for readability
- **Smooth Animations**: Fade-in transitions for content elements

## Link Navigation

### Link Button System

Slides with links feature a circular button in the bottom-right corner:
- **Link Icon**: Indicates links are available
- **Click to Toggle**: Switches between content and links view
- **Smooth Transition**: Content fades out, links fade in
- **X Icon**: Shows when viewing links, click to return

### Link Styling

- Styled as buttons with hover effects
- Support for link text and optional descriptions
- Open in new tabs for safety
- Consistent styling across all layouts

## Versioning System

### Automatic Versioning

- Each generation creates a new version directory
- Versions are numbered sequentially (v1, v2, v3...)
- `current` symlink always points to latest version
- Previous versions are preserved for rollback

### Version Benefits

1. **Asset Preservation**: Never lose previously generated assets
2. **Experimentation**: Try different schemas without losing work
3. **Rollback Capability**: Easy to revert to previous versions
4. **Development Workflow**: Test changes without affecting production

## File Structure

### Project Files

```
slide_presentation_generator/
├── README.md                    # This file
├── SCHEMA.md                   # Detailed schema documentation
├── LAYOUT_GUIDE.md            # Visual layout guide
├── presentation_unified.html   # Core presentation template
├── generate_from_schema.py     # Build script
├── validate_schema.py          # Schema validator
├── presentation.schema.json    # JSON schema definition
└── build/                      # Generated presentations
```

### Presentation Files

- **`your-presentation.json`**: Source schema file
- **`ai_presentation_2025.json`**: Example AI developer presentation
- **`layout-demo.json`**: Demo of all 8 layouts
- **`ai_four.json`**: Another example presentation

## Usage Guide

### Creating a New Presentation

1. **Copy an example schema**:
   ```bash
   cp ai_presentation_2025.json my-presentation.json
   ```

2. **Edit the schema**:
   - Update meta information
   - Modify visual identity (colors, fonts)
   - Define your slides with content and prompts
   - Add any custom icons needed

3. **Validate your schema**:
   ```bash
   python3 validate_schema.py my-presentation.json
   ```

4. **Generate the presentation**:
   ```bash
   python3 generate_from_schema.py my-presentation.json
   ```

5. **View the presentation**:
   ```bash
   cd build/my-presentation/current
   python3 -m http.server 8000
   # Open http://localhost:8000 in browser
   ```

### Example: Creating a Team Transformation Presentation with AI

Here's a comprehensive example of how to create an energizing team presentation using AI tools:

#### 1. Start with Your Raw Content

Provide your presentation content to an AI assistant. For example:

```
Create a slide presentation with upbeat/energetic tone. Here's my content:

Tomorrow morning we're having a prime team meeting, and I'm excited about what we're going to discuss.
I know the September 30th deadline feels overwhelming right now - and that's totally understandable. 
But here's the thing: this is our moment to level up and become the absolute best AI-assisted 
development team we can be. This is our call to arms!

We're making some game-changing moves:
- We're becoming ONE unified team - no more front-end vs back-end silos
- We're unleashing you as developers - no more mandatory PRs!
- Direct communication wins - got a question? Slack whoever can answer it directly
- Marite's joining our scrums - closing that design-dev communication gap
- Daily AI skill building - invest time each day getting better with AI coding
- Weekly CodeRabbit improvements - who can own this for us?
- Supercharged development cycle - smaller stories that ship as complete work
- Daily commits, daily deliverables - everyone commits code every single day
- QA gets fed daily - with 4-6 developers all following this method
- The whole system flows - everything just works more smoothly
```

#### 2. Study the Example Structure

Look at `ai_presentation_2025.json` to understand:
- **Visual consistency through `style_prompt`** (line 28): A base prompt used for ALL backgrounds
- **Individual slide prompts** that build on the base style while adding unique concepts
- **Text zone specifications** in prompts (e.g., "left third (0-640px) kept dark for text overlay")
- **Color palette consistency** across all visual elements

#### 3. Understand Schema Requirements

Reference `presentation.schema.json` to ensure your JSON includes:
- All required sections: `meta`, `visual_identity`, `layout_system`, `asset_config`, `slides`, `runtime_config`
- Proper formatting for colors (hex for primary colors)
- Valid layout types: `title-slide`, `lf`, `rf`, `tb`, `tl`, `tr`, `bl`, `br`
- Correct filename patterns: `SLIDE-XX-Concept.png` for backgrounds, `IC-Name.png` for icons

#### 4. AI Creates Your Presentation JSON

The AI will generate a complete JSON schema with:

**Visual Identity** (maintaining consistency):
```json
"style_prompt": "Bright energetic workspace; vibrant orange #FF6B35 + electric blue #0077FF with warm yellow #FFC947 accents; natural lighting with motion blur suggesting speed; clean modern tech environment; high contrast dynamic compositions; 8K sharp render; no watermarks.",
```

**Individual Slide Backgrounds** (building on base style):
```json
"prompt": "Team of diverse developers silhouettes at sunrise on mountain peak, arms raised in victory pose; golden orange sunburst with speed lines radiating outward; middle 40% kept darker for title overlay; sense of triumph and new beginnings."
```

**Matching Tone to Content**:
- Energetic content → Bright, dynamic colors (orange, blue, yellow)
- Professional content → Deep, sophisticated colors (indigo, violet, teal)
- Technical content → Clean, modern aesthetics with tech elements

#### 5. Validate Your Schema

Before generating assets:
```bash
python3 validate_schema.py team_transformation_sept30.json
```

This catches:
- Missing required fields
- Invalid color formats
- Incorrect filename patterns
- JSON syntax errors

#### 6. Generate Your Presentation

```bash
# First time setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Generate presentation
python3 generate_from_schema.py team_transformation_sept30.json
```

#### 7. View Your Results

```bash
cd build/team-transformation-sept30/current
python3 -m http.server 8000
# Open http://localhost:8000 in browser
```

### Key Tips for Consistent AI-Generated Backgrounds

1. **Base Style Prompt**: Define once in `visual_identity.style_prompt`
   - Include color palette with hex codes
   - Specify lighting and atmosphere
   - Add technical requirements (8K, no watermarks, etc.)

2. **Individual Prompts**: Each slide's `background.prompt`
   - Start with unique concept/scene
   - Include base style elements
   - Specify text zones explicitly
   - Maintain visual vocabulary

3. **Color Consistency**:
   - Always reference your hex colors in prompts
   - Use same lighting approach throughout
   - Keep similar compositional rules

4. **Text Zone Protection**:
   - Explicitly state which areas to keep dark
   - Use pixel measurements (0-640px, 720-1080px)
   - Match zones to your layout system

### Example Visual Consistency Pattern

```
Base: "vibrant orange #FF6B35 + electric blue #0077FF; bright workspace"
Slide 1: "[unique scene]; [base colors]; [text zone dark]"
Slide 2: "[different scene]; [same base colors]; [appropriate text zone dark]"
```

This ensures every background feels part of the same presentation while having unique visual interest!

### Updating a Presentation

Simply edit your schema and regenerate:
- Assets matching existing filenames are reused
- Only new/changed assets are generated
- Version number auto-increments

### Navigation Controls

- **Arrow Keys**: Navigate between slides
- **Space**: Next slide
- **ESC**: Overview mode
- **F**: Fullscreen
- **Link Button**: Toggle links view (when available)

## Advanced Features

### Custom Styling

The visual identity system supports:
- Custom color schemes with transparency
- Typography scaling with viewport units
- Backdrop filters for modern glass effects
- Configurable corner radius and borders

### Responsive Design

- Breakpoints for tablet and mobile
- Content reflows for smaller screens
- Font sizes scale appropriately
- All content centers on mobile

### Debug Mode

Content boxes show their layout type in debug mode:
- Small label above each content box
- Helps verify correct layout application
- Can be disabled in production

### API Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
# Or use a .env file
```

### Performance Optimization

- Assets are generated once and reused
- Lazy loading for smooth initial load
- Efficient DOM generation
- Minimal external dependencies

## Troubleshooting

### Common Issues

1. **Assets not generating**: Check API key and network connection
2. **Schema validation errors**: Use validate_schema.py to debug
3. **Links not showing**: Ensure links array exists in slide content
4. **Background scaling**: Check viewport settings in browser

### Best Practices

1. **Asset Naming**: Use descriptive names in your prompts
2. **Prompt Quality**: Be specific about visual style and elements
3. **Version Control**: Keep your schema files in git
4. **Asset Backup**: Periodically backup the build directory

## Future Enhancements

Potential improvements for the system:
- PDF export functionality
- Speaker notes support
- Animation timeline control
- Theme marketplace
- Collaborative editing
- Real-time preview during editing

---

Built with ❤️ using Reveal.js, DALL-E 3, and Python