import streamlit as st

def load_modern_css():
    """Load modern CSS styling for the Streamlit app"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* CSS Variables for Design System */
        :root {
            --primary: #5B9BD3;
            --primary-dark: #3b82f6;
            --primary-light: #93c5fd;
            --secondary: #3E8A7E;
            --secondary-dark: #2C6B5F;
            --accent: #FF7F50;
            --accent-dark: #e55a3a;
            --danger: #ef4444;
            --danger-dark: #dc2626;
            --success: #77DD77;
            --warning: #f59e0b;
            --info: #60a5fa;
            
            --surface: #ffffff;
            --surface-elevated: #f8fafc;
            --surface-hover: #f1f5f9;
            --background: #F8F8F8;
            --background-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            
            --border: #e2e8f0;
            --border-strong: #cbd5e1;
            --border-focus: var(--primary);
            
            --text: #333333;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --text-inverse: #ffffff;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            
            --radius-sm: 0.375rem;
            --radius: 0.5rem;
            --radius-md: 0.75rem;
            --radius-lg: 1rem;
            --radius-xl: 1.5rem;
            
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 2rem;
            --spacing-2xl: 3rem;
            
            --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-fast: all 0.15s ease;
            --transition-slow: all 0.3s ease;
        }
        
        /* Global Reset and Base Styles */
        .stApp {
            background: var(--background) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            color: var(--text) !important;
            line-height: 1.6 !important;
        }
        
        /* Fix main container layout issues */
        .main .block-container {
            max-width: none !important;
            padding: var(--spacing-xl) var(--spacing-lg) !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Ensure sidebar doesn't interfere with main content */
        .st-emotion-cache-16txtl3 {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            z-index: 999 !important;
            background: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
            overflow-y: auto !important;
        }
        
        /* Adjust main content when sidebar is open */
        section[data-testid="stSidebar"][aria-expanded="true"] ~ .main {
            margin-left: 21rem !important;
        }
        
        section[data-testid="stSidebar"][aria-expanded="false"] ~ .main {
            margin-left: 0 !important;
        }
        
        /* Typography Enhancements */
        h1 {
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-align: center !important;
            margin-bottom: var(--spacing-md) !important;
            letter-spacing: -0.025em !important;
        }
        
        h2 {
            font-weight: 700 !important;
            font-size: 1.875rem !important;
            color: var(--text) !important;
            margin: var(--spacing-xl) 0 var(--spacing-lg) 0 !important;
            letter-spacing: -0.025em !important;
        }
        
        h3 {
            font-weight: 600 !important;
            font-size: 1.5rem !important;
            color: var(--text) !important;
            margin: var(--spacing-lg) 0 var(--spacing-md) 0 !important;
        }
        
        /* Modern Button System */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
            color: var(--text-inverse) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow) !important;
            cursor: pointer !important;
            position: relative !important;
            overflow: hidden !important;
            text-transform: none !important;
            letter-spacing: 0.025em !important;
            width: 100% !important;
        }
        
        .stButton > button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: var(--shadow-lg) !important;
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary) 100%) !important;
        }
        
        .stButton > button:hover:before {
            left: 100%;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: var(--shadow) !important;
        }
        
        .stButton > button:focus {
            outline: none !important;
            box-shadow: var(--shadow-lg), 0 0 0 3px rgba(91, 155, 211, 0.2) !important;
        }
        
        /* Button Variants */
        .stButton[key*="crisis"] > button,
        .stButton[key*="urgent"] > button {
            background: linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%) !important;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3) !important;
        }
        
        .stButton[key*="crisis"] > button:hover,
        .stButton[key*="urgent"] > button:hover {
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4) !important;
        }
        
        .stButton[key*="ai"] > button,
        .stButton[key*="generate"] > button {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%) !important;
            box-shadow: 0 4px 14px rgba(255, 127, 80, 0.3) !important;
        }
        
        .stButton[key*="contact"] > button {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%) !important;
            box-shadow: 0 4px 14px rgba(62, 138, 126, 0.3) !important;
        }
        
        /* Download Button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--success) 0%, #6bc373 100%) !important;
            color: var(--text-inverse) !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow) !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        /* Enhanced Cards and Containers */
        .stMetric {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--spacing-lg) !important;
            box-shadow: var(--shadow) !important;
            transition: var(--transition) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .stMetric:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
            border-color: var(--border-strong) !important;
        }
        
        .stMetric:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .stMetric label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        
        .stMetric [data-testid="metric-value"] {
            color: var(--text) !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
        }
        
        /* Form Elements */
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition) !important;
        }
        
        .stSelectbox > div > div:hover,
        .stMultiSelect > div > div:hover {
            border-color: var(--border-strong) !important;
            box-shadow: var(--shadow) !important;
        }
        
        .stSelectbox > div > div:focus-within,
        .stMultiSelect > div > div:focus-within {
            border-color: var(--border-focus) !important;
            box-shadow: var(--shadow), 0 0 0 3px rgba(91, 155, 211, 0.1) !important;
        }
        
        .stTextInput > div > div > input {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.875rem !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--border-focus) !important;
            box-shadow: var(--shadow), 0 0 0 3px rgba(91, 155, 211, 0.1) !important;
            outline: none !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: var(--text-muted) !important;
        }
        
        /* Sliders */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
            height: 8px !important;
            border-radius: 4px !important;
        }
        
        .stSlider > div > div > div > div > div {
            background: var(--surface) !important;
            border: 2px solid var(--primary) !important;
            box-shadow: var(--shadow) !important;
        }
        
        /* Checkboxes */
        .stCheckbox > label {
            font-weight: 500 !important;
            color: var(--text) !important;
            cursor: pointer !important;
        }
        
        /* Tables */
        .stDataFrame {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow) !important;
            overflow: hidden !important;
        }
        
        .stDataFrame [data-testid="stDataFrame"] > div {
            background: transparent !important;
        }
        
        .stDataFrame table {
            font-size: 0.875rem !important;
        }
        
        .stDataFrame th {
            background: var(--surface-elevated) !important;
            color: var(--text) !important;
            font-weight: 600 !important;
            border-bottom: 2px solid var(--border) !important;
        }
        
        .stDataFrame td {
            border-bottom: 1px solid var(--border) !important;
        }
        
        .stDataFrame tr:hover td {
            background: var(--surface-hover) !important;
        }
        
        /* Charts */
        .js-plotly-plot {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow) !important;
            padding: var(--spacing-md) !important;
            transition: var(--transition) !important;
        }
        
        .js-plotly-plot:hover {
            box-shadow: var(--shadow-md) !important;
        }
        
        /* Status Messages */
        .stSuccess {
            background: rgba(119, 221, 119, 0.1) !important;
            border: 1px solid rgba(119, 221, 119, 0.2) !important;
            border-radius: var(--radius-md) !important;
            color: #166534 !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.2) !important;
            border-radius: var(--radius-md) !important;
            color: #991b1b !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stInfo {
            background: rgba(91, 155, 211, 0.1) !important;
            border: 1px solid rgba(91, 155, 211, 0.2) !important;
            border-radius: var(--radius-md) !important;
            color: #1e40af !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1) !important;
            border: 1px solid rgba(245, 158, 11, 0.2) !important;
            border-radius: var(--radius-md) !important;
            color: #92400e !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        /* AI Summary Box Styling - Improved Light Design WITHOUT WHITE HEADING */
        .ai-summary-box {
            background: linear-gradient(135deg, rgba(91, 155, 211, 0.08), rgba(62, 138, 126, 0.08)) !important;
            border: 2px solid var(--primary) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(91, 155, 211, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .ai-summary-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .ai-summary-box h4 {
            color: var(--primary) !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            background: transparent !important;
        }
        
        .ai-summary-box p {
            color: var(--text) !important;
            line-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
            background: transparent !important;
        }
        
        /* Individual AI Assessment Box - Different Style WITHOUT WHITE HEADING */
        .individual-ai-box {
            background: linear-gradient(135deg, rgba(62, 138, 126, 0.08), rgba(119, 221, 119, 0.08)) !important;
            border: 2px solid var(--secondary) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(62, 138, 126, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .individual-ai-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--secondary), var(--success));
        }
        
        .individual-ai-box h4 {
            color: var(--secondary) !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            background: transparent !important;
        }
        
        .individual-ai-box p {
            color: var(--text) !important;
            line-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
            background: transparent !important;
        }
        
        /* Button Response Box */
        .button-response {
            background: linear-gradient(135deg, rgba(119, 221, 119, 0.1), rgba(62, 138, 126, 0.1)) !important;
            border: 1px solid var(--success) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            color: var(--text) !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 4px rgba(119, 221, 119, 0.1) !important;
        }
        
        /* Q&A Container Styling */
        .qa-container {
            background: rgba(247, 250, 252, 0.8) !important;
            border: 1px solid rgba(91, 155, 211, 0.2) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .qa-question {
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        
        .qa-answer {
            color: var(--text) !important;
            line-height: 1.5 !important;
            padding: 0.5rem !important;
            background: rgba(255, 255, 255, 0.7) !important;
            border-radius: 4px !important;
            border-left: 3px solid var(--primary) !important;
        }
        
        /* Improved responsive layout for mobile */
        @media (max-width: 768px) {
            .main .block-container {
                padding: var(--spacing-sm) !important;
            }
            
            /* Mobile column stacking */
            .row-widget.stHorizontal > div {
                flex-direction: column !important;
                width: 100% !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Mobile metrics layout */
            .stMetric {
                margin-bottom: 1rem !important;
                min-width: 140px !important;
            }
            
            /* Mobile button adjustments */
            .stButton > button {
                font-size: 0.75rem !important;
                padding: 0.4rem 0.8rem !important;
                min-height: 2.5rem !important;
            }
            
            /* Mobile AI boxes */
            .ai-summary-box, .individual-ai-box {
                padding: 1rem !important;
                margin: 0.5rem 0 !important;
            }
            
            .ai-summary-box h4, .individual-ai-box h4 {
                font-size: 1rem !important;
            }
            
            .ai-summary-box p, .individual-ai-box p {
                font-size: 0.9rem !important;
            }
        }
        
        /* Improved tablet layout */
        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                padding: var(--spacing-md) var(--spacing-lg) !important;
            }
            
            .stMetric {
                min-width: 160px !important;
            }
        }
        
        /* Desktop optimizations */
        @media (min-width: 1025px) {
            .main .block-container {
                padding: var(--spacing-xl) var(--spacing-xl) !important;
            }
        }
        
        /* Ensure containers work properly on all screen sizes */
        .stContainer > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Fix for column overflow issues */
        [data-testid="column"] {
            min-width: 0 !important;
            flex: 1 !important;
        }
        
        /* Prevent text overflow in metrics */
        .metric-container .metric-value {
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
        }
        
        /* Individual AI Assessment Box - Different Style */
        .individual-ai-box {
            background: linear-gradient(135deg, rgba(62, 138, 126, 0.08), rgba(119, 221, 119, 0.08)) !important;
            border: 2px solid var(--secondary) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 4px 12px rgba(62, 138, 126, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .individual-ai-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--secondary), var(--success));
        }
        
        .individual-ai-box h4 {
            color: var(--secondary) !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
        }
        
        .individual-ai-box p {
            color: var(--text) !important;
            line-height: 1.6 !important;
            margin-bottom: 0 !important;
            font-size: 0.95rem !important;
        }
        
        /* Q&A Container Styling */
        .qa-container {
            background: rgba(247, 250, 252, 0.8) !important;
            border: 1px solid rgba(91, 155, 211, 0.2) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .qa-question {
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
        }
        
        .qa-answer {
            color: var(--text) !important;
            line-height: 1.5 !important;
            padding: 0.5rem !important;
            background: rgba(255, 255, 255, 0.7) !important;
            border-radius: 4px !important;
            border-left: 3px solid var(--primary) !important;
        }
        
        /* Priority Alert */
        .priority-alert {
            background: linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%) !important;
            color: var(--text-inverse) !important;
            padding: 1rem !important;
            border-radius: var(--radius-lg) !important;
            text-align: center !important;
            font-weight: 600 !important;
            box-shadow: var(--shadow-md) !important;
            animation: pulse-alert 2s infinite !important;
        }
        
        @keyframes pulse-alert {
            0%, 100% { box-shadow: var(--shadow-md), 0 0 0 0 rgba(239, 68, 68, 0.2); }
            50% { box-shadow: var(--shadow-lg), 0 0 0 10px rgba(239, 68, 68, 0); }
        }
        
        /* Sidebar Improvements */
        .css-1d391kg {
            background: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: var(--shadow) !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: var(--surface-elevated) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            transition: var(--transition) !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: var(--surface-hover) !important;
            border-color: var(--border-strong) !important;
        }
        
        /* Loading Spinner */
        .stSpinner > div {
            border-top-color: var(--primary) !important;
            border-right-color: var(--secondary) !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--surface-elevated);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
        }
        
        /* Hide Streamlit elements */
        .css-1rs6os, .css-17ziqus {
            visibility: hidden;
        }
        
        #MainMenu {
            visibility: hidden;
        }
        
        footer {
            visibility: hidden;
        }
        
        header {
            visibility: hidden;
        }
        
        /* Fix column layout issues */
        .row-widget.stHorizontal > div {
            flex-wrap: nowrap !important;
            min-width: 0 !important;
        }
        
        /* Ensure metrics containers don't overflow */
        .metric-container {
            min-width: 0 !important;
            flex-shrink: 1 !important;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main .block-container {
                padding: var(--spacing-md) var(--spacing-sm) !important;
            }
            
            h1 {
                font-size: 2rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            .stButton > button {
                padding: 0.625rem 1.25rem !important;
                font-size: 0.8rem !important;
            }
            
            section[data-testid="stSidebar"][aria-expanded="true"] ~ .main {
                margin-left: 0 !important;
            }
        }
        
        /* Animation Classes */
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .slide-in {
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* AI Status Indicators */
        .ai-status-success {
            background: linear-gradient(135deg, var(--success) 0%, #6bc373 100%) !important;
            color: var(--text-inverse) !important;
            padding: 0.5rem 1rem !important;
            border-radius: var(--radius-md) !important;
            margin: 0.5rem 0 !important;
            box-shadow: var(--shadow-sm) !important;
            font-weight: 500 !important;
        }
        
        .ai-status-error {
            background: linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%) !important;
            color: var(--text-inverse) !important;
            padding: 0.5rem 1rem !important;
            border-radius: var(--radius-md) !important;
            margin: 0.5rem 0 !important;
            box-shadow: var(--shadow-sm) !important;
            font-weight: 500 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def create_modern_container(content, title=None, subtitle=None, gradient=False):
    """Create a modern container with optional title and gradient"""
    gradient_style = ""
    if gradient:
        gradient_style = "background: linear-gradient(135deg, rgba(91, 155, 211, 0.05) 0%, rgba(62, 138, 126, 0.05) 100%);"
    
    container_html = f"""
    <div style="
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xl);
        margin: var(--spacing-lg) 0;
        box-shadow: var(--shadow);
        transition: var(--transition);
        {gradient_style}
    " class="fade-in">
        {f'<h3 style="margin-top: 0; color: var(--primary);">{title}</h3>' if title else ''}
        {f'<p style="color: var(--text-secondary); margin-bottom: var(--spacing-lg);">{subtitle}</p>' if subtitle else ''}
        {content}
    </div>
    """
    return st.markdown(container_html, unsafe_allow_html=True)

def create_metric_card(title, value, change=None, icon=None, color="primary"):
    """Create a custom metric card with modern styling"""
    color_map = {
        "primary": "var(--primary)",
        "success": "var(--success)", 
        "danger": "var(--danger)",
        "warning": "var(--warning)",
        "secondary": "var(--secondary)"
    }
    
    card_color = color_map.get(color, "var(--primary)")
    change_html = f'<div style="color: {card_color}; font-size: 0.875rem; font-weight: 500;">{change}</div>' if change else ''
    icon_html = f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
    
    card_html = f"""
    <div style="
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    " class="metric-card-custom" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='var(--shadow-lg)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='var(--shadow)'">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: {card_color};
        "></div>
        {icon_html}
        <div style="color: var(--text-secondary); font-size: 0.875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">{title}</div>
        <div style="color: var(--text); font-size: 2rem; font-weight: 700; line-height: 1;">{value}</div>
        {change_html}
    </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

def create_status_badge(text, status="default"):
    """Create a modern status badge"""
    status_colors = {
        "success": ("var(--success)", "rgba(119, 221, 119, 0.1)"),
        "danger": ("var(--danger)", "rgba(239, 68, 68, 0.1)"),
        "warning": ("var(--warning)", "rgba(245, 158, 11, 0.1)"),
        "info": ("var(--info)", "rgba(91, 155, 211, 0.1)"),
        "default": ("var(--text-secondary)", "var(--surface-elevated)")
    }
    
    color, bg = status_colors.get(status, status_colors["default"])
    
    badge_html = f"""
    <span style="
        background: {bg};
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: var(--radius);
        font-size: 0.875rem;
        font-weight: 500;
        border: 1px solid {color}33;
    ">{text}</span>
    """
    return st.markdown(badge_html, unsafe_allow_html=True)
