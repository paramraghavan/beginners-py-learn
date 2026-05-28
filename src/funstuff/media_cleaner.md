# Media Cleaner 🧹

A powerful Python tool to identify and safely delete duplicate files, similar photos, accidental/bad quality images, corrupted videos, and irrelevant files from your media library. Optimized for macOS with native HEIC support.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Parameters](#parameters)
- [How Detection Works](#how-detection-works)
- [Web Interface](#web-interface)
- [Safety](#safety)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Features

### 🔀 **Exact Duplicates**
- Finds bit-perfect identical files using SHA256 hashing
- Groups duplicates together
- Automatically marks all-but-one for deletion
- Saves storage space immediately

### 📸 **Similar Photos**
- Uses perceptual hashing to find visually similar images
- Detects:
  - Edited versions of the same photo
  - Multiple shots of the same scene
  - Photos with slight crops or filters
- Configurable sensitivity threshold
- Great for sorting through photo bursts and retakes

### 📱 **Screenshot Detection**
- Automatically identifies screenshots
- Detects by:
  - Standard screen resolutions (1920×1080, 1280×720, etc.)
  - Aspect ratio patterns
  - UI border characteristics (white edges)
- Useful for cleaning up mixed media folders

### ⚠️ **Bad Photos (Accidental/Discard)**
- Detects accidental or low-quality photos you should discard:
  - **Blurry images**: Out of focus, motion blur detected
  - **Too dark**: Underexposed (camera in pocket, lens covered)
  - **Overexposed**: Washed out, blown-out highlights
  - **Completely black**: Accidental dark captures
  - **Completely white**: Flash accidents, pointing at light
  - **Blank shots**: Solid colors, sky, walls, uniform content
  - **Extreme aspect ratio**: Cropped wrong, partial captures
  - **Too small**: Tiny files or low resolution
- Multiple issues reported per photo for easy identification
- Severity indicators for batch review
- Thumbnail previews for quick visual check

### 🎥 **Bad Videos**
- Identifies problematic video files:
  - Corrupted or unplayable videos
  - Too short (< 5 frames)
  - Low resolution (< 320×240)
  - Very low FPS (< 15)
  - Suspiciously small files
- Perfect for cleaning up partial recordings and failed captures

### 📄 **Irrelevant Files**
- Finds non-media files in media folders
- Detects unsupported file types
- Helps organize mixed directories

### 🍎 **HEIC/HEIF Support (Native macOS)**
- Full support for iPhone/iPad HEIC format (no conversion needed)
- Analyzes HEIC files identically to JPEG/PNG
- Detects accidental photos, duplicates, and similar images
- Works seamlessly on macOS with native file handling
- Optional pillow-heif library for advanced image analysis

### 🎬 **Live Photo Detection**
- Identifies paired .MOV + .HEIC Live Photo files
- Marks video component for easy deletion
- Keep photo, delete video or vice versa

---

## Installation

### Requirements
- Python 3.7+
- pip package manager

### Setup

```bash
# Clone or download the script
cd your/media/folder

# Run the script (it will auto-install dependencies)
python media_cleaner.py ~/Pictures

# Or install dependencies manually
pip install Pillow numpy opencv-python imagehash flask
```

### Dependencies

The script automatically installs missing dependencies:
- **Pillow**: Image processing
- **numpy**: Numerical computations
- **opencv-python**: Video analysis
- **imagehash**: Perceptual hashing for similarity detection
- **Flask**: Web server (optional, for `--serve`)
- **pillow-heif**: HEIC/HEIF support (optional, for `--convert-heic`)

### Note on HEIC Support

HEIC files are natively supported on macOS. The script automatically:
- Detects all .heic and .heif files
- Analyzes them for quality, duplicates, and similarity
- Displays them in reports and web interface

No conversion needed—macOS handles HEIC natively!

---

## Quick Start

### Generate Report (Recommended First Step)

```bash
python media_cleaner.py ~/Pictures
```

This creates `media_report.html` - open it in your browser to review findings.

### Review & Delete with Web Interface

```bash
python media_cleaner.py ~/Pictures --serve
```

Opens `http://localhost:5000` with interactive deletion interface.

### Scan with Custom Parameters

```bash
python media_cleaner.py ~/Camera_Uploads --similarity 8 --min-size 100
```

---

## Usage

### Basic Syntax

```bash
python media_cleaner.py <directory> [options]
```

### Options

```
positional arguments:
  directory                 Directory to scan (required)

optional arguments:
  --min-size KB            Minimum file size in KB (default: 50)
  --min-dim PIXELS         Minimum image dimension (default: 100)
  --similarity THRESHOLD   Similarity detection threshold 0-64 (default: 10)
  --report FILE            Output HTML file name (default: media_report.html)
  --serve                  Start web server for interactive deletion
```

---

## Parameters

### `--min-size` (Default: 50)

Minimum file size in kilobytes. Files smaller than this are flagged as suspicious.

```bash
# Strict: Flag files smaller than 100 KB
python media_cleaner.py ~/Pictures --min-size 100

# Lenient: Only flag very small files (< 20 KB)
python media_cleaner.py ~/Pictures --min-size 20
```

**Use when:** Your folder has many corrupt/partial downloads or thumbnails.

---

### `--min-dim` (Default: 100)

Minimum image dimension (width or height) in pixels.

```bash
# Strict: Only consider images >= 200×200 pixels
python media_cleaner.py ~/Pictures --min-dim 200

# Lenient: Allow smaller images >= 50×50
python media_cleaner.py ~/Pictures --min-dim 50
```

**Use when:** You have thumbnails or icon files mixed in.

---

### `--similarity` (Default: 10)

Perceptual hash similarity threshold (0-64).
- **Lower number** = stricter matching (only very similar photos)
- **Higher number** = lenient matching (includes variations and edits)

```bash
# Very strict: Only nearly-identical photos (e.g., burst shots)
python media_cleaner.py ~/Pictures --similarity 5

# Balanced: Good for edited versions and retakes
python media_cleaner.py ~/Pictures --similarity 10

# Lenient: Includes photos with different crops/filters
python media_cleaner.py ~/Pictures --similarity 15
```

**Threshold Reference:**
- **0-5**: Nearly identical only (best for burst detection)
- **5-10**: Identical + very similar (recommended)
- **10-15**: Includes edited/cropped versions
- **15+**: Very lenient (may flag unrelated photos)

---

### `--report` (Default: media_report.html)

Output file name for the HTML report.

```bash
python media_cleaner.py ~/Pictures --report my_cleanup_report.html
```

---

### `--serve`

Start a web server for interactive viewing and deletion. Perfect for reviewing findings before deleting.

```bash
python media_cleaner.py ~/Pictures --serve
```

Opens at `http://localhost:5000`. Press Ctrl+C to stop.

---

## How Detection Works

### Exact Duplicates 🔀

**Method**: SHA256 cryptographic hashing
- Reads entire file content
- Creates unique fingerprint
- Files with identical hash = exact duplicates
- **Accuracy**: 100%

### Similar Photos 📸

**Method**: Average Perceptual Hashing
1. Resize image to 8×8 grid
2. Convert to grayscale
3. Calculate average pixel value
4. Create 64-bit hash based on pixel differences
5. Compare hashes (Hamming distance)

**Example:**
```
Photo A: Hash = 1010110101...
Photo B: Hash = 1010110111...
Distance = 2 (very similar)

Distance < threshold → Similar photo group
```

**Why it works:**
- Detects visual similarity, not exact match
- Survives minor edits (crops, filters, compression)
- Fast and memory-efficient

### Screenshot Detection 📱

**Detects by analyzing:**

1. **Aspect Ratio**
   - Typical screenshots are landscape (16:9, 16:10)
   - Width > 1.5× height usually indicates screenshot

2. **Screen Resolutions**
   - Common widths: 1920, 2560, 1280, 1024, 800
   - Exact match suggests screenshot

3. **UI Patterns**
   - White or light edges (UI frames)
   - Analyzes top, bottom, left, right 5 pixels
   - Light edges + standard ratio = screenshot

**Example:**
```
Image: 1920×1080 (16:9 ratio)
Top edge: 245/255 brightness (white-ish)
Bottom edge: 240/255 brightness (white-ish)
→ Likely screenshot
```

### Bad Photos ⚠️

**Blurry Detection:**
- Uses Laplacian edge detection
- Calculates variance of edge strengths
- Low variance = blurry (variance < 100)

**Dark Photo Detection:**
- Averages all pixel brightness values
- Underexposed if avg brightness < 30 (0-255 scale)

**Overexposed Detection:**
- Avg brightness > 220
- Low color variation (std dev < 30)
- Indicates washed-out highlights

**Blank Shot Detection:**
- Measures pixel color variation (std deviation)
- Low variation (< 20) = uniform color
- Detects sky, walls, blanks

**Size Analysis:**
- Files < min_size KB flagged
- Images < min_dim × min_dim pixels flagged

### HEIC/HEIF Files 🍎 (macOS Native)

**Automatic Support:**
- All .heic and .heif files are automatically detected
- Analyzed with same quality checks as JPEG/PNG
- All detection methods work: blurry, dark, overexposed, etc.
- Live Photo pairs (MOV + HEIC) identified automatically

**No Conversion Needed:**
- macOS natively handles HEIC format
- Finder, Preview, and Photos app all support HEIC
- Keep HEIC as-is—no conversion overhead
- Script just identifies which to delete

**Workflow:**
```bash
# Scan iPhone backup directly (HEIC as-is)
python media_cleaner.py ~/Camera_Roll --serve

# Review and delete:
# - Bad quality HEIC photos
# - Exact duplicate HEICs
# - Similar HEICs (keep best, delete others)
# - Live Photo MOV files (paired with HEIC)
```

**Live Photo Handling:**
- Script detects `.MOV` files paired with `.HEIC`
- Marked as "Live Photo video" for easy filtering
- Delete MOV to keep just the photo
- Or delete HEIC to keep just the video

### Bad Videos 🎥

**Corruption Detection:**
- Attempts to open with OpenCV
- Fails = corrupted/unplayable

**Quality Checks:**
- Frame count < 5 → too short
- Width < 320 or height < 240 → low resolution
- FPS < 15 → very slow
- File size < 100 KB → suspiciously small

---

## Web Interface

When using `--serve`, the interactive HTML dashboard provides:

### Dashboard
- Real-time statistics
- 6-category summary view

### Duplicate Files Section
- Grouped by hash
- Auto-selects duplicates (keeps original)
- Checkbox control
- Thumbnail previews

### Similar Photos Section
- Expandable groups
- Visual thumbnails
- Manual selection (review before deleting)

### Screenshots Section
- Grid layout with previews
- Quick selection
- Individual delete buttons

### Bad Photos Section
- Thumbnail previews
- Color-coded severity
- Issue badges per photo
- File size and path info

### Bad Videos Section
- List with issue details
- Selectable for batch deletion

### Features
- ✅ Checkbox selection (individual or batch)
- ✅ Confirmation dialogs before deletion
- ✅ View button to inspect files
- ✅ Delete button for single files
- ✅ Real-time count updates
- ✅ Mobile-responsive design

---

## Safety

### Design Safeguards

1. **No Auto-Deletion**
   - Every deletion requires manual selection
   - Confirmation dialog mandatory

2. **Preview System**
   - Thumbnails for all images
   - File paths displayed
   - Severity indicators

3. **Server-Based Deletion**
   - Deletion handled server-side (not client-side)
   - Reduces accidental clicks

4. **Selective Controls**
   - Category-level "Select All" buttons
   - Individual file checkboxes
   - Per-file delete options

5. **Backup Recommendation**
   - Always backup before bulk deletion
   - Test with small folder first

### Best Practices

```bash
# 1. Scan without --serve first
python media_cleaner.py ~/Pictures

# 2. Review HTML report in browser
# 3. Backup your folder
cp -r ~/Pictures ~/Pictures_backup

# 4. Then use --serve for deletion
python media_cleaner.py ~/Pictures --serve
```

---

## Examples

### Example 1: Clean Up Phone Photos

Mix of screenshots, burst photos, bad shots:

```bash
python media_cleaner.py ~/Camera_Roll \
  --similarity 8 \
  --serve
```

**Workflow:**
1. Delete exact duplicates (auto-selected)
2. Review similar photos in bursts
3. Delete screenshots
4. Review bad photos (too dark, blurry, etc.)
5. Delete bad videos

**Storage saved:** Often 30-50% for phone backups

---

### Example 2: Archive Old Projects

Mixed media folder with random files:

```bash
python media_cleaner.py ~/Old_Projects \
  --min-size 100 \
  --min-dim 200 \
  --serve
```

**Identifies:**
- Exact duplicates across project backups
- Low-res placeholder images
- Non-image files (PDFs, docs, etc.)
- Corrupted video files

---

### Example 3: Strict Similarity Detection

Only want nearly-identical photos:

```bash
python media_cleaner.py ~/Important_Photos \
  --similarity 5 \
  --serve
```

**Use for:** Professional photos where slight variations matter

---

### Example 4: Lenient Mode

Want to catch all variations:

```bash
python media_cleaner.py ~/Casual_Photos \
  --similarity 15 \
  --serve
```

**Use for:** Casual shots where similar photos are likely duplicates

---

### Example 5: Generate Report Only (No Server)

Just analyze, don't delete:

```bash
python media_cleaner.py ~/Pictures --report analysis.html
```

Open `analysis.html` in browser to review but no delete functionality.

---

### Example 6: Clean iPhone Photos (macOS)

iPhone backup with HEIC files, duplicates, Live Photos, and accidental photos:

```bash
# Direct scan of iPhone backup with native HEIC support
python media_cleaner.py ~/iPhone_Backup --serve
```

**Workflow:**
1. Scans all HEIC files natively (no conversion)
2. Finds exact duplicates
3. Identifies similar photos from bursts
4. Detects bad photos (blurry, dark, accidental)
5. Identifies Live Photo video pairs (.MOV files)
6. Opens web interface with full review
7. Delete exact duplicates (auto-selected)
8. Delete accidental/bad photos
9. Choose Live Photo handling:
   - Keep photo, delete .MOV
   - Or keep .MOV, delete photo

**Result:** iPhone backup cleaned, duplicates removed, HEIC files optimized for macOS

---

## Troubleshooting

### ImportError: No module named 'PIL'

**Solution:**
```bash
pip install Pillow numpy opencv-python imagehash
```

---

### ImportError: No module named 'cv2'

**Solution:**
```bash
pip install opencv-python
```

Note: Large install (~100 MB). If only analyzing images, not videos, you can skip this.

---

### ImportError: No module named 'imagehash'

**Solution:**
```bash
pip install imagehash
```

---

### Flask not found when using --serve

**Solution:**
```bash
pip install flask
```

---

### "Permission denied" when deleting

**Cause:** Script lacks write permissions on directory

**Solution:**
```bash
# Check permissions
ls -ld ~/Pictures

# Fix permissions (if you own the folder)
chmod u+w ~/Pictures
```

---

### Web server won't start

**Cause:** Port 5000 already in use

**Solution:**
```bash
# Use different port (edit script or create wrapper)
# Or kill process using port 5000:
lsof -ti:5000 | xargs kill -9
```

---

### Script is very slow

**Cause:** Similarity detection is computationally intensive

**Solutions:**
```bash
# 1. Disable similarity (remove hash comparison)
# 2. Use smaller threshold (fewer comparisons)
python media_cleaner.py ~/Pictures --similarity 15

# 3. Scan smaller subset first
python media_cleaner.py ~/Pictures/2024_Jan

# 4. Use faster computer
```

---

### macOS can't open certain image files

**Cause:** Pillow doesn't recognize the format; macOS Preview needs the file

**Solution:**
```bash
# Open file directly in macOS Preview
open ~/Pictures/filename.heic
```

---

### Script doesn't detect HEIC files as bad quality

**Reason:** macOS HEIC files may have excellent auto-correction built-in

**Solution:**
1. Check for blurriness (motion or focus issues) - these are reliable
2. Check for extreme lighting (too dark, too bright) - these are reliable
3. Review "completely black" or "completely white" detections
4. Manual review: open suspicious files in Preview to confirm

---

### Deleted wrong file by mistake

**Solution:**
- Check OS trash/recycle bin
- Use file recovery tool (TestDisk, PhotoRec)
- Restore from backup

**Prevention:**
- Always backup before bulk deletion
- Review HTML report before using --serve
- Test with small folder first

---

### Screenshot detection missing some files

**Adjust parameters:**
```bash
# If false negatives (missing screenshots):
# 1. Lower similarity threshold
# 2. Check manually in report

# Issue: Script detection is pattern-based
# Some screenshots may have unusual dimensions
```

---

### Similar photos not detected

**Causes & Solutions:**

```bash
# 1. Threshold too strict
python media_cleaner.py ~/Pictures --similarity 15  # More lenient

# 2. Photos heavily edited
# Perceptual hash survives minor edits but not major ones

# 3. Different image formats
# Convert to same format before comparing
```

---

## Configuration Reference

### Recommended Settings by Use Case

| Use Case | Command |
|----------|---------|
| **Phone backup** | `--similarity 8 --min-size 50` |
| **DSLR photos** | `--similarity 5 --min-size 100` |
| **Mixed media** | `--similarity 10 --min-size 75` |
| **Professional archive** | `--similarity 5 --min-dim 150` |
| **Casual folder** | `--similarity 15 --min-size 30` |

---

## Advanced Usage

### Scripting with JSON Report

The script also generates `media_report_data.json`:

```python
import json

with open('media_report_data.json') as f:
    data = json.load(f)

# Access data programmatically
for hash_val, files in data['duplicates'].items():
    print(f"Duplicate group: {len(files)} files")
    for filepath in files:
        print(f"  - {filepath}")
```

---

## Performance Notes

### Speed Factors

- **Folder size**: Linear with number of files
- **Image resolution**: Higher res = slower similarity detection
- **Similarity threshold**: Lower = more comparisons
- **Video analysis**: Slow (frame extraction)

### Typical Times

| Folder Size | Time |
|------------|------|
| 100 photos | 5-10 seconds |
| 1,000 photos | 30-60 seconds |
| 10,000 photos | 5-15 minutes |
| Mixed with videos | Add 2-5 sec per video |

---

## License & Credits

Created for media organization and cleaning.

- Uses: Pillow, OpenCV, imagehash, NumPy, Flask
- Algorithm: SHA256 hashing, perceptual hashing (aHash)

---

## Tips & Tricks

### Tip 1: Two-Stage Deletion

```bash
# Stage 1: Generate report
python media_cleaner.py ~/Pictures

# Stage 2 (next day, after review): Delete
python media_cleaner.py ~/Pictures --serve
```

### Tip 2: Backup Before Starting

```bash
# Create backup
zip -r Pictures_backup.zip ~/Pictures

# Then clean
python media_cleaner.py ~/Pictures --serve
```

### Tip 3: Organize by Category

Use the HTML report to understand your folder:
1. How many exact duplicates?
2. How many accidental photos?
3. Any corrupted videos?

Then decide on parameters before deletion.

### Tip 4: Test on Small Subset

```bash
# Test on January photos first
python media_cleaner.py ~/Pictures/2024_January --serve

# If satisfied, do all
python media_cleaner.py ~/Pictures --serve
```

---

## FAQ

**Q: Can I recover deleted files?**
A: Yes, with file recovery tools like PhotoRec or Recuva before next major write to disk. Always backup first.

**Q: Does it work on external drives?**
A: Yes, but performance depends on drive speed. USB 2.0 is very slow.

**Q: Can I automate deletions?**
A: No. Script requires manual selection for safety. This is intentional.

**Q: How accurate is similarity detection?**
A: ~85-95% depending on edits and threshold. Always review before deleting.

**Q: Will it handle RAW images?**
A: Partial support. Pillow may not read all RAW formats. Consider converting first.

**Q: Can I exclude certain folders?**
A: Current version scans recursively. Consider running on specific folders instead.

---

## Support & Issues

- Check Troubleshooting section above
- Review generated HTML report for details
- Check file permissions and disk space
- Ensure all dependencies are installed: `pip list | grep -E 'Pillow|numpy|opencv|imagehash|flask'`
