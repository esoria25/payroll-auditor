#!/usr/bin/env python3
"""
Payroll Data Auditing Tool
Compares payroll data from CSV, Excel, and PDF files
Generates detailed reports with differences, side-by-side comparison, and summary statistics
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
import sys

# Try to import optional dependencies
try:
    import openpyxl
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    print("Warning: openpyxl not installed. Excel support limited.")

try:
    import tabulate
    TABULATE_SUPPORT = True
except ImportError:
    TABULATE_SUPPORT = False
    print("Warning: tabulate not installed. Using basic formatting.")

try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pdfplumber not installed. PDF support disabled.")


class PayrollAuditor:
    """Main class for auditing payroll files"""
    
    # Standard payroll field mappings (case-insensitive)
    FIELD_MAPPINGS = {
        'employee': ['employee', 'employee_name', 'name', 'emp_name', 'employee name'],
        'pay_date': ['pay_date', 'paydate', 'date', 'payment_date', 'pay date'],
        'hours': ['hours', 'regular_hours', 'reg_hours', 'regular hours'],
        'overtime': ['overtime', 'ot_hours', 'overtime_hours', 'ot hours', 'overtime hours'],
        'pto': ['pto', 'vacation', 'pto_hours', 'vacation_hours', 'pto hours', 'vacation hours'],
        'sick': ['sick', 'sick_hours', 'sick_leave', 'sick hours', 'sick leave'],
        'tips_cash': ['tips_cash', 'cash_tips', 'tips', 'tips cash', 'cash tips'],
        'tips_paycheck': ['tips_paycheck', 'paycheck_tips', 'tips paycheck'],
        'federal_tax': ['federal_tax', 'fed_tax', 'federal_income_tax', 'federal tax', 'fed tax'],
        'social_security': ['social_security', 'fica', 'socsec', 'ss_tax', 'social security', 'fica tax'],
        'medicare': ['medicare', 'med_wh', 'medicare_tax', 'med wh', 'medicare tax'],
        'state_tax': ['state_tax', 'state_income_tax', 'state tax', 'state income tax'],
        'local_tax': ['local_tax', 'city_tax', 'local_city_tax', 'local tax', 'city tax'],
        'pfml': ['pfml', 'paid_family_leave', 'family_leave', 'paid family leave']
    }
    
    def __init__(self):
        self.file1_data = None
        self.file2_data = None
        self.file1_path = None
        self.file2_path = None
        self.comparison_results = {}
        
    def load_file(self, filepath: str) -> pd.DataFrame:
        """Load a file (CSV, Excel, or PDF) into a DataFrame"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = path.suffix.lower()
        
        if ext == '.csv':
            return self._load_csv(path)
        elif ext in ['.xlsx', '.xls']:
            return self._load_excel(path)
        elif ext == '.pdf':
            return self._load_pdf(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _load_csv(self, path: Path) -> pd.DataFrame:
        """Load CSV file"""
        try:
            df = pd.read_csv(path)
            print(f"✓ Loaded CSV: {path.name} ({len(df)} rows, {len(df.columns)} columns)")
            return df
        except Exception as e:
            raise Exception(f"Error loading CSV: {e}")
    
    def _load_excel(self, path: Path) -> pd.DataFrame:
        """Load Excel file"""
        if not EXCEL_SUPPORT:
            raise Exception("Excel support requires openpyxl. Install with: pip install openpyxl")
        
        try:
            df = pd.read_excel(path, engine='openpyxl')
            print(f"✓ Loaded Excel: {path.name} ({len(df)} rows, {len(df.columns)} columns)")
            return df
        except Exception as e:
            raise Exception(f"Error loading Excel: {e}")
    
    def _load_pdf(self, path: Path) -> pd.DataFrame:
        """Load PDF file and extract table data"""
        if not PDF_SUPPORT:
            raise Exception("PDF support requires pdfplumber. Install with: pip install pdfplumber")
        
        try:
            with pdfplumber.open(path) as pdf:
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    all_tables.extend(tables)
                
                if not all_tables:
                    raise Exception("No tables found in PDF")
                
                # Use the first table or combine tables
                table = all_tables[0]
                df = pd.DataFrame(table[1:], columns=table[0])
                print(f"✓ Loaded PDF: {path.name} ({len(df)} rows, {len(df.columns)} columns)")
                return df
        except Exception as e:
            raise Exception(f"Error loading PDF: {e}")
    
    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to standard format"""
        df = df.copy()
        column_mapping = {}
        
        for col in df.columns:
            col_lower = str(col).lower().strip()
            for standard_name, variations in self.FIELD_MAPPINGS.items():
                if col_lower in variations:
                    column_mapping[col] = standard_name
                    break
        
        if column_mapping:
            df = df.rename(columns=column_mapping)
            print(f"  Normalized {len(column_mapping)} columns: {list(column_mapping.values())}")
        
        return df
    
    def compare_files(self, file1: str, file2: str) -> Dict[str, Any]:
        """Compare two payroll files"""
        print(f"\n{'='*80}")
        print(f"PAYROLL AUDIT COMPARISON")
        print(f"{'='*80}\n")
        
        # Load files
        print("\nLoading files...")
        self.file1_path = file1
        self.file2_path = file2
        self.file1_data = self.load_file(file1)
        self.file2_data = self.load_file(file2)
        
        # Normalize columns
        print("\nNormalizing column names...")
        self.file1_data = self.normalize_columns(self.file1_data)
        self.file2_data = self.normalize_columns(self.file2_data)
        
        # Perform comparison
        print("\nPerforming comparison...")
        results = {
            'metadata': self._compare_metadata(),
            'structure': self._compare_structure(),
            'data': self._compare_data(),
            'summary': {}
        }
        
        # Generate summary statistics
        results['summary'] = self._generate_summary(results)
        
        self.comparison_results = results
        return results
    
    def _compare_metadata(self) -> Dict[str, Any]:
        """Compare file metadata"""
        return {
            'file1': {
                'name': Path(self.file1_path).name,
                'rows': len(self.file1_data),
                'columns': len(self.file1_data.columns)
            },
            'file2': {
                'name': Path(self.file2_path).name,
                'rows': len(self.file2_data),
                'columns': len(self.file2_data.columns)
            }
        }
    
    def _compare_structure(self) -> Dict[str, Any]:
        """Compare file structure (columns)"""
        cols1 = set(self.file1_data.columns)
        cols2 = set(self.file2_data.columns)
        
        return {
            'file1_columns': list(cols1),
            'file2_columns': list(cols2),
            'common_columns': list(cols1 & cols2),
            'only_in_file1': list(cols1 - cols2),
            'only_in_file2': list(cols2 - cols1)
        }
    
    def _compare_data(self) -> Dict[str, Any]:
        """Compare data line-by-line"""
        common_cols = list(set(self.file1_data.columns) & set(self.file2_data.columns))
        
        if not common_cols:
            return {'error': 'No common columns found for comparison'}
        
        # Try to find employee identifier
        id_col = None
        for col in ['employee', 'employee_id', 'id']:
            if col in common_cols:
                id_col = col
                break
        
        differences = []
        matched_rows = 0
        unmatched_file1 = []
        unmatched_file2 = []
        
        if id_col:
            # Match by employee ID
            df1_indexed = self.file1_data.set_index(id_col)
            df2_indexed = self.file2_data.set_index(id_col)
            
            common_ids = set(df1_indexed.index) & set(df2_indexed.index)
            only_file1_ids = set(df1_indexed.index) - set(df2_indexed.index)
            only_file2_ids = set(df2_indexed.index) - set(df1_indexed.index)
            
            # Compare common rows
            for emp_id in common_ids:
                row1 = df1_indexed.loc[emp_id]
                row2 = df2_indexed.loc[emp_id]
                
                row_diffs = self._compare_rows(row1, row2, common_cols, emp_id)
                if row_diffs:
                    differences.append(row_diffs)
                else:
                    matched_rows += 1
            
            unmatched_file1 = [{'id': id, 'data': df1_indexed.loc[id].to_dict()} 
                              for id in only_file1_ids]
            unmatched_file2 = [{'id': id, 'data': df2_indexed.loc[id].to_dict()} 
                              for id in only_file2_ids]
        else:
            # Compare by row index
            max_rows = min(len(self.file1_data), len(self.file2_data))
            for idx in range(max_rows):
                row1 = self.file1_data.iloc[idx]
                row2 = self.file2_data.iloc[idx]
                
                row_diffs = self._compare_rows(row1, row2, common_cols, f"Row {idx}")
                if row_diffs:
                    differences.append(row_diffs)
                else:
                    matched_rows += 1
        
        return {
            'identifier_column': id_col,
            'total_differences': len(differences),
            'matched_rows': matched_rows,
            'differences': differences[:100],  # Limit to first 100 for display
            'unmatched_file1': unmatched_file1[:20],
            'unmatched_file2': unmatched_file2[:20]
        }
    
    def _compare_rows(self, row1: pd.Series, row2: pd.Series, 
                     columns: List[str], identifier: str) -> Dict[str, Any]:
        """Compare two rows and return differences"""
        diffs = {}
        
        for col in columns:
            if col not in row1 or col not in row2:
                continue
            
            val1 = row1[col]
            val2 = row2[col]
            
            # Handle NaN values
            if pd.isna(val1) and pd.isna(val2):
                continue
            
            # Convert to comparable types
            try:
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    if abs(float(val1) - float(val2)) > 0.01:  # Tolerance for floating point
                        diffs[col] = {
                            'file1': val1,
                            'file2': val2,
                            'difference': float(val2) - float(val1)
                        }
                else:
                    if str(val1).strip() != str(val2).strip():
                        diffs[col] = {
                            'file1': val1,
                            'file2': val2
                        }
            except:
                if val1 != val2:
                    diffs[col] = {
                        'file1': val1,
                        'file2': val2
                    }
        
        if diffs:
            return {
                'identifier': identifier,
                'fields': diffs
            }
        return None
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        data_results = results['data']
        
        # Calculate field-level statistics
        field_stats = {}
        if 'differences' in data_results:
            for diff in data_results['differences']:
                for field, values in diff.get('fields', {}).items():
                    if field not in field_stats:
                        field_stats[field] = {'count': 0, 'numeric_diffs': []}
                    
                    field_stats[field]['count'] += 1
                    if 'difference' in values:
                        field_stats[field]['numeric_diffs'].append(values['difference'])
        
        # Calculate statistics for numeric fields
        for field, stats in field_stats.items():
            if stats['numeric_diffs']:
                stats['avg_difference'] = np.mean(stats['numeric_diffs'])
                stats['max_difference'] = max(stats['numeric_diffs'])
                stats['min_difference'] = min(stats['numeric_diffs'])
                stats['total_difference'] = sum(stats['numeric_diffs'])
        
        return {
            'total_rows_compared': data_results.get('matched_rows', 0) + data_results.get('total_differences', 0),
            'rows_with_differences': data_results.get('total_differences', 0),
            'rows_matched': data_results.get('matched_rows', 0),
            'match_rate': (data_results.get('matched_rows', 0) / 
                          max(1, data_results.get('matched_rows', 0) + data_results.get('total_differences', 0))) * 100,
            'field_statistics': field_stats,
            'unmatched_in_file1': len(data_results.get('unmatched_file1', [])),
            'unmatched_in_file2': len(data_results.get('unmatched_file2', []))
        }
    
    def generate_report(self, output_file: str = None, format: str = 'text') -> str:
        """Generate a detailed comparison report"""
        if not self.comparison_results:
            return "No comparison results available. Run compare_files() first."
        
        if format == 'text':
            report = self._generate_text_report()
        elif format == 'html':
            report = self._generate_html_report()
        elif format == 'json':
            report = json.dumps(self.comparison_results, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"
✓ Report saved to: {output_file}")
        
        return report
    
    def _generate_text_report(self) -> str:
        """Generate text-based report"""
        lines = []
        results = self.comparison_results
        
        # Header
        lines.append("=" * 80)
        lines.append("PAYROLL AUDIT REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Metadata
        lines.append("FILE INFORMATION")
        lines.append("-" * 80)
        meta = results['metadata']
        lines.append(f"File 1: {meta['file1']['name']}")
        lines.append(f"  Rows: {meta['file1']['rows']}, Columns: {meta['file1']['columns']}")
        lines.append(f"File 2: {meta['file2']['name']}")
        lines.append(f"  Rows: {meta['file2']['rows']}, Columns: {meta['file2']['columns']}")
        lines.append("")
        
        # Structure comparison
        lines.append("STRUCTURE COMPARISON")
        lines.append("-" * 80)
        struct = results['structure']
        lines.append(f"Common columns: {', '.join(struct['common_columns'])}")
        if struct['only_in_file1']:
            lines.append(f"Only in File 1: {', '.join(struct['only_in_file1'])}")
        if struct['only_in_file2']:
            lines.append(f"Only in File 2: {', '.join(struct['only_in_file2'])}")
        lines.append("")
        
        # Summary statistics
        lines.append("SUMMARY STATISTICS")
        lines.append("-" * 80)
        summary = results['summary']
        lines.append(f"Total rows compared: {summary['total_rows_compared']}")
        lines.append(f"Rows with differences: {summary['rows_with_differences']}")
        lines.append(f"Rows matched perfectly: {summary['rows_matched']}")
        lines.append(f"Match rate: {summary['match_rate']:.2f}%")
        
        if summary.get('unmatched_in_file1', 0) > 0:
            lines.append(f"Unmatched in File 1: {summary['unmatched_in_file1']}")
        if summary.get('unmatched_in_file2', 0) > 0:
            lines.append(f"Unmatched in File 2: {summary['unmatched_in_file2']}")
        lines.append("")
        
        # Field-level statistics
        if summary['field_statistics']:
            lines.append("FIELD-LEVEL DIFFERENCES")
            lines.append("-" * 80)
            for field, stats in summary['field_statistics'].items():
                lines.append(f"
{field.upper()}:")
                lines.append(f"  Differences found: {stats['count']}")
                if 'avg_difference' in stats:
                    lines.append(f"  Average difference: {stats['avg_difference']:.2f}")
                    lines.append(f"  Total difference: {stats['total_difference']:.2f}")
                    lines.append(f"  Range: {stats['min_difference']:.2f} to {stats['max_difference']:.2f}")
            lines.append("")
        
        # Detailed differences
        data = results['data']
        if data.get('differences'):
            lines.append("DETAILED DIFFERENCES (First 20)")
            lines.append("-" * 80)
            for i, diff in enumerate(data['differences'][:20], 1):
                lines.append(f"
{i}. {diff['identifier']}")
                for field, values in diff['fields'].items():
                    lines.append(f"   {field}:")
                    lines.append(f"     File 1: {values['file1']}")
                    lines.append(f"     File 2: {values['file2']}")
                    if 'difference' in values:
                        lines.append(f"     Δ: {values['difference']:.2f}")
        
        # Unmatched records
        if data.get('unmatched_file1'):
            lines.append("

UNMATCHED RECORDS IN FILE 1 (First 10)")
            lines.append("-" * 80)
            for item in data['unmatched_file1'][:10]:
                lines.append(f"  {item['id']}: {item['data']}")
        
        if data.get('unmatched_file2'):
            lines.append("

UNMATCHED RECORDS IN FILE 2 (First 10)")
            lines.append("-" * 80)
            for item in data['unmatched_file2'][:10]:
                lines.append(f"  {item['id']}: {item['data']}")
        
        lines.append("
" + "=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "
".join(lines)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        # Basic HTML template
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Payroll Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
        .metadata {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-box {{ background: #e3f2fd; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #1976d2; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .difference {{ background: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }}
        .match {{ color: #4CAF50; }}
        .mismatch {{ color: #f44336; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Payroll Audit Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        {self._html_metadata()}
        {self._html_summary()}
        {self._html_field_stats()}
        {self._html_differences()}
    </div>
</body>
</html>
"""
        return html
    
    def _html_metadata(self) -> str:
        meta = self.comparison_results['metadata']
        return f"""
        <h2>File Information</h2>
        <div class="metadata">
            <p><strong>File 1:</strong> {meta['file1']['name']} ({meta['file1']['rows']} rows, {meta['file1']['columns']} columns)</p>
            <p><strong>File 2:</strong> {meta['file2']['name']} ({meta['file2']['rows']} rows, {meta['file2']['columns']} columns)</p>
        </div>
        """
    
    def _html_summary(self) -> str:
        summary = self.comparison_results['summary']
        return f"""
        <h2>Summary Statistics</h2>
        <div class="summary">
            <div class="stat-box">
                <div class="stat-value">{summary['total_rows_compared']}</div>
                <div class="stat-label">Total Rows</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{summary['rows_matched']}</div>
                <div class="stat-label">Matched</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{summary['rows_with_differences']}</div>
                <div class="stat-label">Differences</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{summary['match_rate']:.1f}%</div>
                <div class="stat-label">Match Rate</div>
            </div>
        </div>
        """
    
    def _html_field_stats(self) -> str:
        summary = self.comparison_results['summary']
        if not summary['field_statistics']:
            return ""
        
        rows = []
        for field, stats in summary['field_statistics'].items():
            row = f"<tr><td>{field}</td><td>{stats['count']}</td>"
            if 'avg_difference' in stats:
                row += f"<td>{stats['avg_difference']:.2f}</td><td>{stats['total_difference']:.2f}</td>"
            else:
                row += "<td>N/A</td><td>N/A</td>"
            row += "</tr>"
            rows.append(row)
        
        return f"""
        <h2>Field-Level Statistics</h2>
        <table>
            <tr>
                <th>Field</th>
                <th>Differences</th>
                <th>Avg Difference</th>
                <th>Total Difference</th>
            </tr>
            {''.join(rows)}
        </table>
        """
    
    def _html_differences(self) -> str:
        data = self.comparison_results['data']
        if not data.get('differences'):
            return "<h2>No Differences Found</h2>"
        
        diffs_html = []
        for diff in data['differences'][:20]:
            fields_html = []
            for field, values in diff['fields'].items():
                diff_str = f" (Δ: {values['difference']:.2f})" if 'difference' in values else ""
                fields_html.append(f"<strong>{field}:</strong> {values['file1']} → {values['file2']}{diff_str}")
            
            diffs_html.append(f"""
            <div class="difference">
                <strong>{diff['identifier']}</strong><br>
                {' | '.join(fields_html)}
            </div>
            """)
        
        return f"""
        <h2>Detailed Differences (First 20)</h2>
        {''.join(diffs_html)}
        """


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Payroll Data Auditing Tool')
    parser.add_argument('file1', help='First file to compare (CSV, Excel, or PDF)')
    parser.add_argument('file2', help='Second file to compare (CSV, Excel, or PDF)')
    parser.add_argument('-o', '--output', help='Output report file path')
    parser.add_argument('-f', '--format', choices=['text', 'html', 'json'], 
                       default='text', help='Report format (default: text)')
    
    args = parser.parse_args()
    
    try:
        auditor = PayrollAuditor()
        results = auditor.compare_files(args.file1, args.file2)
        
        # Generate and display report
        report = auditor.generate_report(args.output, args.format)
        
        if not args.output:
            print("
" + report)
        
        # Print summary
        summary = results['summary']
        print(f"
{'='*80}")
        print(f"AUDIT COMPLETE")
        print(f"{'='*80}")
        print(f"Match Rate: {summary['match_rate']:.2f}%")
        print(f"Differences Found: {summary['rows_with_differences']}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
