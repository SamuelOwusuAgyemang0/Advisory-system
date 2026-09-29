import joblib, json, pandas as pd
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"

# Programme map keyed by (shs_program, interest)
# Degree programmes for students with strong grades
PROGRAMME_MAP = {
    # General Science
    ("General Science", "Engineering & Technology"):      "BSc Construction Studies",
    ("General Science", "Healthcare & Medicine"):         "BSc Health Administration",
    ("General Science", "Research & Science"):            "BSc Population and Family Health",
    ("General Science", "Environmental Studies"):         "BSc Geo-spatial Science",
    ("General Science", "Mathematics & Computing"):       "BSc Computer Science",
    ("General Science", "Education & Teaching"):          "B.Ed Social Studies",
    ("General Science", "Finance & Economics"):           "BCom Banking and Finance",
    ("General Science", "Management"):                    "BSc Planning",
    ("General Science", "Real Estate & Construction"):    "BSc Real Estate",
    ("General Science", "Public Health"):                 "BSc Population and Family Health",
    ("General Science", "Agriculture & Food Science"):    "BSc Population and Family Health",
    ("General Science", "Energy & Natural Resources"):    "BSc Geo-spatial Science",
    ("General Science", "Data Science & Analytics"):      "BSc Computer Science",
    ("General Science", "Architecture & Planning"):       "BSc Planning",

    # General Arts
    ("General Arts", "Law & Legal Studies"):              "BA African Discourse Studies",
    ("General Arts", "Education & Teaching"):             "B.Ed Social Studies",
    ("General Arts", "Politics & Governance"):            "BA Integrated Development Studies",
    ("General Arts", "Communication & Media"):            "BA Development Communication",
    ("General Arts", "Social Sciences"):                  "BA History and Diaspora Studies",
    ("General Arts", "History & Culture"):                "BA History and Diaspora Studies",
    ("General Arts", "Development Studies"):              "BA Integrated Development Studies",
    ("General Arts", "Finance & Economics"):              "BCom Banking and Finance",
    ("General Arts", "Management"):                       "BA Integrated Development Studies",
    ("General Arts", "Real Estate"):                      "BSc Real Estate",
    ("General Arts", "Journalism & Broadcasting"):        "BA Development Communication",
    ("General Arts", "International Relations"):          "BA Integrated Development Studies",
    ("General Arts", "Philosophy & Ethics"):              "BA African Discourse Studies",
    ("General Arts", "Psychology & Counselling"):         "BSc Population and Family Health",
    ("General Arts", "Religion & Theology"):              "BA African Discourse Studies",
    ("General Arts", "Languages & Linguistics"):          "BA Development Communication",

    # Business
    ("Business", "Accounting & Finance"):                 "BCom Accounting",
    ("Business", "Banking & Investment"):                 "BCom Banking and Finance",
    ("Business", "Entrepreneurship"):                     "BCom Accounting",
    ("Business", "Marketing & Management"):               "BCom Banking and Finance",
    ("Business", "Real Estate"):                          "BSc Real Estate",
    ("Business", "Economics"):                            "BCom Banking and Finance",
    ("Business", "Law & Legal Studies"):                  "BA Integrated Development Studies",
    ("Business", "Education & Teaching"):                 "B.Ed Social Studies",
    ("Business", "Communication & Media"):                "BA Development Communication",
    ("Business", "Supply Chain & Logistics"):             "BCom Accounting",
    ("Business", "Human Resource Management"):            "BCom Banking and Finance",
    ("Business", "Insurance & Risk Management"):          "BCom Banking and Finance",
    ("Business", "International Business"):               "BCom Banking and Finance",
    ("Business", "E-commerce & Digital Business"):        "BCom Accounting",

    # Home Economics
    ("Home Economics", "Healthcare & Public Health"):     "BSc Health Administration",
    ("Home Economics", "Education & Teaching"):           "B.Ed Social Studies",
    ("Home Economics", "Nutrition & Dietetics"):          "BSc Population and Family Health",
    ("Home Economics", "Social Sciences"):                "BSc Population and Family Health",
    ("Home Economics", "Management"):                     "BA Integrated Development Studies",
    ("Home Economics", "Entrepreneurship"):               "BCom Accounting",
    ("Home Economics", "Communication & Media"):          "BA Development Communication",
    ("Home Economics", "Development Studies"):            "BA Integrated Development Studies",
    ("Home Economics", "Fashion & Textile Design"):       "BA African Discourse Studies",
    ("Home Economics", "Hospitality & Catering"):         "BSc Health Administration",
    ("Home Economics", "Child Development & Family Studies"): "BSc Population and Family Health",
    ("Home Economics", "Interior Design & Housing"):      "BSc Real Estate",
    ("Home Economics", "Community Development"):          "BA Integrated Development Studies",
    ("Home Economics", "Social Work"):                    "BSc Population and Family Health",

    # Visual Arts
    ("Visual Arts", "Communication & Media"):             "BA Development Communication",
    ("Visual Arts", "Education & Teaching"):              "B.Ed Social Studies",
    ("Visual Arts", "Design & Creative Arts"):            "BA African Discourse Studies",
    ("Visual Arts", "Entrepreneurship"):                  "BCom Accounting",
    ("Visual Arts", "Development Studies"):               "BA Integrated Development Studies",
    ("Visual Arts", "Social Sciences"):                   "BA History and Diaspora Studies",
    ("Visual Arts", "History & Culture"):                 "BA History and Diaspora Studies",
    ("Visual Arts", "Management"):                        "BA Integrated Development Studies",
    ("Visual Arts", "Graphic Design & Advertising"):      "BA Development Communication",
    ("Visual Arts", "Photography & Film"):                "BA Development Communication",
    ("Visual Arts", "Architecture & Urban Design"):       "BSc Planning",
    ("Visual Arts", "Fashion Design"):                    "BA African Discourse Studies",
    ("Visual Arts", "Art Curating & Museum Studies"):     "BA History and Diaspora Studies",
    ("Visual Arts", "Journalism & Broadcasting"):         "BA Development Communication",

    # Agricultural Science
    ("Agricultural Science", "Research & Science"):           "BSc Population and Family Health",
    ("Agricultural Science", "Education & Teaching"):         "B.Ed Social Studies",
    ("Agricultural Science", "Environmental Studies"):        "BSc Geo-spatial Science",
    ("Agricultural Science", "Development Studies"):          "BA Integrated Development Studies",
    ("Agricultural Science", "Management"):                   "BSc Planning",
    ("Agricultural Science", "Finance & Economics"):          "BCom Banking and Finance",
    ("Agricultural Science", "Healthcare & Public Health"):   "BSc Health Administration",
    ("Agricultural Science", "Real Estate & Construction"):   "BSc Real Estate",
    ("Agricultural Science", "Agriculture & Food Science"):   "BSc Population and Family Health",
    ("Agricultural Science", "Forestry & Natural Resources"): "BSc Geo-spatial Science",
    ("Agricultural Science", "Animal Science & Veterinary"):  "BSc Population and Family Health",
    ("Agricultural Science", "Rural Development"):            "BA Integrated Development Studies",
    ("Agricultural Science", "Agribusiness & Entrepreneurship"): "BCom Accounting",
    ("Agricultural Science", "Water & Irrigation Management"): "BSc Geo-spatial Science",
}

# Diploma fallback map — one diploma per degree programme
# Applied when aggregate is poor (eligible=False)
DIPLOMA_MAP = {
    "BSc Construction Studies":          "Diploma in Construction Technology",
    "BSc Health Administration":         "Diploma in Health Services Management",
    "BSc Population and Family Health":  "Diploma in Community Health",
    "BSc Geo-spatial Science":           "Diploma in Geographic Information Systems",
    "BSc Computer Science":              "Diploma in Information Technology",
    "B.Ed Social Studies":               "Diploma in Education (Social Studies)",
    "BCom Banking and Finance":          "Diploma in Banking and Finance",
    "BSc Planning":                      "Diploma in Urban and Regional Planning",
    "BSc Real Estate":                   "Diploma in Real Estate Management",
    "BCom Accounting":                   "Diploma in Accounting",
    "BA African Discourse Studies":      "Diploma in African Studies",
    "BA Integrated Development Studies": "Diploma in Development Studies",
    "BA Development Communication":      "Diploma in Communication Studies",
    "BA History and Diaspora Studies":   "Diploma in History and Culture",
    "B.Ed Geography":                    "Diploma in Education (Geography)",
}

# Fallback degree by SHS program if interest not matched
PROGRAM_FALLBACK = {
    "General Science":     "BSc Health Administration",
    "General Arts":        "BA Integrated Development Studies",
    "Business":            "BCom Accounting",
    "Home Economics":      "BSc Population and Family Health",
    "Visual Arts":         "BA Development Communication",
    "Agricultural Science":"BSc Planning",
}

CAREER_MAP = {
    # ── Degree career paths ──────────────────────────────────────
    "BCom Accounting": [
        {"title": "Accountant",               "industry": "Finance"},
        {"title": "Auditor",                  "industry": "Finance"},
        {"title": "Tax Consultant",           "industry": "Finance"},
    ],
    "BCom Banking and Finance": [
        {"title": "Bank Officer",             "industry": "Banking"},
        {"title": "Financial Analyst",        "industry": "Banking"},
        {"title": "Investment Advisor",       "industry": "Finance"},
    ],
    "BSc Health Administration": [
        {"title": "Hospital Administrator",   "industry": "Healthcare"},
        {"title": "Health Policy Analyst",    "industry": "Public Health"},
        {"title": "Community Health Officer", "industry": "Public Health"},
    ],
    "BSc Population and Family Health": [
        {"title": "Public Health Officer",    "industry": "Public Health"},
        {"title": "Health Educator",          "industry": "Healthcare"},
        {"title": "Demographer",              "industry": "Research"},
    ],
    "BSc Real Estate": [
        {"title": "Real Estate Agent",        "industry": "Real Estate"},
        {"title": "Property Valuer",          "industry": "Real Estate"},
        {"title": "Facilities Manager",       "industry": "Real Estate"},
    ],
    "BSc Construction Studies": [
        {"title": "Construction Manager",     "industry": "Construction"},
        {"title": "Quantity Surveyor",        "industry": "Construction"},
        {"title": "Site Engineer",            "industry": "Construction"},
    ],
    "BSc Planning": [
        {"title": "Urban Planner",            "industry": "Government"},
        {"title": "Regional Planner",         "industry": "Government"},
        {"title": "Development Officer",      "industry": "NGO"},
    ],
    "BSc Geo-spatial Science": [
        {"title": "GIS Analyst",              "industry": "Technology"},
        {"title": "Remote Sensing Officer",   "industry": "Research"},
        {"title": "Cartographer",             "industry": "Government"},
    ],
    "BSc Computer Science": [
        {"title": "Software Developer",       "industry": "Technology"},
        {"title": "Data Scientist",           "industry": "Technology"},
        {"title": "Cybersecurity Analyst",    "industry": "Technology"},
    ],
    "BA Integrated Development Studies": [
        {"title": "Development Officer",      "industry": "NGO"},
        {"title": "Project Manager",          "industry": "NGO"},
        {"title": "Community Developer",      "industry": "Government"},
    ],
    "BA Development Communication": [
        {"title": "Communications Officer",   "industry": "NGO"},
        {"title": "Media Specialist",         "industry": "Media"},
        {"title": "Public Relations Officer", "industry": "Corporate"},
    ],
    "BA History and Diaspora Studies": [
        {"title": "Historian",                "industry": "Education"},
        {"title": "Archivist",                "industry": "Government"},
        {"title": "Museum Curator",           "industry": "Culture"},
    ],
    "BA African Discourse Studies": [
        {"title": "Cultural Analyst",         "industry": "Research"},
        {"title": "Lecturer",                 "industry": "Education"},
        {"title": "Policy Researcher",        "industry": "Government"},
    ],
    "B.Ed Social Studies": [
        {"title": "Social Studies Teacher",   "industry": "Education"},
        {"title": "Curriculum Developer",     "industry": "Education"},
        {"title": "Education Officer",        "industry": "Government"},
    ],
    "B.Ed Geography": [
        {"title": "Geography Teacher",        "industry": "Education"},
        {"title": "Education Officer",        "industry": "Government"},
        {"title": "Environmental Educator",   "industry": "Education"},
    ],

    # ── Diploma career paths ─────────────────────────────────────
    "Diploma in Accounting": [
        {"title": "Accounts Clerk",           "industry": "Finance"},
        {"title": "Bookkeeper",               "industry": "Finance"},
        {"title": "Payroll Officer",          "industry": "Finance"},
    ],
    "Diploma in Banking and Finance": [
        {"title": "Bank Teller",              "industry": "Banking"},
        {"title": "Credit Officer",           "industry": "Banking"},
        {"title": "Microfinance Officer",     "industry": "Finance"},
    ],
    "Diploma in Health Services Management": [
        {"title": "Health Records Officer",   "industry": "Healthcare"},
        {"title": "Ward Administrator",       "industry": "Healthcare"},
        {"title": "Community Health Assistant","industry": "Public Health"},
    ],
    "Diploma in Community Health": [
        {"title": "Community Health Worker",  "industry": "Public Health"},
        {"title": "Health Promoter",          "industry": "Healthcare"},
        {"title": "Disease Surveillance Officer","industry": "Public Health"},
    ],
    "Diploma in Geographic Information Systems": [
        {"title": "GIS Technician",           "industry": "Technology"},
        {"title": "Survey Assistant",         "industry": "Government"},
        {"title": "Mapping Technician",       "industry": "Research"},
    ],
    "Diploma in Information Technology": [
        {"title": "IT Support Technician",    "industry": "Technology"},
        {"title": "Network Technician",       "industry": "Technology"},
        {"title": "Web Developer",            "industry": "Technology"},
    ],
    "Diploma in Education (Social Studies)": [
        {"title": "Primary School Teacher",   "industry": "Education"},
        {"title": "Teaching Assistant",       "industry": "Education"},
        {"title": "Community Educator",       "industry": "Education"},
    ],
    "Diploma in Education (Geography)": [
        {"title": "Junior High School Teacher","industry": "Education"},
        {"title": "Teaching Assistant",       "industry": "Education"},
        {"title": "Field Studies Coordinator","industry": "Education"},
    ],
    "Diploma in Urban and Regional Planning": [
        {"title": "Planning Technician",      "industry": "Government"},
        {"title": "Community Development Assistant","industry": "NGO"},
        {"title": "Land Use Officer",         "industry": "Government"},
    ],
    "Diploma in Real Estate Management": [
        {"title": "Property Officer",         "industry": "Real Estate"},
        {"title": "Estate Agent Assistant",   "industry": "Real Estate"},
        {"title": "Letting Officer",          "industry": "Real Estate"},
    ],
    "Diploma in Construction Technology": [
        {"title": "Construction Technician",  "industry": "Construction"},
        {"title": "Site Supervisor",          "industry": "Construction"},
        {"title": "Building Inspector",       "industry": "Construction"},
    ],
    "Diploma in African Studies": [
        {"title": "Cultural Programme Officer","industry": "Culture"},
        {"title": "Community Liaison Officer","industry": "NGO"},
        {"title": "Research Assistant",       "industry": "Research"},
    ],
    "Diploma in Development Studies": [
        {"title": "Field Officer",            "industry": "NGO"},
        {"title": "Community Mobiliser",      "industry": "Government"},
        {"title": "Project Assistant",        "industry": "NGO"},
    ],
    "Diploma in Communication Studies": [
        {"title": "Radio Presenter",          "industry": "Media"},
        {"title": "Content Creator",          "industry": "Media"},
        {"title": "Community Reporter",       "industry": "Media"},
    ],
    "Diploma in History and Culture": [
        {"title": "Archive Assistant",        "industry": "Government"},
        {"title": "Cultural Guide",           "industry": "Culture"},
        {"title": "Museum Assistant",         "industry": "Culture"},
    ],
}


class AdvisoryMLService:
    def __init__(self):
        registry_path = ML_DIR / "model_registry.json"
        if not registry_path.exists():
            raise FileNotFoundError(
                f"model_registry.json not found in {ML_DIR}. "
                "Run export_model.py first."
            )
        with open(registry_path) as f:
            registry = json.load(f)

        version           = registry["active_version"]
        self.version      = version
        self.model        = joblib.load(ML_DIR / registry["versions"][version]["file"])
        self.label_encoders = joblib.load(ML_DIR / registry["versions"][version]["encoders"])

    def _grade_num(self, grade: str) -> float:
        return float(grade[1])

    def _safe_encode(self, col: str, val: str) -> int:
        le = self.label_encoders.get(col)
        if le is None or val not in le.classes_:
            return 0
        return int(le.transform([val])[0])

    def _get_programme(self, shs_program: str, interest: str) -> str:
        programme = PROGRAMME_MAP.get((shs_program, interest))
        if programme:
            return programme
        return PROGRAM_FALLBACK.get(shs_program, "BCom Accounting")

    def predict(self, data: dict) -> dict:
        core_math    = self._grade_num(data["core_math_grade"])
        core_english = self._grade_num(data["english_grade"])
        social       = self._grade_num(data["social_grade"])
        science      = self._grade_num(data["science_grade"])
        e1 = self._grade_num(data.get("elective_1_grade", "C6"))
        e2 = self._grade_num(data.get("elective_2_grade", "C6"))
        e3 = self._grade_num(data.get("elective_3_grade", "C6"))

        grades    = sorted([core_math, core_english, social, science, e1, e2, e3])
        aggregate = float(sum(grades[:6]))
        cut_off   = max(6.0, 36.0 - aggregate)

        shs_program = data.get("shs_program", "")
        interest    = data.get("interest", "")

        # Get the degree programme based on SHS program + interest
        degree_programme = self._get_programme(shs_program, interest)

        # Encode known values for model
        known_shs = shs_program if shs_program in [
            "General Arts", "General Science", "Business"
        ] else "General Arts"

        row = {
            "Core_Math":             core_math,
            "Core_English":          core_english,
            "Social_Studies":        social,
            "Integrated_Science":    science,
            "SHS_Program":           self._safe_encode("SHS_Program", known_shs),
            "Elective_1_Name":       self._safe_encode("Elective_1_Name", data.get("elective_1", "")),
            "Elective_1_Grade":      e1,
            "Elective_2_Name":       self._safe_encode("Elective_2_Name", data.get("elective_2", "")),
            "Elective_2_Grade":      e2,
            "Elective_3_Name":       self._safe_encode("Elective_3_Name", data.get("elective_3", "")),
            "Elective_3_Grade":      e3,
            "Interest":              self._safe_encode("Interest", "Engineering"),
            "Aggregate":             aggregate,
            "Qualified_for_Degree":  self._safe_encode("Qualified_for_Degree", "Yes"),
            "Recommended_Programme": self._safe_encode(
                "Recommended_Programme",
                degree_programme if degree_programme in self.label_encoders.get(
                    "Recommended_Programme",
                    type("obj", (object,), {"classes_": []})()
                ).classes_ else "BCom Accounting"
            ),
            "Cut_Off_Point":         cut_off,
        }

        X    = pd.DataFrame([row])
        pred = int(self.model.predict(X)[0])
        prob = float(self.model.predict_proba(X)[0].max())

        eligible = pred == 1

        # If eligible → recommend degree programme
        # If not eligible → recommend the matching diploma instead
        if eligible:
            recommended = degree_programme
            programme_type = "Degree"
        else:
            recommended = DIPLOMA_MAP.get(degree_programme, "Diploma in Development Studies")
            programme_type = "Diploma"

        return {
            "eligible":              eligible,
            "confidence":            round(prob, 4),
            "model_version":         self.version,
            "recommended_programme": recommended,
            "programme_type":        programme_type,
            "degree_equivalent":     degree_programme,
            "careers":               CAREER_MAP.get(recommended, []),
        }


# Loaded once when FastAPI starts
ml_service = AdvisoryMLService()