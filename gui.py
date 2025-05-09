import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from expert_system import MalnutritionExpertSystem
from datetime import datetime
import json

class MalnutritionExpertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Malnutrition Expert System")
        self.root.geometry("900x700")
        
        # Initialize the expert system
        try:
            self.expert_system = MalnutritionExpertSystem("knowledge_base.json")
            self.symptoms = self.expert_system.get_all_symptoms()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize expert system: {str(e)}")
            self.root.destroy()
            return
        
        # Create main containers
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Initialize variables
        self.current_question = 0
        self.responses = {}
        
        # Apply a theme
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 11))
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
        self.style.configure("Question.TLabel", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 10))

    def create_header(self):
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            header_frame, 
            text="Child Malnutrition Diagnosis System",
            style="Header.TLabel"
        )
        title.pack()
        
        description = ttk.Label(
            header_frame,
            text="This expert system helps identify potential malnutrition conditions in children.\n"
                 "Please answer all questions accurately for the best possible diagnosis.",
            wraplength=700
        )
        description.pack(pady=10)

    def create_main_content(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=len(self.symptoms)
        )
        self.progress.pack(fill=tk.X, pady=(0, 20))
        
        # Question display
        self.question_frame = ttk.Frame(self.main_frame)
        self.question_frame.pack(fill=tk.X, pady=10)
        
        self.question_label = ttk.Label(
            self.question_frame,
            text="Click 'Start Diagnosis' to begin",
            wraplength=700,
            style="Question.TLabel"
        )
        self.question_label.pack()
        
        # Response buttons frame
        self.response_frame = ttk.Frame(self.main_frame)
        self.response_frame.pack(pady=20)
        
        # Yes/No buttons with improved styling
        self.yes_btn = ttk.Button(
            self.response_frame,
            text="Yes",
            command=lambda: self.handle_response(True),
            state=tk.DISABLED,
            width=20
        )
        self.yes_btn.pack(side=tk.LEFT, padx=10)
        
        self.no_btn = ttk.Button(
            self.response_frame,
            text="No",
            command=lambda: self.handle_response(False),
            state=tk.DISABLED,
            width=20
        )
        self.no_btn.pack(side=tk.LEFT)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=15,
            width=80,
            font=("Helvetica", 10),
            state=tk.DISABLED
        )
        self.results_text.pack(pady=20)

    def create_footer(self):
        footer_frame = ttk.Frame(self.root, padding="20")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.start_btn = ttk.Button(
            footer_frame,
            text="Start New Diagnosis",
            command=self.start_diagnosis,
            width=20
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            footer_frame,
            text="Clear",
            command=self.clear_diagnosis,
            width=15
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        self.save_btn = ttk.Button(
            footer_frame,
            text="Save Report",
            command=self.save_report,
            state=tk.DISABLED,
            width=15
        )
        self.save_btn.pack(side=tk.RIGHT)

    def start_diagnosis(self):
        self.current_question = 0
        self.responses = {}
        self.progress_var.set(0)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.display_question()
        self.start_btn.config(state=tk.DISABLED)
        self.yes_btn.config(state=tk.NORMAL)
        self.no_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)

    def display_question(self):
        if self.current_question < len(self.symptoms):
            symptom = self.symptoms[self.current_question]
            self.question_label.config(text=symptom.question)
            self.progress_var.set(self.current_question)
        else:
            self.process_responses()

    def handle_response(self, is_yes):
        symptom = self.symptoms[self.current_question]
        self.responses[symptom.name] = is_yes
        self.current_question += 1
        
        if self.current_question < len(self.symptoms):
            self.display_question()
        else:
            self.process_responses()

    def process_responses(self):
        self.yes_btn.config(state=tk.DISABLED)
        self.no_btn.config(state=tk.DISABLED)
        self.question_label.config(text="Analysis complete. See results below.")
        self.progress_var.set(len(self.symptoms))
        
        # Get diagnoses from expert system
        diagnoses = self.expert_system.diagnose(self.responses)
        
        # Generate and display report
        report = self.expert_system.generate_report(self.responses, diagnoses)
        self.display_results(report)
        
        self.start_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

    def display_results(self, report):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, report)
        self.results_text.config(state=tk.DISABLED)

    def clear_diagnosis(self):
        self.current_question = 0
        self.responses = {}
        self.progress_var.set(0)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.question_label.config(text="Click 'Start New Diagnosis' to begin")
        self.start_btn.config(state=tk.NORMAL)
        self.yes_btn.config(state=tk.DISABLED)
        self.no_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

    def save_report(self):
        try:
            report = self.results_text.get(1.0, tk.END)
            filename = self.expert_system.save_report(report)
            messagebox.showinfo("Success", f"Report saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MalnutritionExpertGUI(root)
    root.mainloop() 