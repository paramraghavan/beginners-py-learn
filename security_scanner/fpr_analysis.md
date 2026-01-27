Fortify stores scan results in FPR (Fortify Project Results) files, which are essentially ZIP archives containing XML
data. Here's how to decode and access the vulnerability information:

## Quick Methods

**1. Rename and extract as ZIP**

The simplest approach—FPR files are ZIP archives:

```bash
cp your_scan.fpr your_scan.zip
unzip your_scan.zip -d fpr_contents/
```

Inside you'll find:

- `audit.fvdl` — the main XML file containing all vulnerabilities
- `audit.xml` — audit/triage data
- Various metadata files

**2. Parse the FVDL file**

The `audit.fvdl` file is XML that contains the vulnerability details. You can parse it with standard XML tools:

```python
import xml.etree.ElementTree as ET
import zipfile

with zipfile.ZipFile('your_scan.fpr', 'r') as z:
    with z.open('audit.fvdl') as f:
        tree = ET.parse(f)
        root = tree.getroot()

# The namespace is typically:
ns = {'fvdl': 'xmlns://www.fortifysoftware.com/schema/fvdl'}

# Find vulnerabilities
for vuln in root.findall('.//fvdl:Vulnerability', ns):
    # Extract category, severity, file, line, etc.
    class_info = vuln.find('fvdl:ClassInfo', ns)
    if class_info is not None:
        category = class_info.find('fvdl:Type', ns)
        print(category.text if category is not None else 'Unknown')
```

**3. Use Fortify's tools**

If you have Fortify installed:

- **Audit Workbench** — GUI tool to open FPR files directly
- **FPRUtility** — command-line tool to export to XML/CSV:
  ```bash
  FPRUtility -project your_scan.fpr -information -listIssues
  ```
- **ReportGenerator** — create reports in various formats

## Key Data Structure in FVDL

The vulnerability entries typically contain:

- **ClassInfo** — vulnerability category and type
- **AnalysisInfo** — severity, confidence, impact
- **InstanceInfo** — specific instance ID
- **Source/Sink** — dataflow information for taint-based findings
- **Location** — file path, line number, function name
