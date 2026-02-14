#!/usr/bin/env python3
"""
Goose Payroll Auditor Extension
Custom integration for Goose Desktop application
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import json

# Import the universal auditor
try:
    from universal_payroll_auditor import UniversalPayrollAuditor
except ImportError:
    # If not installed, try local import
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from universal_payroll_auditor import UniversalPayrollAuditor


class GoosePayrollAuditor:
    """
    Goose-specific integration for payroll auditing
    Provides simplified interface optimized for Goose workflows
    """
    
    def __init__(self):
        self.auditor = UniversalPayrollAuditor()
        self.last_result = None
        self.history = []
    
    def quick_audit(self, file1: str, file2: str) -> str:
        """
        Quick audit with formatted output for Goose
        
        Args:
            file1: Path to first payroll file
            file2: Path to second payroll file
            
        Returns:
            Formatted summary string
        """
        try:
            result = self.auditor.audit(file1, file2)
            self.last_result = result
            self.history.append({
                'file1': file1,
                'file2': file2,
                'timestamp': result.get('timestamp'),
                'match_rate': result['summary']['match_rate']
            })
            
            return self._format_summary(result)
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _format_summary(self, result: Dict) -> str:
        """Format result for Goose display"""
        summary = result['summary']
        meta = result['metadata']
        
        output = []
        output.append("\n" + "="*60)
        output.append("📊 PAYROLL AUDIT SUMMARY")
        output.append("="*60)
        output.append(f"\n📁 Files Compared:")
        output.append(f"   • {meta['file1']['name']} ({meta['file1']['rows']} rows)")
        output.append(f"   • {meta['file2']['name']} ({meta['file2']['rows']} rows)")
        output.append(f"\n📈 Results:")
        output.append(f"   • Total Rows: {summary['total_rows_compared']}")
        output.append(f"   • Matched: {summary['rows_matched']} ✓")
        output.append(f"   • Differences: {summary['rows_with_differences']}")
        output.append(f"   • Match Rate: {summary['match_rate']:.2f}%")
        
        if summary['match_rate'] >= 95:
            output.append(f"\n✅ EXCELLENT - High match rate!")
        elif summary['match_rate'] >= 85:
            output.append(f"\n⚠️  WARNING - Moderate differences found")
        else:
            output.append(f"\n❌ ALERT - Significant differences detected!")
        
        # Field-level stats
        if summary['field_statistics']:
            output.append(f"\n🔍 Field Differences:")
            for field, stats in list(summary['field_statistics'].items())[:5]:
                output.append(f"   • {field}: {stats['count']} differences")
                if 'avg_difference' in stats:
                    output.append(f"     Avg: {stats['avg_difference']:.2f}")
        
        output.append("\n" + "="*60)
        return "\n".join(output)
    
    def get_differences(self, limit: int = 10) -> str:
        """
        Get detailed differences from last audit
        
        Args:
            limit: Maximum number of differences to show
            
        Returns:
            Formatted differences string
        """
        if not self.last_result:
            return "❌ No audit results available. Run quick_audit() first."
        
        diffs = self.last_result['data'].get('differences', [])[:limit]
        
        if not diffs:
            return "✅ No differences found!"
        
        output = []
        output.append("\n" + "="*60)
        output.append(f"📋 DETAILED DIFFERENCES (showing {len(diffs)})")
        output.append("="*60)
        
        for i, diff in enumerate(diffs, 1):
            output.append(f"\n{i}. {diff['identifier']}")
            for field, values in diff['fields'].items():
                output.append(f"   {field}:")
                output.append(f"      File 1: {values['file1']}")
                output.append(f"      File 2: {values['file2']}")
                if 'difference' in values:
                    output.append(f"      Δ: {values['difference']:.2f}")
        
        output.append("\n" + "="*60)
        return "\n".join(output)
    
    def generate_report(self, output_path: str, format: str = 'html') -> str:
        """
        Generate detailed report
        
        Args:
            output_path: Path to save report
            format: 'html', 'json', or 'text'
            
        Returns:
            Success message
        """
        if not self.last_result:
            return "❌ No audit results available. Run quick_audit() first."
        
        try:
            self.auditor.comparison_results = self.last_result
            self.auditor.generate_report(output_path, format)
            return f"✅ Report saved to: {output_path}"
        except Exception as e:
            return f"❌ Error generating report: {str(e)}"
    
    def batch_audit(self, directory: str, pattern: str = "*.csv") -> str:
        """
        Audit all matching files in a directory
        
        Args:
            directory: Directory containing files
            pattern: File pattern to match
            
        Returns:
            Formatted batch results
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return f"❌ Directory not found: {directory}"
        
        files = sorted(dir_path.glob(pattern))
        if len(files) < 2:
            return f"❌ Need at least 2 files. Found {len(files)}"
        
        output = []
        output.append("\n" + "="*60)
        output.append("📦 BATCH AUDIT RESULTS")
        output.append("="*60)
        output.append(f"\nFound {len(files)} files in {directory}")
        output.append(f"\nComparing consecutive files...\n")
        
        results = []
        for i in range(len(files) - 1):
            file1 = str(files[i])
            file2 = str(files[i + 1])
            
            try:
                result = self.auditor.audit(file1, file2)
                match_rate = result['summary']['match_rate']
                diffs = result['summary']['rows_with_differences']
                
                status = "✅" if match_rate >= 95 else "⚠️" if match_rate >= 85 else "❌"
                output.append(f"{status} {files[i].name} vs {files[i+1].name}")
                output.append(f"   Match: {match_rate:.1f}% | Diffs: {diffs}")
                
                results.append({
                    'file1': files[i].name,
                    'file2': files[i+1].name,
                    'match_rate': match_rate,
                    'differences': diffs
                })
            except Exception as e:
                output.append(f"❌ Error: {files[i].name} vs {files[i+1].name}: {str(e)}")
        
        # Summary
        if results:
            avg_match = sum(r['match_rate'] for r in results) / len(results)
            total_diffs = sum(r['differences'] for r in results)
            output.append(f"\n📊 Overall Summary:")
            output.append(f"   • Comparisons: {len(results)}")
            output.append(f"   • Avg Match Rate: {avg_match:.2f}%")
            output.append(f"   • Total Differences: {total_diffs}")
        
        output.append("\n" + "="*60)
        return "\n".join(output)
    
    def compare_latest(self, directory: str, pattern: str = "*.csv") -> str:
        """
        Compare the two most recent files in a directory
        
        Args:
            directory: Directory containing files
            pattern: File pattern to match
            
        Returns:
            Formatted comparison result
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return f"❌ Directory not found: {directory}"
        
        files = sorted(dir_path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if len(files) < 2:
            return f"❌ Need at least 2 files. Found {len(files)}"
        
        return self.quick_audit(str(files[1]), str(files[0]))
    
    def get_history(self) -> str:
        """Get audit history"""
        if not self.history:
            return "📝 No audit history available"
        
        output = []
        output.append("\n" + "="*60)
        output.append("📜 AUDIT HISTORY")
        output.append("="*60)
        
        for i, item in enumerate(self.history[-10:], 1):
            output.append(f"\n{i}. {Path(item['file1']).name} vs {Path(item['file2']).name}")
            output.append(f"   Match Rate: {item['match_rate']:.2f}%")
        
        output.append("\n" + "="*60)
        return "\n".join(output)


# Convenience functions for Goose
_auditor = None

def init_auditor():
    """Initialize the global auditor instance"""
    global _auditor
    if _auditor is None:
        _auditor = GoosePayrollAuditor()
    return _auditor

def audit(file1: str, file2: str) -> str:
    """Quick audit two files"""
    return init_auditor().quick_audit(file1, file2)

def differences(limit: int = 10) -> str:
    """Show differences from last audit"""
    return init_auditor().get_differences(limit)

def report(output_path: str, format: str = 'html') -> str:
    """Generate report from last audit"""
    return init_auditor().generate_report(output_path, format)

def batch(directory: str, pattern: str = "*.csv") -> str:
    """Batch audit files in directory"""
    return init_auditor().batch_audit(directory, pattern)

def latest(directory: str, pattern: str = "*.csv") -> str:
    """Compare two most recent files"""
    return init_auditor().compare_latest(directory, pattern)

def history() -> str:
    """Show audit history"""
    return init_auditor().get_history()


# CLI for testing
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Goose Payroll Auditor')
    parser.add_argument('command', choices=['audit', 'batch', 'latest', 'history'])
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    if args.command == 'audit':
        if len(args.args) < 2:
            print("Usage: audit <file1> <file2>")
            sys.exit(1)
        print(audit(args.args[0], args.args[1]))
    
    elif args.command == 'batch':
        if len(args.args) < 1:
            print("Usage: batch <directory> [pattern]")
            sys.exit(1)
        pattern = args.args[1] if len(args.args) > 1 else "*.csv"
        print(batch(args.args[0], pattern))
    
    elif args.command == 'latest':
        if len(args.args) < 1:
            print("Usage: latest <directory> [pattern]")
            sys.exit(1)
        pattern = args.args[1] if len(args.args) > 1 else "*.csv"
        print(latest(args.args[0], pattern))
    
    elif args.command == 'history':
        print(history())
