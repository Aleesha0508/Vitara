# reports/services/extractor.py
import pdfplumber
import re

REFERENCE_RANGES = {
    'CBC': {
        'Hemoglobin':  {'min': 12.0, 'max': 17.5, 'unit': 'g/dL'},
        'WBC':         {'min': 4.0,  'max': 11.0,  'unit': 'x10³/µL'},
        'Platelets':   {'min': 150,  'max': 400,   'unit': 'x10³/µL'},
        'RBC':         {'min': 4.2,  'max': 5.9,   'unit': 'x10⁶/µL'},
    },
    'LFT': {
        'ALT':         {'min': 7,    'max': 56,    'unit': 'U/L'},
        'AST':         {'min': 10,   'max': 40,    'unit': 'U/L'},
        'Bilirubin':   {'min': 0.2,  'max': 1.2,   'unit': 'mg/dL'},
    },
    'KFT': {
        'Creatinine':  {'min': 0.6,  'max': 1.2,   'unit': 'mg/dL'},
        'BUN':         {'min': 7,    'max': 20,    'unit': 'mg/dL'},
        'eGFR':        {'min': 60,   'max': 120,   'unit': 'mL/min'},
    },
    'LIPID': {
        'Total Cholesterol': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
        'LDL':         {'min': 0,    'max': 100,   'unit': 'mg/dL'},
        'HDL':         {'min': 40,   'max': 999,   'unit': 'mg/dL'},
        'Triglycerides':{'min': 0,   'max': 150,   'unit': 'mg/dL'},
    }
}

def extract_lab_values(pdf_path):
    values = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # try table extraction first
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and len(row) >= 2:
                        name = row[0]
                        value = row[1]
                        if name and value:
                            nums = re.findall(r'\d+\.?\d*', str(value))
                            if nums:
                                values[name.strip()] = float(nums[0])
    return values

def flag_abnormals(extracted_values, panel_type):
    findings = []
    ranges = REFERENCE_RANGES.get(panel_type, {})
    for test, value in extracted_values.items():
        if test in ranges:
            ref = ranges[test]
            if value < ref['min']:
                status = 'low'
            elif value > ref['max']:
                status = 'high'
            else:
                status = 'normal'
            findings.append({
                'test': test,
                'value': value,
                'unit': ref['unit'],
                'reference': f"{ref['min']}–{ref['max']}",
                'status': status
            })
    return findings

def extract_and_analyze(report):
    """Called after report is saved. Populates extracted_values and findings."""
    pdf_path = report.pdf_file.path
    extracted = extract_lab_values(pdf_path)
    findings = flag_abnormals(extracted, report.panel_type)
    report.extracted_values = extracted
    report.findings = findings
    report.save()