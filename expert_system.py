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
        required_symptoms_matched = 0
        
        # Check required symptoms first
        for req_symptom in disease.required_symptoms:
            symptom_response = responses.get(req_symptom, False)
            if symptom_response:
                required_symptoms_matched += 1
        
        # If not all required symptoms are present, return very low confidence
        if required_symptoms_matched < len(disease.required_symptoms):
            return 0.0
        
        # Calculate weighted score
        for symptom in disease.symptoms:
            if responses.get(symptom.name, False):
                weight = symptom.weight
                # Increase weight for required symptoms
                if symptom.name in disease.required_symptoms:
                    weight *= self.settings['required_symptoms_weight']
                matched_weight += weight
        
        # Calculate base confidence
        base_confidence = matched_weight / total_weight
        
        # Apply penalty for missing high-weight symptoms
        missing_penalty = 0
        for symptom in disease.symptoms:
            if not responses.get(symptom.name, False) and symptom.weight >= 0.8:
                missing_penalty += symptom.weight * 0.1
        
        # Apply bonus for having multiple symptoms
        symptom_count = sum(1 for response in responses.values() if response)
        symptom_bonus = min(symptom_count * 0.02, 0.1)  # Max 10% bonus
        
        confidence = base_confidence - missing_penalty + symptom_bonus
        return max(0.0, min(confidence, 1.0))  # Ensure between 0 and 1
    
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
        report.append("=" * 60)
        report.append("CHILD MALNUTRITION EXPERT SYSTEM - DIAGNOSTIC REPORT")
        report.append("=" * 60)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Risk Assessment
        risk_level = self.assess_risk_level(responses)
        risk_colors = {
            "high": "🔴 HIGH RISK",
            "moderate": "🟡 MODERATE RISK", 
            "low": "🟢 LOW RISK",
            "minimal": "⚪ MINIMAL RISK"
        }
        report.append(f"RISK ASSESSMENT: {risk_colors.get(risk_level, 'UNKNOWN')}")
        report.append("")
        
        # Symptoms Summary
        report.append("SYMPTOMS REPORTED:")
        report.append("-" * 30)
        positive_symptoms = [name for name, present in responses.items() if present]
        negative_symptoms = [name for name, present in responses.items() if not present]
        
        if positive_symptoms:
            report.append("Present Symptoms:")
            for symptom in positive_symptoms:
                report.append(f"✓ {symptom.replace('_', ' ').title()}")
        
        if negative_symptoms:
            report.append("\nAbsent Symptoms:")
            for symptom in negative_symptoms:
                report.append(f"✗ {symptom.replace('_', ' ').title()}")
        
        report.append(f"\nTotal Symptoms Checked: {len(responses)}")
        report.append(f"Positive Responses: {len(positive_symptoms)}")
        report.append("")
        
        # Diagnoses
        if diagnoses:
            report.append("POTENTIAL DIAGNOSES:")
            report.append("-" * 30)
            for i, diagnosis in enumerate(diagnoses, 1):
                disease = diagnosis['disease']
                confidence = diagnosis['confidence']
                severity_icons = {"severe": "🔴", "moderate": "🟡", "mild": "🟢"}
                severity_icon = severity_icons.get(disease.severity, "⚪")
                
                report.append(f"\n{i}. {disease.name} {severity_icon}")
                report.append(f"   Confidence: {confidence:.1%}")
                report.append(f"   Severity: {disease.severity.upper()}")
                report.append(f"   Description: {disease.description}")
                
                if self.settings.get('enable_treatment_recommendations', True):
                    report.append("\n   Recommended Treatments:")
                    for treatment in disease.treatments:
                        report.append(f"   • {treatment}")
        else:
            report.append("NO MATCHING CONDITIONS FOUND")
            report.append("-" * 30)
            report.append("No conditions were identified with sufficient confidence.")
            report.append("This could indicate:")
            report.append("• The child may not have malnutrition-related conditions")
            report.append("• Additional symptoms may need to be assessed")
            report.append("• A healthcare professional should be consulted")
        
        # Immediate Recommendations
        immediate_recs = self.get_immediate_recommendations(diagnoses, risk_level)
        if immediate_recs:
            report.append(f"\nIMMEDIATE RECOMMENDATIONS:")
            report.append("-" * 30)
            for rec in immediate_recs:
                report.append(f"• {rec}")
        
        # Follow-up Actions
        follow_up_actions = self.get_follow_up_actions(diagnoses)
        if follow_up_actions:
            report.append(f"\nFOLLOW-UP ACTIONS:")
            report.append("-" * 30)
            for action in follow_up_actions:
                report.append(f"• {action}")
        
        # Disclaimer
        report.append("\n" + "=" * 60)
        report.append("IMPORTANT DISCLAIMER")
        report.append("=" * 60)
        report.append("This expert system provides preliminary guidance only.")
        report.append("It is NOT a substitute for professional medical diagnosis.")
        report.append("Always consult with a qualified healthcare professional")
        report.append("for proper diagnosis, treatment, and medical advice.")
        
        if risk_level == "high":
            report.append("\n🚨 URGENT: Seek immediate medical attention!")
        
        return "\n".join(report)
    
    def save_report(self, report: str, filename: str = None):
        """Save the diagnostic report to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"diagnosis_report_{timestamp}.txt"
            
        with open(filename, 'w') as f:
            f.write(report)
        
        return filename
    
    def assess_risk_level(self, responses: Dict[str, bool]) -> str:
        """Assess the overall risk level based on responses."""
        if not self.settings.get('enable_risk_assessment', True):
            return "unknown"
        
        # Count severe symptoms
        severe_symptoms = 0
        for disease in self.diseases.values():
            if disease.severity == "severe":
                for symptom in disease.symptoms:
                    if responses.get(symptom.name, False) and symptom.weight >= 0.8:
                        severe_symptoms += 1
        
        # Count total positive responses
        total_positive = sum(1 for response in responses.values() if response)
        
        if severe_symptoms >= 3 or total_positive >= 8:
            return "high"
        elif severe_symptoms >= 1 or total_positive >= 5:
            return "moderate"
        elif total_positive >= 2:
            return "low"
        else:
            return "minimal"
    
    def get_immediate_recommendations(self, diagnoses: List[Dict], risk_level: str) -> List[str]:
        """Get immediate recommendations based on diagnoses and risk level."""
        recommendations = []
        
        if risk_level == "high":
            recommendations.append("URGENT: Seek immediate medical attention")
            recommendations.append("Consider emergency care if child shows signs of severe distress")
        
        if diagnoses:
            for diagnosis in diagnoses:
                disease = diagnosis['disease']
                if disease.severity == "severe":
                    recommendations.append(f"Immediate medical evaluation recommended for {disease.name}")
        
        # General recommendations
        if risk_level in ["moderate", "high"]:
            recommendations.append("Monitor child's vital signs closely")
            recommendations.append("Ensure adequate hydration")
            recommendations.append("Avoid any dietary restrictions without medical supervision")
        
        return recommendations
    
    def get_follow_up_actions(self, diagnoses: List[Dict]) -> List[str]:
        """Get follow-up actions based on diagnoses."""
        actions = []
        
        for diagnosis in diagnoses:
            disease = diagnosis['disease']
            confidence = diagnosis['confidence']
            
            if confidence >= 0.8:
                actions.append(f"Schedule follow-up appointment within 1-2 weeks for {disease.name}")
            elif confidence >= 0.6:
                actions.append(f"Schedule follow-up appointment within 2-4 weeks for {disease.name}")
            
            if disease.severity == "severe":
                actions.append("Arrange for nutritional assessment by a dietitian")
                actions.append("Consider referral to a pediatric nutrition specialist")
        
        return actions

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