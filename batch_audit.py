#!/usr/bin/env python3
"""
Example batch processing script for payroll auditing
"""

from payroll_auditor import PayrollAuditor
from pathlib import Path
import sys

def batch_audit(directory: str, pattern1: str = "*_original.*", pattern2: str = "*_corrected.*"):
    """
    Batch audit all file pairs in a directory
    
    Args:
        directory: Path to directory containing files
        pattern1: Glob pattern for first set of files
        pattern2: Glob pattern for second set of files
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"Error: Directory not found: {directory}")
        return
    
    # Find all original files
    original_files = sorted(dir_path.glob(pattern1))
    
    if not original_files:
        print(f"No files found matching pattern: {pattern1}")
        return
    
    print(f"Found {len(original_files)} files to audit\n")
    
    auditor = PayrollAuditor()
    results_summary = []
    
    for original_file in original_files:
        # Try to find corresponding corrected file
        base_name = original_file.stem.replace('_original', '')
        corrected_file = None
        
        # Look for matching corrected file
        for ext in ['.csv', '.xlsx', '.xls']:
            potential_match = dir_path / f"{base_name}_corrected{ext}"
            if potential_match.exists():
                corrected_file = potential_match
                break
        
        if not corrected_file:
            print(f"⚠ No matching corrected file for: {original_file.name}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Auditing: {original_file.name} vs {corrected_file.name}")
        print(f"{'='*80}")
        
        try:
            # Perform comparison
            results = auditor.compare_files(str(original_file), str(corrected_file))
            
            # Generate HTML report
            report_name = f"audit_{base_name}.html"
            report_path = dir_path / report_name
            auditor.generate_report(str(report_path), format='html')
            
            # Store summary
            summary = results['summary']
            results_summary.append({
                'original': original_file.name,
                'corrected': corrected_file.name,
                'match_rate': summary['match_rate'],
                'differences': summary['rows_with_differences'],
                'total_rows': summary['total_rows_compared'],
                'report': report_name
            })
            
            print(f"✓ Audit complete - Match rate: {summary['match_rate']:.2f}%")
            print(f"✓ Report saved: {report_name}")
            
        except Exception as e:
            print(f"✗ Error auditing files: {e}")
            continue
    
    # Print overall summary
    print(f"\n\n{'='*80}")
    print("BATCH AUDIT SUMMARY")
    print(f"{'='*80}\n")
    
    if results_summary:
        print(f"{'File Pair':<50} {'Match Rate':<12} {'Differences':<12}")
        print("-" * 80)
        
        for result in results_summary:
            file_pair = f"{result['original']} vs {result['corrected']}"
            print(f"{file_pair:<50} {result['match_rate']:>10.2f}% {result['differences']:>12}")
        
        # Calculate overall statistics
        avg_match_rate = sum(r['match_rate'] for r in results_summary) / len(results_summary)
        total_differences = sum(r['differences'] for r in results_summary)
        total_rows = sum(r['total_rows'] for r in results_summary)
        
        print("-" * 80)
        print(f"{'OVERALL':<50} {avg_match_rate:>10.2f}% {total_differences:>12}")
        print(f"\nTotal rows audited: {total_rows}")
        print(f"Average match rate: {avg_match_rate:.2f}%")
    else:
        print("No files were successfully audited.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python batch_audit.py <directory> [pattern1] [pattern2]")
        print("\nExample:")
        print("  python batch_audit.py ./payroll_data")
        print("  python batch_audit.py ./payroll_data '*_jan.*' '*_jan_corrected.*'")
        sys.exit(1)
    
    directory = sys.argv[1]
    pattern1 = sys.argv[2] if len(sys.argv) > 2 else "*_original.*"
    pattern2 = sys.argv[3] if len(sys.argv) > 3 else "*_corrected.*"
    
    batch_audit(directory, pattern1, pattern2)
