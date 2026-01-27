import csv


def export_to_csv(fpr_path, output_csv):
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

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Category', 'Subtype', 'File', 'Line',
            'Severity', 'Remediation', 'Status'
        ])

        for class_id, issues in findings.items():
            desc = descriptions.get(class_id, {})
            remediation = desc.get('recommendations', '').strip()

            for issue in issues:
                writer.writerow([
                    issue['category'],
                    issue['subtype'],
                    issue['file'],
                    issue['line'],
                    issue.get('severity', ''),
                    remediation,
                    'TODO'  # For tracking
                ])


export_to_csv('your_scan.fpr', 'remediation_tasks.csv')