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

# --- Page Configuration ---
st.set_page_config(
    page_title="TriageView - Veteran Mental Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN FUTURISTIC COLOR PALETTE ---
COLORS = {
    "primary_blue": "#3B82F6",        # Modern vibrant blue
    "primary_teal": "#06B6D4",        # Cyan accent
    "secondary_light_sky": "#E0F2FE",
    "secondary_deep_teal": "#0891B2",
    "secondary_sandstone": "#F59E0B",
    "accent_coral": "#EF4444",        # Modern red
    "accent_green": "#10B981",        # Emerald green
    "accent_purple": "#8B5CF6",       # Violet accent
    "neutral_white": "#FFFFFF",
    "neutral_off_white": "#F8FAFC",
    "neutral_light_gray": "#E2E8F0",
    "neutral_medium_gray": "#64748B",
    "neutral_charcoal": "#1E293B",
    "dark_bg": "#0F172A",             # Dark theme
    "glass_bg": "rgba(255, 255, 255, 0.1)",  # Glassmorphism
    "glass_border": "rgba(255, 255, 255, 0.2)"
}

# --- Gemini AI Configuration (Free Tier) ---
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

# --- Custom CSS for Enhanced Styling ---
def load_css():
    st.markdown(f"""
    <style>
        /* Main App Font and Background */
        html, body, [class*="st-"], .main {{
            background-color: {COLORS['neutral_off_white']};
            color: {COLORS['neutral_charcoal']};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Sidebar Styling */
        .st-emotion-cache-16txtl3 {{
            background-color: {COLORS['neutral_white']};
        }}
        
        /* Headers and Titles */
        h1, h2, h3 {{
            color: {COLORS['neutral_charcoal']};
            font-weight: 600;
        }}
        
        /* Chart container styling for centered titles */
        .chart-container {{
            background-color: {COLORS['neutral_white']};
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }}
        
        /* Custom metric styling */
        .metric-card {{
            background-color: {COLORS['neutral_white']};
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid {COLORS['primary_blue']};
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Priority alert styling */
        .priority-alert {{
            background-color: {COLORS['accent_coral']};
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* AI Summary Box */
        .ai-summary-box {{
            background: linear-gradient(135deg, {COLORS['primary_blue']}, {COLORS['primary_teal']});
            color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        /* Action Button Styling */
        .action-button {{
            background-color: {COLORS['primary_blue']};
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            cursor: pointer;
            margin: 0.25rem;
            transition: background-color 0.3s;
        }}
        
        .action-button:hover {{
            background-color: {COLORS['primary_teal']};
        }}
        
        /* Filter reset notification */
        .filter-reset-notification {{
            background-color: {COLORS['accent_green']};
            color: white;
            padding: 0.5rem;
            border-radius: 0.25rem;
            margin: 0.5rem 0;
            text-align: center;
        }}
        
        /* Enhanced table styling */
        .stDataFrame {{
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid {COLORS['neutral_light_gray']};
        }}
        
        /* AI status indicators */
        .ai-status-success {{
            background-color: {COLORS['accent_green']};
            color: white;
            padding: 0.5rem;
            border-radius: 0.25rem;
            margin: 0.5rem 0;
        }}
        
        .ai-status-error {{
            background-color: {COLORS['accent_coral']};
            color: white;
            padding: 0.5rem;
            border-radius: 0.25rem;
            margin: 0.5rem 0;
        }}
        
        /* Chart container improvements - remove white boxes */
        .js-plotly-plot {{
            border-radius: 0.5rem;
            background: transparent !important;
        }}
        
        /* Button styling improvements - clean and professional */
        .stButton > button {{
            border-radius: 0.375rem !important;
            border: none !important;
            background-color: {COLORS['primary_blue']} !important;
            color: white !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            width: 100% !important;
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['primary_teal']} !important;
            transform: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }}
        
        .stButton > button:focus {{
            box-shadow: 0 0 0 3px rgba(91, 155, 211, 0.2) !important;
            outline: none !important;
        }}
        
        .stButton > button:active {{
            background-color: {COLORS['secondary_deep_teal']} !important;
            transform: translateY(1px) !important;
        }}
        
        /* Remove any default button styling */
        .stButton > button * {{
            background: transparent !important;
        }}
        
        /* Specific button color variants */
        .stButton[data-testid*="review"] > button {{
            background-color: {COLORS['primary_blue']} !important;
        }}
        
        .stButton[data-testid*="contact"] > button {{
            background-color: {COLORS['primary_teal']} !important;
        }}
        
        .stButton[data-testid*="crisis"] > button {{
            background-color: {COLORS['accent_coral']} !important;
        }}
        
        .stButton[data-testid*="urgent"] > button {{
            background-color: {COLORS['secondary_sandstone']} !important;
            color: {COLORS['neutral_charcoal']} !important;
        }}
        
        /* Download button styling */
        .stDownloadButton > button {{
            background-color: {COLORS['accent_green']} !important;
            border: none !important;
            color: white !important;
            border-radius: 0.375rem !important;
            font-weight: 500 !important;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: #6bc373 !important;
        }}
        
        /* Primary action buttons */
        .stButton[key*="generate"] > button,
        .stButton[key*="ai"] > button {{
            background-color: {COLORS['accent_coral']} !important;
        }}
        
        .stButton[key*="generate"] > button:hover,
        .stButton[key*="ai"] > button:hover {{
            background-color: #e55a3a !important;
        }}
        
        /* Section headers */
        .section-header {{
            background: linear-gradient(90deg, {COLORS['primary_blue']}, {COLORS['primary_teal']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
            font-size: 1.5rem;
            margin: 1.5rem 0 1rem 0;
        }}
        
        /* Sidebar improvements */
        .css-1d391kg {{
            background: linear-gradient(180deg, {COLORS['neutral_white']}, #f8f9fa);
        }}
        
        /* Selectbox improvements */
        .stSelectbox > div > div {{
            border-radius: 0.375rem;
            border: 1px solid {COLORS['neutral_light_gray']};
            transition: border-color 0.2s ease;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: {COLORS['primary_blue']};
            box-shadow: 0 0 0 3px rgba(91, 155, 211, 0.1);
        }}
        
        /* Text input improvements */
        .stTextInput > div > div > input {{
            border-radius: 0.375rem;
            border: 1px solid {COLORS['neutral_light_gray']};
            transition: all 0.2s ease;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {COLORS['primary_blue']};
            box-shadow: 0 0 0 3px rgba(91, 155, 211, 0.1);
        }}
        
        /* Slider improvements */
        .stSlider > div > div > div > div {{
            background-color: {COLORS['primary_blue']};
        }}
        
        /* Multiselect improvements */
        .stMultiSelect > div > div {{
            border-radius: 0.375rem;
            border: 1px solid {COLORS['neutral_light_gray']};
        }}
        
        /* Loading spinner customization */
        .stSpinner > div {{
            border-top-color: {COLORS['primary_blue']} !important;
        }}
        
        /* Success/error message improvements */
        .stSuccess {{
            background-color: {COLORS['accent_green']};
            color: white;
            border-radius: 0.375rem;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stError {{
            background-color: {COLORS['accent_coral']};
            color: white;
            border-radius: 0.375rem;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stInfo {{
            background-color: {COLORS['primary_blue']};
            color: white;
            border-radius: 0.375rem;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stWarning {{
            background-color: #f39c12;
            color: white;
            border-radius: 0.375rem;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Metric card improvements - remove boxes */
        .metric-card {{
            background: transparent;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {COLORS['primary_blue']};
            margin: 0.5rem 0;
            transition: transform 0.2s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
        }}
        
        /* Custom expander styling */
        .streamlit-expanderHeader {{
            border-radius: 0.375rem;
            background-color: #f8f9fa;
        }}
        
        /* Remove excessive shadows and boxes */
        .element-container {{
            background: transparent !important;
        }}
        
        /* Checkbox styling */
        .stCheckbox > label {{
            font-weight: 500;
            color: {COLORS['neutral_charcoal']};
        }}
        
        /* Download button styling */
        .stDownloadButton > button {{
            background-color: {COLORS['accent_green']};
            border-color: {COLORS['accent_green']};
            color: white;
        }}
        
        .stDownloadButton > button:hover {{
            background-color: #6bc373;
            border-color: #6bc373;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- AI Integration Functions (Fixed for Gemini API) ---
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

def generate_ai_summary(data, summary_type="overview"):
    """Generate AI summary using Gemini API"""
    try:
        if summary_type == "overview":
            critical_cases = len(data[data['Risk Level'].str.contains('Critical', na=False)])
            high_cases = len(data[data['Risk Level'].str.contains('High', na=False)])
            homeless_count = len(data[data['Housing Status'] == 'Homeless'])
            avg_phq9 = data['PHQ-9 Score'].mean()
            avg_gad7 = data['GAD-7 Score'].mean()
            
            prompt = f"""
As a clinical psychologist specializing in veteran mental health, provide a professional clinical summary based on this veteran population data:

POPULATION STATISTICS:
- Total Veterans: {len(data)}
- Critical Risk Cases: {critical_cases}
- High Risk Cases: {high_cases}
- Medium Risk Cases: {len(data[data['Risk Level'] == 'Medium'])}
- Low Risk Cases: {len(data[data['Risk Level'] == 'Low'])}
- Average Age: {data['Age'].mean():.1f} years
- Homeless Veterans: {homeless_count}
- Veterans with Low Social Support: {len(data[data['Social Support'] == 'Low'])}
- High Substance Use Risk: {len(data[data['Substance Use Risk'] == 'High'])}

CLINICAL METRICS:
- Average PHQ-9 Score: {avg_phq9:.1f} (Depression)
- Average GAD-7 Score: {avg_gad7:.1f} (Anxiety)
- Average PCL-5 Score: {data['PCL-5 Score'].mean():.1f} (PTSD)

Please provide:
1. Key clinical insights (2-3 sentences)
2. Primary areas of concern (1-2 sentences)
3. Recommended priority actions (1-2 sentences)

Keep response professional and concise (under 200 words).
            """
        
        elif summary_type == "individual":
            veteran = data.iloc[0]
            prompt = f"""
As a clinical psychologist, provide a comprehensive assessment for this veteran:

VETERAN PROFILE:
- ID: {veteran['Veteran ID']}
- Name: {veteran.get('Name', 'Not provided')}
- Age: {veteran['Age']}, Gender: {veteran['Gender']}
- Military Branch: {veteran['Branch']}, Service Era: {veteran['Service Era']}

RISK ASSESSMENT:
- AI Risk Level: {veteran['Risk Level']} (Score: {veteran['Risk Score']})
- C-SSRS Screen: {veteran['C-SSRS Screen']}
- PHQ-9 Q9 Self-Harm: {veteran['PHQ-9 Q9 (Self-Harm)']}

CLINICAL SCORES:
- PHQ-9 (Depression): {veteran['PHQ-9 Score']}/27
- GAD-7 (Anxiety): {veteran['GAD-7 Score']}/21
- PCL-5 (PTSD): {veteran['PCL-5 Score']}/80

SOCIAL DETERMINANTS:
- Housing Status: {veteran['Housing Status']}
- Social Support: {veteran['Social Support']}
- Substance Use Risk: {veteran['Substance Use Risk']}
- Emergency Contact: {veteran['Emergency Contact']}
- Transportation: {veteran['Transportation']}

CLINICAL NOTES:
- Priority Notes: {veteran.get('Priority Notes', 'None')}
- Assigned Clinician: {veteran['Assigned Clinician']}
- Last Contact: {veteran['Last Contact']}

Please provide:
1. Clinical risk assessment summary
2. Key psychosocial factors
3. Recommended interventions
4. Follow-up priorities

Keep response professional and actionable (under 300 words).
            """
        
        return call_gemini_api(prompt, "gemini-1.5-flash")
        
    except Exception as e:
        return f"Error generating AI summary: {str(e)}"

def ask_ai_question(question, data_context):
    """Ask AI questions about the veteran population data"""
    try:
        prompt = f"""
As a clinical expert in veteran mental health, answer this question based on the provided veteran population data:

QUESTION: {question}

DATA CONTEXT: {data_context}

Please provide a professional, evidence-based response that:
1. Directly addresses the question
2. References relevant clinical data when appropriate
3. Includes actionable insights for clinical staff
4. Maintains professional medical terminology

Keep response concise and practical (under 200 words).
        """
        
        return call_gemini_api(prompt, "gemini-1.5-flash")
        
    except Exception as e:
        return f"Error processing question: {str(e)}"

def ask_ai_individual_question(question, veteran_data):
    """Ask AI questions about a specific veteran"""
    try:
        veteran = veteran_data.iloc[0]
        prompt = f"""
As a clinical psychologist specializing in veteran mental health, answer this question about a specific veteran:

QUESTION: {question}

VETERAN PROFILE:
- ID: {veteran['Veteran ID']}
- Name: {veteran.get('Name', 'Not provided')}
- Age: {veteran['Age']}, Gender: {veteran['Gender']}
- Military Background: {veteran['Branch']}, {veteran['Service Era']}
- Risk Level: {veteran['Risk Level']} (Score: {veteran['Risk Score']})

CLINICAL ASSESSMENTS:
- C-SSRS Screen: {veteran['C-SSRS Screen']}
- PHQ-9 Q9 Self-Harm: {veteran['PHQ-9 Q9 (Self-Harm)']}
- PHQ-9 Depression Score: {veteran['PHQ-9 Score']}/27
- GAD-7 Anxiety Score: {veteran['GAD-7 Score']}/21
- PCL-5 PTSD Score: {veteran['PCL-5 Score']}/80

SOCIAL FACTORS:
- Housing Status: {veteran['Housing Status']}
- Social Support: {veteran['Social Support']}
- Substance Use Risk: {veteran['Substance Use Risk']}
- Emergency Contact: {veteran['Emergency Contact']}
- Transportation: {veteran['Transportation']}
- Previous Mental Health Treatment: {veteran['Previous Mental Health Treatment']}

CLINICAL NOTES:
- Priority Notes: {veteran.get('Priority Notes', 'None')}
- Assigned Clinician: {veteran['Assigned Clinician']}
- Last Contact: {veteran['Last Contact']}
- Contact Method: {veteran['Contact Method']}

Please provide a professional, clinical response that:
1. Directly addresses the question about this specific veteran
2. References relevant assessment scores and risk factors
3. Considers the veteran's unique circumstances
4. Provides actionable clinical recommendations when appropriate
5. Uses professional medical terminology

Keep response focused and practical (under 250 words).
        """
        
        return call_gemini_api(prompt, "gemini-1.5-flash")
        
    except Exception as e:
        return f"Error processing individual question: {str(e)}"

# --- Enhanced Synthetic Data Generation ---
@st.cache_data
def generate_synthetic_data(num_records=100):
    """Generate consistent synthetic veteran mental health data"""
    # Fixed seed for consistent dataset
    random.seed(42)
    np.random.seed(42)
    
    data = []
    c_ssrs_options = [
        'Negative', 'Positive - Passive Ideation', 'Positive - Active Ideation', 'Positive - Recent Behavior'
    ]
    
    # Realistic veteran names for more authentic feel
    first_names = ['James', 'Michael', 'Robert', 'John', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Christopher',
                   'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez']
    
    for i in range(num_records):
        # Generate realistic risk distribution
        c_ssrs_status = random.choices(c_ssrs_options, weights=[0.78, 0.14, 0.06, 0.02], k=1)[0]
        phq9_q9_suicide = "No"
        
        # Create correlated scores based on C-SSRS status
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
        else:  # Negative C-SSRS
            phq9_score = random.randint(0, 16)
            gad7_score = random.randint(0, 12)
            pcl5_score = random.randint(0, 45)
            if phq9_score > 12:
                phq9_q9_suicide = random.choices(["Yes", "No"], weights=[0.1, 0.9], k=1)[0]

        # Generate realistic demographic and clinical data
        age = random.randint(22, 75)
        gender = random.choices(["Male", "Female", "Other"], weights=[0.85, 0.14, 0.01], k=1)[0]
        
        # Realistic service era distribution
        if age > 65:
            service_era = "Vietnam"
        elif age > 50:
            service_era = random.choice(["Vietnam", "Gulf War"])
        elif age > 35:
            service_era = random.choice(["Gulf War", "OEF/OIF"])
        else:
            service_era = random.choice(["OEF/OIF", "Recent"])

        record = {
            "Veteran ID": f"VET-{1000 + i:04d}",
            "Name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "Intake Date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
            "Age": age,
            "Gender": gender,
            "Branch": random.choice(["Army", "Navy", "Air Force", "Marines", "Coast Guard", "Space Force"]),
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
            "Last Contact": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
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

# --- Risk Scoring Logic ---
def calculate_risk_score(row):
    score = 0
    explanation = []

    # Priority 1: C-SSRS Screening
    if row["C-SSRS Screen"] == 'Positive - Recent Behavior':
        return 6, "Critical - Behavior", "C-SSRS Positive: Recent suicidal behavior reported. REQUIRES IMMEDIATE INTERVENTION."
    if row["C-SSRS Screen"] == 'Positive - Active Ideation':
        return 5, "Critical - Ideation", "C-SSRS Positive: Active suicidal ideation with plan/intent. Requires urgent evaluation."
    
    # Priority 2: PHQ-9 Question 9
    if row["PHQ-9 Q9 (Self-Harm)"] == "Yes":
        score = 4
        explanation.append("PHQ-9 Q9 Positive (Self-Harm)")
    
    # Priority 3: High Symptom Scores
    if row["PHQ-9 Score"] >= 20 or row["GAD-7 Score"] >= 15 or row["PCL-5 Score"] >= 55:
        if score < 3:
            score = 3
            explanation.append("High symptom severity on standard screeners")

    # Priority 4: Moderate Symptoms
    if (15 <= row["PHQ-9 Score"] < 20) or (10 <= row["GAD-7 Score"] < 15):
        if score < 2:
            score = 2
            explanation.append("Moderate symptom severity")

    # Priority 5: Compounding Factors
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

# --- UI Styling Functions ---
def style_risk_levels(df):
    def highlight_row(row):
        level = row['Risk Level']
        if 'Critical' in level:
            color = COLORS['accent_coral']
            text_color = COLORS['neutral_white']
        elif 'High' in level:
            color = COLORS['secondary_sandstone']
            text_color = COLORS['neutral_charcoal']
        elif 'Medium' in level:
            color = COLORS['secondary_light_sky']
            text_color = COLORS['neutral_charcoal']
        else:
            color = 'transparent'
            text_color = COLORS['neutral_charcoal']
        return [f'background-color: {color}; color: {text_color}'] * len(row)
    return df.style.apply(highlight_row, axis=1)

# --- Enhanced Visualization Functions ---
def create_risk_distribution_chart(df):
    risk_counts = df['Risk Level'].value_counts()
    
    color_map = {
        'Critical - Behavior': COLORS['accent_coral'],
        'Critical - Ideation': COLORS['accent_coral'],
        'High - Self-Harm Flag': COLORS['secondary_sandstone'],
        'High - Symptom Severity': COLORS['secondary_sandstone'],
        'Medium': COLORS['primary_blue'],
        'Low': COLORS['accent_green']
    }
    
    fig = px.bar(
        x=risk_counts.index, 
        y=risk_counts.values,
        color=risk_counts.index,
        color_discrete_map=color_map,
        title="Risk Level Distribution",
        labels={'x': 'Risk Level', 'y': 'Number of Veterans'}
    )
    fig.update_layout(
        showlegend=False,
        height=400,
        title={
            'text': "Risk Level Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': "Segoe UI", 'color': COLORS['neutral_charcoal']}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis={
            'title': {'text': 'Risk Level', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickangle': 45,
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        yaxis={
            'title': {'text': 'Number of Veterans', 'font': {'size': 14, 'color': COLORS['neutral_charcoal']}},
            'tickfont': {'size': 12, 'color': COLORS['neutral_charcoal']}
        },
        margin=dict(t=60, b=80, l=60, r=20)
    )
    return fig

def create_intake_timeline(df):
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
            'font': {'size': 18, 'family': "Segoe UI", 'color': COLORS['neutral_charcoal']}
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

def create_clinician_workload_chart(df):
    workload = df['Assigned Clinician'].value_counts()
    
    # Use consistent color palette
    colors = [COLORS['primary_blue'], COLORS['primary_teal'], COLORS['accent_coral'], 
              COLORS['accent_green'], COLORS['secondary_sandstone'], COLORS['neutral_medium_gray']]
    
    fig = px.pie(
        values=workload.values,
        names=workload.index,
        title="Clinician Workload Distribution",
        color_discrete_sequence=colors
    )
    fig.update_layout(
        height=400,
        title={
            'text': "Clinician Workload Distribution",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': "Segoe UI", 'color': COLORS['neutral_charcoal']}
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
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=11,
        marker_line=dict(color='white', width=2)
    )
    return fig

# --- Export Functions ---
def export_data_with_summary(df_filtered, summary_text):
    """Export data with AI summary"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create summary report
    report = f"""
TRIAGEVIEW VETERAN MENTAL HEALTH REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===========================================

AI CLINICAL SUMMARY:
{summary_text}

STATISTICS:
- Total Veterans: {len(df_filtered)}
- Critical Risk: {len(df_filtered[df_filtered['Risk Level'].str.contains('Critical', na=False)])}
- High Risk: {len(df_filtered[df_filtered['Risk Level'].str.contains('High', na=False)])}
- Medium Risk: {len(df_filtered[df_filtered['Risk Level'] == 'Medium'])}
- Low Risk: {len(df_filtered[df_filtered['Risk Level'] == 'Low'])}

===========================================
DETAILED DATA FOLLOWS BELOW:

"""
    
    csv_data = df_filtered.to_csv(index=False)
    return report + "\n" + csv_data

# --- Reset Filters Function ---
def reset_all_filters():
    filter_keys = [
        'c_ssrs_filter', 'risk_level_filter', 'gender_filter', 'branch_filter',
        'clinician_filter', 'phq9_slider', 'gad7_slider', 'pcl5_slider',
        'age_slider', 'date_filter', 'housing_filter', 'substance_filter',
        'social_support_filter', 'contact_method_filter'
    ]
    
    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.filter_reset_counter += 1
    st.session_state.reset_filters = True

# --- Main Application ---
def main():
    initialize_session_state()
    load_css()
    
    # Generate consistent dataset
    df = generate_synthetic_data()
    
    # Apply risk scoring
    risk_info = df.apply(calculate_risk_score, axis=1, result_type='expand')
    df[['Risk Score', 'Risk Level', 'Risk Explanation']] = risk_info
    df = df.sort_values(by="Risk Score", ascending=False).reset_index(drop=True)

    # --- Header ---
    st.title("🏥 TriageView: Veteran Mental Health Dashboard")
    st.markdown("*Advanced AI-powered clinical decision support for veteran mental health triage*")

    # Critical cases alert
    critical_cases = len(df[df['Risk Level'].str.contains('Critical', na=False)])
    if critical_cases > 0:
        st.markdown(f"""
        <div class="priority-alert">
        🚨 PRIORITY ALERT: {critical_cases} veteran(s) require immediate intervention
        </div>
        """, unsafe_allow_html=True)

    # --- AI Summary Section ---
    st.header("🤖 AI Clinical Overview")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🧠 Generate AI Population Summary", key="generate_summary", type="primary"):
            with st.spinner("🤖 Generating AI clinical summary..."):
                summary = generate_ai_summary(df, "overview")
                st.session_state.ai_summaries['overview'] = summary
                
                # Show success/error status
                if "Error" not in summary and "API Error" not in summary:
                    st.markdown("""
                    <div class="ai-status-success">
                    ✅ AI Summary Generated Successfully
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="ai-status-error">
                    ❌ AI Summary Generation Failed
                    </div>
                    """, unsafe_allow_html=True)
        
        if 'overview' in st.session_state.ai_summaries:
            summary_text = st.session_state.ai_summaries['overview']
            st.markdown(f"""
            <div class="ai-summary-box">
            <h4>🎯 AI Clinical Population Insights</h4>
            <p>{summary_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # AI Q&A Section
        st.subheader("💬 Ask AI About Population")
        question = st.text_input("Ask clinical question:", placeholder="e.g., What are the main risk factors?")
        if st.button("🤖 Ask AI", key="ask_ai") and question:
            with st.spinner("🤖 Processing question..."):
                critical_count = len(df[df['Risk Level'].str.contains('Critical', na=False)])
                high_count = len(df[df['Risk Level'].str.contains('High', na=False)])
                context = f"""
                Population Overview:
                - Total Veterans: {len(df)}
                - Critical Risk: {critical_count}
                - High Risk: {high_count}
                - Average Age: {df['Age'].mean():.1f}
                - Homeless: {len(df[df['Housing Status'] == 'Homeless'])}
                - Low Social Support: {len(df[df['Social Support'] == 'Low'])}
                - High Substance Risk: {len(df[df['Substance Use Risk'] == 'High'])}
                - Average PHQ-9: {df['PHQ-9 Score'].mean():.1f}
                - Average GAD-7: {df['GAD-7 Score'].mean():.1f}
                """
                answer = ask_ai_question(question, context)
                
                # Display answer with status indicator
                if "Error" not in answer and "API Error" not in answer:
                    st.success("🤖 AI Response:")
                    st.info(answer)
                else:
                    st.error("❌ AI service unavailable. Please try again.")
                    st.warning(answer)

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Advanced Filtering")
    
    if st.sidebar.button("🔄 Reset All Filters", key=f"reset_button_{st.session_state.filter_reset_counter}"):
        reset_all_filters()
        st.sidebar.success("✅ Filters Reset!")
        st.rerun()
    
    # Get unique values and set defaults
    c_ssrs_unique = sorted(df["C-SSRS Screen"].unique())
    risk_level_unique = sorted(df["Risk Level"].unique(), key=lambda x: (
        0 if "Critical" in x else 1 if "High" in x else 2 if "Medium" in x else 3
    ))
    
    # Default values
    if st.session_state.reset_filters:
        defaults = {
            'c_ssrs': c_ssrs_unique,
            'risk_level': risk_level_unique,
            'gender': sorted(df["Gender"].unique()),
            'branch': sorted(df["Branch"].unique()),
            'clinician': sorted(df["Assigned Clinician"].unique()),
        }
        st.session_state.reset_filters = False
    else:
        defaults = {
            'c_ssrs': c_ssrs_unique,
            'risk_level': risk_level_unique,
            'gender': sorted(df["Gender"].unique()),
            'branch': sorted(df["Branch"].unique()),
            'clinician': sorted(df["Assigned Clinician"].unique()),
        }
    
    # Filters with unique keys
    c_ssrs_filter = st.sidebar.multiselect(
        "C-SSRS Status", c_ssrs_unique, defaults['c_ssrs'],
        key=f"c_ssrs_filter_{st.session_state.filter_reset_counter}"
    )
    
    risk_level_filter = st.sidebar.multiselect(
        "Risk Level", risk_level_unique, defaults['risk_level'],
        key=f"risk_level_filter_{st.session_state.filter_reset_counter}"
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
    
    if c_ssrs_filter:
        df_filtered = df_filtered[df_filtered["C-SSRS Screen"].isin(c_ssrs_filter)]
    if risk_level_filter:
        df_filtered = df_filtered[df_filtered["Risk Level"].isin(risk_level_filter)]
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
    
    # Simple, clean chart layout without unnecessary containers
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    with col1:
        if not df_filtered.empty:
            fig1 = create_risk_distribution_chart(df_filtered)
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for risk distribution chart.")
    
    with col2:
        if not df_filtered.empty:
            fig2 = create_intake_timeline(df_filtered)
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for intake timeline.")
    
    with col3:
        if not df_filtered.empty:
            fig3 = create_clinician_workload_chart(df_filtered)
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for clinician workload.")

    # --- Key Metrics Dashboard ---
    st.header("📈 Key Performance Indicators")
    
    # Clean metrics without excessive styling
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")
    
    with col1:
        critical_count = len(df_filtered[df_filtered['Risk Level'].str.contains('Critical', na=False)])
        st.metric("🚨 Critical", critical_count, help="Veterans requiring immediate intervention")
    
    with col2:
        high_count = len(df_filtered[df_filtered['Risk Level'].str.contains('High', na=False)])
        st.metric("⚠️ High Risk", high_count, help="Veterans requiring urgent attention")
    
    with col3:
        medium_count = len(df_filtered[df_filtered['Risk Level'] == 'Medium'])
        st.metric("🔶 Medium", medium_count, help="Veterans requiring regular monitoring")
    
    with col4:
        low_count = len(df_filtered[df_filtered['Risk Level'] == 'Low'])
        st.metric("🟢 Low Risk", low_count, help="Veterans with minimal risk factors")
    
    with col5:
        unassigned_count = len(df_filtered[df_filtered['Assigned Clinician'] == 'Unassigned'])
        st.metric("👥 Unassigned", unassigned_count, help="Veterans awaiting clinician assignment")
    
    with col6:
        avg_age = df_filtered['Age'].mean() if not df_filtered.empty else 0
        st.metric("👤 Avg Age", f"{avg_age:.1f}", help="Average age of veterans in current view")

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

    # --- Triage Queue ---
    st.header(f"🎯 Triage Queue ({len(df_filtered)} Veterans)")
    
    # Controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown("*Veterans prioritized by AI risk assessment. Click rows for detailed view.*")
    
    with col2:
        show_critical_only = st.checkbox("Critical/High Only", value=False)
    
    with col3:
        show_all_columns = st.checkbox("All Columns", value=False)
    
    with col4:
        # Enhanced export with AI summary
        if not df_filtered.empty:
            if st.button("📥 Export Report"):
                summary_text = st.session_state.ai_summaries.get('overview', 'AI summary not generated')
                export_data = export_data_with_summary(df_filtered, summary_text)
                st.download_button(
                    label="💾 Download Complete Report",
                    data=export_data,
                    file_name=f"triageview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    # Apply critical filter if selected
    if show_critical_only:
        df_display = df_filtered[df_filtered['Risk Level'].str.contains('Critical|High', na=False)]
    else:
        df_display = df_filtered

    # Display dataframe
    if not df_display.empty:
        if show_all_columns:
            display_columns = df_display.columns.tolist()
        else:
            display_columns = [
                'Veteran ID', 'Name', 'Risk Level', 'Risk Score', 'Age', 'Gender',
                'C-SSRS Screen', 'PHQ-9 Score', 'GAD-7 Score', 'Assigned Clinician', 'Last Contact'
            ]
        
        display_df = df_display[display_columns].copy()
        
        st.dataframe(
            style_risk_levels(display_df),
            use_container_width=True,
            hide_index=True,
        )
        
        # Quick actions for critical cases
        critical_in_view = df_display[df_display['Risk Level'].str.contains('Critical', na=False)]
        if not critical_in_view.empty:
            st.subheader("🚨 Immediate Action Required")
            for _, veteran in critical_in_view.head(5).iterrows():  # Show top 5 critical
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{veteran['Name']}** ({veteran['Veteran ID']}) - {veteran['Risk Level']}")
                with col2:
                    st.button("📋 Review", key=f"review_{veteran['Veteran ID']}")
                with col3:
                    st.button("📞 Contact", key=f"contact_{veteran['Veteran ID']}")
                with col4:
                    st.button("🏥 Crisis", key=f"crisis_{veteran['Veteran ID']}")
                with col5:
                    st.button("📅 Schedule", key=f"urgent_{veteran['Veteran ID']}")
    else:
        st.warning("⚠️ No veterans match the current criteria. Adjust filters to view data.")

    # --- Individual Veteran Analysis ---
    st.header("🔍 Individual Veteran Analysis")
    
    if not df_filtered.empty:
        # Veteran selection
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_vet_id = st.selectbox(
                "Select Veteran for Detailed Analysis",
                options=df_filtered["Veteran ID"].unique(),
                key="veteran_detail_selector"
            )
        
        with col2:
            if st.button("🤖 Generate AI Assessment", key="individual_ai", type="primary"):
                if selected_vet_id:
                    with st.spinner("🤖 Generating individual AI assessment..."):
                        vet_data = df_filtered[df_filtered["Veteran ID"] == selected_vet_id]
                        individual_summary = generate_ai_summary(vet_data, "individual")
                        st.session_state.ai_summaries[selected_vet_id] = individual_summary
                        
                        # Show status
                        if "Error" not in individual_summary and "API Error" not in individual_summary:
                            st.success("✅ AI Assessment Generated")
                        else:
                            st.error("❌ AI Assessment Failed")
        
        if selected_vet_id:
            veteran = df_filtered[df_filtered["Veteran ID"] == selected_vet_id].iloc[0]
            
            # AI Q&A Section for Individual Veteran
            st.subheader("💬 Ask AI About This Veteran")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                individual_question = st.text_input(
                    f"Ask about {veteran['Name']}:",
                    placeholder="e.g., What treatment approach would you recommend? What are the primary risk factors?",
                    key=f"individual_question_{selected_vet_id}"
                )
            
            with col2:
                ask_individual_button = st.button(
                    "🤖 Ask About Veteran", 
                    key=f"ask_individual_{selected_vet_id}",
                    type="secondary"
                )
            
            # Process individual question
            if ask_individual_button and individual_question:
                with st.spinner("🤖 Analyzing veteran profile..."):
                    vet_data = df_filtered[df_filtered["Veteran ID"] == selected_vet_id]
                    individual_answer = ask_ai_individual_question(individual_question, vet_data)
                    
                    # Store the Q&A for this veteran
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
                for i, qa in enumerate(reversed(st.session_state[qa_key])):  # Show most recent first
                    with st.expander(f"Q: {qa['question'][:50]}... ({qa['timestamp']})", expanded=(i==0)):
                        st.markdown(f"**Question:** {qa['question']}")
                        if "Error" not in qa['answer'] and "API Error" not in qa['answer']:
                            st.success("🤖 AI Response:")
                            st.info(qa['answer'])
                        else:
                            st.error("❌ AI service unavailable")
                            st.warning(qa['answer'])
            
            # Display AI assessment if available
            if selected_vet_id in st.session_state.ai_summaries:
                assessment_text = st.session_state.ai_summaries[selected_vet_id]
                if "Error" not in assessment_text and "API Error" not in assessment_text:
                    st.markdown(f"""
                    <div class="ai-summary-box">
                    <h4>🤖 AI Clinical Assessment for {veteran['Name']}</h4>
                    <p>{assessment_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"AI Assessment Error: {assessment_text}")
            
            # Veteran details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Risk assessment display
                risk_level = veteran['Risk Level']
                if 'Critical' in risk_level:
                    st.error(f"**🚨 Risk Level: {risk_level} (Score: {veteran['Risk Score']})**")
                elif 'High' in risk_level:
                    st.warning(f"**⚠️ Risk Level: {risk_level} (Score: {veteran['Risk Score']})**")
                elif 'Medium' in risk_level:
                    st.info(f"**🔶 Risk Level: {risk_level} (Score: {veteran['Risk Score']})**")
                else:
                    st.success(f"**🟢 Risk Level: {risk_level} (Score: {veteran['Risk Score']})**")
                
                st.markdown("**Clinical Reasoning:**")
                st.markdown(f"> {veteran['Risk Explanation']}")
                
                if veteran['Priority Notes']:
                    st.markdown("**Priority Notes:**")
                    st.markdown(f"> {veteran['Priority Notes']}")
            
            with col2:
                st.markdown("### 👤 Demographics")
                st.markdown(f"**Name:** {veteran['Name']}")
                st.markdown(f"**Age:** {veteran['Age']} | **Gender:** {veteran['Gender']}")
                st.markdown(f"**Branch:** {veteran['Branch']}")
                st.markdown(f"**Service Era:** {veteran['Service Era']}")
                st.markdown(f"**Intake:** {veteran['Intake Date']}")
                st.markdown(f"**Clinician:** {veteran['Assigned Clinician']}")

            # Clinical scores with interpretation
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
                         delta=interp, help="Patient Health Questionnaire-9")
            
            with col2:
                interp, color = get_score_interpretation(veteran['GAD-7 Score'], "GAD-7")
                st.metric("GAD-7 Anxiety", f"{color} {veteran['GAD-7 Score']}", 
                         delta=interp, help="Generalized Anxiety Disorder-7")
            
            with col3:
                interp, color = get_score_interpretation(veteran['PCL-5 Score'], "PCL-5")
                st.metric("PCL-5 PTSD", f"{color} {veteran['PCL-5 Score']}", 
                         delta=interp, help="PTSD Checklist for DSM-5")

            # Risk factors matrix
            st.markdown("### ⚠️ Risk Factor Analysis")
            risk_factors = {
                "Suicide Risk (C-SSRS)": veteran['C-SSRS Screen'],
                "Self-Harm Ideation": veteran['PHQ-9 Q9 (Self-Harm)'],
                "Social Support": veteran['Social Support'],
                "Substance Use Risk": veteran['Substance Use Risk'],
                "Housing Stability": veteran['Housing Status'],
                "Emergency Contact": veteran['Emergency Contact'],
                "Transportation Access": veteran['Transportation']
            }
            
            cols = st.columns(4)
            for i, (factor, value) in enumerate(risk_factors.items()):
                with cols[i % 4]:
                    # Color coding based on risk level
                    if factor == "Suicide Risk (C-SSRS)":
                        color = "🔴" if value != "Negative" else "🟢"
                    elif factor == "Self-Harm Ideation":
                        color = "🔴" if value == "Yes" else "🟢"
                    elif "Low" in str(value) or "Homeless" in str(value) or "None" in str(value):
                        color = "🔴"
                    elif "Medium" in str(value) or "At Risk" in str(value) or "Limited" in str(value):
                        color = "🟡"
                    else:
                        color = "🟢"
                    
                    st.markdown(f"**{factor}:**<br>{color} {value}", unsafe_allow_html=True)

            # Clinical actions
            st.markdown("### 🎯 Recommended Clinical Actions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.button("📋 Update Assessment", key="update_assessment")
            
            with col2:
                if st.button("📞 Contact Info", key="prep_contact"):
                    contact_info = f"""
                    **Contact Information for {veteran['Name']}:**
                    - Preferred Method: {veteran['Contact Method']}
                    - Last Contact: {veteran['Last Contact']}
                    - Emergency Contact: {veteran['Emergency Contact']}
                    """
                    st.info(contact_info)
            
            with col3:
                if st.button("📅 Schedule Appointment", key="schedule_appt"):
                    urgency = "URGENT" if 'Critical' in veteran['Risk Level'] else "Standard"
                    st.success(f"{urgency} appointment scheduling initiated")
            
            with col4:
                st.button("📧 Generate Referral", key="generate_referral")

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
                
                if st.button("💾 Save Documentation"):
                    if clinical_note:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.success(f"{note_type} saved to veteran record at {timestamp}")
                    else:
                        st.warning("Please enter documentation before saving")

            # Export individual veteran report with Q&A
            if st.button("📊 Generate Individual Report"):
                # Include Q&A history in the report
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

RISK ASSESSMENT:
Risk Level: {veteran['Risk Level']} (Score: {veteran['Risk Score']})
Clinical Reasoning: {veteran['Risk Explanation']}

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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Total Veterans:** {len(df)}")
    with col2:
        st.info(f"**Current View:** {len(df_filtered)}")
    with col3:
        ai_count = len([k for k in st.session_state.ai_summaries.keys() if not st.session_state.ai_summaries[k].startswith("Error")])
        st.info(f"**AI Summaries Generated:** {ai_count}")
    with col4:
        st.info(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")

    # Quick add veteran button (placeholder for future integration)
    if st.button("➕ Add New Veteran", key="add_veteran"):
        st.info("📋 New veteran intake form will open here (integration with intake app)")

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
