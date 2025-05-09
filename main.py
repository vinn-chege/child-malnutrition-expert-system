from greetings import Greetings
diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

#load the knowledge from .txt files into variables to allow the code to use it
def preprocess():
    #global diseases_list, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map
    diseases = open("diseases.txt")
    diseases_t = diseases.read()
    diseases_lst = diseases_t.split("\n")
    diseases.close()

    for disease in diseases_lst:
        disease_s_file = open("Disease symptoms/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease
        disease_s_file.close()

        disease_s_file = open("Diseases descriptions/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()

        disease_s_file = open("Disease treatments/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_treatment_map[disease] = disease_s_data
        disease_s_file.close()


def identify_disease(*arguments):
    symptom_list = []
    for symptom in arguments:
        symptom_list.append(symptom)

    return symptom_map[str(symptom_list)]


def get_details(disease):
    details = {
        "Anaemia": "A condition where the body lacks enough healthy red blood cells to carry adequate oxygen to the body's tissues.",
        "Kwashiakor": "A form of severe protein malnutrition characterized by edema and an enlarged liver with fatty infiltrates.",
        "Marasmus": "A form of severe malnutrition characterized by energy deficiency and wasting of body tissues."
    }
    return details.get(disease, "No details available")


def get_treatments(disease):
    treatments = {
        "Anaemia": "Iron supplements, Vitamin B12 supplements, Dietary changes to include iron-rich foods",
        "Kwashiakor": "Gradual protein and calorie increase, Vitamin and mineral supplements, Treatment of infections",
        "Marasmus": "Gradual refeeding, Nutritional rehabilitation, Treatment of underlying infections"
    }
    return treatments.get(disease, "No treatment information available")


def if_not_matched(disease):
    print(f"\nThe closest matching disease is: {disease}")
    print("Please consult a healthcare professional for proper diagnosis.")

#driver function
if __name__ == "__main__":
    preprocess()
    #creating class object
    engine = Greetings(symptom_map, if_not_matched, get_treatments, get_details)
    #loop to keep running the code until user says no when asked for another diagnosis
    while 1:
        engine.reset()
        engine.run()
        print("Would you like to diagnose some other symptoms?\n Reply yes or no")
        if input() == "no":
            exit()
