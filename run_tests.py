#!/usr/bin/env python3
"""
Test runner script for the Ice Cream API
This script runs all unit tests and provides detailed reporting
"""

import sys
import os
import unittest
import subprocess

def run_tests():
    """Run all unit tests and return the result."""
    print("=" * 60)
    print("Running Ice Cream API Unit Tests")
    print("=" * 60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Return success/failure
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n All tests passed!")
        return 0
    else:
        print("\n Some tests failed!")
        return 1

def run_with_coverage():
    """Run tests with coverage reporting."""
    try:
        print("Running tests with coverage...")
        
        # Run coverage
        cmd = [sys.executable, '-m', 'coverage', 'run', '-m', 'unittest', 'discover', '-v']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Generate coverage report
        if result.returncode == 0:
            print("\nGenerating coverage report...")
            coverage_cmd = [sys.executable, '-m', 'coverage', 'report']
            coverage_result = subprocess.run(coverage_cmd, capture_output=True, text=True)
            print(coverage_result.stdout)
        
        return result.returncode
        
    except FileNotFoundError:
        print("Coverage not available, running tests without coverage...")
        return run_tests()

if __name__ == '__main__':
    # Check if coverage is available
    try:
        import coverage
        exit_code = run_with_coverage()
    except ImportError:
        print("Coverage module not found, running basic tests...")
        exit_code = run_tests()
    
    sys.exit(exit_code) 