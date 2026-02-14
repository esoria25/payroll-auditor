#!/usr/bin/env python3
"""
Universal Payroll Auditing Tool
Can be used as standalone, imported as module, or integrated into other systems
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import sys

class UniversalPayrollAuditor:
    """
    Universal auditing tool that can be:
    1. Used as a standalone CLI tool
    2. Imported as a Python module
    3. Called via API/REST endpoint
    4. Integrated into Goose or other automation tools
    """
    
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
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize with optional configuration
        
        Args:
            config: Optional configuration dict with custom field mappings, tolerance, etc.
        """
        self.config = config or {}
        self.file1_data = None
        self.file2_data = None
        self.file1_path = None
        self.file2_path = None
        self.comparison_results = {}
        
        # Allow custom field mappings
        if 'field_mappings' in self.config:
            self.FIELD_MAPPINGS.update(self.config['field_mappings'])
    
    def load_file(self, filepath: str) -> pd.DataFrame:
        """Load CSV, Excel, or PDF file"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = path.suffix.lower()
        if ext == '.csv':
            return pd.read_csv(path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(path, engine='openpyxl')
        elif ext == '.pdf':
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                tables = []
                for page in pdf.pages:
                    tables.extend(page.extract_tables())
                if tables:
                    return pd.DataFrame(tables[0][1:], columns=tables[0][0])
        raise ValueError(f"Unsupported file type: {ext}")
    
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
        return df
    
    def compare_files(self, file1: str, file2: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Compare two payroll files
        
        Args:
            file1: Path to first file
            file2: Path to second file
            verbose: Print progress messages
            
        Returns:
            Dictionary with comparison results
        """
        if verbose:
            print(f"\n{'='*80}")
            print("PAYROLL AUDIT COMPARISON")
            print(f"{'='*80}\n")
        
        # Load files
        if verbose:
            print("Loading files...")
        self.file1_path = file1
        self.file2_path = file2
        self.file1_data = self.load_file(file1)
        self.file2_data = self.load_file(file2)
        
        # Normalize columns
        if verbose:
            print("Normalizing column names...")
        self.file1_data = self.normalize_columns(self.file1_data)
        self.file2_data = self.normalize_columns(self.file2_data)
        
        # Perform comparison
        if verbose:
            print("Performing comparison...")
        
        results = {
            'metadata': self._compare_metadata(),
            'structure': self._compare_structure(),
            'data': self._compare_data(),
            'summary': {}
        }
        
        results['summary'] = self._generate_summary(results)
        self.comparison_results = results
        
        if verbose:
            print(f"\n✓ Comparison complete!")
            print(f"  Match rate: {results['summary']['match_rate']:.2f}%")
            print(f"  Differences: {results['summary']['rows_with_differences']}")
        
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
        """Compare file structure"""
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
        
        # Find identifier column
        id_col = None
        for col in ['employee', 'employee_id', 'id']:
            if col in common_cols:
                id_col = col
                break
        
        differences = []
        matched_rows = 0
        
        if id_col:
            df1_indexed = self.file1_data.set_index(id_col)
            df2_indexed = self.file2_data.set_index(id_col)
            common_ids = set(df1_indexed.index) & set(df2_indexed.index)
            
            for emp_id in common_ids:
                row_diffs = self._compare_rows(
                    df1_indexed.loc[emp_id], 
                    df2_indexed.loc[emp_id], 
                    common_cols, 
                    emp_id
                )
                if row_diffs:
                    differences.append(row_diffs)
                else:
                    matched_rows += 1
        else:
            max_rows = min(len(self.file1_data), len(self.file2_data))
            for idx in range(max_rows):
                row_diffs = self._compare_rows(
                    self.file1_data.iloc[idx],
                    self.file2_data.iloc[idx],
                    common_cols,
                    f"Row {idx}"
                )
                if row_diffs:
                    differences.append(row_diffs)
                else:
                    matched_rows += 1
        
        return {
            'identifier_column': id_col,
            'total_differences': len(differences),
            'matched_rows': matched_rows,
            'differences': differences[:100]
        }
    
    def _compare_rows(self, row1: pd.Series, row2: pd.Series, 
                     columns: List[str], identifier: str) -> Optional[Dict[str, Any]]:
        """Compare two rows"""
        tolerance = self.config.get('numeric_tolerance', 0.01)
        diffs = {}
        
        for col in columns:
            if col not in row1 or col not in row2:
                continue
            
            val1, val2 = row1[col], row2[col]
            
            if pd.isna(val1) and pd.isna(val2):
                continue
            
            try:
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    if abs(float(val1) - float(val2)) > tolerance:
                        diffs[col] = {
                            'file1': val1,
                            'file2': val2,
                            'difference': float(val2) - float(val1)
                        }
                else:
                    if str(val1).strip() != str(val2).strip():
                        diffs[col] = {'file1': val1, 'file2': val2}
            except:
                if val1 != val2:
                    diffs[col] = {'file1': val1, 'file2': val2}
        
        return {'identifier': identifier, 'fields': diffs} if diffs else None
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        data_results = results['data']
        field_stats = {}
        
        if 'differences' in data_results:
            for diff in data_results['differences']:
                for field, values in diff.get('fields', {}).items():
                    if field not in field_stats:
                        field_stats[field] = {'count': 0, 'numeric_diffs': []}
                    
                    field_stats[field]['count'] += 1
                    if 'difference' in values:
                        field_stats[field]['numeric_diffs'].append(values['difference'])
        
        for field, stats in field_stats.items():
            if stats['numeric_diffs']:
                stats['avg_difference'] = np.mean(stats['numeric_diffs'])
                stats['max_difference'] = max(stats['numeric_diffs'])
                stats['min_difference'] = min(stats['numeric_diffs'])
                stats['total_difference'] = sum(stats['numeric_diffs'])
        
        total_rows = data_results.get('matched_rows', 0) + data_results.get('total_differences', 0)
        matched = data_results.get('matched_rows', 0)
        
        return {
            'total_rows_compared': total_rows,
            'rows_with_differences': data_results.get('total_differences', 0),
            'rows_matched': matched,
            'match_rate': (matched / max(1, total_rows)) * 100,
            'field_statistics': field_stats
        }
    
    def generate_report(self, output_file: Optional[str] = None, 
                       format: str = 'json') -> str:
        """
        Generate report in specified format
        
        Args:
            output_file: Optional file path to save report
            format: 'json', 'text', or 'html'
            
        Returns:
            Report as string
        """
        if not self.comparison_results:
            return json.dumps({'error': 'No comparison results available'})
        
        if format == 'json':
            report = json.dumps(self.comparison_results, indent=2, default=str)
        elif format == 'text':
            report = self._generate_text_report()
        elif format == 'html':
            report = self._generate_html_report()
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
    
    def _generate_text_report(self) -> str:
        """Generate text report"""
        lines = ["=" * 80, "PAYROLL AUDIT REPORT", "=" * 80]
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        summary = self.comparison_results['summary']
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total rows: {summary['total_rows_compared']}")
        lines.append(f"Matched: {summary['rows_matched']}")
        lines.append(f"Differences: {summary['rows_with_differences']}")
        lines.append(f"Match rate: {summary['match_rate']:.2f}%")
        
        return "\n".join(lines)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        summary = self.comparison_results['summary']
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Payroll Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .stat {{ display: inline-block; margin: 10px 20px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #1976d2; }}
    </style>
</head>
<body>
    <h1>Payroll Audit Report</h1>
    <div class="summary">
        <div class="stat">
            <div class="stat-value">{summary['total_rows_compared']}</div>
            <div>Total Rows</div>
        </div>
        <div class="stat">
            <div class="stat-value">{summary['match_rate']:.1f}%</div>
            <div>Match Rate</div>
        </div>
        <div class="stat">
            <div class="stat-value">{summary['rows_with_differences']}</div>
            <div>Differences</div>
        </div>
    </div>
</body>
</html>"""

    # API-style methods for integration
    def audit(self, file1: str, file2: str, config: Optional[Dict] = None) -> Dict:
        """
        Simple API-style method for integration
        
        Usage:
            auditor = UniversalPayrollAuditor()
            result = auditor.audit('file1.csv', 'file2.csv')
        """
        if config:
            self.config.update(config)
        return self.compare_files(file1, file2, verbose=False)
    
    def get_summary(self) -> Dict:
        """Get summary of last comparison"""
        return self.comparison_results.get('summary', {})
    
    def get_differences(self, limit: int = 100) -> List[Dict]:
        """Get list of differences"""
        return self.comparison_results.get('data', {}).get('differences', [])[:limit]


# CLI Interface
def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Payroll Auditing Tool')
    parser.add_argument('file1', help='First file to compare')
    parser.add_argument('file2', help='Second file to compare')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-f', '--format', choices=['text', 'html', 'json'], 
                       default='json', help='Report format')
    parser.add_argument('-t', '--tolerance', type=float, default=0.01,
                       help='Numeric comparison tolerance')
    
    args = parser.parse_args()
    
    try:
        config = {'numeric_tolerance': args.tolerance}
        auditor = UniversalPayrollAuditor(config)
        results = auditor.compare_files(args.file1, args.file2)
        
        report = auditor.generate_report(args.output, args.format)
        
        if not args.output:
            print("\n" + report)
        else:
            print(f"\n✓ Report saved to: {args.output}")
        
        print(f"\n{'='*80}")
        print("AUDIT COMPLETE")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
