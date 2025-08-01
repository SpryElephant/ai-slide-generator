#!/usr/bin/env python3
"""
Presentation Schema Validator
Validates presentation JSON files against the defined schema.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

class SchemaValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def error(self, message: str):
        """Add an error message"""
        self.errors.append(f"❌ ERROR: {message}")
    
    def warning(self, message: str):
        """Add a warning message"""
        self.warnings.append(f"⚠️  WARNING: {message}")
    
    def validate_color(self, color: str, field_name: str) -> bool:
        """Validate color format (hex or rgba)"""
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        rgba_pattern = r'^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*[\d.]+)?\s*\)$'
        
        if re.match(hex_pattern, color) or re.match(rgba_pattern, color):
            return True
        else:
            self.error(f"{field_name} must be valid hex (#RRGGBB) or rgba() format, got: {color}")
            return False
    
    def validate_version(self, version: str) -> bool:
        """Validate semantic version format"""
        pattern = r'^\d+\.\d+\.\d+$'
        if re.match(pattern, version):
            return True
        else:
            self.error(f"version must be semantic version (x.y.z), got: {version}")
            return False
    
    def validate_date(self, date: str) -> bool:
        """Validate date format YYYY-MM-DD"""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(pattern, date):
            return True
        else:
            self.error(f"created date must be YYYY-MM-DD format, got: {date}")
            return False
    
    def validate_short_name(self, short_name: str) -> bool:
        """Validate short_name format"""
        pattern = r'^[a-z0-9-]+$'
        if re.match(pattern, short_name):
            return True
        else:
            self.error(f"short_name must be lowercase alphanumeric with hyphens only, got: {short_name}")
            return False
    
    def validate_dimensions(self, dimensions: str, field_name: str) -> bool:
        """Validate dimension format (e.g., '1792x1024')"""
        pattern = r'^\d+x\d+$'
        if re.match(pattern, dimensions):
            return True
        else:
            self.error(f"{field_name} must be WIDTHxHEIGHT format, got: {dimensions}")
            return False
    
    def validate_slide_id(self, slide_id: str) -> bool:
        """Validate slide ID format (two digits, zero-padded)"""
        pattern = r'^\d{2}$'
        if re.match(pattern, slide_id):
            return True
        else:
            self.error(f"slide id must be two-digit zero-padded (e.g., '01'), got: {slide_id}")
            return False
    
    def validate_filename_pattern(self, filename: str, pattern_type: str) -> bool:
        """Validate filename patterns"""
        if pattern_type == "slide":
            pattern = r'^SLIDE-\d{2}-[A-Za-z]+\.png$'
            if re.match(pattern, filename):
                return True
            else:
                self.error(f"slide filename must match 'SLIDE-XX-Concept.png', got: {filename}")
                return False
        elif pattern_type == "icon":
            pattern = r'^IC-[A-Za-z]+\.png$'
            if re.match(pattern, filename):
                return True
            else:
                self.error(f"icon filename must match 'IC-Name.png', got: {filename}")
                return False
        return False
    
    def validate_css_units(self, value: str, field_name: str) -> bool:
        """Validate CSS unit values"""
        # Allow common CSS units
        pattern = r'^\d+(\.\d+)?(px|em|rem|vw|vh|%)?$'
        if re.match(pattern, value):
            return True
        else:
            self.warning(f"{field_name} should use valid CSS units, got: {value}")
            return False
    
    def validate_meta(self, meta: Dict[str, Any]) -> bool:
        """Validate meta section"""
        required_fields = ["title", "short_name", "version", "created", "theme"]
        valid = True
        
        for field in required_fields:
            if field not in meta:
                self.error(f"meta.{field} is required")
                valid = False
        
        if "short_name" in meta:
            valid &= self.validate_short_name(meta["short_name"])
        
        if "version" in meta:
            valid &= self.validate_version(meta["version"])
        
        if "created" in meta:
            valid &= self.validate_date(meta["created"])
        
        return valid
    
    def validate_visual_identity(self, visual_identity: Dict[str, Any]) -> bool:
        """Validate visual_identity section"""
        required_fields = ["colors", "typography", "style_prompt", "atmosphere"]
        valid = True
        
        for field in required_fields:
            if field not in visual_identity:
                self.error(f"visual_identity.{field} is required")
                valid = False
        
        # Validate colors
        if "colors" in visual_identity:
            colors = visual_identity["colors"]
            required_colors = ["primary", "secondary", "accent", "text_primary", "text_secondary", "overlay_bg", "border"]
            
            for color_field in required_colors:
                if color_field not in colors:
                    self.error(f"visual_identity.colors.{color_field} is required")
                    valid = False
                else:
                    # Only validate hex format for primary colors
                    if color_field in ["primary", "secondary", "accent"] and isinstance(colors[color_field], str):
                        if not colors[color_field].startswith('#'):
                            self.error(f"visual_identity.colors.{color_field} should be hex format")
                            valid = False
        
        # Validate typography
        if "typography" in visual_identity:
            typography = visual_identity["typography"]
            required_typo = ["font_family", "title_size", "subtitle_size", "body_size", "small_size"]
            
            for typo_field in required_typo:
                if typo_field not in typography:
                    self.error(f"visual_identity.typography.{typo_field} is required")
                    valid = False
                elif typo_field != "font_family":
                    self.validate_css_units(typography[typo_field], f"visual_identity.typography.{typo_field}")
        
        return valid
    
    def validate_layout_system(self, layout_system: Dict[str, Any]) -> bool:
        """Validate layout_system section"""
        valid = True
        
        if "layouts" not in layout_system:
            self.error("layout_system.layouts is required")
            return False
        
        layouts = layout_system["layouts"]
        required_layouts = ["title-slide", "lf", "rf", "tb"]
        optional_layouts = ["tl", "tr", "bl", "br"]
        
        # Validate required layouts
        for layout_name in required_layouts:
            if layout_name not in layouts:
                self.error(f"layout_system.layouts.{layout_name} is required")
                valid = False
            else:
                layout = layouts[layout_name]
                required_layout_fields = ["description", "text_position", "text_zone", "max_width"]
                
                for field in required_layout_fields:
                    if field not in layout:
                        self.error(f"layout_system.layouts.{layout_name}.{field} is required")
                        valid = False
                    elif field == "max_width":
                        self.validate_css_units(layout[field], f"layout_system.layouts.{layout_name}.max_width")
        
        # Validate optional layouts if present
        for layout_name in optional_layouts:
            if layout_name in layouts:
                layout = layouts[layout_name]
                required_layout_fields = ["description", "text_position", "text_zone", "max_width"]
                
                for field in required_layout_fields:
                    if field not in layout:
                        self.error(f"layout_system.layouts.{layout_name}.{field} is required")
                        valid = False
                    elif field == "max_width":
                        self.validate_css_units(layout[field], f"layout_system.layouts.{layout_name}.max_width")
        
        return valid
    
    def validate_asset_config(self, asset_config: Dict[str, Any]) -> bool:
        """Validate asset_config section"""
        required_fields = ["dimensions", "naming_convention", "dalle_model"]
        valid = True
        
        for field in required_fields:
            if field not in asset_config:
                self.error(f"asset_config.{field} is required")
                valid = False
        
        # Validate dimensions
        if "dimensions" in asset_config:
            dimensions = asset_config["dimensions"]
            required_dims = ["background", "icons"]
            
            for dim_type in required_dims:
                if dim_type not in dimensions:
                    self.error(f"asset_config.dimensions.{dim_type} is required")
                    valid = False
                else:
                    dim_config = dimensions[dim_type]
                    if "generation_size" not in dim_config:
                        self.error(f"asset_config.dimensions.{dim_type}.generation_size is required")
                        valid = False
                    else:
                        valid &= self.validate_dimensions(
                            dim_config["generation_size"], 
                            f"asset_config.dimensions.{dim_type}.generation_size"
                        )
                    
                    if "final_size" not in dim_config:
                        self.error(f"asset_config.dimensions.{dim_type}.final_size is required")
                        valid = False
                    elif not isinstance(dim_config["final_size"], list) or len(dim_config["final_size"]) != 2:
                        self.error(f"asset_config.dimensions.{dim_type}.final_size must be [width, height] array")
                        valid = False
        
        # Validate dalle_model
        if "dalle_model" in asset_config:
            if asset_config["dalle_model"] not in ["dall-e-3", "dall-e-2"]:
                self.error(f"asset_config.dalle_model must be 'dall-e-3' or 'dall-e-2'")
                valid = False
        
        return valid
    
    def validate_slides(self, slides: List[Dict[str, Any]]) -> bool:
        """Validate slides section"""
        valid = True
        
        if not slides:
            self.error("slides array cannot be empty")
            return False
        
        slide_ids = set()
        
        for i, slide in enumerate(slides):
            required_fields = ["id", "layout", "content", "background"]
            
            for field in required_fields:
                if field not in slide:
                    self.error(f"slides[{i}].{field} is required")
                    valid = False
            
            # Validate slide ID
            if "id" in slide:
                slide_id = slide["id"]
                valid &= self.validate_slide_id(slide_id)
                
                if slide_id in slide_ids:
                    self.error(f"duplicate slide id: {slide_id}")
                    valid = False
                slide_ids.add(slide_id)
            
            # Validate layout
            if "layout" in slide:
                valid_layouts = ["title-slide", "lf", "rf", "tb", "tl", "tr", "bl", "br"]
                if slide["layout"] not in valid_layouts:
                    self.error(f"slides[{i}].layout must be one of: {valid_layouts}")
                    valid = False
            
            # Validate background
            if "background" in slide:
                background = slide["background"]
                required_bg_fields = ["filename", "concept", "prompt", "text_zones"]
                
                for field in required_bg_fields:
                    if field not in background:
                        self.error(f"slides[{i}].background.{field} is required")
                        valid = False
                
                if "filename" in background:
                    valid &= self.validate_filename_pattern(background["filename"], "slide")
                
                if "text_zones" in background:
                    text_zones = background["text_zones"]
                    if "primary" not in text_zones:
                        self.error(f"slides[{i}].background.text_zones.primary is required")
                        valid = False
        
        return valid
    
    def validate_icons(self, icons: Optional[List[Dict[str, Any]]]) -> bool:
        """Validate icons section (optional)"""
        if not icons:
            return True
        
        valid = True
        icon_filenames = set()
        
        for i, icon in enumerate(icons):
            required_fields = ["filename", "prompt", "transparent"]
            
            for field in required_fields:
                if field not in icon:
                    self.error(f"icons[{i}].{field} is required")
                    valid = False
            
            if "filename" in icon:
                filename = icon["filename"]
                valid &= self.validate_filename_pattern(filename, "icon")
                
                if filename in icon_filenames:
                    self.error(f"duplicate icon filename: {filename}")
                    valid = False
                icon_filenames.add(filename)
            
            if "transparent" in icon:
                if not isinstance(icon["transparent"], bool):
                    self.error(f"icons[{i}].transparent must be boolean")
                    valid = False
        
        return valid
    
    def validate_runtime_config(self, runtime_config: Dict[str, Any]) -> bool:
        """Validate runtime_config section"""
        required_fields = ["reveal_js", "responsive_breakpoints", "content_sizing"]
        valid = True
        
        for field in required_fields:
            if field not in runtime_config:
                self.error(f"runtime_config.{field} is required")
                valid = False
        
        # Validate reveal_js
        if "reveal_js" in runtime_config:
            reveal_js = runtime_config["reveal_js"]
            required_reveal = ["transition", "transition_speed", "background_transition", "controls", "progress", "keyboard", "touch", "hash"]
            
            for field in required_reveal:
                if field not in reveal_js:
                    self.error(f"runtime_config.reveal_js.{field} is required")
                    valid = False
            
            # Validate enum values
            if "transition" in reveal_js:
                valid_transitions = ["none", "fade", "slide", "convex", "concave", "zoom"]
                if reveal_js["transition"] not in valid_transitions:
                    self.error(f"runtime_config.reveal_js.transition must be one of: {valid_transitions}")
                    valid = False
            
            if "transition_speed" in reveal_js:
                valid_speeds = ["default", "fast", "slow"]
                if reveal_js["transition_speed"] not in valid_speeds:
                    self.error(f"runtime_config.reveal_js.transition_speed must be one of: {valid_speeds}")
                    valid = False
        
        # Validate responsive_breakpoints
        if "responsive_breakpoints" in runtime_config:
            breakpoints = runtime_config["responsive_breakpoints"]
            required_breakpoints = ["tablet", "mobile"]
            
            for field in required_breakpoints:
                if field not in breakpoints:
                    self.error(f"runtime_config.responsive_breakpoints.{field} is required")
                    valid = False
                elif not breakpoints[field].endswith('px'):
                    self.error(f"runtime_config.responsive_breakpoints.{field} must end with 'px'")
                    valid = False
        
        return valid
    
    def validate_presentation(self, data: Dict[str, Any]) -> bool:
        """Validate entire presentation schema"""
        required_sections = ["meta", "visual_identity", "layout_system", "asset_config", "slides", "runtime_config"]
        valid = True
        
        # Check required top-level sections
        for section in required_sections:
            if section not in data:
                self.error(f"required section '{section}' is missing")
                valid = False
        
        # Validate each section
        if "meta" in data:
            valid &= self.validate_meta(data["meta"])
        
        if "visual_identity" in data:
            valid &= self.validate_visual_identity(data["visual_identity"])
        
        if "layout_system" in data:
            valid &= self.validate_layout_system(data["layout_system"])
        
        if "asset_config" in data:
            valid &= self.validate_asset_config(data["asset_config"])
        
        if "slides" in data:
            valid &= self.validate_slides(data["slides"])
        
        if "icons" in data:
            valid &= self.validate_icons(data["icons"])
        
        if "runtime_config" in data:
            valid &= self.validate_runtime_config(data["runtime_config"])
        
        return valid
    
    def validate_file(self, file_path: str) -> bool:
        """Validate a presentation JSON file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for common JSON errors (but exclude URLs)
            if '/*' in content or '*/' in content:
                self.error("JSON files cannot contain block comments (/* */). Remove all comments from the file.")
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if '/*' in line or '*/' in line:
                        self.error(f"  → Comment found on line {i}: {line.strip()[:60]}...")
                return False
            
            # Check for line comments but exclude URLs
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('//') and 'http' not in stripped:
                    self.error("JSON files cannot contain line comments (//).")
                    self.error(f"  → Comment found on line {i}: {line.strip()[:60]}...")
                    return False
            
            # Check for trailing commas (common JSON error)
            if re.search(r',\s*[}\]]', content):
                self.error("JSON has trailing commas before closing brackets. Remove commas before } or ]")
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if re.search(r',\s*[}\]]', line):
                        self.error(f"  → Trailing comma on line {i}: {line.strip()}")
            
            # Try to parse JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                self.error(f"JSON parsing error at line {e.lineno}, column {e.colno}")
                self.error(f"  → Details: {e.msg}")
                
                # Show the problematic line
                lines = content.split('\n')
                if 0 < e.lineno <= len(lines):
                    problem_line = lines[e.lineno - 1]
                    self.error(f"  → Line {e.lineno}: {problem_line.strip()}")
                    if e.colno:
                        self.error(f"  → {' ' * 11}{' ' * (e.colno - 1)}^")
                return False
                
        except FileNotFoundError:
            self.error(f"file not found: {file_path}")
            return False
        
        return self.validate_presentation(data)
    
    def print_results(self, file_path: str):
        """Print validation results"""
        print(f"\n📋 Validating: {file_path}")
        print("=" * 50)
        
        if self.errors:
            print(f"\n🚨 {len(self.errors)} ERROR(S) FOUND:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNING(S):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors and not self.warnings:
            print("✅ VALIDATION PASSED - No errors or warnings found!")
        elif not self.errors:
            print(f"✅ VALIDATION PASSED - {len(self.warnings)} warnings (non-critical)")
        else:
            print(f"❌ VALIDATION FAILED - {len(self.errors)} errors must be fixed")

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_schema.py <presentation.json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    validator = SchemaValidator()
    is_valid = validator.validate_file(file_path)
    validator.print_results(file_path)
    
    if not is_valid:
        sys.exit(1)

if __name__ == "__main__":
    main()