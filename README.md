# 🏥 Child Malnutrition Expert System v2.0

[![Python Version](https://img.shields.io/badge/python-3.7+-blue)](https://www.python.org/downloads/)
[![Experta Version](https://img.shields.io/badge/experta-1.9.0-brightgreen)](https://pypi.org/project/experta/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A comprehensive AI-powered system for diagnosing malnutrition conditions in children. This advanced expert system provides both graphical and command-line interfaces with enhanced accuracy and user experience.

## 🚀 New Features in v2.0

- **🧠 Advanced AI-Powered Diagnosis**: Improved confidence scoring and risk assessment
- **🎨 Modern GUI**: Beautiful, user-friendly interface with progress tracking
- **📊 Comprehensive Knowledge Base**: Expanded to include 4 conditions with 24+ symptoms
- **⚠️ Risk Assessment**: Automatic risk level evaluation (High/Moderate/Low/Minimal)
- **📋 Enhanced Reporting**: Detailed diagnostic reports with treatment recommendations
- **🖥️ Multiple Interfaces**: Both GUI and command-line options
- **💾 Export Functionality**: Save and export reports in multiple formats
- **⚡ Real-time Processing**: Background processing to prevent GUI freezing

## 🏥 Supported Conditions

### 1. Iron Deficiency Anaemia
- **Severity**: Moderate
- **Key Symptoms**: Fatigue, pale skin, cold hands/feet, brittle nails
- **Treatment**: Iron supplementation, dietary changes, vitamin C

### 2. Kwashiorkor
- **Severity**: Severe
- **Key Symptoms**: Edema, enlarged abdomen, hair changes, skin lesions
- **Treatment**: Immediate medical attention, protein reintroduction

### 3. Marasmus
- **Severity**: Severe
- **Key Symptoms**: Severe weight loss, muscle wasting, visible bones
- **Treatment**: Hospitalization, careful refeeding program

### 4. Vitamin A Deficiency
- **Severity**: Moderate
- **Key Symptoms**: Night blindness, dry eyes, frequent infections
- **Treatment**: Vitamin A supplementation, dietary improvements

## 🎯 How to Use

### Graphical Interface (Recommended)
```bash
python main.py
# or
python main.py --gui
```

### Command-Line Interface
```bash
python main.py --cli
```

### Help
```bash
python main.py --help
```

## 📋 Requirements

- Python 3.7+
- experta==1.9.0
- frozendict==1.2
- schema==0.6.7

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd child-malnutrition-expert-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the system**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
child-malnutrition-expert-system/
├── main.py                 # Main entry point with CLI/GUI options
├── expert_system.py        # Core AI-powered expert system
├── gui.py                  # Modern graphical user interface
├── knowledge_base.json     # Comprehensive medical knowledge base
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # License information
└── legacy/                # Legacy files (for reference)
    ├── greetings.py       # Original rule-based engine
    ├── diseases.txt       # Original disease list
    ├── Disease symptoms/  # Original symptom files
    ├── Diseases descriptions/
    └── Disease treatments/
```

## 🧠 System Architecture

### Expert System Core (`expert_system.py`)
- **Confidence Scoring**: Advanced algorithm with weighted symptoms
- **Risk Assessment**: Multi-level risk evaluation
- **Treatment Recommendations**: Evidence-based treatment suggestions
- **Report Generation**: Comprehensive diagnostic reports

### Knowledge Base (`knowledge_base.json`)
- **Diseases**: 4 malnutrition conditions with detailed information
- **Symptoms**: 24+ medically accurate symptoms with weights
- **Treatments**: Evidence-based treatment recommendations
- **Settings**: Configurable system parameters

### User Interface (`gui.py`)
- **Modern Design**: Clean, professional interface
- **Progress Tracking**: Real-time progress indicators
- **Responsive Layout**: Adapts to different screen sizes
- **Error Handling**: Comprehensive error management

## 🔍 Key Improvements from v1.0

### Accuracy Enhancements
- ✅ Medically accurate symptom descriptions
- ✅ Weighted confidence scoring algorithm
- ✅ Required symptom validation
- ✅ Risk assessment based on symptom severity
- ✅ Expanded knowledge base with 4 conditions

### User Experience Improvements
- ✅ Modern, intuitive GUI design
- ✅ Progress tracking and status updates
- ✅ Real-time processing with threading
- ✅ Export functionality for reports
- ✅ Help system and documentation
- ✅ Error handling and validation

### Technical Improvements
- ✅ Modular, maintainable code structure
- ✅ Comprehensive error handling
- ✅ Background processing for better performance
- ✅ Configurable system settings
- ✅ Multiple interface options

## 📊 Usage Examples

### GUI Mode
1. Launch the application: `python main.py`
2. Click "🚀 Start New Diagnosis"
3. Answer questions about the child's symptoms
4. View the comprehensive diagnostic report
5. Save or export the report as needed

### CLI Mode
1. Run in command-line: `python main.py --cli`
2. Answer questions interactively
3. View the diagnostic report in terminal
4. Optionally save the report to file

## 🎨 GUI Features

- **Modern Interface**: Clean, professional design with intuitive navigation
- **Progress Tracking**: Real-time progress bar and percentage display
- **Status Updates**: Live status messages and error handling
- **Export Options**: Save reports in multiple formats
- **Help System**: Built-in help and documentation
- **Responsive Design**: Adapts to different screen sizes

## ⚠️ Important Disclaimer

**This system is for educational and informational purposes only.**

- ❌ **NOT a substitute for professional medical diagnosis**
- ❌ **NOT intended for emergency medical situations**
- ❌ **NOT a replacement for qualified healthcare professionals**

**Always consult with a qualified healthcare professional for:**
- ✅ Proper medical diagnosis
- ✅ Treatment recommendations
- ✅ Emergency medical situations
- ✅ Any concerns about a child's health

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Support

For questions or support, please:
1. Check the help system within the application
2. Review the documentation
3. Consult with healthcare professionals for medical advice

---

**Version**: 2.0  
**Last Updated**: 2024  
**Compatibility**: Python 3.7+