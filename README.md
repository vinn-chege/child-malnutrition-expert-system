# 🏥 Child Malnutrition Expert System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Experta Version](https://img.shields.io/badge/experta-1.9.4-brightgreen)](https://pypi.org/project/experta/)
[![IDE](https://img.shields.io/badge/IDE-Pycharm%20%7C%20VSCode-orange)](https://www.jetbrains.com/pycharm/)

An intelligent expert system designed to help healthcare professionals and caregivers identify malnutrition conditions in children. Built with Python and Experta, it provides accurate diagnoses and treatment recommendations through a modern GUI interface.

## ✨ Features

- 🖥️ Modern GUI interface for easy interaction
- 🎯 Confidence-based diagnosis system
- 🔍 Detailed symptom analysis
- 💊 Comprehensive treatment recommendations
- 📝 Report generation and saving
- 📊 Progress tracking during diagnosis
- 🔄 Support for multiple conditions

## 🚀 Installation

1. Ensure you have Python 3.8 or later installed
2. Clone this repository:
   ```bash
   git clone https://github.com/vinn-chege/child-malnutrition-expert-system.git
   cd child-malnutrition-expert-system
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Launch the application:
   ```bash
   python gui.py
   ```
2. Click "Start New Diagnosis" to begin
3. Answer symptom-related questions
4. Review diagnosis and treatment recommendations
5. Save the report if needed

## 📚 Knowledge Base

The system uses a JSON-based knowledge base (`knowledge_base.json`) containing:
- Disease definitions and descriptions
- Symptom lists with weighted importance
- Treatment recommendations
- Severity levels
- Required symptoms for each condition

## 🤝 Contributing

Contributions are welcome! You can help by:
- Adding new diseases to the knowledge base
- Improving the symptom matching algorithm
- Enhancing the GUI
- Adding new features

## ⚠️ Disclaimer

This system is for educational purposes only and should not replace professional medical advice. Always consult healthcare professionals for proper diagnosis and treatment.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.