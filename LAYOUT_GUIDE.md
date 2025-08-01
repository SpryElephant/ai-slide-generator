# Layout System Guide

## Available Layouts

The presentation system supports 8 layouts (4 required + 4 optional):

### 1. `title-slide` - Centered Title Layout
- **Position**: Content centered both horizontally and vertically
- **Max Width**: 60vw
- **Use Case**: Opening slides, section dividers
- **Text Alignment**: Center
- **Visual Zone**: Full screen background

### 2. `lf` - Left-Focused Layout  
- **Position**: Content on left side, vertically centered
- **Max Width**: 28vw
- **Use Case**: Text on left, visual emphasis on right
- **Text Alignment**: Left
- **Visual Zone**: Right 2/3 of screen (640-1920px)

### 3. `rf` - Right-Focused Layout
- **Position**: Content on right side, vertically centered  
- **Max Width**: 28vw
- **Use Case**: Visual emphasis on left, text on right
- **Text Alignment**: Left
- **Visual Zone**: Left 2/3 of screen (0-1280px)

### 4. `tb` - Top-Bottom Layout
- **Position**: Content at bottom center
- **Max Width**: 50vw
- **Use Case**: Banner visual on top, text below
- **Text Alignment**: Center
- **Visual Zone**: Top 2/3 of screen (0-720px)

### 5. `tl` - Top-Left Layout (Optional)
- **Position**: Content in top-left corner
- **Max Width**: 28vw
- **Use Case**: Corner callouts, annotations
- **Text Alignment**: Left
- **Visual Zone**: Bottom-right area

### 6. `tr` - Top-Right Layout (Optional)
- **Position**: Content in top-right corner
- **Max Width**: 28vw
- **Use Case**: Corner annotations, secondary info
- **Text Alignment**: Left
- **Visual Zone**: Bottom-left area

### 7. `bl` - Bottom-Left Layout (Optional)
- **Position**: Content in bottom-left corner
- **Max Width**: 28vw
- **Use Case**: Citations, footnotes
- **Text Alignment**: Left
- **Visual Zone**: Top-right area

### 8. `br` - Bottom-Right Layout (Optional)
- **Position**: Content in bottom-right corner
- **Max Width**: 28vw
- **Use Case**: Page numbers, metadata
- **Text Alignment**: Left
- **Visual Zone**: Top-left area

## How Layouts Work

1. **Background Images**: Full screen coverage with text zones
2. **Content Wrapper**: Semi-transparent overlay containing text
3. **Positioning**: CSS absolute positioning based on layout type
4. **Animations**: Fade-in effects with staggered delays
5. **Responsive**: All layouts center on mobile devices

## Debug Mode

The presentation includes a debug label showing the layout type above each content box. This helps verify layouts are working correctly.

## Text Zone Guidelines

When creating background images, ensure dark/clear areas in these zones:
- **title-slide**: Center 40% of canvas
- **lf**: Left third (0-640px width)
- **rf**: Right third (1280-1920px width)  
- **tb**: Bottom third (720-1080px height)
- **tl**: Top-left corner (0-640px width, 0-360px height)
- **tr**: Top-right corner (1280-1920px width, 0-360px height)
- **bl**: Bottom-left corner (0-640px width, 720-1080px height)
- **br**: Bottom-right corner (1280-1920px width, 720-1080px height)

## Links Feature

Each slide can include optional clickable links that appear with special navigation:

### How Links Work
1. **Initial State**: Links are hidden when slide loads
2. **Arrow Key Behavior**: On slides with links, pressing → or Space shows links instead of advancing
3. **Second Press**: After links are shown, → or Space advances to next slide
4. **Reset**: Links hide again when changing slides

### Schema Format
```json
"content": {
  "title": "Your Title",
  "bullets": ["..."],
  "links": [
    {
      "text": "Link Text",
      "url": "https://example.com",
      "description": "Optional description" 
    }
  ]
}
```

### Link Properties
- **text** (required): Display text for the link
- **url** (required): Target URL (opens in new tab)
- **description** (optional): Additional text shown below link

### Visual Styling
- Electric teal accent color with hover effects
- Semi-transparent background with backdrop blur
- Smooth slide-in animation from the right
- Hover: background fills with accent color

## Troubleshooting

If layouts aren't working:
1. Check browser console for JavaScript errors
2. Verify schema has correct layout names
3. Ensure CSS classes match (layout-title-slide, layout-lf, etc.)
4. Look for the debug label to confirm layout assignment
5. Check if responsive styles are overriding desktop layouts

If links aren't working:
1. Verify links array is properly formatted in schema
2. Check browser console for navigation setup messages
3. Ensure URLs are valid and include protocol (https://)