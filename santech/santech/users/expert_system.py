from experta import *

class PatientData(Fact):
    """Faits médicaux : température, fréquence cardiaque et saturation en oxygène"""
    pass

class MedicalExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostics = []
        self.recommendations = []
    # ---------- Température ----------
    @Rule(PatientData(temp=P(lambda t: 0 <= t < 35.0)))
    def hypothermie_severe(self):
        self.diagnostics.append(("Hypothermie sévère", "danger", "thermometer-empty"))
        self.recommendations.append("L'urgent est de réchauffer le patient immédiatement.")

    @Rule(PatientData(temp=P(lambda t: 35.0 <= t < 36.1)))
    def hypothermie_legere(self):
        self.diagnostics.append(("Hypothermie légère", "warning", "thermometer-quarter"))
        self.recommendations.append("Réchauffer progressivement le patient.")
    
    @Rule(PatientData(temp=P(lambda t: 36.1 <= t <= 37.5)))
    def temperature_normale(self):
        self.diagnostics.append(("Température normale", "success", "thermometer-half"))
        self.recommendations.append("Température normale, pas d'action nécessaire.")
    
    @Rule(PatientData(temp=P(lambda t: 37.6 <= t <= 38.0)))
    def fièvre_legère(self):
        self.diagnostics.append(("Fièvre légère", "warning", "thermometer-half"))
        self.recommendations.append("Se reposer et boire beaucoup d'eau.")
    
    @Rule(PatientData(temp=P(lambda t: 38.1 <= t <= 39.0)))
    def fièvre_moderee(self):
        self.diagnostics.append(("Fièvre modérée", "warning", "thermometer-three-quarters"))
        self.recommendations.append("Prendre un antipyrétique et consulter un médecin si la fièvre persiste.")

    # ---------- Fréquence cardiaque ----------
    @Rule(PatientData(fc=P(lambda f: 60<= f <=100)))
    def frequence_cardiaque_normale(self):
        self.diagnostics.append(("Fréquence cardiaque normale", "success", "heartbeat"))
        self.recommendations.append("Fréquence cardiaque normale.")
    
    @Rule(PatientData(fc=P(lambda f: f < 60)))
    def bradycardie(self):
        self.diagnostics.append(("Bradycardie", "warning", "heartbeat"))
        self.recommendations.append("Fréquence cardiaque basse. Consultez un médecin si des symptômes apparaissent.")

    @Rule(PatientData(fc=P(lambda f: f > 100)))
    def tachycardie(self):
        self.diagnostics.append(("Tachycardie", "danger", "heartbeat"))
        self.recommendations.append("Fréquence cardiaque élevée. Consulter immédiatement un médecin.")

    # ---------- Saturation en oxygène ----------
    @Rule(PatientData(oxygene=P(lambda o: 95 <= o <= 99)))
    def oxygene_normal(self):
        self.diagnostics.append(("Saturation en oxygène normale", "success", "lungs"))
        self.recommendations.append("Saturation en oxygène optimale.")
    
    @Rule(PatientData(oxygene=P(lambda o: 90 <= o < 95)))
    def oxygene_legere_baisse(self):
        self.diagnostics.append(("Saturation légèrement basse", "warning", "lungs"))
        self.recommendations.append("Reposer et surveiller. Consultez un médecin si cela persiste.")
    
    @Rule(PatientData(oxygene=P(lambda o: 0 <= o < 90)))
    def oxygene_basse(self):
        self.diagnostics.append(("Saturation en oxygène faible ⚠️", "danger", "lungs"))
        self.recommendations.append("Urgent : augmentations immédiates d'oxygène ou consultez un médecin.")
    
    # ---------- Fonction d'analyse ----------
    def analyser_symptomes(self, temp, fc, oxygene):
        self.reset()
        self.declare(PatientData(temp=temp, fc=fc, oxygene=oxygene))
        self.run()
        return self.diagnostics, self.recommendations
