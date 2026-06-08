from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.rag_knowledge_base import (
    RAGKnowledgeBase
)

from app.ai.rag.embedding_service import (
    generate_embedding
)

medical_knowledge = [

# ==========================
# EMERGENCY
# ==========================

{
    "title": "Heart Attack Symptoms",
    "category": "Emergency",
    "source": "Medical Guidelines",
    "content": "Severe chest pain, sweating, shortness of breath, nausea, pain radiating to arm or jaw.",
    "medical_specialty": "Cardiology",
    "keywords": "heart attack,chest pain,sweating,shortness of breath",
    "chunk_index": 1
},

{
    "title": "Stroke Symptoms",
    "category": "Emergency",
    "source": "Medical Guidelines",
    "content": "Facial drooping, arm weakness, speech difficulty, sudden confusion, loss of balance.",
    "medical_specialty": "Neurology",
    "keywords": "stroke,facial droop,speech difficulty,weakness",
    "chunk_index": 2
},

{
    "title": "Sepsis Warning Signs",
    "category": "Emergency",
    "source": "Medical Guidelines",
    "content": "High fever, rapid heart rate, low blood pressure, confusion and difficulty breathing.",
    "medical_specialty": "Emergency",
    "keywords": "sepsis,fever,confusion,low blood pressure",
    "chunk_index": 3
},

{
    "title": "Anaphylaxis",
    "category": "Emergency",
    "source": "Medical Guidelines",
    "content": "Severe allergic reaction causing swelling, breathing difficulty, wheezing and shock.",
    "medical_specialty": "Emergency",
    "keywords": "anaphylaxis,allergy,wheezing,swelling",
    "chunk_index": 4
},

# ==========================
# CARDIOLOGY
# ==========================

{
    "title": "Angina",
    "category": "Cardiology",
    "source": "Medical Guidelines",
    "content": "Chest discomfort triggered by exertion and relieved by rest.",
    "medical_specialty": "Cardiology",
    "keywords": "angina,chest pain,exertion",
    "chunk_index": 5
},

{
    "title": "Arrhythmia",
    "category": "Cardiology",
    "source": "Medical Guidelines",
    "content": "Palpitations, dizziness, fainting episodes and irregular heartbeat.",
    "medical_specialty": "Cardiology",
    "keywords": "arrhythmia,palpitations,irregular heartbeat",
    "chunk_index": 6
},

{
    "title": "Heart Failure",
    "category": "Cardiology",
    "source": "Medical Guidelines",
    "content": "Breathlessness, swollen legs, fatigue and reduced exercise tolerance.",
    "medical_specialty": "Cardiology",
    "keywords": "heart failure,leg swelling,fatigue",
    "chunk_index": 7
},

# ==========================
# NEUROLOGY
# ==========================

{
    "title": "Migraine",
    "category": "Neurology",
    "source": "Medical Guidelines",
    "content": "Severe headache associated with nausea, sensitivity to light and visual disturbances.",
    "medical_specialty": "Neurology",
    "keywords": "migraine,headache,nausea,blurred vision",
    "chunk_index": 8
},

{
    "title": "Seizure Disorder",
    "category": "Neurology",
    "source": "Medical Guidelines",
    "content": "Loss of consciousness, involuntary body movements and post seizure confusion.",
    "medical_specialty": "Neurology",
    "keywords": "seizure,convulsion,loss of consciousness",
    "chunk_index": 9
},

{
    "title": "Parkinson Disease",
    "category": "Neurology",
    "source": "Medical Guidelines",
    "content": "Resting tremor, slow movements, muscle rigidity and balance issues.",
    "medical_specialty": "Neurology",
    "keywords": "parkinson,tremor,rigidity",
    "chunk_index": 10
},

# ==========================
# PULMONOLOGY
# ==========================

{
    "title": "Asthma Exacerbation",
    "category": "Pulmonology",
    "source": "Medical Guidelines",
    "content": "Wheezing, chest tightness, cough and shortness of breath.",
    "medical_specialty": "Pulmonology",
    "keywords": "asthma,wheezing,cough",
    "chunk_index": 11
},

{
    "title": "Pneumonia",
    "category": "Pulmonology",
    "source": "Medical Guidelines",
    "content": "Fever, productive cough, chest pain and breathing difficulty.",
    "medical_specialty": "Pulmonology",
    "keywords": "pneumonia,fever,cough",
    "chunk_index": 12
},

{
    "title": "COPD Exacerbation",
    "category": "Pulmonology",
    "source": "Medical Guidelines",
    "content": "Chronic cough, wheezing and worsening shortness of breath.",
    "medical_specialty": "Pulmonology",
    "keywords": "copd,chronic cough,wheezing",
    "chunk_index": 13
},

# ==========================
# ORTHOPEDICS
# ==========================

{
    "title": "Bone Fracture",
    "category": "Orthopedics",
    "source": "Medical Guidelines",
    "content": "Severe pain, swelling, deformity and inability to move affected limb.",
    "medical_specialty": "Orthopedics",
    "keywords": "fracture,broken bone,swelling",
    "chunk_index": 14
},

{
    "title": "Ligament Injury",
    "category": "Orthopedics",
    "source": "Medical Guidelines",
    "content": "Joint pain, instability, swelling and reduced movement.",
    "medical_specialty": "Orthopedics",
    "keywords": "ligament,sprain,joint injury",
    "chunk_index": 15
},

{
    "title": "Osteoarthritis",
    "category": "Orthopedics",
    "source": "Medical Guidelines",
    "content": "Joint stiffness, pain during movement and decreased mobility.",
    "medical_specialty": "Orthopedics",
    "keywords": "arthritis,joint pain,stiffness",
    "chunk_index": 16
},

# ==========================
# ENT
# ==========================

{
    "title": "Acute Sinusitis",
    "category": "ENT",
    "source": "Medical Guidelines",
    "content": "Facial pain, nasal congestion and thick nasal discharge.",
    "medical_specialty": "ENT",
    "keywords": "sinusitis,facial pain,nasal congestion",
    "chunk_index": 17
},

{
    "title": "Tonsillitis",
    "category": "ENT",
    "source": "Medical Guidelines",
    "content": "Sore throat, fever, swollen tonsils and painful swallowing.",
    "medical_specialty": "ENT",
    "keywords": "tonsillitis,sore throat,swallowing pain",
    "chunk_index": 18
},

{
    "title": "Otitis Media",
    "category": "ENT",
    "source": "Medical Guidelines",
    "content": "Ear pain, fever and temporary hearing loss.",
    "medical_specialty": "ENT",
    "keywords": "ear infection,ear pain,hearing loss",
    "chunk_index": 19
},

# ==========================
# DERMATOLOGY
# ==========================

{
    "title": "Eczema",
    "category": "Dermatology",
    "source": "Medical Guidelines",
    "content": "Dry itchy skin with redness and inflammation.",
    "medical_specialty": "Dermatology",
    "keywords": "eczema,itching,skin rash",
    "chunk_index": 20
},

{
    "title": "Psoriasis",
    "category": "Dermatology",
    "source": "Medical Guidelines",
    "content": "Scaly plaques on skin with itching and irritation.",
    "medical_specialty": "Dermatology",
    "keywords": "psoriasis,skin plaques",
    "chunk_index": 21
},

{
    "title": "Fungal Skin Infection",
    "category": "Dermatology",
    "source": "Medical Guidelines",
    "content": "Circular itchy rash with redness and scaling.",
    "medical_specialty": "Dermatology",
    "keywords": "fungal infection,ringworm,itching",
    "chunk_index": 22
},

# ==========================
# PEDIATRICS
# ==========================

{
    "title": "Childhood Fever",
    "category": "Pediatrics",
    "source": "Medical Guidelines",
    "content": "Elevated body temperature with irritability and reduced feeding.",
    "medical_specialty": "Pediatrics",
    "keywords": "child fever,pediatric fever",
    "chunk_index": 23
},

{
    "title": "Bronchiolitis",
    "category": "Pediatrics",
    "source": "Medical Guidelines",
    "content": "Cough, wheezing and breathing difficulty in infants.",
    "medical_specialty": "Pediatrics",
    "keywords": "bronchiolitis,infant cough,wheezing",
    "chunk_index": 24
},

{
    "title": "Pediatric Asthma",
    "category": "Pediatrics",
    "source": "Medical Guidelines",
    "content": "Recurring wheezing, cough and shortness of breath in children.",
    "medical_specialty": "Pediatrics",
    "keywords": "child asthma,wheezing",
    "chunk_index": 25
},

# ==========================
# GENERAL MEDICINE
# ==========================

{
    "title": "Viral Fever",
    "category": "General Medicine",
    "source": "Medical Guidelines",
    "content": "Fever, body aches, fatigue, headache and mild respiratory symptoms.",
    "medical_specialty": "General Medicine",
    "keywords": "viral fever,fever,body ache",
    "chunk_index": 26
},

{
    "title": "Hypertension",
    "category": "General Medicine",
    "source": "Medical Guidelines",
    "content": "Persistently elevated blood pressure, headache and dizziness.",
    "medical_specialty": "General Medicine",
    "keywords": "hypertension,blood pressure,dizziness",
    "chunk_index": 27
},

{
    "title": "Type 2 Diabetes",
    "category": "General Medicine",
    "source": "Medical Guidelines",
    "content": "Increased thirst, frequent urination, fatigue and blurred vision.",
    "medical_specialty": "General Medicine",
    "keywords": "diabetes,frequent urination,thirst",
    "chunk_index": 28
},

# ==========================
# GASTROENTEROLOGY
# ==========================

{
    "title": "Gastritis",
    "category": "Gastroenterology",
    "source": "Medical Guidelines",
    "content": "Burning stomach pain, nausea, bloating and indigestion.",
    "medical_specialty": "Gastroenterology",
    "keywords": "gastritis,stomach pain,bloating",
    "chunk_index": 29
},

{
    "title": "Peptic Ulcer Disease",
    "category": "Gastroenterology",
    "source": "Medical Guidelines",
    "content": "Upper abdominal pain, nausea and burning sensation after meals.",
    "medical_specialty": "Gastroenterology",
    "keywords": "ulcer,abdominal pain,burning stomach",
    "chunk_index": 30
},

{
    "title": "Acute Appendicitis",
    "category": "Gastroenterology",
    "source": "Medical Guidelines",
    "content": "Right lower abdominal pain, fever, nausea and loss of appetite.",
    "medical_specialty": "Gastroenterology",
    "keywords": "appendicitis,right lower abdomen pain",
    "chunk_index": 31
},

{
    "title": "Gallstones",
    "category": "Gastroenterology",
    "source": "Medical Guidelines",
    "content": "Upper right abdominal pain after meals, nausea and vomiting.",
    "medical_specialty": "Gastroenterology",
    "keywords": "gallstones,gallbladder pain",
    "chunk_index": 32
},

# ==========================
# NEPHROLOGY
# ==========================

{
    "title": "Kidney Stone",
    "category": "Nephrology",
    "source": "Medical Guidelines",
    "content": "Severe flank pain, blood in urine, nausea and vomiting.",
    "medical_specialty": "Nephrology",
    "keywords": "kidney stone,flank pain,blood urine",
    "chunk_index": 33
},

{
    "title": "Urinary Tract Infection",
    "category": "Nephrology",
    "source": "Medical Guidelines",
    "content": "Burning urination, urinary frequency and lower abdominal pain.",
    "medical_specialty": "Nephrology",
    "keywords": "uti,burning urination,urinary frequency",
    "chunk_index": 34
},

{
    "title": "Chronic Kidney Disease",
    "category": "Nephrology",
    "source": "Medical Guidelines",
    "content": "Fatigue, swelling of legs, reduced urine output and nausea.",
    "medical_specialty": "Nephrology",
    "keywords": "ckd,kidney disease,leg swelling",
    "chunk_index": 35
},

# ==========================
# PSYCHIATRY
# ==========================

{
    "title": "Major Depression",
    "category": "Psychiatry",
    "source": "Medical Guidelines",
    "content": "Persistent sadness, loss of interest, fatigue and sleep disturbances.",
    "medical_specialty": "Psychiatry",
    "keywords": "depression,sadness,fatigue",
    "chunk_index": 36
},

{
    "title": "Generalized Anxiety Disorder",
    "category": "Psychiatry",
    "source": "Medical Guidelines",
    "content": "Excessive worry, restlessness, irritability and sleep problems.",
    "medical_specialty": "Psychiatry",
    "keywords": "anxiety,worry,restlessness",
    "chunk_index": 37
},

{
    "title": "Panic Attack",
    "category": "Psychiatry",
    "source": "Medical Guidelines",
    "content": "Sudden fear, chest tightness, palpitations and shortness of breath.",
    "medical_specialty": "Psychiatry",
    "keywords": "panic attack,palpitations,fear",
    "chunk_index": 38
},

# ==========================
# ONCOLOGY
# ==========================

{
    "title": "Cancer Warning Signs",
    "category": "Oncology",
    "source": "Medical Guidelines",
    "content": "Unexplained weight loss, persistent fatigue and abnormal lumps.",
    "medical_specialty": "Oncology",
    "keywords": "cancer,weight loss,lump",
    "chunk_index": 39
},

{
    "title": "Lung Cancer Symptoms",
    "category": "Oncology",
    "source": "Medical Guidelines",
    "content": "Persistent cough, coughing blood, chest pain and weight loss.",
    "medical_specialty": "Oncology",
    "keywords": "lung cancer,coughing blood",
    "chunk_index": 40
},

# ==========================
# GYNECOLOGY
# ==========================

{
    "title": "Pelvic Inflammatory Disease",
    "category": "Gynecology",
    "source": "Medical Guidelines",
    "content": "Lower abdominal pain, fever and abnormal vaginal discharge.",
    "medical_specialty": "Gynecology",
    "keywords": "pid,pelvic pain,vaginal discharge",
    "chunk_index": 41
},

{
    "title": "Pregnancy Complications",
    "category": "Gynecology",
    "source": "Medical Guidelines",
    "content": "Vaginal bleeding, severe abdominal pain and dizziness during pregnancy.",
    "medical_specialty": "Gynecology",
    "keywords": "pregnancy bleeding,abdominal pain",
    "chunk_index": 42
},

{
    "title": "Polycystic Ovary Syndrome",
    "category": "Gynecology",
    "source": "Medical Guidelines",
    "content": "Irregular periods, weight gain and excessive hair growth.",
    "medical_specialty": "Gynecology",
    "keywords": "pcos,irregular periods",
    "chunk_index": 43
},

# ==========================
# UROLOGY
# ==========================

{
    "title": "Benign Prostatic Hyperplasia",
    "category": "Urology",
    "source": "Medical Guidelines",
    "content": "Frequent urination, weak urinary stream and incomplete bladder emptying.",
    "medical_specialty": "Urology",
    "keywords": "bph,prostate,frequent urination",
    "chunk_index": 44
},

{
    "title": "Acute Urinary Retention",
    "category": "Urology",
    "source": "Medical Guidelines",
    "content": "Sudden inability to urinate with severe lower abdominal discomfort.",
    "medical_specialty": "Urology",
    "keywords": "urinary retention,cannot urinate",
    "chunk_index": 45
},

# ==========================
# ENDOCRINOLOGY
# ==========================

{
    "title": "Hypothyroidism",
    "category": "Endocrinology",
    "source": "Medical Guidelines",
    "content": "Fatigue, weight gain, cold intolerance and dry skin.",
    "medical_specialty": "Endocrinology",
    "keywords": "hypothyroidism,weight gain,fatigue",
    "chunk_index": 46
},

{
    "title": "Hyperthyroidism",
    "category": "Endocrinology",
    "source": "Medical Guidelines",
    "content": "Weight loss, palpitations, sweating and anxiety.",
    "medical_specialty": "Endocrinology",
    "keywords": "hyperthyroidism,palpitations,weight loss",
    "chunk_index": 47
},

{
    "title": "Diabetic Ketoacidosis",
    "category": "Endocrinology",
    "source": "Medical Guidelines",
    "content": "Excessive thirst, vomiting, abdominal pain and confusion.",
    "medical_specialty": "Endocrinology",
    "keywords": "dka,diabetes,confusion,vomiting",
    "chunk_index": 48
},

{
    "title": "Hypoglycemia",
    "category": "Endocrinology",
    "source": "Medical Guidelines",
    "content": "Sweating, tremors, dizziness, confusion and fainting.",
    "medical_specialty": "Endocrinology",
    "keywords": "hypoglycemia,low sugar,dizziness",
    "chunk_index": 49
},

{
    "title": "Adrenal Insufficiency",
    "category": "Endocrinology",
    "source": "Medical Guidelines",
    "content": "Fatigue, weight loss, low blood pressure and dizziness.",
    "medical_specialty": "Endocrinology",
    "keywords": "adrenal insufficiency,low blood pressure",
    "chunk_index": 50
}
]

def load_knowledge():

    db: Session = SessionLocal()

    try:

        for item in medical_knowledge:

            existing = (

                db.query(
                    RAGKnowledgeBase
                )

                .filter(
                    RAGKnowledgeBase.title
                    == item["title"]
                )

                .first()
            )

            if existing:

                print(
                    f"Skipping {item['title']}"
                )

                continue

            embedding_text = f"""
            {item['title']}
            {item['content']}
            {item['keywords']}
            """

            embedding = generate_embedding(
                embedding_text
            )

            knowledge = RAGKnowledgeBase(

                title=item["title"],

                category=item["category"],

                source=item["source"],

                content=item["content"],

                medical_specialty=
                item["medical_specialty"],

                keywords=item["keywords"],

                chunk_index=item["chunk_index"],

                embedding=embedding
            )

            db.add(
                knowledge
            )

            print(
                f"Added {item['title']}"
            )

        db.commit()

        print(
            "Medical knowledge loaded successfully"
        )

    finally:

        db.close()


if __name__ == "__main__":

    load_knowledge()