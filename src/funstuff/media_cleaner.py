#!/usr/bin/env python3
"""
Advanced media cleaner with interactive HTML report.
Identifies duplicates, similar photos, screenshots, bad videos, and bad photos.
"""

import os
import hashlib
import json
import shutil
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from datetime import datetime
import argparse
import base64
from urllib.parse import quote

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Installing required packages...")
    os.system("pip install Pillow numpy opencv-python")
    from PIL import Image
    import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import imagehash
except ImportError:
    print("Installing imagehash for similarity detection...")
    os.system("pip install imagehash")
    import imagehash

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    print("⚠️  pillow-heif not installed. HEIC/HEIF files will be skipped.")
    print("   To enable HEIC support, run: pip install pillow-heif")
    HEIC_SUPPORT = False


class MediaAnalyzer:
    def __init__(self, min_size_kb=50, min_dimension=100, similarity_threshold=10):
        """
        Args:
            min_size_kb: Minimum file size in KB
            min_dimension: Minimum image dimension
            similarity_threshold: Hamming distance for perceptual hash (lower = more similar)
        """
        self.min_size_kb = min_size_kb
        self.min_dimension = min_dimension
        self.similarity_threshold = similarity_threshold
        self.duplicates = defaultdict(list)
        self.similar_photos = []  # Groups of similar photos
        self.bad_photos = []
        self.bad_videos = []
        self.screenshots = []
        self.irrelevant_files = []
        self.hash_map = {}  # For similarity detection

    def get_file_hash(self, filepath: str, chunk_size=65536) -> str:
        """Get SHA256 hash of file for duplicate detection."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"  Error hashing {filepath}: {e}")
            return None

    def is_blurry(self, image_path: str, threshold=80) -> bool:
        """
        Detect blurry images using Laplacian variance.
        Lower threshold = stricter (more images flagged as blurry).
        Default 80 catches most accidental/bad shots.
        """
        if cv2 is None:
            return False
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return True
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            return laplacian_var < threshold
        except Exception:
            return False

    def is_underexposed(self, image_path: str) -> bool:
        """Detect very dark images."""
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img)
            avg_brightness = np.mean(pixels)
            return avg_brightness < 30
        except Exception:
            return False

    def is_overexposed(self, image_path: str) -> bool:
        """Detect very bright/washed out images."""
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img)
            avg_brightness = np.mean(pixels)
            return avg_brightness > 220 and np.std(pixels) < 30
        except Exception:
            return False

    def is_uniform_color(self, image_path: str) -> bool:
        """Detect blank/solid color shots."""
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img)
            return np.std(pixels) < 20
        except Exception:
            return False

    def analyze_image(self, filepath: str) -> Tuple[bool, List[str]]:
        """Analyze image for quality issues."""
        reasons = []

        try:
            img = Image.open(filepath)
            width, height = img.size

            if width < self.min_dimension or height < self.min_dimension:
                reasons.append(f"too small ({width}x{height})")

            file_size_kb = os.path.getsize(filepath) / 1024
            if file_size_kb < self.min_size_kb:
                reasons.append(f"tiny file ({file_size_kb:.1f}KB)")

            if self.is_blurry(filepath):
                reasons.append("blurry")
            if self.is_underexposed(filepath):
                reasons.append("too dark")
            if self.is_overexposed(filepath):
                reasons.append("overexposed")
            if self.is_uniform_color(filepath):
                reasons.append("blank/solid color")

        except Exception as e:
            reasons.append(f"unreadable: {e}")

        # Additional checks for images to discard
        if self.is_pure_black(filepath):
            reasons.append("completely black")
        if self.is_pure_white(filepath):
            reasons.append("blown out white")
        if self.is_extreme_aspect_ratio(filepath):
            reasons.append("extreme aspect ratio")

        return len(reasons) > 0, reasons

    def is_pure_black(self, image_path: str) -> bool:
        """Detect completely black images (camera in pocket, lens cap, etc)."""
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img)
            avg_brightness = np.mean(pixels)
            # Very dark - avg < 10 on 0-255 scale
            return avg_brightness < 10
        except Exception:
            return False

    def is_pure_white(self, image_path: str) -> bool:
        """Detect completely blown-out white images (flash accident, pointing at light)."""
        try:
            img = Image.open(image_path).convert("RGB")
            pixels = np.array(img)
            avg_brightness = np.mean(pixels)
            # Very bright with low variation
            color_std = np.std(pixels)
            return avg_brightness > 245 and color_std < 10
        except Exception:
            return False

    def is_extreme_aspect_ratio(self, image_path: str) -> bool:
        """Detect images with extreme aspect ratios (cropped wrong, partial captures)."""
        try:
            img = Image.open(image_path)
            width, height = img.size
            ratio = width / height if height > 0 else 0

            # Extreme ratios: very wide (>4:1) or very tall (>4:1)
            # These are often accidental crops or test shots
            return ratio > 4 or ratio < 0.25
        except Exception:
            return False

    def is_screenshot(self, filepath: str) -> bool:
        """Detect screenshots by analyzing patterns and metadata."""
        try:
            img = Image.open(filepath)
            width, height = img.size

            # Common screenshot aspect ratios
            ratio = width / height if height > 0 else 0

            # Screenshots are often full-width or have specific aspect ratios
            # Check for common screen resolutions
            common_widths = [1920, 1280, 1024, 800, 640, 2560, 3840]
            is_standard_width = width in common_widths

            # Check for high aspect ratio (landscape) - typical of screenshots
            is_wide = ratio > 1.5

            # Screenshot markers: check for common UI patterns (white backgrounds, consistent colors at edges)
            pixels = np.array(img.convert("RGB"))

            # Many screenshots have white or near-white edges (UI frames)
            top_edge = np.mean(pixels[0:5, :])  # Top pixels
            bottom_edge = np.mean(pixels[-5:, :])  # Bottom pixels
            left_edge = np.mean(pixels[:, 0:5])  # Left pixels
            right_edge = np.mean(pixels[:, -5:])  # Right pixels

            # If edges are very light (white-ish), likely UI frame
            edge_values = [top_edge, bottom_edge, left_edge, right_edge]
            light_edges = sum(1 for e in edge_values if e > 200)

            return (is_standard_width or is_wide) and light_edges >= 2

        except Exception:
            return False

    def get_perceptual_hash(self, filepath: str):
        """Get perceptual hash for similarity detection."""
        try:
            img = Image.open(filepath)
            # Use average hash (fast and good for similar photos)
            return imagehash.average_hash(img)
        except Exception:
            return None

    def analyze_video(self, filepath: str) -> Tuple[bool, List[str]]:
        """Analyze video for quality issues."""
        reasons = []

        try:
            if cv2 is None:
                return False, ["ffprobe not available"]

            cap = cv2.VideoCapture(filepath)
            if not cap.isOpened():
                return True, ["corrupted or unplayable"]

            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            cap.release()

            # Check for issues
            if frame_count < 5:
                reasons.append(f"too short ({frame_count} frames)")
            if width < 320 or height < 240:
                reasons.append(f"low resolution ({width}x{height})")
            if fps < 15:
                reasons.append(f"very low FPS ({fps:.1f})")

            file_size_kb = os.path.getsize(filepath) / 1024
            if file_size_kb < 100:  # Videos should be larger
                reasons.append(f"suspiciously small ({file_size_kb:.1f}KB)")

        except Exception as e:
            reasons.append(f"unreadable: {e}")

        return len(reasons) > 0, reasons

    def is_live_photo_video(self, filepath: str) -> bool:
        """
        Detect if this is the MOV file from an iPhone Live Photo.
        Live photos have paired .HEIC + .MOV files with the same base name.
        """
        if filepath.lower().endswith('.mov'):
            # Check if there's a corresponding .heic or .heif
            base_path = filepath.rsplit('.', 1)[0]
            heic_path = base_path + '.heic'
            heif_path = base_path + '.heif'
            if os.path.exists(heic_path) or os.path.exists(heif_path):
                return True  # This MOV is the video part of a Live Photo
        return False

    def is_valid_media(self, filepath: str) -> bool:
        """Check if file is valid media."""
        valid_extensions = {
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
            ".heic", ".heif",  # Apple formats
            ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"
        }
        return Path(filepath).suffix.lower() in valid_extensions

    def scan_directory(self, directory: str) -> None:
        """Scan directory for duplicates, similar photos, bad photos, and bad videos."""
        print(f"Scanning {directory}...")
        hashes = {}
        total_files = 0
        image_count = 0
        video_count = 0

        # First pass: collect exact duplicates and hashes
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                total_files += 1

                if not self.is_valid_media(filepath):
                    self.irrelevant_files.append({
                        "path": filepath,
                        "reason": "unsupported file type"
                    })
                    continue

                # Exact duplicate detection
                file_hash = self.get_file_hash(filepath)
                if file_hash:
                    if file_hash in hashes:
                        self.duplicates[file_hash].append(filepath)
                    else:
                        hashes[file_hash] = filepath

                # Image analysis
                if filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif')):
                    image_count += 1

                    # Check HEIC support
                    if filepath.lower().endswith(('.heic', '.heif')) and not HEIC_SUPPORT:
                        self.bad_photos.append({
                            "path": filepath,
                            "issues": ["HEIC format not supported - install pillow-heif"],
                            "type": "unsupported_format"
                        })
                        continue

                    is_bad, reasons = self.analyze_image(filepath)
                    if is_bad:
                        self.bad_photos.append({
                            "path": filepath,
                            "issues": reasons,
                            "type": "bad_quality"
                        })

                    # Screenshot detection
                    if self.is_screenshot(filepath):
                        self.screenshots.append({
                            "path": filepath,
                            "reason": "screenshot detected"
                        })

                    # Get perceptual hash for similarity
                    ph = self.get_perceptual_hash(filepath)
                    if ph:
                        self.hash_map[filepath] = ph

                # Video analysis
                elif filepath.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm')):
                    video_count += 1

                    # Check if this is a Live Photo video file
                    is_live_video = self.is_live_photo_video(filepath)

                    is_bad, reasons = self.analyze_video(filepath)
                    if is_live_video:
                        reasons.insert(0, "Live Photo video (paired with .heic)")

                    if is_bad or is_live_video:
                        self.bad_videos.append({
                            "path": filepath,
                            "issues": reasons
                        })

        # Second pass: find similar photos (after all hashes collected)
        self._find_similar_photos()

        print(f"Scanned {total_files} files ({image_count} images, {video_count} videos)")

    def _find_similar_photos(self) -> None:
        """Find groups of similar photos using perceptual hashing."""
        if not self.hash_map:
            return

        grouped = set()
        similar_groups = []

        filepaths = list(self.hash_map.keys())
        for i, filepath1 in enumerate(filepaths):
            if filepath1 in grouped:
                continue

            group = [filepath1]
            hash1 = self.hash_map[filepath1]

            for filepath2 in filepaths[i+1:]:
                if filepath2 in grouped:
                    continue

                hash2 = self.hash_map[filepath2]
                distance = hash1 - hash2

                if distance <= self.similarity_threshold:
                    group.append(filepath2)
                    grouped.add(filepath2)

            if len(group) > 1:
                grouped.add(filepath1)
                similar_groups.append(group)
                self.similar_photos.append({
                    "group": group,
                    "count": len(group)
                })

    def get_thumbnail_base64(self, filepath: str, size=200) -> str:
        """Create base64 thumbnail for HTML embedding."""
        try:
            img = Image.open(filepath)
            img.thumbnail((size, size))

            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img

            import io
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/jpeg;base64,{img_str}"
        except Exception:
            return None

    def generate_html_report(self, output_file="media_report.html") -> None:
        """Generate interactive HTML report."""

        # Prepare data
        duplicate_groups = []
        for file_hash, files in self.duplicates.items():
            if len(files) > 1:
                duplicate_groups.append({
                    "hash": file_hash[:8],
                    "files": files,
                    "count": len(files)
                })

        bad_photos_sorted = sorted(
            self.bad_photos,
            key=lambda x: len(x['issues']),
            reverse=True
        )[:100]

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Cleaner Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f5f7fa;
            border-bottom: 1px solid #e0e0e0;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .stat-card h3 {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}

        .section {{
            padding: 30px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .section h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .controls {{
            background: #f5f7fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .controls button {{
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .btn-select-all {{
            background: #667eea;
            color: white;
        }}

        .btn-select-all:hover {{
            background: #5568d3;
        }}

        .btn-delete {{
            background: #ff6b6b;
            color: white;
        }}

        .btn-delete:hover {{
            background: #ff5252;
        }}

        .checkbox {{
            cursor: pointer;
            width: 18px;
            height: 18px;
        }}

        .duplicate-group {{
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            overflow: hidden;
        }}

        .group-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            cursor: pointer;
            user-select: none;
        }}

        .group-header:hover {{
            color: #667eea;
        }}

        .group-title {{
            flex: 1;
            font-weight: 600;
        }}

        .group-count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
        }}

        .file-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }}

        .file-item input[type="checkbox"] {{
            flex-shrink: 0;
        }}

        .file-info {{
            flex: 1;
            min-width: 0;
        }}

        .file-name {{
            font-weight: 500;
            color: #333;
            word-break: break-all;
            font-size: 0.95em;
        }}

        .file-details {{
            font-size: 0.85em;
            color: #888;
            margin-top: 4px;
        }}

        .file-action {{
            flex-shrink: 0;
            display: flex;
            gap: 8px;
        }}

        .btn-small {{
            padding: 4px 8px;
            font-size: 0.8em;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btn-view {{
            background: #667eea;
            color: white;
        }}

        .btn-view:hover {{
            background: #5568d3;
        }}

        .btn-delete-single {{
            background: #ff6b6b;
            color: white;
        }}

        .btn-delete-single:hover {{
            background: #ff5252;
        }}

        .bad-photo-item {{
            background: #fff9f0;
            border: 1px solid #ffe0b2;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
        }}

        .bad-photo-item.critical {{
            background: #ffebee;
            border-color: #ffcdd2;
        }}

        .thumbnail {{
            flex-shrink: 0;
            width: 120px;
            height: 120px;
            background: #f0f0f0;
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .thumbnail.no-image {{
            color: #999;
            font-size: 0.9em;
        }}

        .bad-photo-content {{
            flex: 1;
        }}

        .bad-photo-name {{
            font-weight: 600;
            color: #333;
            margin-bottom: 6px;
            word-break: break-all;
        }}

        .issue-badges {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}

        .issue-badge {{
            background: #ff6b6b;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}

        .file-size {{
            color: #888;
            font-size: 0.9em;
        }}

        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }}

        .modal.active {{
            display: flex;
        }}

        .modal-content {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 400px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}

        .modal-content h3 {{
            margin-bottom: 15px;
            color: #333;
        }}

        .modal-content p {{
            color: #666;
            margin-bottom: 20px;
            line-height: 1.5;
        }}

        .modal-buttons {{
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }}

        .btn-cancel {{
            padding: 8px 16px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
        }}

        .btn-confirm {{
            padding: 8px 16px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }}

        .btn-confirm:hover {{
            background: #ff5252;
        }}

        .footer {{
            padding: 20px 30px;
            background: #f5f7fa;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        .toggle {{
            display: inline-block;
            width: 20px;
            height: 20px;
            text-align: center;
            font-size: 1.2em;
        }}

        .irrelevant-files {{
            max-height: 300px;
            overflow-y: auto;
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 10px;
        }}

        .file-path {{
            padding: 8px;
            border-bottom: 1px solid #e0e0e0;
            font-family: monospace;
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
        }}

        .file-path:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧹 Media Cleaner Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="summary">
            <div class="stat-card">
                <h3>Exact Duplicates</h3>
                <div class="number">{len(duplicate_groups)}</div>
            </div>
            <div class="stat-card">
                <h3>Similar Photos</h3>
                <div class="number">{len(self.similar_photos)}</div>
            </div>
            <div class="stat-card">
                <h3>Bad Photos</h3>
                <div class="number">{len(bad_photos_sorted)}</div>
            </div>
            <div class="stat-card">
                <h3>Bad Videos</h3>
                <div class="number">{len(self.bad_videos)}</div>
            </div>
            <div class="stat-card">
                <h3>Screenshots</h3>
                <div class="number">{len(self.screenshots)}</div>
            </div>
            <div class="stat-card">
                <h3>Irrelevant Files</h3>
                <div class="number">{len(self.irrelevant_files)}</div>
            </div>
        </div>
"""

        # Duplicates Section
        if duplicate_groups:
            html += f"""
        <div class="section">
            <h2>🔀 Duplicate Files ({len(duplicate_groups)} groups)</h2>
            <div class="controls">
                <button class="btn-select-all" onclick="selectAllDuplicates()">Select Duplicates to Delete</button>
                <button class="btn-delete" onclick="deleteDuplicates()">Delete Selected</button>
                <span id="dup-count">0 selected</span>
            </div>
            <div id="duplicates-container">
"""
            for i, group in enumerate(duplicate_groups):
                html += f"""
                <div class="duplicate-group">
                    <div class="group-header" onclick="toggleGroup({i})">
                        <span class="toggle">▶</span>
                        <span class="group-title">Group {i+1} (Hash: {group['hash']}...)</span>
                        <span class="group-count">{group['count']} files</span>
                    </div>
                    <div class="group-content-{i}" style="display:none;">
"""
                for j, filepath in enumerate(group['files']):
                    size_mb = os.path.getsize(filepath) / (1024*1024)
                    filename = os.path.basename(filepath)
                    # First file is original, rest are duplicates
                    is_duplicate = j > 0
                    checked = "checked" if is_duplicate else ""

                    html += f"""
                        <div class="file-item">
                            <input type="checkbox" class="dup-checkbox" data-path="{quote(filepath)}" {checked}>
                            <div class="file-info">
                                <div class="file-name">{filename}</div>
                                <div class="file-details">{filepath} • {size_mb:.2f}MB {'(KEEP)' if not is_duplicate else '(DUPLICATE)'}</div>
                            </div>
                            <div class="file-action">
                                <button class="btn-small btn-view" onclick="viewFile('{quote(filepath)}')">View</button>
                                <button class="btn-small btn-delete-single" onclick="deleteSingleFile('{quote(filepath)}')">Delete</button>
                            </div>
                        </div>
"""

                html += """
                    </div>
                </div>
"""
            html += """
            </div>
        </div>
"""

        # Similar Photos Section
        if self.similar_photos:
            html += f"""
        <div class="section">
            <h2>📸 Similar Photos ({len(self.similar_photos)} groups)</h2>
            <p style="color: #888; margin-bottom: 15px;">These are photos that look very similar. You might want to keep the best one and delete the rest.</p>
            <div class="controls">
                <button class="btn-select-all" onclick="selectAllSimilar()">Select to Review</button>
                <button class="btn-delete" onclick="deleteSimilar()">Delete Selected</button>
                <span id="sim-count">0 selected</span>
            </div>
            <div id="similar-container">
"""
            for group_idx, group in enumerate(self.similar_photos):
                html += f"""
                <div class="duplicate-group">
                    <div class="group-header" onclick="toggleGroup('similar', {group_idx})">
                        <span class="toggle">▶</span>
                        <span class="group-title">Similar Group {group_idx+1}</span>
                        <span class="group-count">{group['count']} photos</span>
                    </div>
                    <div class="group-content-similar-{group_idx}" style="display:none;">
"""
                for filepath in group['group']:
                    size_mb = os.path.getsize(filepath) / (1024*1024)
                    filename = os.path.basename(filepath)
                    thumbnail = self.get_thumbnail_base64(filepath, size=100)

                    html += f"""
                        <div class="file-item">
                            <input type="checkbox" class="sim-checkbox" data-path="{quote(filepath)}">
                            <div class="thumbnail {'no-image' if not thumbnail else ''}" style="width: 80px; height: 80px;">
                                {'<img src="' + thumbnail + '">' if thumbnail else '?'}
                            </div>
                            <div class="file-info">
                                <div class="file-name">{filename}</div>
                                <div class="file-details">{filepath} • {size_mb:.2f}MB</div>
                            </div>
                            <div class="file-action">
                                <button class="btn-small btn-view" onclick="viewFile('{quote(filepath)}')">View</button>
                                <button class="btn-small btn-delete-single" onclick="deleteSingleFile('{quote(filepath)}')">Delete</button>
                            </div>
                        </div>
"""
                html += """
                    </div>
                </div>
"""
            html += """
            </div>
        </div>
"""

        # Screenshots Section
        if self.screenshots:
            html += f"""
        <div class="section">
            <h2>📱 Screenshots ({len(self.screenshots)})</h2>
            <p style="color: #888; margin-bottom: 15px;">Detected screenshots. Review before deleting.</p>
            <div class="controls">
                <button class="btn-select-all" onclick="selectAllScreenshots()">Select All</button>
                <button class="btn-delete" onclick="deleteScreenshots()">Delete Selected</button>
                <span id="ss-count">0 selected</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px;">
"""
            for item in self.screenshots:
                filepath = item['path']
                filename = os.path.basename(filepath)
                thumbnail = self.get_thumbnail_base64(filepath, size=150)

                html += f"""
                <div style="border: 1px solid #ddd; border-radius: 6px; overflow: hidden;">
                    <div class="thumbnail" style="width: 100%; height: 150px;">
                        {'<img src="' + thumbnail + '">' if thumbnail else 'No preview'}
                    </div>
                    <div style="padding: 10px;">
                        <div style="font-size: 0.8em; color: #666; word-break: break-all; margin-bottom: 8px;">{filename}</div>
                        <input type="checkbox" class="ss-checkbox" data-path="{quote(filepath)}">
                        <button class="btn-small btn-delete-single" onclick="deleteSingleFile('{quote(filepath)}')" style="margin-left: 5px;">Delete</button>
                    </div>
                </div>
"""
            html += """
            </div>
        </div>
"""

        # Bad Videos Section
        if self.bad_videos:
            html += f"""
        <div class="section">
            <h2>🎥 Bad Videos ({len(self.bad_videos)})</h2>
            <div class="controls">
                <button class="btn-select-all" onclick="selectAllBadVideos()">Select All</button>
                <button class="btn-delete" onclick="deleteBadVideos()">Delete Selected</button>
                <span id="bv-count">0 selected</span>
            </div>
"""
            for item in self.bad_videos:
                filepath = item['path']
                filename = os.path.basename(filepath)
                size_mb = os.path.getsize(filepath) / (1024*1024)
                issues = item['issues']

                html += f"""
                <div class="bad-photo-item">
                    <div class="file-info">
                        <div class="bad-photo-name">{filename}</div>
                        <div class="issue-badges">
"""
                for issue in issues:
                    html += f'<span class="issue-badge">{issue}</span>'

                html += f"""
                        </div>
                        <div class="file-size">{filepath}</div>
                        <div class="file-size">{size_mb:.2f}MB</div>
                    </div>
                    <div class="file-action" style="flex-direction: column; gap: 5px;">
                        <input type="checkbox" class="bv-checkbox" data-path="{quote(filepath)}">
                        <button class="btn-small btn-delete-single" onclick="deleteSingleFile('{quote(filepath)}')">Delete</button>
                    </div>
                </div>
"""
            html += """
        </div>
"""

        # Bad Photos Section
        if bad_photos_sorted:
            html += f"""
        <div class="section">
            <h2>⚠️ Bad/Accidental Photos ({len(bad_photos_sorted)})</h2>
            <div class="controls">
                <button class="btn-select-all" onclick="selectAllBadPhotos()">Select to Review</button>
                <button class="btn-delete" onclick="deleteBadPhotos()">Delete Selected</button>
                <span id="bad-count">0 selected</span>
            </div>
            <div id="bad-photos-container">
"""
            for item in bad_photos_sorted:
                filepath = item['path']
                filename = os.path.basename(filepath)
                size_mb = os.path.getsize(filepath) / (1024*1024)
                issues = item['issues']
                severity = len(issues)
                critical_class = "critical" if severity >= 3 else ""

                thumbnail = self.get_thumbnail_base64(filepath)

                html += f"""
                <div class="bad-photo-item {critical_class}">
                    <div class="thumbnail {'no-image' if not thumbnail else ''}">
                        {'<img src="' + thumbnail + '">' if thumbnail else 'No preview'}
                    </div>
                    <div class="bad-photo-content">
                        <div class="bad-photo-name">{filename}</div>
                        <div class="issue-badges">
"""
                for issue in issues:
                    html += f'<span class="issue-badge">{issue}</span>'

                html += f"""
                        </div>
                        <div class="file-size">{filepath}</div>
                        <div class="file-size">{size_mb:.2f}MB</div>
                    </div>
                    <div class="file-action" style="flex-direction: column; gap: 5px;">
                        <input type="checkbox" class="bad-checkbox" data-path="{quote(filepath)}">
                        <button class="btn-small btn-view" onclick="viewFile('{quote(filepath)}')">View</button>
                        <button class="btn-small btn-delete-single" onclick="deleteSingleFile('{quote(filepath)}')">Delete</button>
                    </div>
                </div>
"""
            html += """
            </div>
        </div>
"""

        # Irrelevant Files Section
        if self.irrelevant_files:
            html += f"""
        <div class="section">
            <h2>📄 Irrelevant Files ({len(self.irrelevant_files)})</h2>
            <div class="irrelevant-files">
"""
            for item in self.irrelevant_files:
                html += f'<div class="file-path">{item["path"]} <em>({item["reason"]})</em></div>'

            html += """
            </div>
        </div>
"""

        html += """
        <div class="footer">
            <p>💡 Tip: Review items carefully before deleting. Deleted files cannot be recovered.</p>
        </div>
    </div>

    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <h3>Confirm Deletion</h3>
            <p id="confirmText"></p>
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="closeModal()">Cancel</button>
                <button class="btn-confirm" onclick="confirmDelete()">Delete</button>
            </div>
        </div>
    </div>

    <script>
        let filesToDelete = [];

        function updateCounts() {
            const dupCount = document.querySelectorAll('.dup-checkbox:checked').length;
            const badCount = document.querySelectorAll('.bad-checkbox:checked').length;
            const simCount = document.querySelectorAll('.sim-checkbox:checked').length;
            const ssCount = document.querySelectorAll('.ss-checkbox:checked').length;
            const bvCount = document.querySelectorAll('.bv-checkbox:checked').length;

            if (document.getElementById('dup-count')) document.getElementById('dup-count').textContent = dupCount + ' selected';
            if (document.getElementById('bad-count')) document.getElementById('bad-count').textContent = badCount + ' selected';
            if (document.getElementById('sim-count')) document.getElementById('sim-count').textContent = simCount + ' selected';
            if (document.getElementById('ss-count')) document.getElementById('ss-count').textContent = ssCount + ' selected';
            if (document.getElementById('bv-count')) document.getElementById('bv-count').textContent = bvCount + ' selected';
        }

        function toggleGroup(type, index) {
            let selector;
            if (type === 'similar') {
                selector = '.group-content-similar-' + index;
            } else {
                selector = '.group-content-' + index;
            }
            const content = document.querySelector(selector);
            const toggle = event.target.closest('.group-header').querySelector('.toggle');
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
            toggle.textContent = content.style.display === 'none' ? '▶' : '▼';
        }

        function selectAllDuplicates() {
            const checkboxes = document.querySelectorAll('.dup-checkbox:not(:checked)');
            checkboxes.forEach(cb => cb.checked = true);
            updateCounts();
        }

        function selectAllSimilar() {
            const checkboxes = document.querySelectorAll('.sim-checkbox:not(:checked)');
            checkboxes.forEach(cb => cb.checked = true);
            updateCounts();
        }

        function selectAllScreenshots() {
            const checkboxes = document.querySelectorAll('.ss-checkbox:not(:checked)');
            checkboxes.forEach(cb => cb.checked = true);
            updateCounts();
        }

        function selectAllBadPhotos() {
            const checkboxes = document.querySelectorAll('.bad-checkbox:not(:checked)');
            checkboxes.forEach(cb => cb.checked = true);
            updateCounts();
        }

        function selectAllBadVideos() {
            const checkboxes = document.querySelectorAll('.bv-checkbox:not(:checked)');
            checkboxes.forEach(cb => cb.checked = true);
            updateCounts();
        }

        function deleteDuplicates() {
            const selected = Array.from(document.querySelectorAll('.dup-checkbox:checked'))
                .map(cb => decodeURIComponent(cb.dataset.path));
            if (selected.length === 0) {
                alert('No files selected');
                return;
            }
            showConfirmation(selected, 'duplicate files');
        }

        function deleteSimilar() {
            const selected = Array.from(document.querySelectorAll('.sim-checkbox:checked'))
                .map(cb => decodeURIComponent(cb.dataset.path));
            if (selected.length === 0) {
                alert('No files selected');
                return;
            }
            showConfirmation(selected, 'similar photos');
        }

        function deleteScreenshots() {
            const selected = Array.from(document.querySelectorAll('.ss-checkbox:checked'))
                .map(cb => decodeURIComponent(cb.dataset.path));
            if (selected.length === 0) {
                alert('No files selected');
                return;
            }
            showConfirmation(selected, 'screenshots');
        }

        function deleteBadPhotos() {
            const selected = Array.from(document.querySelectorAll('.bad-checkbox:checked'))
                .map(cb => decodeURIComponent(cb.dataset.path));
            if (selected.length === 0) {
                alert('No files selected');
                return;
            }
            showConfirmation(selected, 'bad photos');
        }

        function deleteBadVideos() {
            const selected = Array.from(document.querySelectorAll('.bv-checkbox:checked'))
                .map(cb => decodeURIComponent(cb.dataset.path));
            if (selected.length === 0) {
                alert('No files selected');
                return;
            }
            showConfirmation(selected, 'bad videos');
        }

        function deleteSingleFile(encodedPath) {
            const path = decodeURIComponent(encodedPath);
            showConfirmation([path], 'file');
        }

        function showConfirmation(files, type) {
            filesToDelete = files;
            const modal = document.getElementById('confirmModal');
            const text = document.getElementById('confirmText');

            if (type === 'file') {
                text.innerHTML = `Are you sure you want to delete:<br><strong>${files[0].split('/').pop()}</strong><br><br>This action cannot be undone.`;
            } else {
                text.innerHTML = `Are you sure you want to delete <strong>${files.length} ${type}</strong>?<br><br>This action cannot be undone.`;
            }

            modal.classList.add('active');
        }

        function closeModal() {
            document.getElementById('confirmModal').classList.remove('active');
        }

        function confirmDelete() {
            closeModal();
            deleteFiles(filesToDelete);
        }

        function deleteFiles(files) {
            // Send to server
            fetch('/api/delete', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({files: files})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert('Deleted ' + data.count + ' files');
                    location.reload();
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(err => alert('Error: ' + err));
        }

        function viewFile(encodedPath) {
            const path = decodeURIComponent(encodedPath);
            // For local files, we can't directly open, but show path
            alert('File: ' + path);
        }

        // Update counts on checkbox change
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('dup-checkbox') || e.target.classList.contains('bad-checkbox')) {
                updateCounts();
            }
        });
    </script>
</body>
</html>
"""

        with open(output_file, "w") as f:
            f.write(html)
        print(f"💾 HTML report saved to {output_file}")

        # Save JSON data for server
        self.save_json_data(output_file.replace('.html', '_data.json'))

    def save_json_data(self, output_file: str) -> None:
        """Save data as JSON for server deletion."""
        data = {
            "duplicates": {
                hash_val: files
                for hash_val, files in self.duplicates.items()
                if len(files) > 1
            },
            "bad_photos": [item["path"] for item in self.bad_photos],
            "irrelevant_files": self.irrelevant_files
        }
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Find and discard bad photos/videos on macOS")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--min-size", type=int, default=50, help="Min file size in KB (default: 50)")
    parser.add_argument("--min-dim", type=int, default=100, help="Min image dimension (default: 100)")
    parser.add_argument("--similarity", type=int, default=10, help="Similarity threshold 0-64 (default: 10)")
    parser.add_argument("--report", type=str, default="media_report.html", help="Report output file")
    parser.add_argument("--serve", action="store_true", help="Start web server to view/delete files")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return

    analyzer = MediaAnalyzer(
        min_size_kb=args.min_size,
        min_dimension=args.min_dim,
        similarity_threshold=args.similarity
    )
    analyzer.scan_directory(args.directory)
    analyzer.generate_html_report(args.report)

    if args.serve:
        start_server(args.report)


def start_server(report_file: str) -> None:
    """Start a simple HTTP server to view and delete files."""
    try:
        from flask import Flask, send_file, request, jsonify
    except ImportError:
        print("Installing Flask...")
        os.system("pip install flask")
        from flask import Flask, send_file, request, jsonify

    app = Flask(__name__)
    report_dir = os.path.dirname(os.path.abspath(report_file))

    @app.route('/')
    def index():
        return send_file(report_file)

    @app.route('/api/delete', methods=['POST'])
    def delete_files():
        files = request.json.get('files', [])
        deleted = 0
        errors = []

        for filepath in files:
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    deleted += 1
                    print(f"Deleted: {filepath}")
            except Exception as e:
                errors.append(f"{filepath}: {e}")

        return jsonify({
            "success": len(errors) == 0,
            "count": deleted,
            "error": ", ".join(errors) if errors else None
        })

    port = 5000
    print(f"\n🌐 Starting web server on http://localhost:{port}")
    print(f"📊 Open the report in your browser to delete files")
    print(f"Press Ctrl+C to stop\n")

    app.run(debug=False, port=port)


if __name__ == "__main__":
    main()
