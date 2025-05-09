# Child Malnutrition Expert System

A rule-based expert system for diagnosing child malnutrition conditions. The system uses a knowledge base of symptoms, diseases, and treatments to provide accurate diagnoses and treatment recommendations.

## Features

- Modern GUI interface for easy interaction
- Confidence-based diagnosis system
- Detailed symptom analysis
- Comprehensive treatment recommendations
- Report generation and saving
- Progress tracking during diagnosis
- Support for multiple conditions

## Installation

1. Ensure you have Python 3.8 or later installed
2. Clone this repository
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the GUI application:
   ```bash
   python gui.py
   ```

2. Click "Start New Diagnosis" to begin
3. Answer each question about the child's symptoms
4. Review the diagnosis and treatment recommendations
5. Save the report if needed

## Knowledge Base

The system uses a JSON-based knowledge base (`knowledge_base.json`) that contains:
- Disease definitions
- Symptom lists with weights
- Treatment recommendations
- Severity levels
- Required symptoms for each condition

## Contributing

Feel free to contribute to this project by:
1. Adding new diseases to the knowledge base
2. Improving the symptom matching algorithm
3. Enhancing the GUI
4. Adding new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This system is for educational purposes only and should not be used as a substitute for professional medical advice. Always consult with healthcare professionals for proper diagnosis and treatment.

# Child Malnutrition Expert System in Python

[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/)
[![Experta Version](https://img.shields.io/badge/experta-1.9.4-brightgreen)](https://pypi.org/project/experta/)
[![IDE](https://img.shields.io/badge/IDE-Pycharm%20%7C%20VSCode-orange)](https://www.jetbrains.com/pycharm/)

An intelligent child malnutrition diagnosis expert system designed to help healthcare professionals and caregivers identify malnutrition diseases in children. This project is implemented using Python and the Experta shell library, providing an easy-to-use and efficient solution for diagnosing child malnutrition.

## Table of Contents
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description
Child malnutrition is a critical health concern, especially in developing countries. Timely and accurate diagnosis is essential to ensure children receive appropriate treatment and care. This expert system employs an inference engine to evaluate various symptoms and medical data to provide an accurate assessment of the child's nutritional status. The system is designed to be user-friendly, making it accessible to healthcare professionals, nutritionists, and even caregivers.

## Prerequisites
To get started with the Child Malnutrition Expert System, ensure you have the following prerequisites installed:

- **Python 3.7 or 3.8:** If you don't have Python installed, download it from the official website: [Python Downloads](https://www.python.org/downloads/)

- **Experta Python Library:** This project relies on the Experta library for building the expert system. You can install it using pip:

  ```
  pip install experta
  ```

- **PyCharm/VSCode IDE:** Choose your preferred integrated development environment (IDE) to work with the code. If you don't have one installed, you can download PyCharm from [here](https://www.jetbrains.com/pycharm/) and VSCode from [here](https://code.visualstudio.com/).

## Installation
1. Clone this repository to your local machine using:

   ```
   git clone https://github.com/vinn-chege/child-malnutrition-expert-system.git
   ```

2. Navigate to the project directory:

   ```
   cd child-malnutrition-expert-system 
   ```

## Usage
1. Open your preferred IDE (PyCharm or VSCode) and open the project folder.

2. Make sure you have satisfied the prerequisites mentioned above.

3. Run the `main.py` script:

   ```
   python main.py
   ```

   The expert system will start, and you can follow the prompts to input the child's symptoms and medical data. The system will then analyze the information and provide a diagnosis for the child's nutritional status.

## Contributing
Contributions to this project are welcome!

