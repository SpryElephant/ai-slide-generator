# 📋 Unified Presentation Schema Documentation

## Schema Structure

```json
{
  "meta": { /* Presentation metadata */ },
  "visual_identity": { /* Branding and styling */ },
  "layout_system": { /* Layout definitions */ },
  "asset_config": { /* Generation settings */ },
  "slides": [ /* Slide definitions */ ],
  "icons": [ /* Icon definitions */ ],
  "runtime_config": { /* Presentation settings */ }
}
```

## 📝 Detailed Field Specifications

### `meta` - Presentation Metadata
```json
{
  "meta": {
    "title": "string",           // Display title
    "short_name": "string",      // Short directory name (e.g. "ai-dev")
    "version": "string",         // Version number
    "created": "YYYY-MM-DD",     // Creation date
    "theme": "string",           // Theme identifier
    "description": "string"      // Brief description
  }
}
```

### `visual_identity` - Brand & Style Configuration
```json
{
  "visual_identity": {
    "colors": {
      "primary": "#HEX",         // Main background color
      "secondary": "#HEX",       // Secondary color
      "accent": "#HEX",          // Highlight color
      "text_primary": "#HEX",    // Main text color
      "text_secondary": "#HEX",  // Secondary text color
      "overlay_bg": "rgba(...)", // Content box background
      "border": "rgba(...)"      // Border color
    },
    "typography": {
      "font_family": "string",   // CSS font stack
      "title_size": "string",    // H1 font size (vw units)
      "subtitle_size": "string", // H2 font size (vw units)
      "body_size": "string",     // Body text size (vw units)
      "small_size": "string"     // Small text size (vw units)
    },
    "style_prompt": "string",    // Base DALL-E style prompt
    "atmosphere": "string"       // Visual atmosphere description
  }
}
```

### `layout_system` - Layout Definitions
```json
{
  "layout_system": {
    "layouts": {
      "layout_name": {
        "description": "string",    // Layout description
        "text_position": "string",  // Position identifier
        "text_zone": "string",      // Text area specification
        "max_width": "string"       // Maximum content width
      }
    }
  }
}
```

**Standard Layouts:**
- `title-slide`: Centered title/subtitle
- `lf`: Content left, visual right
- `rf`: Content right, visual left  
- `tb`: Content bottom, visual top

### `asset_config` - Generation Settings
```json
{
  "asset_config": {
    "dimensions": {
      "background": {
        "generation_size": "WIDTHxHEIGHT", // DALL-E generation size
        "final_size": [width, height]       // Final image dimensions
      },
      "icons": {
        "generation_size": "WIDTHxHEIGHT",
        "final_size": [width, height]
      }
    },
    "naming_convention": "string",    // File naming pattern
    "dalle_model": "string"          // DALL-E model version
  }
}
```

### `slides` - Slide Definitions
```json
{
  "slides": [
    {
      "id": "string",              // Unique slide identifier
      "layout": "string",          // Layout type (from layout_system)
      "content": {
        "title": "string",         // Slide title (optional)
        "subtitle": "string",      // Slide subtitle (optional)
        "bullets": ["string"],     // Bullet points (optional)
        "text": "string",          // Paragraph text (optional)
        "text_class": "string",    // CSS class for text (optional)
        "icons": ["filename"]      // Icon filenames (optional)
      },
      "background": {
        "filename": "string",      // Background image filename
        "concept": "string",       // Concept name for reference
        "prompt": "string",        // DALL-E generation prompt
        "text_zones": {
          "primary": "string"      // Text zone specification
        }
      }
    }
  ]
}
```

### `icons` - Icon Definitions  
```json
{
  "icons": [
    {
      "filename": "string",       // Icon filename
      "prompt": "string",         // DALL-E generation prompt
      "transparent": boolean      // Whether icon should be transparent
    }
  ]
}
```

### `runtime_config` - Presentation Runtime Settings
```json
{
  "runtime_config": {
    "reveal_js": {
      "transition": "string",           // Slide transition type
      "transition_speed": "string",     // Transition speed
      "background_transition": "string", // Background transition
      "controls": boolean,              // Show navigation controls
      "progress": boolean,              // Show progress bar
      "keyboard": boolean,              // Enable keyboard navigation
      "touch": boolean,                 // Enable touch navigation
      "hash": boolean                   // Enable URL hashing
    },
    "responsive_breakpoints": {
      "tablet": "string",               // Tablet breakpoint (px)
      "mobile": "string"                // Mobile breakpoint (px)
    },
    "content_sizing": {
      "max_height": "string",           // Max content height
      "border_radius": "string",        // Content box border radius
      "backdrop_blur": "string"         // Backdrop blur amount
    }
  }
}
```

## 🎨 Background Prompt Guidelines

### Text Zone Specifications
Always include specific pixel ranges for text areas:

```
"Left third (0-640px width) kept dark for text overlay"
"Bottom third (720-1080px height) dark zone for text"
"Center horizontal band (400-680px height) minimal for text"
"Right third (1280-1920px width) darker for text overlay"
```

### Visual Consistency Requirements
- Use the `style_prompt` from `visual_identity` as base
- Maintain consistent lighting direction
- Use the same color palette across all slides
- Specify atmospheric depth and cinematic quality

### Example Background Prompt Structure
```
"[STYLE_PROMPT] — [SCENE_DESCRIPTION]; [TEXT_ZONE_SPEC]; [VISUAL_ELEMENTS]; [LIGHTING_ATMOSPHERE]"
```

## 🔧 Usage Patterns

### Creating New Presentations
1. Copy existing schema as template
2. Update `meta` information
3. Modify `visual_identity` for new brand/theme
4. Design slide content and background concepts
5. Generate assets with `generate_from_schema.py`
6. Present with `presentation_unified.html`

### Customizing Visual Identity
```json
{
  "visual_identity": {
    "colors": {
      "primary": "#YOUR_PRIMARY",
      "accent": "#YOUR_ACCENT"
    },
    "style_prompt": "Your visual style description with specific artistic direction"
  }
}
```

### Adding New Layouts
```json
{
  "layout_system": {
    "layouts": {
      "custom_layout": {
        "description": "Custom layout description",
        "text_position": "position_identifier", 
        "text_zone": "Specific pixel area description",
        "max_width": "CSS width value"
      }
    }
  }
}
```

## ✅ Validation Rules

### Required Fields
- `meta.title`
- `visual_identity.style_prompt`
- `slides[].id`
- `slides[].layout`
- `slides[].background.filename`
- `slides[].background.prompt`

### Naming Conventions
- Slide IDs: `"01"`, `"02"`, etc. (zero-padded)
- Background files: `"SLIDE-XX-Concept.png"`
- Icon files: `"IC-Name.png"`

### Layout Requirements
- Each layout must exist in `layout_system.layouts`
- Text zones must specify pixel ranges
- Max widths should use viewport units (vw)

---

📋 **Schema Version 1.0.0**  
*Unified Presentation System*