import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import time
from calendar import monthrange
import calendar

# --- Page Configuration ---
st.set_page_config(
    page_title="TriageView - Veteran Mental Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- VETERAN-FOCUSED COLOR PALETTE ---
COLORS = {
    "primary_blue": "#5B9BD3",
    "primary_teal": "#3E8A7E",
    "secondary_light_sky": "#A8D8F0",
    "secondary_deep_teal": "#2C6B5F",
    "secondary_sandstone": "#D8C9B8",
    "accent_coral": "#FF7F50",
    "accent_green": "#77DD77",
    "neutral_white": "#FFFFFF",
    "neutral_off_white": "#F8F8F8",
    "neutral_light_gray": "#E0E0E0",
    "neutral_medium_gray": "#757575",
    "neutral_charcoal": "#333333"
}

# --- Gemini AI Configuration ---
GEMINI_API_KEY = "AIzaSyAdvvEDdIaXUqQvNR__5NB_RDHkzAzKuXc"

# --- Initialize session state ---
def initialize_session_state():
    if 'reset_filters' not in st.session_state:
        st.session_state.reset_filters = False
    if 'filters_initialized' not in st.session_state:
        st.session_state.filters_initialized = False
    if 'filter_reset_counter' not in st.session_state:
        st.session_state.filter_reset_counter = 0
    if 'ai_summaries' not in st.session_state:
        st.session_state.ai_summaries = {}
    if 'dataset_generated' not in st.session_state:
        st.session_state.dataset_generated = False
    if 'button_responses' not in st.session_state:
        st.session_state.button_responses = {}
    if 'calendar_view' not in st.session_state:
        st.session_state.calendar_view = datetime.now()
    if 'appointments' not in st.session_state:
        st.session_state.appointments = generate_sample_appointments()
    if 'selected_calendar_day' not in st.session_state:
        st.session_state.selected_calendar_day = None

def generate_sample_appointments():
    """Generate sample appointments for the calendar - NO WEEKENDS, 60-minute slots"""
    appointments = []
    today = datetime.now()
    
    for i in range(30):
        date = today + timedelta(days=i)
        
        # Skip weekends (Saturday = 5, Sunday = 6)
        if date.weekday() in [5, 6]:  # Skip Saturday and Sunday
            continue
            
        # Generate appointments only for weekdays (Monday-Friday)
        # Standard business hours: 8 AM to 4 PM (8 total hour slots)
        available_hours = [8, 9, 10, 11, 12, 13, 14, 15, 16]  # 8 AM to 4 PM
        
        # Randomly assign some of these hours as appointments
        num_appointments = random.randint(0, min(8, len(available_hours)))
        selected_hours = random.sample(available_hours, num_appointments)
        
        for hour in selected_hours:
            # 60-minute appointments starting on the hour (minute = 0)
            appointment_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            status = random.choices(['available', 'reserved', 'cancelled'], weights=[0.4, 0.5, 0.1])[0]
            
            # Determine appointment type (face-to-face vs online)
            appointment_mode = random.choices(['Face-to-Face', 'Video Call'], weights=[0.6, 0.4])[0]
            
            appointments.append({
                'date': appointment_time.date(),
                'time': appointment_time.time(),
                'datetime': appointment_time,
                'status': status,
                'mode': appointment_mode,  # New field for appointment type
                'veteran_id': f"VET-{1000 + random.randint(1, 100):04d}" if status == 'reserved' else None,
                'clinician': random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis"]) if status == 'reserved' else None,
                'type': random.choice(["Initial Assessment", "Follow-up", "Crisis Intervention", "Medication Review"]) if status == 'reserved' else None
            })
    
    return appointments

# --- Enhanced CSS for Better UI/UX (Updated Calendar Styling) ---
def load_enhanced_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            background-color: {COLORS['neutral_off_white']};
            color: {COLORS['neutral_charcoal']};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Fix sidebar and main content layout issues */
        .css-1d391kg {{
            background: linear-gradient(180deg, {COLORS['neutral_white']}, #f8f9fa);
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            z-index: 999 !important;
            width: 21rem !important;
            overflow-y: auto !important;
        }}
        
        .main .block-container {{
            padding: 2rem 2rem 2rem 2rem !important;
            margin-left: 0 !important;
            max-width: none !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {{
            margin-left: 21rem !important;
            transition: margin-left 0.3s ease !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {{
            margin-left: 0 !important;
            transition: margin-left 0.3s ease !important;
        }}
        
        @media (max-width: 768px) {{
            section[data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {{
                margin-left: 0 !important;
            }}
            
            .css-1d391kg {{
                width: 100% !important;
            }}
            
            .main .block-container {{
                padding: 1rem !important;
            }}
        }}
        
        /* Enhanced AI summary boxes */
        .ai-summary-all-patients {{
            background: linear-gradient(135deg, rgba(91, 155, 211, 0.15), rgba(62, 138, 126, 0.15)) !important;
            border: 2px solid {COLORS['primary_blue']} !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(91, 155, 211, 0.2) !important;
            position: relative !important;
        }}
        
        .ai-summary-all-patients::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {COLORS['primary_blue']}, {COLORS['primary_teal']});
            border-radius: 12px 12px 0 0;
        }}
        
        .ai-summary-all-patients h4 {{
            color: {COLORS['primary_blue']} !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            background: transparent !important;
        }}
        
        .ai-summary-all-patients p {{
            color: {COLORS['neutral_charcoal']} !important;
            line-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
            background: transparent !important;
        }}
        
        .ai-summary-individual {{
            background: linear-gradient(135deg, rgba(62, 138, 126, 0.15), rgba(119, 221, 119, 0.15)) !important;
            border: 2px solid {COLORS['primary_teal']} !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(62, 138, 126, 0.2) !important;
            position: relative !important;
        }}
        
        .ai-summary-individual::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {COLORS['primary_teal']}, {COLORS['accent_green']});
            border-radius: 12px 12px 0 0;
        }}
        
        .ai-summary-individual h4 {{
            color: {COLORS['primary_teal']} !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            background: transparent !important;
        }}
        
        .ai-summary-individual p {{
            color: {COLORS['neutral_charcoal']} !important;
            line-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
            background: transparent !important;
        }}
        
        /* Button response styling */
        .button-response {{
            background: linear-gradient(135deg, rgba(119, 221, 119, 0.2), rgba(62, 138, 126, 0.2)) !important;
            border: 1px solid {COLORS['accent_green']} !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            color: {COLORS['neutral_charcoal']} !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 4px rgba(119, 221, 119, 0.1) !important;
        }}
        
        /* Enhanced button styling */
        .stButton > button {{
            border-radius: 0.5rem !important;
            border: none !important;
            background: linear-gradient(135deg, {COLORS['primary_blue']}, {COLORS['primary_teal']}) !important;
            color: white !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            width: 100% !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            background: linear-gradient(135deg, {COLORS['secondary_deep_teal']}, {COLORS['primary_blue']}) !important;
        }}
        
        /* FIXED Calendar styling */
        .calendar-container {{
            background: {COLORS['neutral_white']};
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        
        .calendar-day {{
            aspect-ratio: 1;
            border: 1px solid {COLORS['neutral_light_gray']};
            border-radius: 8px;
            padding: 0.4rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            min-height: 90px;
            max-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            overflow: hidden;
            position: relative;
        }}
        
        .calendar-day:hover {{
            background-color: {COLORS['secondary_light_sky']};
            transform: scale(1.02);
            z-index: 10;
        }}
        
        .calendar-day-empty {{
            border: none;
            cursor: default;
        }}
        
        .calendar-day-empty:hover {{
            background: transparent;
            transform: none;
        }}
        
        .appointment-available {{
            background-color: rgba(119, 221, 119, 0.3);
            border-color: {COLORS['accent_green']};
        }}
        
        .appointment-reserved {{
            background-color: rgba(91, 155, 211, 0.3);
            border-color: {COLORS['primary_blue']};
        }}
        
        .appointment-cancelled {{
            background-color: rgba(255, 127, 80, 0.3);
            border-color: {COLORS['accent_coral']};
        }}
        
        .appointment-details {{
            background: {COLORS['neutral_white']};
            border: 1px solid {COLORS['neutral_light_gray']};
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        /* Calendar day number styling */
        .calendar-day-number {{
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.2rem;
            line-height: 1;
        }}
        
        /* Calendar appointment info styling */
        .calendar-appointment-info {{
            font-size: 0.6rem;
            line-height: 1.1;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
        }}
        
        .calendar-appointment-line {{
            margin: 0.1rem 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        /* Priority alert enhancements */
        .priority-alert {{
            background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
            color: white !important;
            padding: 1rem !important;
            border-radius: 0.75rem !important;
            margin: 1rem 0 !important;
            text-align: center !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
            border: none !important;
            animation: pulse-alert 2s infinite !important;
        }}
        
        @keyframes pulse-alert {{
            0%, 100% {{ 
                box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3), 0 0 0 0 rgba(220, 38, 38, 0.2); 
            }}
            50% {{ 
                box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3), 0 0 0 10px rgba(220, 38, 38, 0); 
            }}
        }}
        
        /* Enhanced metrics - remove arrows */
        .stMetric {{
            background: {COLORS['neutral_white']} !important;
            border: 1px solid {COLORS['neutral_light_gray']} !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            position: relative !important;
        }}
        
        .stMetric:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        }}
        
        /* Hide metric delta arrows */
        .stMetric [data-testid="metric-delta"] {{
            display: none !important;
        }}
        
        /* Category styling */
        .category-emergent {{
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(185, 28, 28, 0.05));
            border-left: 4px solid #dc2626;
            color: #7f1d1d;
        }}
        
        .category-urgent {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.05));
            border-left: 4px solid #f59e0b;
            color: #78350f;
        }}
        
        .category-routine {{
            background: linear-gradient(135deg, rgba(119, 221, 119, 0.1), rgba(107, 195, 115, 0.05));
            border-left: 4px solid #77dd77;
            color: #166534;
        }}
        
        /* Form enhancements */
        .stSelectbox > div > div,
        .stMultiSelect > div > div {{
            border-radius: 0.5rem !important;
            border: 1px solid {COLORS['neutral_light_gray']} !important;
            transition: all 0.2s ease !important;
        }}
        
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {{
            border-color: {COLORS['primary_blue']} !important;
            box-shadow: 0 0 0 3px rgba(91, 155, 211, 0.1) !important;
        }}
        
        /* Hide unwanted elements */
        .css-1rs6os, .css-17ziqus {{
            visibility: hidden;
        }}
        
        #MainMenu {{
            visibility: hidden;
        }}
        
        footer {{
            visibility: hidden;
        }}
        
        header {{
            visibility: hidden;
        }}
        
        /* Data table improvements */
        .stDataFrame {{
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
            border: 1px solid {COLORS['neutral_light_gray']} !important;
        }}
        
        /* Success/error messages */
        .stSuccess {{
            background: linear-gradient(135deg, {COLORS['accent_green']}, #6bc373) !important;
            color: white !important;
            border-radius: 0.5rem !important;
            border: none !important;
        }}
        
        .stError {{
            background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
            color: white !important;
            border-radius: 0.5rem !important;
            border: none !important;
        }}
        
        .stWarning {{
            background: linear-gradient(135deg, #f59e0b, #d97706) !important;
            color: white !important;
            border-radius: 0.5rem !important;
            border: none !important;
        }}
        
        .stInfo {{
            background: linear-gradient(135deg, {COLORS['primary_blue']}, {COLORS['primary_teal']}) !important;
            color: white !important;
            border-radius: 0.5rem !important;
            border: none !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- AI Integration Functions ---
def call_gemini_api(prompt, model="gemini-1.5-flash"):
    """Call Gemini API with proper error handling"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                if 'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content']:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "AI response format unexpected. Please try again."
            else:
                return "No response generated. Please try again."
        else:
            error_detail = response.json() if response.content else "Unknown error"
            return f"API Error ({response.status_code}): {error_detail}"
            
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Network error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def generate_ai_summary(data, summary_type="all_patients"):
    """Generate AI summary using enhanced prompts"""
    try:
        if summary_type == "all_patients":
            emergent_cases = len(data[data['VA Category'] == 'Emergent'])
            urgent_cases = len(data[data['VA Category'] == 'Urgent'])
            routine_cases = len(data[data['VA Category'] == 'Routine'])
            
            prompt = f"""
You are a senior clinical psychologist and veteran mental health specialist with 20+ years of experience in VA clinical settings. Analyze this veteran patient population data and provide actionable clinical insights.

VETERAN POPULATION METRICS:
• Total Veterans in Current Caseload: {len(data)}
• EMERGENT Cases (Imminent Suicide Risk): {emergent_cases} veterans
• URGENT Cases (Same-Day Evaluation Needed): {urgent_cases} veterans  
• ROUTINE Cases (Timely Follow-up): {routine_cases} veterans

CLINICAL SEVERITY INDICATORS:
• Average Depression Severity (PHQ-9): {data['PHQ-9 Score'].mean():.1f}/27
• Average Anxiety Severity (GAD-7): {data['GAD-7 Score'].mean():.1f}/21
• Average PTSD Severity (PCL-5): {data['PCL-5 Score'].mean():.1f}/80
• Veterans with Active Suicidal Ideation: {len(data[data['PHQ-9 Q9 (Self-Harm)'] == 'Yes'])}

PSYCHOSOCIAL RISK FACTORS:
• Housing Instability: {len(data[data['Housing Status'].isin(['At Risk', 'Homeless'])])} veterans ({(len(data[data['Housing Status'].isin(['At Risk', 'Homeless'])]) / len(data) * 100):.1f}%)
• Social Isolation (Low Support): {len(data[data['Social Support'] == 'Low'])} veterans ({(len(data[data['Social Support'] == 'Low']) / len(data) * 100):.1f}%)
• High Substance Use Risk: {len(data[data['Substance Use Risk'] == 'High'])} veterans ({(len(data[data['Substance Use Risk'] == 'High']) / len(data) * 100):.1f}%)

TREATMENT READINESS:
• Therapy-Focused Treatment: {len(data[data['Treatment Preference'] == 'Therapy'])} veterans
• Medication-Focused Treatment: {len(data[data['Treatment Preference'] == 'Medication'])} veterans
• Integrated Treatment (Both): {len(data[data['Treatment Preference'] == 'Both'])} veterans

CLINICAL PRIORITIES TO ADDRESS:
1. **Immediate Crisis Intervention**: Focus on {emergent_cases + urgent_cases} high-acuity cases requiring same-day response
2. **Risk Stratification**: Prioritize resource allocation based on VA triage categories
3. **Treatment Matching**: Align interventions with veteran preferences and clinical needs

Provide a concise clinical summary (150-200 words) that includes:
- Key population health trends
- Primary clinical concerns requiring immediate attention  
- Evidence-based recommendations for care coordination
- Specific actions for improving outcomes

Write in professional clinical language suitable for interdisciplinary team meetings.
            """
        
        elif summary_type == "individual_patient":
            veteran = data.iloc[0]
            
            prompt = f"""
You are a licensed clinical psychologist conducting a comprehensive assessment for a veteran patient. Provide a thorough clinical formulation and treatment recommendations.

VETERAN CLINICAL PROFILE:
• Patient: {veteran.get('Name', 'Veteran')} ({veteran['Veteran ID']})
• Demographics: {veteran['Age']}-year-old {veteran['Gender']}, {veteran['Branch']} veteran from {veteran['Service Era']} era
• Current Triage Status: {veteran['VA Category']} (Risk Score: {veteran['Risk Score']}/6)

SUICIDE RISK ASSESSMENT:
• C-SSRS Screening Result: {veteran['C-SSRS Screen']}
• PHQ-9 Item 9 (Suicidal Ideation): {veteran['PHQ-9 Q9 (Self-Harm)']}
• Clinical Risk Explanation: {veteran['Risk Explanation']}

STANDARDIZED ASSESSMENT SCORES:
• PHQ-9 Depression Scale: {veteran['PHQ-9 Score']}/27 (Clinical Range: {'Severe' if veteran['PHQ-9 Score'] >= 20 else 'Moderate-Severe' if veteran['PHQ-9 Score'] >= 15 else 'Moderate' if veteran['PHQ-9 Score'] >= 10 else 'Mild' if veteran['PHQ-9 Score'] >= 5 else 'Minimal'})
• GAD-7 Anxiety Scale: {veteran['GAD-7 Score']}/21 (Clinical Range: {'Severe' if veteran['GAD-7 Score'] >= 15 else 'Moderate' if veteran['GAD-7 Score'] >= 10 else 'Mild' if veteran['GAD-7 Score'] >= 5 else 'Minimal'})
• PCL-5 PTSD Scale: {veteran['PCL-5 Score']}/80 (Clinical Significance: {'Likely PTSD' if veteran['PCL-5 Score'] >= 50 else 'Probable PTSD' if veteran['PCL-5 Score'] >= 32 else 'Subclinical'})

PSYCHOSOCIAL DETERMINANTS:
• Housing Stability: {veteran['Housing Status']}
• Social Support Network: {veteran['Social Support']}
• Substance Use Risk Level: {veteran['Substance Use Risk']}
• Emergency Contact Availability: {veteran['Emergency Contact']}
• Transportation Access: {veteran['Transportation']}
• Mental Health Treatment History: {veteran['Previous Mental Health Treatment']}

TREATMENT PREFERENCES & READINESS:
• Preferred Treatment Modality: {veteran['Treatment Preference']}
• Current Clinical Assignment: {veteran['Assigned Clinician']}
• Last Clinical Contact: {veteran['Last Contact']}

Provide a comprehensive clinical assessment (250-300 words) including:

1. **Clinical Formulation**: Integrate presenting concerns with risk factors and strengths
2. **Differential Considerations**: Primary diagnoses to consider based on symptom profile
3. **Evidence-Based Treatment Recommendations**: Specific interventions aligned with veteran preferences
4. **Safety Planning**: Immediate risk mitigation strategies if applicable
5. **Care Coordination**: Recommended frequency and modality of follow-up
6. **Prognostic Factors**: Protective and risk factors influencing treatment outcomes

Write in professional clinical language suitable for treatment planning and case consultation.
            """
        
        return call_gemini_api(prompt, "gemini-1.5-flash")
        
    except Exception as e:
        return f"Error generating AI summary: {str(e)}"

def ask_ai_question(question, data_context):
    """Enhanced AI questioning with better prompts"""
    try:
        prompt = f"""
You are a senior clinical consultant and veteran mental health expert providing guidance to clinical staff. A colleague has asked you the following question about the current patient population.

CLINICAL QUESTION: {question}

CURRENT PATIENT POPULATION DATA:
{data_context}

Please provide a professional, evidence-based response that:
1. Directly addresses the clinical question with specific recommendations
2. References relevant patient data and clinical indicators where appropriate
3. Includes actionable next steps for clinical staff
4. Cites evidence-based practices when applicable
5. Considers VA-specific guidelines and best practices for veteran care

Respond in clear, professional language appropriate for clinical decision-making. Keep response focused and practical (150-200 words).
        """
        
        return call_gemini_api(prompt, "gemini-1.5-flash")
        
    except Exception as e:
        return f"Error processing question: {str(e)}"

# --- Enhanced Synthetic Data Generation ---
@st.cache_data
def generate_synthetic_data(num_records=100):
    """Generate realistic synthetic veteran mental health data"""
    random.seed(42)
    np.random.seed(42)
    
    data = []
    c_ssrs_options = [
        'Negative', 'Positive - Passive Ideation', 'Positive - Active Ideation', 'Positive - Recent Behavior'
    ]
    
    # Separate male and female names for accurate gender matching
    male_first_names = ['James', 'Michael', 'Robert', 'John', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Christopher',
                        'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth',
                        'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Jason', 'Edward', 'Jeffrey', 'Ryan', 'Jacob',
                        'Nicholas', 'Eric', 'Jonathan', 'Stephen', 'Larry', 'Justin', 'Scott', 'Brandon', 'Benjamin', 'Samuel']
    
    female_first_names = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen',
                          'Lisa', 'Nancy', 'Betty', 'Helen', 'Sandra', 'Donna', 'Carol', 'Ruth', 'Sharon', 'Michelle',
                          'Laura', 'Kimberly', 'Deborah', 'Dorothy', 'Amy', 'Angela', 'Ashley', 'Brenda', 'Emma', 'Olivia',
                          'Cynthia', 'Marie', 'Janet', 'Catherine', 'Frances', 'Christine', 'Samantha', 'Debra', 'Rachel', 'Carolyn']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez',
                  'Lee', 'Gonzalez', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young',
                  'Allen', 'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill']
    
    # Pre-generate ages with median of 50
    ages = []
    for _ in range(num_records):
        # Use normal distribution centered at 50 with appropriate spread
        age = int(np.random.normal(50, 12))  # Standard deviation of 12 gives good spread
        # Clamp to realistic veteran age range
        age = max(22, min(80, age))
        ages.append(age)
    
    # Sort ages to ensure median is close to 50
    ages.sort()
    # Adjust if needed to ensure median is exactly 50
    mid_point = len(ages) // 2
    if len(ages) % 2 == 0:
        current_median = (ages[mid_point - 1] + ages[mid_point]) / 2
        adjustment = 50 - current_median
        for i in range(len(ages)):
            ages[i] = max(22, min(80, int(ages[i] + adjustment)))
    else:
        ages[mid_point] = 50
    
    # Shuffle ages to randomize assignment
    random.shuffle(ages)
    
    for i in range(num_records):
        # Generate gender first (85% male, 15% female based on VA demographics)
        gender = random.choices(["Male", "Female"], weights=[0.85, 0.15], k=1)[0]
        
        # Choose appropriate first name based on gender - THIS IS THE KEY FIX
        if gender == "Male":
            first_name = random.choice(male_first_names)
        else:  # gender == "Female"
            first_name = random.choice(female_first_names)
        
        # Generate last name
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        # Use pre-generated age with median 50
        age = ages[i]
        current_year = 2025
        birth_year = current_year - age
        
        # Determine service era based on realistic age and service periods
        if age >= 70:  # Born 1955 or earlier
            service_era = "Vietnam"
        elif age >= 55:  # Born 1956-1970
            service_era = random.choices(["Vietnam", "Gulf War"], weights=[0.3, 0.7], k=1)[0]
        elif age >= 40:  # Born 1971-1985
            service_era = random.choices(["Gulf War", "OEF/OIF"], weights=[0.4, 0.6], k=1)[0]
        elif age >= 30:  # Born 1986-1995
            service_era = "OEF/OIF"
        else:  # Born 1996+
            service_era = random.choices(["OEF/OIF", "Recent"], weights=[0.7, 0.3], k=1)[0]
        
        # Generate realistic branch distribution
        branch = random.choices(
            ["Army", "Navy", "Air Force", "Marines", "Coast Guard"], 
            weights=[0.36, 0.26, 0.24, 0.13, 0.01], k=1
        )[0]
        
        # Generate clinical scores with realistic correlations
        c_ssrs_status = random.choices(c_ssrs_options, weights=[0.78, 0.14, 0.06, 0.02], k=1)[0]
        phq9_q9_suicide = "No"
        
        if c_ssrs_status == 'Positive - Recent Behavior':
            phq9_score = random.randint(18, 27)
            gad7_score = random.randint(14, 21)
            pcl5_score = random.randint(55, 80)
            phq9_q9_suicide = "Yes"
        elif c_ssrs_status == 'Positive - Active Ideation':
            phq9_score = random.randint(14, 24)
            gad7_score = random.randint(11, 20)
            pcl5_score = random.randint(45, 70)
            phq9_q9_suicide = "Yes"
        elif c_ssrs_status == 'Positive - Passive Ideation':
            phq9_score = random.randint(8, 20)
            gad7_score = random.randint(6, 16)
            pcl5_score = random.randint(25, 55)
            phq9_q9_suicide = random.choices(["Yes", "No"], weights=[0.4, 0.6], k=1)[0]
        else:
            phq9_score = random.randint(0, 16)
            gad7_score = random.randint(0, 12)
            pcl5_score = random.randint(0, 45)
            if phq9_score > 12:
                phq9_q9_suicide = random.choices(["Yes", "No"], weights=[0.1, 0.9], k=1)[0]

        # Generate realistic intake date (last 30 days) - DATE ONLY, NO TIME
        days_ago = random.randint(0, 30)
        intake_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Generate realistic last contact (within last 7 days) - DATE ONLY, NO TIME
        contact_days_ago = random.randint(0, 7)
        last_contact = (datetime.now() - timedelta(days=contact_days_ago)).strftime("%Y-%m-%d")

        record = {
            "Veteran ID": f"VET-{1000 + i:04d}",
            "Name": full_name,  # Use the properly constructed name
            "Intake Date": intake_date,  # This will be date only
            "Age": age,
            "Gender": gender,
            "Branch": branch,
            "Service Era": service_era,
            "C-SSRS Screen": c_ssrs_status,
            "PHQ-9 Q9 (Self-Harm)": phq9_q9_suicide,
            "PHQ-9 Score": phq9_score,
            "GAD-7 Score": gad7_score,
            "PCL-5 Score": pcl5_score,
            "Social Support": random.choices(["Low", "Medium", "High"], weights=[0.3, 0.5, 0.2], k=1)[0],
            "Substance Use Risk": random.choices(["Low", "Medium", "High"], weights=[0.5, 0.35, 0.15], k=1)[0],
            "Housing Status": random.choices(["Stable", "At Risk", "Homeless"], weights=[0.75, 0.18, 0.07], k=1)[0],
            "Previous Mental Health Treatment": random.choices(["Yes", "No"], weights=[0.65, 0.35], k=1)[0],
            "Treatment Preference": random.choices(["Therapy", "Medication", "Both"], weights=[0.35, 0.25, 0.4], k=1)[0],
            "Last Contact": last_contact,  # This will be date only
            "Assigned Clinician": random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis", "Unassigned"]),
            "Priority Notes": random.choice(["", "Family concerns", "Recent hospitalization", "Employment issues", 
                                           "Financial stress", "Medication compliance", "Transportation barriers", ""]),
            "Contact Method": random.choice(["Phone", "Email", "Video Call", "In-Person"]),
            "Emergency Contact": random.choices(["Available", "Limited", "None"], weights=[0.7, 0.2, 0.1], k=1)[0],
            "Transportation": random.choices(["Own Vehicle", "Public Transit", "VA Transport", "Family/Friends", "None"], 
                                           weights=[0.6, 0.15, 0.1, 0.1, 0.05], k=1)[0],
        }
        data.append(record)
        
    return pd.DataFrame(data)

# --- VA-Compliant Risk Scoring Logic ---
def calculate_va_category_and_risk(row):
    """Calculate VA Category and Risk Score based on official VA guidelines"""
    
    # EMERGENT: Imminent risk of suicide or harm to self or others
    if (row["C-SSRS Screen"] == 'Positive - Recent Behavior' or 
        (row["C-SSRS Screen"] == 'Positive - Active Ideation' and row["PHQ-9 Q9 (Self-Harm)"] == "Yes")):
        return "Emergent", 6, "EMERGENT - Imminent risk of suicide or harm. Requires immediate crisis response."
    
    # URGENT: Same day evaluation or care needed
    if (row["C-SSRS Screen"] in ['Positive - Active Ideation', 'Positive - Passive Ideation'] or
        row["PHQ-9 Q9 (Self-Harm)"] == "Yes" or
        row["PHQ-9 Score"] >= 20 or 
        row["GAD-7 Score"] >= 15 or 
        row["PCL-5 Score"] >= 55):
        return "Urgent", 4, "URGENT - Same day mental health evaluation required."
    
    # ROUTINE: Needs timely care but not at imminent risk
    return "Routine", 2, "ROUTINE - Timely mental health care needed, but not at imminent risk."

def calculate_detailed_risk_score(row):
    """Calculate detailed risk score for internal prioritization"""
    score = 0
    explanation = []

    if row["C-SSRS Screen"] == 'Positive - Recent Behavior':
        return 6, "Critical - Behavior", "C-SSRS Positive: Recent suicidal behavior reported. REQUIRES IMMEDIATE INTERVENTION."
    if row["C-SSRS Screen"] == 'Positive - Active Ideation':
        return 5, "Critical - Ideation", "C-SSRS Positive: Active suicidal ideation with plan/intent. Requires urgent evaluation."
    
    if row["PHQ-9 Q9 (Self-Harm)"] == "Yes":
        score = 4
        explanation.append("PHQ-9 Q9 Positive (Self-Harm)")
    
    if row["PHQ-9 Score"] >= 20 or row["GAD-7 Score"] >= 15 or row["PCL-5 Score"] >= 55:
        if score < 3:
            score = 3
            explanation.append("High symptom severity on standard screeners")

    if (15 <= row["PHQ-9 Score"] < 20) or (10 <= row["GAD-7 Score"] < 15):
        if score < 2:
            score = 2
            explanation.append("Moderate symptom severity")

    if score <= 2:
        compounding_factors = 0
        compounding_details = []
        if row["Social Support"] == "Low": 
            compounding_factors += 1
            compounding_details.append("Low Social Support")
        if row["Substance Use Risk"] == "High": 
            compounding_factors += 1
            compounding_details.append("High Substance Use Risk")
        if row["Housing Status"] == "Homeless":
            compounding_factors += 1
            compounding_details.append("Homeless")
        
        if compounding_factors >= 1:
            score = max(score, 2)
            explanation.append(f"Compounding factors: {', '.join(compounding_details)}")

    if score == 0:
        score = 1
        explanation.append("Low to minimal symptoms reported")

    risk_levels = {
        6: "Critical - Behavior", 5: "Critical - Ideation", 4: "High - Self-Harm Flag",
        3: "High - Symptom Severity", 2: "Medium", 1: "Low"
    }
    return score, risk_levels[score], ". ".join(explanation) + "."

# --- Button Response Functions ---
def handle_button_click(button_type, veteran_id=None, context=""):
    """Handle various button clicks with appropriate responses"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    responses = {
        "review": f"📋 Review initiated for {veteran_id or 'selected veteran'} at {timestamp}. Opening clinical assessment interface.",
        "contact": f"📞 Contact preparation for {veteran_id or 'selected veteran'}. Gathering contact information and communication preferences.",
        "crisis": f"🚨 CRISIS INTERVENTION activated for {veteran_id or 'selected veteran'} at {timestamp}. Emergency protocols initiated.",
        "schedule": f"📅 Scheduling appointment for {veteran_id or 'selected veteran'}. Checking clinician availability for urgent placement.",
        "update_assessment": f"📝 Assessment update form opened. Ready to input new clinical data and observations.",
        "prep_contact": f"📞 Contact information prepared. Phone: Primary contact method. Email: Secondary. Last successful contact: Recent.",
        "schedule_appt": f"📅 Appointment scheduling system accessed. Available slots identified based on urgency level.",
        "generate_referral": f"📧 Referral documentation generated. Specialist recommendations based on assessment scores."
    }
    
    response = responses.get(button_type, f"✅ Action '{button_type}' completed successfully at {timestamp}.")
    
    if 'button_responses' not in st.session_state:
        st.session_state.button_responses = {}
    
    key = f"{button_type}_{veteran_id}_{timestamp}"
    st.session_state.button_responses[key] = response
    
    return response

# --- Enhanced Calendar Functions ---
def create_calendar_view(appointments, year, month):
    """Create an improved calendar view for appointments with better text handling"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    st.subheader(f"📅 Appointment Calendar - {month_name} {year}")
    
    # Calendar navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀ Previous", key="prev_month"):
            if month == 1:
                st.session_state.calendar_view = datetime(year - 1, 12, 1)
            else:
                st.session_state.calendar_view = datetime(year, month - 1, 1)
            st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; font-weight: 600;'>{month_name} {year}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ▶", key="next_month"):
            if month == 12:
                st.session_state.calendar_view = datetime(year + 1, 1, 1)
            else:
                st.session_state.calendar_view = datetime(year, month + 1, 1)
            st.rerun()
    
    # Calendar header with weekend colors
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            # Color weekends (Sat, Sun) in red
            if day in ['Sat', 'Sun']:
                color = '#dc2626'  # Red color for weekends
            else:
                color = COLORS['neutral_charcoal']  # Normal color for weekdays
                
            st.markdown(f"<div style='text-align: center; font-weight: 600; padding: 0.5rem; border-bottom: 2px solid {COLORS['neutral_light_gray']}; color: {color};'>{day}</div>", unsafe_allow_html=True)
    
    # Calendar body
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    # Empty day - no content
                    st.markdown('<div style="height: 90px;"></div>', unsafe_allow_html=True)
                else:
                    date_obj = datetime(year, month, day).date()
                    weekday = date_obj.weekday()  # Monday = 0, Sunday = 6
                    
                    # Check if it's weekend (Saturday = 5, Sunday = 6)
                    is_weekend = weekday in [5, 6]
                    
                    if is_weekend:
                        # Weekend - no appointments, different styling
                        day_html = f"""
                        <div class="calendar-day" style="background-color: #f8f9fa; border-color: #dc2626; min-height: 90px; max-height: 90px;">
                            <div class="calendar-day-number" style="color: #dc2626;">{day}</div>
                            <div class="calendar-appointment-info" style="color: #6b7280; font-size: 0.6rem;">No Appointments</div>
                        </div>
                        """
                        st.markdown(day_html, unsafe_allow_html=True)
                    else:
                        # Weekday - normal appointment logic
                        day_appointments = [apt for apt in appointments if apt['date'] == date_obj]
                        
                        # Count appointments by status
                        available_count = len([apt for apt in day_appointments if apt['status'] == 'available'])
                        reserved_count = len([apt for apt in day_appointments if apt['status'] == 'reserved'])
                        cancelled_count = len([apt for apt in day_appointments if apt['status'] == 'cancelled'])
                        
                        # Count by mode
                        face_to_face_count = len([apt for apt in day_appointments if apt['mode'] == 'Face-to-Face'])
                        video_count = len([apt for apt in day_appointments if apt['mode'] == 'Video Call'])
                        
                        # Check if there are any appointments at all
                        total_appointments = available_count + reserved_count + cancelled_count
                        
                        if total_appointments == 0:
                            # No appointments - show clean empty day
                            day_html = f"""
                            <div class="calendar-day" style="min-height: 90px; max-height: 90px;">
                                <div class="calendar-day-number">{day}</div>
                            </div>
                            """
                            st.markdown(day_html, unsafe_allow_html=True)
                        else:
                            # Has appointments - show with appointment info
                            # Determine day style based on HIGHEST COUNT
                            day_classes = ["calendar-day"]
                            
                            # Find which appointment type has the highest count
                            max_count = max(reserved_count, available_count, cancelled_count)
                            
                            if reserved_count == max_count:
                                day_classes.append("appointment-reserved")
                            elif available_count == max_count:
                                day_classes.append("appointment-available")
                            elif cancelled_count == max_count:
                                day_classes.append("appointment-cancelled")
                            
                            # Build appointment info with better formatting
                            appointment_lines = []
                            
                            # Status lines (prioritize most important)
                            if reserved_count > 0:
                                appointment_lines.append(f'<div class="calendar-appointment-line" style="color: #2563eb;">🔵 {reserved_count}</div>')
                            if available_count > 0:
                                appointment_lines.append(f'<div class="calendar-appointment-line" style="color: #16a34a;">🟢 {available_count}</div>')
                            if cancelled_count > 0:
                                appointment_lines.append(f'<div class="calendar-appointment-line" style="color: #dc2626;">🔴 {cancelled_count}</div>')
                            
                            # Mode lines (only if there are appointments)
                            if face_to_face_count > 0:
                                appointment_lines.append(f'<div class="calendar-appointment-line" style="color: #8b5cf6;">🏥 {face_to_face_count}</div>')
                            if video_count > 0:
                                appointment_lines.append(f'<div class="calendar-appointment-line" style="color: #06b6d4;">💻 {video_count}</div>')
                            
                            # Limit to max 4 lines to prevent overflow
                            if len(appointment_lines) > 4:
                                appointment_lines = appointment_lines[:3]
                                appointment_lines.append('<div class="calendar-appointment-line" style="color: #6b7280;">...</div>')
                            
                            appointment_info = ''.join(appointment_lines)
                            
                            day_html = f"""
                            <div class="{' '.join(day_classes)}" style="min-height: 90px; max-height: 90px;">
                                <div class="calendar-day-number">{day}</div>
                                <div class="calendar-appointment-info">
                                    {appointment_info}
                                </div>
                            </div>
                            """
                            st.markdown(day_html, unsafe_allow_html=True)
                            
                            # Day details button only for weekdays with appointments
                            if st.button(f"View", key=f"view_day_{day}", help=f"View appointments for {month_name} {day}"):
                                st.session_state.selected_calendar_day = day
    
    # Show selected day details
    if st.session_state.selected_calendar_day:
        selected_day = st.session_state.selected_calendar_day
        date_obj = datetime(year, month, selected_day).date()
        day_appointments = [apt for apt in appointments if apt['date'] == date_obj]
        
        if day_appointments:
            st.markdown(f"""
            <div class="appointment-details">
                <h4>📅 Appointments for {month_name} {selected_day}, {year}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for apt in sorted(day_appointments, key=lambda x: x['time']):
                status_colors = {"available": "#16a34a", "reserved": "#2563eb", "cancelled": "#dc2626"}
                status_icons = {"available": "🟢", "reserved": "🔵", "cancelled": "🔴"}
                mode_icons = {"Face-to-Face": "🏥", "Video Call": "💻"}
                
                time_str = apt['time'].strftime("%H:%M")
                end_hour = int(time_str.split(':')[0]) + 1
                time_range = f"{time_str}-{end_hour:02d}:00"
                
                color = status_colors[apt['status']]
                icon = status_icons[apt['status']]
                mode_icon = mode_icons[apt['mode']]
                
                if apt['status'] == 'reserved':
                    st.markdown(f"""
                    <div style="background: rgba(37, 99, 235, 0.1); border-left: 4px solid {color}; padding: 0.5rem; margin: 0.25rem 0; border-radius: 4px;">
                        {icon} <strong>{time_range}</strong> - {apt['veteran_id']} with {apt['clinician']} ({apt['type']}) {mode_icon} {apt['mode']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding: 0.5rem; margin: 0.25rem 0; border-radius: 4px;">
                        {icon} <strong>{time_range}</strong> - {apt['status'].title()} slot {mode_icon} {apt['mode']}
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("Close Details", key="close_day_details"):
                st.session_state.selected_calendar_day = None
                st.rerun()
                
# --- Enhanced Visualization Functions ---
def create_va_category_chart(df):
    """Create VA Category distribution chart"""
    category_counts = df['VA Category'].value_counts()
    
    color_map = {
        'Emergent': '#dc2626',
        'Urgent': '#f59e0b', 
        'Routine': '#77dd77'
    }
    
    fig = px.bar(
        x=category_counts.index, 
        y=category_counts.values,
        color=category_counts.index,
        color_discrete_map=color_map,
        title="VA Triage Category Distribution",
        labels={'x': 'VA Category', 'y': 'Number of Veterans'}
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        title={
            'text': "VA Triage Category Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': "Inter", 'color': COLORS['neutral_charcoal']}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis={
            'title': {'text': 'VA Category', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        yaxis={
            'title': {'text': 'Number of Veterans', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        margin=dict(t=60, b=60, l=60, r=20)
    )
    return fig

def create_treatment_preference_chart(df):
    """Create treatment preference distribution chart"""
    treatment_counts = df['Treatment Preference'].value_counts()
    
    color_map = {
        'Therapy': COLORS['primary_teal'],
        'Medication': COLORS['primary_blue'],
        'Both': COLORS['accent_coral']
    }
    
    fig = px.pie(
        values=treatment_counts.values,
        names=treatment_counts.index,
        title="Treatment Preference Distribution",
        color_discrete_map=color_map
    )
    
    fig.update_layout(
        height=400,
        title={
            'text': "Treatment Preference Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': "Inter", 'color': COLORS['neutral_charcoal']}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'size': 12, 'color': COLORS['neutral_charcoal']},
        legend={
            'orientation': 'v',
            'yanchor': 'middle',
            'y': 0.5,
            'xanchor': 'left',
            'x': 1.05,
            'font': {'size': 11}
        },
        margin=dict(t=60, b=20, l=20, r=120)
    )
    return fig

def create_intake_timeline(df):
    """Create intake timeline chart"""
    df['Intake Date'] = pd.to_datetime(df['Intake Date'])
    daily_intakes = df.groupby(df['Intake Date'].dt.date).size().reset_index()
    daily_intakes.columns = ['Date', 'Count']
    
    fig = px.line(
        daily_intakes, 
        x='Date', 
        y='Count',
        title='Daily Intake Volume (Last 30 Days)',
        markers=True
    )
    fig.update_traces(
        line_color=COLORS['primary_teal'], 
        marker_color=COLORS['primary_teal'],
        line_width=3,
        marker_size=8
    )
    fig.update_layout(
        height=400,
        title={
            'text': "Daily Intake Volume (Last 30 Days)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': "Inter", 'color': COLORS['neutral_charcoal']}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis={
            'title': {'text': 'Date', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        yaxis={
            'title': {'text': 'Count', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        margin=dict(t=60, b=60, l=60, r=20)
    )
    return fig

# --- Enhanced UI Styling Functions ---
def style_veterans_table(df):
    """Style the veterans table based on VA categories"""
    def highlight_row(row):
        category = row['VA Category']
        if category == 'Emergent':
            return ['background-color: rgba(220, 38, 38, 0.1); color: #7f1d1d'] * len(row)
        elif category == 'Urgent':
            return ['background-color: rgba(245, 158, 11, 0.1); color: #78350f'] * len(row)
        elif category == 'Routine':
            return ['background-color: rgba(119, 221, 119, 0.1); color: #166534'] * len(row)
        else:
            return [''] * len(row)
    return df.style.apply(highlight_row, axis=1)

# --- Reset Filters Function ---
def reset_all_filters():
    """Reset all filter states"""
    filter_keys = [
        'c_ssrs_filter', 'va_category_filter', 'risk_level_filter', 'gender_filter', 'branch_filter',
        'clinician_filter', 'phq9_slider', 'gad7_slider', 'pcl5_slider', 'treatment_preference_filter',
        'age_slider', 'date_filter', 'housing_filter', 'substance_filter',
        'social_support_filter', 'contact_method_filter'
    ]
    
    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.filter_reset_counter += 1
    st.session_state.reset_filters = True

# --- Export Functions ---
def export_data_with_summary(df_filtered, summary_text):
    """Export data with AI summary"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    report = f"""
TRIAGEVIEW VETERAN MENTAL HEALTH REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===========================================

AI CLINICAL SUMMARY:
{summary_text}

VA CATEGORY STATISTICS:
- Total Veterans: {len(df_filtered)}
- Emergent (Imminent Risk): {len(df_filtered[df_filtered['VA Category'] == 'Emergent'])}
- Urgent (Same Day Eval): {len(df_filtered[df_filtered['VA Category'] == 'Urgent'])}
- Routine (Timely Care): {len(df_filtered[df_filtered['VA Category'] == 'Routine'])}

TREATMENT PREFERENCES:
- Therapy Only: {len(df_filtered[df_filtered['Treatment Preference'] == 'Therapy'])}
- Medication Only: {len(df_filtered[df_filtered['Treatment Preference'] == 'Medication'])}
- Both Therapy & Medication: {len(df_filtered[df_filtered['Treatment Preference'] == 'Both'])}

===========================================
DETAILED DATA FOLLOWS BELOW:

"""
    
    csv_data = df_filtered.to_csv(index=False)
    return report + "\n" + csv_data

# --- Main Application ---
def main():
    initialize_session_state()
    load_enhanced_css()
    
    # Generate consistent dataset
    df = generate_synthetic_data()
    
    # Apply VA category and risk scoring
    va_info = df.apply(calculate_va_category_and_risk, axis=1, result_type='expand')
    df[['VA Category', 'VA Risk Score', 'VA Explanation']] = va_info
    
    risk_info = df.apply(calculate_detailed_risk_score, axis=1, result_type='expand')
    df[['Risk Score', 'Risk Level', 'Risk Explanation']] = risk_info
    
    # Sort by VA Category priority, then by Risk Score
    category_order = {'Emergent': 3, 'Urgent': 2, 'Routine': 1}
    df['Category Order'] = df['VA Category'].map(category_order)
    df = df.sort_values(by=['Category Order', 'Risk Score'], ascending=[False, False]).reset_index(drop=True)
    df = df.drop('Category Order', axis=1)

    # --- Header ---
    st.title("🏥 TriageView: Veteran Mental Health Dashboard")
    st.markdown("*Advanced AI-powered clinical decision support for veteran mental health triage*")

    # Enhanced alert for emergent cases
    emergent_cases = len(df[df['VA Category'] == 'Emergent'])
    urgent_cases = len(df[df['VA Category'] == 'Urgent'])
    
    if emergent_cases > 0:
        st.markdown(f"""
        <div class="priority-alert">
        🚨 EMERGENT ALERT: {emergent_cases} veteran(s) at imminent risk require immediate crisis intervention
        </div>
        """, unsafe_allow_html=True)
    elif urgent_cases > 0:
        st.warning(f"⚠️ URGENT: {urgent_cases} veteran(s) require same-day evaluation")

    # --- AI Summary Section ---
    st.header("🤖 AI Clinical Overview")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🧠 Generate AI Summary for All Patients", key="generate_summary", type="primary"):
            with st.spinner("🤖 Generating AI clinical summary for all patients..."):
                summary = generate_ai_summary(df, "all_patients")
                st.session_state.ai_summaries['all_patients'] = summary
                
                if "Error" not in summary and "API Error" not in summary:
                    st.success("✅ AI Summary Generated Successfully")
                else:
                    st.error("❌ AI Summary Generation Failed")
        
        if 'all_patients' in st.session_state.ai_summaries:
            summary_text = st.session_state.ai_summaries['all_patients']
            st.markdown(f"""
            <div class="ai-summary-all-patients">
            <h4>🎯 AI Clinical Insights - All Patients</h4>
            <p>{summary_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💬 Ask AI About All Patients")
        question = st.text_input("Ask clinical question:", placeholder="e.g., What are the main risk factors?")
        if st.button("🤖 Ask AI", key="ask_ai") and question:
            with st.spinner("🤖 Processing question..."):
                emergent_count = len(df[df['VA Category'] == 'Emergent'])
                urgent_count = len(df[df['VA Category'] == 'Urgent'])
                routine_count = len(df[df['VA Category'] == 'Routine'])
                
                context = f"""
                All Patients Overview:
                - Total Veterans: {len(df)}
                - Emergent Cases: {emergent_count}
                - Urgent Cases: {urgent_count}
                - Routine Cases: {routine_count}
                - Average Age: {df['Age'].mean():.1f}
                - Homeless: {len(df[df['Housing Status'] == 'Homeless'])}
                - Low Social Support: {len(df[df['Social Support'] == 'Low'])}
                - High Substance Risk: {len(df[df['Substance Use Risk'] == 'High'])}
                - Average PHQ-9: {df['PHQ-9 Score'].mean():.1f}
                - Average GAD-7: {df['GAD-7 Score'].mean():.1f}
                - Treatment Preferences - Therapy: {len(df[df['Treatment Preference'] == 'Therapy'])}, Medication: {len(df[df['Treatment Preference'] == 'Medication'])}, Both: {len(df[df['Treatment Preference'] == 'Both'])}
                """
                answer = ask_ai_question(question, context)
                
                if "Error" not in answer and "API Error" not in answer:
                    st.success("🤖 AI Response:")
                    st.info(answer)
                else:
                    st.error("❌ AI service unavailable. Please try again.")

    # --- Enhanced Sidebar Filters ---
    st.sidebar.header("🔍 Advanced Filtering")
    
    if st.sidebar.button("🔄 Reset All Filters", key=f"reset_button_{st.session_state.filter_reset_counter}"):
        reset_all_filters()
        st.sidebar.success("✅ Filters Reset!")
        st.rerun()
    
    # Get unique values for filters
    va_categories = sorted(df["VA Category"].unique(), key=lambda x: ['Emergent', 'Urgent', 'Routine'].index(x))
    c_ssrs_unique = sorted(df["C-SSRS Screen"].unique())
    risk_level_unique = sorted(df["Risk Level"].unique(), key=lambda x: (
        0 if "Critical" in x else 1 if "High" in x else 2 if "Medium" in x else 3
    ))
    
    # Default values
    defaults = {
        'va_category': va_categories,
        'c_ssrs': c_ssrs_unique,
        'risk_level': risk_level_unique,
        'gender': sorted(df["Gender"].unique()),
        'branch': sorted(df["Branch"].unique()),
        'clinician': sorted(df["Assigned Clinician"].unique()),
        'treatment_preference': sorted(df["Treatment Preference"].unique())
    }
    
    # Enhanced filters
    va_category_filter = st.sidebar.multiselect(
        "VA Triage Category", va_categories, defaults['va_category'],
        key=f"va_category_filter_{st.session_state.filter_reset_counter}",
        help="Official VA triage categories: Emergent (imminent risk), Urgent (same day eval), Routine (timely care)"
    )
    
    c_ssrs_filter = st.sidebar.multiselect(
        "C-SSRS Status", c_ssrs_unique, defaults['c_ssrs'],
        key=f"c_ssrs_filter_{st.session_state.filter_reset_counter}"
    )
    
    risk_level_filter = st.sidebar.multiselect(
        "Risk Level", risk_level_unique, defaults['risk_level'],
        key=f"risk_level_filter_{st.session_state.filter_reset_counter}"
    )
    
    # New Treatment Preference Filter
    treatment_preference_filter = st.sidebar.multiselect(
        "Treatment Preference", sorted(df["Treatment Preference"].unique()), defaults['treatment_preference'],
        key=f"treatment_preference_filter_{st.session_state.filter_reset_counter}",
        help="Filter by veteran's preferred treatment modality"
    )
    
    gender_filter = st.sidebar.multiselect(
        "Gender", sorted(df["Gender"].unique()), defaults['gender'],
        key=f"gender_filter_{st.session_state.filter_reset_counter}"
    )
    
    clinician_filter = st.sidebar.multiselect(
        "Assigned Clinician", sorted(df["Assigned Clinician"].unique()), defaults['clinician'],
        key=f"clinician_filter_{st.session_state.filter_reset_counter}"
    )
    
    # Score sliders
    phq9_slider = st.sidebar.slider(
        "PHQ-9 Depression Score", 0, 27, (0, 27),
        key=f"phq9_slider_{st.session_state.filter_reset_counter}"
    )
    
    gad7_slider = st.sidebar.slider(
        "GAD-7 Anxiety Score", 0, 21, (0, 21),
        key=f"gad7_slider_{st.session_state.filter_reset_counter}"
    )

    # --- Apply Filters ---
    df_filtered = df.copy()
    
    if va_category_filter:
        df_filtered = df_filtered[df_filtered["VA Category"].isin(va_category_filter)]
    if c_ssrs_filter:
        df_filtered = df_filtered[df_filtered["C-SSRS Screen"].isin(c_ssrs_filter)]
    if risk_level_filter:
        df_filtered = df_filtered[df_filtered["Risk Level"].isin(risk_level_filter)]
    if treatment_preference_filter:
        df_filtered = df_filtered[df_filtered["Treatment Preference"].isin(treatment_preference_filter)]
    if gender_filter:
        df_filtered = df_filtered[df_filtered["Gender"].isin(gender_filter)]
    if clinician_filter:
        df_filtered = df_filtered[df_filtered["Assigned Clinician"].isin(clinician_filter)]
    
    df_filtered = df_filtered[
        (df_filtered["PHQ-9 Score"] >= phq9_slider[0]) & 
        (df_filtered["PHQ-9 Score"] <= phq9_slider[1]) &
        (df_filtered["GAD-7 Score"] >= gad7_slider[0]) & 
        (df_filtered["GAD-7 Score"] <= gad7_slider[1])
    ]

    # --- Analytics Overview ---
    st.header("📊 Analytics Overview")
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    with col1:
        if not df_filtered.empty:
            fig1 = create_va_category_chart(df_filtered)
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for VA category chart.")
    
    with col2:
        if not df_filtered.empty:
            fig2 = create_treatment_preference_chart(df_filtered)
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for treatment preference chart.")
    
    with col3:
        if not df_filtered.empty:
            fig3 = create_intake_timeline(df_filtered)
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for intake timeline.")

    # --- Key Metrics Dashboard ---
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")
    
    with col1:
        emergent_count = len(df_filtered[df_filtered['VA Category'] == 'Emergent'])
        st.metric("🚨 Emergent", emergent_count, help="Veterans at imminent risk requiring immediate crisis intervention")
    
    with col2:
        urgent_count = len(df_filtered[df_filtered['VA Category'] == 'Urgent'])
        st.metric("⚠️ Urgent", urgent_count, help="Veterans requiring same-day evaluation or care")
    
    with col3:
        routine_count = len(df_filtered[df_filtered['VA Category'] == 'Routine'])
        st.metric("📋 Routine", routine_count, help="Veterans needing timely care but not at imminent risk")
    
    with col4:
        therapy_count = len(df_filtered[df_filtered['Treatment Preference'] == 'Therapy'])
        st.metric("🗣️ Therapy", therapy_count, help="Veterans preferring therapy-only treatment")
    
    with col5:
        medication_count = len(df_filtered[df_filtered['Treatment Preference'] == 'Medication'])
        st.metric("💊 Medication", medication_count, help="Veterans preferring medication-only treatment")
    
    with col6:
        both_count = len(df_filtered[df_filtered['Treatment Preference'] == 'Both'])
        st.metric("🔄 Both", both_count, help="Veterans preferring both therapy and medication")

    # Additional clinical metrics
    if not df_filtered.empty:
        st.subheader("🔍 Clinical Insights")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            homeless_count = len(df_filtered[df_filtered['Housing Status'] == 'Homeless'])
            homeless_pct = (homeless_count / len(df_filtered)) * 100
            st.metric("🏠 Housing Risk", f"{homeless_count} ({homeless_pct:.1f}%)",
                     help="Veterans experiencing homelessness")
        
        with col2:
            high_substance = len(df_filtered[df_filtered['Substance Use Risk'] == 'High'])
            substance_pct = (high_substance / len(df_filtered)) * 100
            st.metric("🍺 Substance Risk", f"{high_substance} ({substance_pct:.1f}%)",
                     help="Veterans with high substance use risk")
        
        with col3:
            low_support = len(df_filtered[df_filtered['Social Support'] == 'Low'])
            support_pct = (low_support / len(df_filtered)) * 100
            st.metric("👥 Social Risk", f"{low_support} ({support_pct:.1f}%)",
                     help="Veterans with limited social support")
        
        with col4:
            avg_phq9 = df_filtered['PHQ-9 Score'].mean()
            st.metric("📊 Avg PHQ-9", f"{avg_phq9:.1f}",
                     help="Average depression severity score")

    # --- Appointment Calendar ---
    st.header("📅 Appointment Calendar")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_date = st.session_state.calendar_view
        create_calendar_view(st.session_state.appointments, current_date.year, current_date.month)
    
    with col2:
        st.subheader("📊 Calendar Legend")
        st.markdown("""
        <div style="padding: 1rem; background: white; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="margin-bottom: 0.5rem;"><span style="color: #77dd77;">🟢</span> Available slots</div>
        <div style="margin-bottom: 0.5rem;"><span style="color: #5B9BD3;">🔵</span> Reserved appointments</div>
        <div style="margin-bottom: 0.5rem;"><span style="color: #FF7F50;">🔴</span> Cancelled appointments</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📈 Calendar Statistics")
        current_date = st.session_state.calendar_view
        month_appointments = [apt for apt in st.session_state.appointments 
                            if apt['date'].month == current_date.month and apt['date'].year == current_date.year]
        
        available_total = len([apt for apt in month_appointments if apt['status'] == 'available'])
        reserved_total = len([apt for apt in month_appointments if apt['status'] == 'reserved'])
        cancelled_total = len([apt for apt in month_appointments if apt['status'] == 'cancelled'])
        
        st.metric("Available Slots", available_total)
        st.metric("Reserved Appointments", reserved_total)
        st.metric("Cancelled Slots", cancelled_total)

# --- Triage Queue ---
    # Get the display data first to calculate correct count
    show_priority_only = False
    
    # Controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown("*Veterans prioritized by VA categories and AI risk assessment. Click actions for immediate response.*")
    
    with col2:
        show_priority_only = st.checkbox("Emergent/Urgent Only", value=False)
    
    with col3:
        show_all_columns = st.checkbox("All Columns", value=False)
    
    with col4:
        if not df_filtered.empty:
            if st.button("📥 Export Report"):
                summary_text = st.session_state.ai_summaries.get('all_patients', 'AI summary not generated')
                export_data = export_data_with_summary(df_filtered, summary_text)
                st.download_button(
                    label="💾 Download Complete Report",
                    data=export_data,
                    file_name=f"triageview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    # Apply priority filter if selected
    if show_priority_only:
        df_display = df_filtered[df_filtered['VA Category'].isin(['Emergent', 'Urgent'])]
    else:
        df_display = df_filtered
    
    # Updated header with correct count
    st.header(f"🎯 Triage Queue ({len(df_display)} Veterans)")

    # Display dataframe
    if not df_display.empty:
        if show_all_columns:
            display_columns = df_display.columns.tolist()
        else:
            display_columns = [
                'Veteran ID', 'Name', 'VA Category', 'Risk Level', 'Age', 'Gender',
                'C-SSRS Screen', 'PHQ-9 Score', 'GAD-7 Score', 'Treatment Preference',
                'Assigned Clinician', 'Last Contact'
            ]
        
        display_df = df_display[display_columns].copy()
        
        st.dataframe(
            style_veterans_table(display_df),
            use_container_width=True,
            hide_index=True,
        )
        
        # Enhanced quick actions for priority cases
        emergent_in_view = df_display[df_display['VA Category'] == 'Emergent']
        urgent_in_view = df_display[df_display['VA Category'] == 'Urgent']
        
        if not emergent_in_view.empty:
            st.subheader("🚨 Emergent Cases - Immediate Action Required")
            for _, veteran in emergent_in_view.head(5).iterrows():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                with col1:
                    st.markdown(f"**{veteran['Name']}** ({veteran['Veteran ID']}) - {veteran['VA Category']}")
                with col2:
                    if st.button("📋 Review", key=f"review_{veteran['Veteran ID']}", help="Open clinical review"):
                        response = handle_button_click("review", veteran['Veteran ID'])
                        st.success(response)
                with col3:
                    if st.button("📞 Contact", key=f"contact_{veteran['Veteran ID']}", help="Prepare contact info"):
                        response = handle_button_click("contact", veteran['Veteran ID'])
                        st.success(response)
                with col4:
                    if st.button("🏥 Crisis", key=f"crisis_{veteran['Veteran ID']}", help="Activate crisis protocol"):
                        response = handle_button_click("crisis", veteran['Veteran ID'])
                        st.error(response)
                with col5:
                    if st.button("📅 Schedule", key=f"schedule_{veteran['Veteran ID']}", help="Emergency scheduling"):
                        response = handle_button_click("schedule", veteran['Veteran ID'])
                        st.info(response)
        
        if not urgent_in_view.empty:
            st.subheader("⚠️ Urgent Cases - Same Day Evaluation Required")
            for _, veteran in urgent_in_view.head(3).iterrows():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                with col1:
                    st.markdown(f"**{veteran['Name']}** ({veteran['Veteran ID']}) - {veteran['VA Category']}")
                with col2:
                    if st.button("📋 Review", key=f"review_urgent_{veteran['Veteran ID']}", help="Open clinical review"):
                        response = handle_button_click("review", veteran['Veteran ID'])
                        st.success(response)
                with col3:
                    if st.button("📞 Contact", key=f"contact_urgent_{veteran['Veteran ID']}", help="Prepare contact info"):
                        response = handle_button_click("contact", veteran['Veteran ID'])
                        st.success(response)
                with col4:
                    if st.button("⚠️ Urgent", key=f"urgent_{veteran['Veteran ID']}", help="Same-day scheduling"):
                        response = handle_button_click("schedule", veteran['Veteran ID'])
                        st.warning(response)
                with col5:
                    if st.button("📅 Schedule", key=f"schedule_urgent_{veteran['Veteran ID']}", help="Same-day appointment"):
                        response = handle_button_click("schedule", veteran['Veteran ID'])
                        st.info(response)
    else:
        st.warning("⚠️ No veterans match the current criteria. Adjust filters to view data.")

# --- Individual Veteran Analysis ---
    st.header("🔍 Individual Patient Analysis")
    
    if not df_filtered.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            # Create display options with both name and ID
            veteran_options = []
            veteran_lookup = {}
            
            for _, row in df_filtered.iterrows():
                display_name = f"{row['Name']} ({row['Veteran ID']})"
                veteran_options.append(display_name)
                veteran_lookup[display_name] = row['Veteran ID']
            
            selected_display_option = st.selectbox(
                "Select Veteran for Detailed Analysis",
                options=veteran_options,
                key="veteran_detail_selector"
            )
            
            # Get the actual Veteran ID from the selected display option
            selected_vet_id = veteran_lookup[selected_display_option]
        
        with col2:
            if st.button("🤖 Generate AI Assessment", key="individual_ai", type="primary"):
                if selected_vet_id:
                    with st.spinner("🤖 Generating individual patient AI assessment..."):
                        vet_data = df_filtered[df_filtered["Veteran ID"] == selected_vet_id]
                        individual_summary = generate_ai_summary(vet_data, "individual_patient")
                        st.session_state.ai_summaries[selected_vet_id] = individual_summary
                        
                        if "Error" not in individual_summary and "API Error" not in individual_summary:
                            st.success("✅ AI Assessment Generated")
                        else:
                            st.error("❌ AI Assessment Failed")
        
        if selected_vet_id:
            veteran = df_filtered[df_filtered["Veteran ID"] == selected_vet_id].iloc[0]
            
            # AI Q&A Section for Individual Veteran
            st.subheader("💬 Ask AI About This Patient")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                individual_question = st.text_input(
                    f"Ask about {veteran['Name']}:",
                    placeholder="e.g., What treatment approach would you recommend? What are the primary risk factors?",
                    key=f"individual_question_{selected_vet_id}"
                )
            
            with col2:
                ask_individual_button = st.button(
                    "🤖 Ask About Patient", 
                    key=f"ask_individual_{selected_vet_id}",
                    type="secondary"
                )
            
            # Process individual question
            if ask_individual_button and individual_question:
                with st.spinner("🤖 Analyzing patient profile..."):
                    vet_data = df_filtered[df_filtered["Veteran ID"] == selected_vet_id]
                    individual_answer = ask_ai_question(individual_question, f"Individual patient data: {vet_data.iloc[0].to_dict()}")
                    
                    qa_key = f"{selected_vet_id}_qa"
                    if qa_key not in st.session_state:
                        st.session_state[qa_key] = []
                    
                    st.session_state[qa_key].append({
                        "question": individual_question,
                        "answer": individual_answer,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            # Display previous Q&A for this veteran
            qa_key = f"{selected_vet_id}_qa"
            if qa_key in st.session_state and st.session_state[qa_key]:
                st.subheader("📝 Previous Questions & Answers")
                for i, qa in enumerate(reversed(st.session_state[qa_key])):
                    with st.expander(f"Q: {qa['question'][:50]}... ({qa['timestamp']})", expanded=(i==0)):
                        st.markdown(f"**Question:** {qa['question']}")
                        if "Error" not in qa['answer'] and "API Error" not in qa['answer']:
                            st.success("🤖 AI Response:")
                            st.info(qa['answer'])
                        else:
                            st.error("❌ AI service unavailable")
            
            # Display AI assessment if available
            if selected_vet_id in st.session_state.ai_summaries:
                assessment_text = st.session_state.ai_summaries[selected_vet_id]
                if "Error" not in assessment_text and "API Error" not in assessment_text:
                    st.markdown(f"""
                    <div class="ai-summary-individual">
                    <h4>🤖 AI Clinical Assessment for {veteran['Name']}</h4>
                    <p>{assessment_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"AI Assessment Error: {assessment_text}")
            
            # Veteran details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Enhanced VA Category and Risk assessment display
                va_category = veteran['VA Category']
                if va_category == 'Emergent':
                    st.error(f"**🚨 VA Category: {va_category}** - Imminent risk requiring immediate crisis intervention")
                elif va_category == 'Urgent':
                    st.warning(f"**⚠️ VA Category: {va_category}** - Same day evaluation or care required")
                else:
                    st.success(f"**📋 VA Category: {va_category}** - Timely care needed, not at imminent risk")
                
                st.markdown(f"**Risk Level:** {veteran['Risk Level']} (Score: {veteran['Risk Score']})")
                st.markdown("**Clinical Reasoning:**")
                st.markdown(f"> {veteran['Risk Explanation']}")
                
                # Treatment preference display
                treatment_pref = veteran['Treatment Preference']
                if treatment_pref == 'Therapy':
                    st.markdown("**Treatment Preference:** 🗣️ Therapy Only")
                elif treatment_pref == 'Medication':
                    st.markdown("**Treatment Preference:** 💊 Medication Only")
                else:
                    st.markdown("**Treatment Preference:** 🔄 Both Therapy & Medication")
                
                if veteran['Priority Notes']:
                    st.markdown("**Priority Notes:**")
                    st.markdown(f"> {veteran['Priority Notes']}")

            with col2:
                st.markdown("### 👤 Demographics")
                st.markdown(f"**Name:** {veteran['Name']}")
                st.markdown(f"**Age:** {veteran['Age']} | **Gender:** {veteran['Gender']}")
                st.markdown(f"**Branch:** {veteran['Branch']}")
                st.markdown(f"**Service Era:** {veteran['Service Era']}")
                # Clean the intake date display to remove time
                intake_date_clean = str(veteran['Intake Date']).split(' ')[0] if ' ' in str(veteran['Intake Date']) else str(veteran['Intake Date'])
                st.markdown(f"**Intake:** {intake_date_clean}")
                st.markdown(f"**Clinician:** {veteran['Assigned Clinician']}")    

            # Clinical scores with interpretation (without arrows)
            st.markdown("### 📊 Clinical Assessment Scores")
            col1, col2, col3 = st.columns(3)
            
            def get_score_interpretation(score, scale_type):
                if scale_type == "PHQ-9":
                    if score >= 20: return "Severe Depression", "🔴"
                    elif score >= 15: return "Moderately Severe", "🟠"
                    elif score >= 10: return "Moderate Depression", "🟡"
                    elif score >= 5: return "Mild Depression", "🟢"
                    else: return "Minimal Depression", "🟢"
                elif scale_type == "GAD-7":
                    if score >= 15: return "Severe Anxiety", "🔴"
                    elif score >= 10: return "Moderate Anxiety", "🟡"
                    elif score >= 5: return "Mild Anxiety", "🟢"
                    else: return "Minimal Anxiety", "🟢"
                elif scale_type == "PCL-5":
                    if score >= 50: return "Likely PTSD", "🔴"
                    elif score >= 32: return "Probable PTSD", "🟡"
                    else: return "No PTSD Indicated", "🟢"
                return "Unknown", "⚪"
            
            with col1:
                interp, color = get_score_interpretation(veteran['PHQ-9 Score'], "PHQ-9")
                st.metric("PHQ-9 Depression", f"{color} {veteran['PHQ-9 Score']}", 
                         help="Patient Health Questionnaire-9")
                st.markdown(f"<small>{interp}</small>", unsafe_allow_html=True)
            
            with col2:
                interp, color = get_score_interpretation(veteran['GAD-7 Score'], "GAD-7")
                st.metric("GAD-7 Anxiety", f"{color} {veteran['GAD-7 Score']}", 
                         help="Generalized Anxiety Disorder-7")
                st.markdown(f"<small>{interp}</small>", unsafe_allow_html=True)
            
            with col3:
                interp, color = get_score_interpretation(veteran['PCL-5 Score'], "PCL-5")
                st.metric("PCL-5 PTSD", f"{color} {veteran['PCL-5 Score']}", 
                         help="PTSD Checklist for DSM-5")
                st.markdown(f"<small>{interp}</small>", unsafe_allow_html=True)

            # Risk factors matrix
            st.markdown("### ⚠️ Risk Factor Analysis")
            risk_factors = {
                "Suicide Risk (C-SSRS)": veteran['C-SSRS Screen'],
                "Self-Harm Ideation": veteran['PHQ-9 Q9 (Self-Harm)'],
                "Social Support": veteran['Social Support'],
                "Substance Use Risk": veteran['Substance Use Risk'],
                "Housing Stability": veteran['Housing Status'],
                "Emergency Contact": veteran['Emergency Contact'],
                "Transportation Access": veteran['Transportation'],
                "Treatment Preference": veteran['Treatment Preference']
            }
            
            cols = st.columns(4)
            for i, (factor, value) in enumerate(risk_factors.items()):
                with cols[i % 4]:
                    if factor == "Suicide Risk (C-SSRS)":
                        color = "🔴" if value != "Negative" else "🟢"
                    elif factor == "Self-Harm Ideation":
                        color = "🔴" if value == "Yes" else "🟢"
                    elif factor == "Treatment Preference":
                        color = "🔵"  # Neutral for treatment preference
                    elif "Low" in str(value) or "Homeless" in str(value) or "None" in str(value):
                        color = "🔴"
                    elif "Medium" in str(value) or "At Risk" in str(value) or "Limited" in str(value):
                        color = "🟡"
                    else:
                        color = "🟢"
                    
                    st.markdown(f"**{factor}:**<br>{color} {value}", unsafe_allow_html=True)

            # Enhanced clinical actions
            st.markdown("### 🎯 Clinical Actions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📋 Update Assessment", key="update_assessment"):
                    response = handle_button_click("update_assessment", veteran['Veteran ID'])
                    st.success(response)
            
            with col2:
                if st.button("📞 Contact Info", key="prep_contact"):
                    response = handle_button_click("prep_contact", veteran['Veteran ID'])
                    st.info(response)
            
            with col3:
                if st.button("📅 Schedule Appointment", key="schedule_appt"):
                    response = handle_button_click("schedule_appt", veteran['Veteran ID'])
                    urgency = "URGENT" if veteran['VA Category'] in ['Emergent', 'Urgent'] else "ROUTINE"
                    st.success(f"{urgency} appointment scheduling initiated")
            
            with col4:
                if st.button("📧 Generate Referral", key="generate_referral"):
                    response = handle_button_click("generate_referral", veteran['Veteran ID'])
                    st.success(response)

            # Clinical notes interface
            st.markdown("### 📝 Clinical Documentation")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                note_type = st.selectbox(
                    "Documentation Type",
                    ["Progress Note", "Crisis Assessment", "Treatment Plan Update", 
                     "Risk Assessment", "Discharge Planning", "Referral Note"]
                )
                
                clinical_note = st.text_area(
                    "Clinical Note:",
                    placeholder="Enter clinical observations, interventions, and plans...",
                    height=120
                )
            
            with col2:
                st.markdown("**Documentation Guidelines:**")
                st.markdown("- Include objective observations")
                st.markdown("- Note risk factors and protective factors")
                st.markdown("- Document intervention plans")
                st.markdown("- Include follow-up requirements")
                st.markdown("- Consider treatment preferences")
                
                if st.button("💾 Save Documentation"):
                    if clinical_note:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.success(f"{note_type} saved to veteran record at {timestamp}")
                    else:
                        st.warning("Please enter documentation before saving")

            # Enhanced export individual veteran report
            if st.button("📊 Generate Individual Report"):
                qa_history = ""
                qa_key = f"{selected_vet_id}_qa"
                if qa_key in st.session_state and st.session_state[qa_key]:
                    qa_history = "\nAI CONSULTATION HISTORY:\n" + "="*50 + "\n"
                    for qa in st.session_state[qa_key]:
                        qa_history += f"\nQ ({qa['timestamp']}): {qa['question']}\n"
                        qa_history += f"A: {qa['answer']}\n{'-'*30}\n"
                
                individual_report = f"""
INDIVIDUAL VETERAN ASSESSMENT REPORT
===================================
Veteran: {veteran['Name']} ({veteran['Veteran ID']})
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

VA TRIAGE CATEGORY: {veteran['VA Category']}
Risk Level: {veteran['Risk Level']} (Score: {veteran['Risk Score']})
Clinical Reasoning: {veteran['Risk Explanation']}

TREATMENT PREFERENCES: {veteran['Treatment Preference']}

CLINICAL SCORES:
- PHQ-9 (Depression): {veteran['PHQ-9 Score']} - {get_score_interpretation(veteran['PHQ-9 Score'], "PHQ-9")[0]}
- GAD-7 (Anxiety): {veteran['GAD-7 Score']} - {get_score_interpretation(veteran['GAD-7 Score'], "GAD-7")[0]}
- PCL-5 (PTSD): {veteran['PCL-5 Score']} - {get_score_interpretation(veteran['PCL-5 Score'], "PCL-5")[0]}

DEMOGRAPHICS & BACKGROUND:
Age: {veteran['Age']} | Gender: {veteran['Gender']}
Military Branch: {veteran['Branch']} | Service Era: {veteran['Service Era']}
Assigned Clinician: {veteran['Assigned Clinician']}

RISK FACTORS:
{chr(10).join([f"- {k}: {v}" for k, v in risk_factors.items()])}

AI COMPREHENSIVE ASSESSMENT:
{st.session_state.ai_summaries.get(selected_vet_id, 'AI assessment not generated')}
{qa_history}
===================================
Generated by TriageView Clinical Decision Support System
                """
                
                st.download_button(
                    label="📥 Download Complete Individual Report",
                    data=individual_report,
                    file_name=f"veteran_report_{veteran['Veteran ID']}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

    # --- System Information ---
    st.markdown("---")
    st.markdown("### 📊 System Status")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.info(f"**Total Veterans:** {len(df)}")
    with col2:
        st.info(f"**Current View:** {len(df_filtered)}")
    with col3:
        ai_count = len([k for k in st.session_state.ai_summaries.keys() if not st.session_state.ai_summaries[k].startswith("Error")])
        st.info(f"**AI Summaries:** {ai_count}")
    with col4:
        st.info(f"**Calendar Slots:** {len(st.session_state.appointments)}")
    with col5:
        st.info(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

    # Quick add veteran button
    if st.button("➕ Add New Veteran", key="add_veteran"):
        st.info("📋 New veteran intake form will open here (integration with intake system)")

    # API Status Check
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Status")
    if st.sidebar.button("🔧 Test AI Connection"):
        with st.spinner("Testing Gemini AI..."):
            test_response = call_gemini_api("Hello, respond with 'AI connection successful'")
            if "AI connection successful" in test_response:
                st.sidebar.success("✅ AI Connected")
            else:
                st.sidebar.error("❌ AI Connection Failed")
                st.sidebar.error(test_response)

if __name__ == "__main__":
    main()        
