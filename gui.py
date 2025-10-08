import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from expert_system import MalnutritionExpertSystem
from datetime import datetime
import json
import threading

class MalnutritionExpertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Malnutrition Expert System v2.0")
        self.root.geometry("1000x900")
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
        
        # Initialize the expert system
        try:
            self.expert_system = MalnutritionExpertSystem("knowledge_base.json")
            self.symptoms = self.expert_system.get_all_symptoms()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize expert system: {str(e)}")
            self.root.destroy()
            return
        
        # Apply a modern theme first
        self.setup_theme()
        
        # Initialize variables
        self.current_question = 0
        self.responses = {}
        self.is_processing = False
        
        # Create main containers
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_theme(self):
        """Setup modern theme and styling."""
        self.style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        # Configure styles
        self.style.configure("Header.TLabel", 
                           font=("Segoe UI", 18, "bold"),
                           foreground=self.colors['primary'])
        
        self.style.configure("Subheader.TLabel",
                           font=("Segoe UI", 12),
                           foreground=self.colors['dark'])
        
        self.style.configure("Question.TLabel",
                           font=("Segoe UI", 11),
                           foreground=self.colors['dark'],
                           wraplength=800)
        
        self.style.configure("TButton",
                           font=("Segoe UI", 10, "bold"),
                           padding=(10, 5))
        
        self.style.configure("Success.TButton",
                           font=("Segoe UI", 10, "bold"),
                           foreground="white",
                           background=self.colors['success'])
        
        self.style.configure("Danger.TButton",
                           font=("Segoe UI", 10, "bold"),
                           foreground="white",
                           background=self.colors['danger'])
        
        self.style.configure("Info.TButton",
                           font=("Segoe UI", 10, "bold"),
                           foreground="white",
                           background=self.colors['secondary'])

    def create_header(self):
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.pack(fill=tk.X)
        
        # Main title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            title_frame, 
            text="🏥 Child Malnutrition Expert System",
            style="Header.TLabel"
        )
        title.pack(side=tk.LEFT)
        
        # Version label
        version_label = ttk.Label(
            title_frame,
            text="v2.0",
            font=("Segoe UI", 10),
            foreground=self.colors['secondary']
        )
        version_label.pack(side=tk.RIGHT)
        
        # Description
        description = ttk.Label(
            header_frame,
            text="Advanced AI-powered system for identifying malnutrition conditions in children.\n"
                 "Please answer all questions accurately for the most reliable diagnosis.",
            style="Subheader.TLabel",
            wraplength=800
        )
        description.pack(pady=(10, 0))
        
        # Status bar
        self.status_frame = ttk.Frame(header_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready to begin diagnosis",
            font=("Segoe UI", 9),
            foreground=self.colors['success']
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.question_count_label = ttk.Label(
            self.status_frame,
            text=f"Total Questions: {len(self.symptoms)}",
            font=("Segoe UI", 9),
            foreground=self.colors['dark']
        )
        self.question_count_label.pack(side=tk.RIGHT)

    def create_main_content(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Progress bar with percentage
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=len(self.symptoms),
            length=400
        )
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.progress_label = ttk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors['primary']
        )
        self.progress_label.pack(side=tk.RIGHT)
        
        # Question section
        question_section = ttk.LabelFrame(self.main_frame, text="Current Question", padding="15")
        question_section.pack(fill=tk.X, pady=(0, 20))
        
        self.question_label = ttk.Label(
            question_section,
            text="Click 'Start New Diagnosis' to begin the assessment",
            style="Question.TLabel",
            wraplength=800
        )
        self.question_label.pack()
        
        # Response buttons section
        response_section = ttk.LabelFrame(self.main_frame, text="Your Response", padding="15")
        response_section.pack(fill=tk.X, pady=(0, 20))
        
        # Yes/No buttons with improved styling
        button_frame = ttk.Frame(response_section)
        button_frame.pack()
        
        self.yes_btn = ttk.Button(
            button_frame,
            text="Yes",
            command=lambda: self.handle_response(True),
            state=tk.DISABLED,
            width=15
        )
        self.yes_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        self.no_btn = ttk.Button(
            button_frame,
            text="No",
            command=lambda: self.handle_response(False),
            state=tk.DISABLED,
            width=15
        )
        self.no_btn.pack(side=tk.LEFT)
        
        # Skip button for optional questions
        self.skip_btn = ttk.Button(
            button_frame,
            text="Skip",
            command=lambda: self.handle_response(None),
            state=tk.DISABLED,
            width=15
        )
        self.skip_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # Results display section
        results_section = ttk.LabelFrame(self.main_frame, text="Diagnostic Results", padding="10")
        results_section.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_section,
            height=20,
            width=90,
            font=("Consolas", 9),
            state=tk.DISABLED,
            wrap=tk.WORD,
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for better formatting
        self.results_text.tag_configure("header", font=("Consolas", 11, "bold"), foreground="#2c3e50")
        self.results_text.tag_configure("success", foreground="#27ae60")
        self.results_text.tag_configure("warning", foreground="#f39c12")
        self.results_text.tag_configure("danger", foreground="#e74c3c")
        self.results_text.tag_configure("info", foreground="#3498db")

    def create_footer(self):
        footer_frame = ttk.Frame(self.root, padding="20")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Left side buttons
        left_buttons = ttk.Frame(footer_frame)
        left_buttons.pack(side=tk.LEFT)
        
        self.start_btn = ttk.Button(
            left_buttons,
            text="Start New Diagnosis",
            command=self.start_diagnosis,
            width=20
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            left_buttons,
            text="Clear",
            command=self.clear_diagnosis,
            width=15
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right side buttons
        right_buttons = ttk.Frame(footer_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        self.export_btn = ttk.Button(
            right_buttons,
            text="Export Report",
            command=self.export_report,
            state=tk.DISABLED,
            width=18
        )
        self.export_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.save_btn = ttk.Button(
            right_buttons,
            text="Save Report",
            command=self.save_report,
            state=tk.DISABLED,
            width=15
        )
        self.save_btn.pack(side=tk.RIGHT)
        
        # Help button
        self.help_btn = ttk.Button(
            right_buttons,
            text="Help",
            command=self.show_help,
            width=10
        )
        self.help_btn.pack(side=tk.RIGHT, padx=(10, 0))

    def start_diagnosis(self):
        self.current_question = 0
        self.responses = {}
        self.progress_var.set(0)
        self.update_progress_label()
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.display_question()
        self.start_btn.config(state=tk.DISABLED)
        self.yes_btn.config(state=tk.NORMAL)
        self.no_btn.config(state=tk.NORMAL)
        self.skip_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.update_status("Diagnosis in progress...")

    def display_question(self):
        if self.current_question < len(self.symptoms):
            symptom = self.symptoms[self.current_question]
            question_text = f"Question {self.current_question + 1} of {len(self.symptoms)}:\n\n{symptom.question}"
            self.question_label.config(text=question_text)
            self.progress_var.set(self.current_question)
            self.update_progress_label()
        else:
            self.process_responses()

    def handle_response(self, response):
        if self.current_question < len(self.symptoms):
            symptom = self.symptoms[self.current_question]
            self.responses[symptom.name] = response
            self.current_question += 1
            
            if self.current_question < len(self.symptoms):
                self.display_question()
            else:
                self.process_responses()
    
    def update_progress_label(self):
        """Update the progress percentage label."""
        if len(self.symptoms) > 0:
            percentage = (self.current_question / len(self.symptoms)) * 100
            self.progress_label.config(text=f"{percentage:.0f}%")
    
    def update_status(self, message, color=None):
        """Update the status label with a message."""
        if color is None:
            color = self.colors['success']
        self.status_label.config(text=message, foreground=color)

    def process_responses(self):
        self.yes_btn.config(state=tk.DISABLED)
        self.no_btn.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)
        self.question_label.config(text="Analysis complete. See results below.")
        self.progress_var.set(len(self.symptoms))
        self.update_progress_label()
        self.update_status("Processing diagnosis...", self.colors['warning'])
        
        # Process in a separate thread to prevent GUI freezing
        def process_diagnosis():
            try:
                # Get diagnoses from expert system
                diagnoses = self.expert_system.diagnose(self.responses)
                
                # Generate and display report
                report = self.expert_system.generate_report(self.responses, diagnoses)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.display_results(report))
                self.root.after(0, lambda: self.update_status("Diagnosis complete", self.colors['success']))
                
            except Exception as e:
                error_msg = f"Error during diagnosis: {str(e)}"
                self.root.after(0, lambda: self.update_status(error_msg, self.colors['danger']))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        # Start processing in background thread
        threading.Thread(target=process_diagnosis, daemon=True).start()
        
        self.start_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL)

    def display_results(self, report):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Insert report with formatting
        lines = report.split('\n')
        for line in lines:
            if line.startswith('='):
                self.results_text.insert(tk.END, line + '\n', "header")
            elif line.startswith('RISK ASSESSMENT:'):
                self.results_text.insert(tk.END, line + '\n', "danger")
            elif line.startswith('URGENT:'):
                self.results_text.insert(tk.END, line + '\n', "danger")
            elif line.startswith('✓'):
                self.results_text.insert(tk.END, line + '\n', "success")
            elif line.startswith('✗'):
                self.results_text.insert(tk.END, line + '\n', "warning")
            elif line.startswith('•'):
                self.results_text.insert(tk.END, line + '\n', "info")
            else:
                self.results_text.insert(tk.END, line + '\n')
        
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(tk.END)

    def clear_diagnosis(self):
        self.current_question = 0
        self.responses = {}
        self.progress_var.set(0)
        self.update_progress_label()
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.question_label.config(text="Click 'Start New Diagnosis' to begin the assessment")
        self.start_btn.config(state=tk.NORMAL)
        self.yes_btn.config(state=tk.DISABLED)
        self.no_btn.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.update_status("Ready to begin diagnosis")

    def save_report(self):
        try:
            report = self.results_text.get(1.0, tk.END)
            filename = self.expert_system.save_report(report)
            messagebox.showinfo("Success", f"Report saved as {filename}")
            self.update_status(f"Report saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
            self.update_status(f"Save failed: {str(e)}", self.colors['danger'])
    
    def export_report(self):
        """Export report in different formats."""
        try:
            from tkinter import filedialog
            report = self.results_text.get(1.0, tk.END)
            
            # Ask user for file location and format
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                title="Export Report"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report exported to {filename}")
                self.update_status(f"Report exported: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
            self.update_status(f"Export failed: {str(e)}", self.colors['danger'])
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
Child Malnutrition Expert System v2.0
=====================================

HOW TO USE:
1. Click 'Start New Diagnosis' to begin
2. Answer each question with Yes, No, or Skip
3. Complete all questions for best results
4. View the diagnostic report
5. Save or export the report if needed

FEATURES:
• Advanced AI-powered diagnosis
• Risk assessment and recommendations
• Detailed treatment suggestions
• Export reports in multiple formats
• Modern, user-friendly interface

IMPORTANT:
This system provides guidance only and is not a substitute for professional medical diagnosis. Always consult with a qualified healthcare professional.

For support or questions, please contact your healthcare provider.
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Child Malnutrition Expert System")
        help_window.geometry("500x400")
        help_window.configure(bg='#f0f0f0')
        
        # Center the help window
        help_window.transient(self.root)
        help_window.grab_set()
        
        text_widget = scrolledtext.ScrolledText(
            help_window,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg='#f8f9fa',
            fg='#2c3e50',
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            style="Info.TButton"
        )
        close_btn.pack(pady=(0, 20))

if __name__ == "__main__":
    root = tk.Tk()
    app = MalnutritionExpertGUI(root)
    root.mainloop() 