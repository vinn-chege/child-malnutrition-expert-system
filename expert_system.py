import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Symptom:
    name: str
    question: str
    weight: float

@dataclass
class Disease:
    name: str
    symptoms: List[Symptom]
    description: str
    treatments: List[str]
    severity: str
    required_symptoms: List[str]
    confidence_threshold: float

class MalnutritionExpertSystem:
    def __init__(self, knowledge_base_path: str):
        self.load_knowledge_base(knowledge_base_path)
        
    def load_knowledge_base(self, path: str):
        """Load and parse the knowledge base from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
            
        self.diseases = {}
        for disease_name, disease_data in data['diseases'].items():
            symptoms = [
                Symptom(**symptom_data)
                for symptom_data in disease_data['symptoms']
            ]
            self.diseases[disease_name] = Disease(
                name=disease_name,
                symptoms=symptoms,
                description=disease_data['description'],
                treatments=disease_data['treatments'],
                severity=disease_data['severity'],
                required_symptoms=disease_data['required_symptoms'],
                confidence_threshold=disease_data['confidence_threshold']
            )
            
        self.settings = data['system_settings']
    
    def calculate_confidence(self, disease: Disease, responses: Dict[str, bool]) -> float:
        """Calculate confidence score for a disease given the responses."""
        total_weight = sum(s.weight for s in disease.symptoms)
        matched_weight = 0
        
        # Check required symptoms first
        for req_symptom in disease.required_symptoms:
            symptom_response = responses.get(req_symptom, False)
            if not symptom_response:
                return 0.0  # Missing required symptom
        
        # Calculate weighted score
        for symptom in disease.symptoms:
            if responses.get(symptom.name, False):
                weight = symptom.weight
                # Increase weight for required symptoms
                if symptom.name in disease.required_symptoms:
                    weight *= self.settings['required_symptoms_weight']
                matched_weight += weight
        
        confidence = matched_weight / total_weight
        return min(confidence, 1.0)  # Cap at 1.0
    
    def diagnose(self, responses: Dict[str, bool]) -> List[Dict]:
        """
        Diagnose conditions based on responses.
        Returns list of potential diagnoses with confidence scores.
        """
        diagnoses = []
        
        for disease in self.diseases.values():
            confidence = self.calculate_confidence(disease, responses)
            
            if confidence >= self.settings['min_confidence_threshold']:
                diagnoses.append({
                    'disease': disease,
                    'confidence': confidence,
                    'severity': disease.severity
                })
        
        # Sort by confidence score
        diagnoses.sort(key=lambda x: x['confidence'], reverse=True)
        return diagnoses
    
    def get_all_symptoms(self) -> List[Symptom]:
        """Get a deduplicated list of all symptoms."""
        symptoms = {}
        for disease in self.diseases.values():
            for symptom in disease.symptoms:
                if symptom.name not in symptoms:
                    symptoms[symptom.name] = symptom
        return list(symptoms.values())
    
    def generate_report(self, responses: Dict[str, bool], diagnoses: List[Dict]) -> str:
        """Generate a detailed diagnostic report."""
        report = []
        report.append("Child Malnutrition Expert System - Diagnostic Report")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        report.append("Symptoms Reported:")
        for symptom_name, is_present in responses.items():
            report.append(f"- {symptom_name}: {'Yes' if is_present else 'No'}")
        report.append("")
        
        if diagnoses:
            report.append("Potential Diagnoses:")
            for diagnosis in diagnoses:
                disease = diagnosis['disease']
                confidence = diagnosis['confidence']
                report.append(f"\n{disease.name} (Confidence: {confidence:.1%}, Severity: {disease.severity})")
                report.append(f"Description: {disease.description}")
                report.append("\nRecommended Treatments:")
                for treatment in disease.treatments:
                    report.append(f"- {treatment}")
        else:
            report.append("No matching conditions found with sufficient confidence.")
        
        report.append("\nIMPORTANT: This system provides guidance only.")
        report.append("Please consult a healthcare professional for proper diagnosis and treatment.")
        
        return "\n".join(report)
    
    def save_report(self, report: str, filename: str = None):
        """Save the diagnostic report to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"diagnosis_report_{timestamp}.txt"
            
        with open(filename, 'w') as f:
            f.write(report)
        
        return filename

# Example usage:
if __name__ == "__main__":
    # Initialize the expert system
    expert_system = MalnutritionExpertSystem("knowledge_base.json")
    
    # Get all possible symptoms
    symptoms = expert_system.get_all_symptoms()
    
    # Collect responses (in a real application, this would be from the GUI)
    responses = {}
    print("Please answer the following questions with 'yes' or 'no':\n")
    for symptom in symptoms:
        response = input(f"{symptom.question} ").lower()
        responses[symptom.name] = response == 'yes'
    
    # Get diagnoses
    diagnoses = expert_system.diagnose(responses)
    
    # Generate and save report
    report = expert_system.generate_report(responses, diagnoses)
    filename = expert_system.save_report(report)
    
    print(f"\nDiagnostic report has been saved to: {filename}") 