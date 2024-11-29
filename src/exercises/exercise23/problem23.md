# Create a Python script that converts JSON to CSV, handling arrays within the JSON structure and remove columns in the resulting csv.
In the example below remove json section **"contact"** 

```json
   # Sample JSON data
    sample_data = [
        {
            "id": 1,
            "name": "John Doe",
            "tags": ["developer", "python", "web"],
            "skills": ["JavaScript", "Python"],
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
            }
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "tags": ["designer", "ui/ux"],
            "skills": ["Figma", "Sketch", "CSS"],
            "contact": {
                "email": "jane@example.com",
                "phone": "098-765-4321"
            }
        }
    ]
```

## REsult
```csv
id,name,tags,skills
1,John Doe,developer|python|web,JavaScript|Python
2,Jane Smith,designer|ui/ux,Figma|Sketch|CSS
```