import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict


def extract_remediations(fpr_path):
    ns = {'fvdl': 'xmlns://www.fortifysoftware.com/schema/fvdl'}

    with zipfile.ZipFile(fpr_path, 'r') as z:
        with z.open('audit.fvdl') as f:
            tree = ET.parse(f)
            root = tree.getroot()

    # Get vulnerability descriptions (contains remediation info)
    descriptions = {}
    for desc in root.findall('.//fvdl:Description', ns):
        class_id = desc.get('classID')

        abstract = desc.find('fvdl:Abstract', ns)
        explanation = desc.find('fvdl:Explanation', ns)
        recommendations = desc.find('fvdl:Recommendations', ns)

        descriptions[class_id] = {
            'abstract': abstract.text if abstract is not None else '',
            'explanation': explanation.text if explanation is not None else '',
            'recommendations': recommendations.text if recommendations is not None else ''
        }

    # Get all vulnerabilities with their locations
    findings = defaultdict(list)

    for vuln in root.findall('.//fvdl:Vulnerability', ns):
        class_info = vuln.find('fvdl:ClassInfo', ns)
        if class_info is None:
            continue

        class_id = class_info.find('fvdl:ClassID', ns)
        category = class_info.find('fvdl:Type', ns)
        subtype = class_info.find('fvdl:Subtype', ns)

        # Get location info
        analysis_info = vuln.find('fvdl:AnalysisInfo', ns)
        primary = None
        if analysis_info is not None:
            unified = analysis_info.find('.//fvdl:Unified', ns)
            if unified is not None:
                primary = unified.find('.//fvdl:SourceLocation', ns)

        finding = {
            'category': category.text if category is not None else 'Unknown',
            'subtype': subtype.text if subtype is not None else '',
            'file': primary.get('path', 'Unknown') if primary is not None else 'Unknown',
            'line': primary.get('line', '?') if primary is not None else '?'
        }

        cid = class_id.text if class_id is not None else 'unknown'
        findings[cid].append(finding)

    # Combine and print remediation report
    print("=" * 80)
    print("FORTIFY REMEDIATION REPORT")
    print("=" * 80)

    for class_id, issues in findings.items():
        desc = descriptions.get(class_id, {})
        category = issues[0]['category']
        subtype = issues[0]['subtype']

        print(f"\n{'=' * 80}")
        print(f"ISSUE: {category}" + (f" - {subtype}" if subtype else ""))
        print(f"OCCURRENCES: {len(issues)}")
        print("-" * 40)

        print("\nAFFECTED LOCATIONS:")
        for issue in issues:
            print(f"  • {issue['file']}:{issue['line']}")

        if desc.get('recommendations'):
            print(f"\nREMEDIATION:")
            # Clean up HTML tags often present in recommendations
            rec_text = desc['recommendations']
            rec_text = rec_text.replace('<br/>', '\n').replace('<br>', '\n')
            rec_text = rec_text.replace('<p>', '\n').replace('</p>', '')
            # Remove other HTML tags
            import re
            rec_text = re.sub('<[^>]+>', '', rec_text)
            print(f"  {rec_text.strip()}")

        print()


# Run it
extract_remediations('your_scan.fpr')