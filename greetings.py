from experta import *

class Greetings(KnowledgeEngine):

    def __init__(self, symptom_map, if_not_matched, get_treatments, get_details):
        self.symptom_map = symptom_map
        self.if_not_matched = if_not_matched
        self.get_details = get_details
        self.get_treatments = get_treatments
        KnowledgeEngine.__init__(self)

    #code giving instructions on how to use the Expert System
    @DefFacts()
    def _initial_action(self):
        print("")
        print("This is a rule based expert system to diagnose child malnutrition diseases")
        print("")
        print("Does the child have any of the following symptoms?")
        print("Reply with a yes or a no")
        print("")
        yield Fact(action="find_disease")

    #taking various input from the patient
    @Rule(Fact(action="find_disease"), NOT(Fact(tiredness=W())), salience=4)
    def symptom_0(self):
        self.declare(Fact(tiredness=input("\nDoes the child show characteristics of tiredness?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(enlarged_tummy=W())), salience=1)
    def symptom_1(self):
        self.declare(Fact(enlarged_tummy=input("\nDoes the child have an enlarged tummy?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(brittle_hair=W())), salience=1)
    def symptom_2(self):
        self.declare(Fact(brittle_hair=input("\nDoes the child inhibit brittle hair?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(diarrhoea=W())), salience=3)
    def symptom_3(self):
        self.declare(Fact(diarrhoea=input("\nDoes the child have symptoms of diarrhoea?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(dry_skin=W())), salience=1)
    def symptom_4(self):
        self.declare(Fact(dry_skin=input("\nDoes the child have dry skin?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(cold_hands_feet=W())), salience=1)
    def symptom_5(self):
        self.declare(Fact(cold_hands_feet=input("\nDoes the child have cold hands and feet?: ")))

    @Rule(Fact(action="find_disease"), NOT(Fact(swollen_tongue=W())), salience=1)
    def symptom_6(self):
        self.declare(Fact(swollen_tongue=input("\nDoes the child have a swollen tongue?: ")))


    #different rules checking for each disease match
    @Rule(
        Fact(action="find_disease"),
        Fact(tiredness="yes"),
        Fact(enlarged_tummy="no"),
        Fact(brittle_hair="no"),
        Fact(diarrhoea="yes"),
        Fact(dry_skin="yes"),
        Fact(cold_hands_feet="yes"),
        Fact(swollen_tongue="no")
    )
    def disease_anaemia(self):
        self.declare(Fact(disease="Anaemia"))

    @Rule(
        Fact(action="find_disease"),
        Fact(tiredness="yes"),
        Fact(enlarged_tummy="yes"),
        Fact(brittle_hair="yes"),
        Fact(diarrhoea="yes"),
        Fact(dry_skin="yes"),
        Fact(cold_hands_feet="no"),
        Fact(swollen_tongue="no")
    )
    def disease_kwashiakor(self):
        self.declare(Fact(disease="Kwashiakor"))

    @Rule(
        Fact(action="find_disease"),
        Fact(tiredness="yes"),
        Fact(enlarged_tummy="no"),
        Fact(brittle_hair="no"),
        Fact(diarrhoea="yes"),
        Fact(dry_skin="yes"),
        Fact(cold_hands_feet="yes"),
        Fact(swollen_tongue="no")
    )
    def disease_marasmus(self):
        self.declare(Fact(disease="Marasmus"))


    #when the user's input  matches any disease in the knowledge base
    @Rule(Fact(action="find_disease"), Fact(disease=MATCH.disease), salience=-998)
    def disease(self, disease):
        print("")
        id_disease = disease
        disease_details = self.get_details(id_disease)
        treatments = self.get_treatments(id_disease)
        print("")
        print("Your symptoms match %s\n" % id_disease)
        print("A short description of the disease is given below :\n")
        print(disease_details + "\n")
        print(
            "The common medications and procedures suggested by other real doctors are: \n"
        )
        print(treatments + "\n")

    @Rule(
        Fact(action="find_disease"),
        Fact(tiredness=MATCH.tiredness),
        Fact(enlarged_tummy=MATCH.enlarged_tummy),
        Fact(brittle_hair=MATCH.brittle_hair),
        Fact(diarrhoea=MATCH.diarrhoea),
        Fact(dry_skin=MATCH.dry_skin),
        Fact(cold_hands_feet=MATCH.cold_hands_feet),
        Fact(swollen_tongue=MATCH.swollen_tongue),
        NOT(Fact(disease=MATCH.disease)),
        salience=-999
    )
    def not_matched(
        self,
        tiredness,
        enlarged_tummy,
        brittle_hair,
        diarrhoea,
        dry_skin,
        cold_hands_feet,
        swollen_tongue
    ):
        print("\nThe expert system did not find a disease that matches the child's exact symptoms.")
        lis = [
            tiredness,
            enlarged_tummy,
            brittle_hair,
            diarrhoea,
            dry_skin,
            cold_hands_feet,
            swollen_tongue
        ]
        max_count = 0
        max_disease = ""
        for key, val in self.symptom_map.items():
            count = 0
            temp_list = eval(key)
            for j in range(0, len(lis)):
                if temp_list[j] == lis[j] and (lis[j] == "yes" or lis[j] == "no"):
                    count = count + 1
            if count > max_count:
                max_count = count
                max_disease = val
        if max_disease != "":
            self.if_not_matched(max_disease)