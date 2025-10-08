#!/usr/bin/env python3
"""
Child Malnutrition Expert System v2.0
=====================================

A comprehensive AI-powered system for diagnosing malnutrition conditions in children.
This system provides both GUI and command-line interfaces.

Author: AI Assistant
Version: 2.0
"""

import sys
import argparse
from gui import MalnutritionExpertGUI
from expert_system import MalnutritionExpertSystem
import tkinter as tk

def run_gui():
    """Run the graphical user interface."""
    try:
        root = tk.Tk()
        app = MalnutritionExpertGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)

def run_cli():
    """Run the command-line interface."""
    try:
        expert_system = MalnutritionExpertSystem("knowledge_base.json")
        symptoms = expert_system.get_all_symptoms()
        
        print("=" * 60)
        print("CHILD MALNUTRITION EXPERT SYSTEM v2.0")
        print("=" * 60)
        print("This system helps identify potential malnutrition conditions in children.")
        print("Please answer all questions accurately for the best possible diagnosis.\n")
        
        responses = {}
        print("Please answer the following questions with 'yes', 'no', or 'skip':\n")
        
        for i, symptom in enumerate(symptoms, 1):
            while True:
                response = input(f"{i}. {symptom.question}\n   Answer (yes/no/skip): ").lower().strip()
                if response in ['yes', 'y', 'no', 'n', 'skip', 's']:
                    if response in ['yes', 'y']:
                        responses[symptom.name] = True
                    elif response in ['no', 'n']:
                        responses[symptom.name] = False
                    else:  # skip
                        responses[symptom.name] = None
                    break
                else:
                    print("   Please enter 'yes', 'no', or 'skip'")
        
        print("\n" + "=" * 60)
        print("PROCESSING DIAGNOSIS...")
        print("=" * 60)
        
        # Get diagnoses
        diagnoses = expert_system.diagnose(responses)
        
        # Generate and display report
        report = expert_system.generate_report(responses, diagnoses)
        print(report)
        
        # Ask if user wants to save report
        save = input("\nWould you like to save this report? (yes/no): ").lower().strip()
        if save in ['yes', 'y']:
            filename = expert_system.save_report(report)
            print(f"Report saved as: {filename}")
        
    except Exception as e:
        print(f"Error running CLI: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Child Malnutrition Expert System v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run GUI interface
  python main.py --gui        # Run GUI interface
  python main.py --cli        # Run command-line interface
        """
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help='Run graphical user interface (default)'
    )
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Run command-line interface'
    )
    
    args = parser.parse_args()
    
    if args.cli:
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
