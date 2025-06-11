import streamlit as st

def load_modern_css():
    """Load modern CSS styling for the Streamlit app"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* CSS Variables for Design System */
        :root {
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --primary-light: #93c5fd;
            --secondary: #10b981;
            --secondary-dark: #059669;
            --accent: #f59e0b;
            --accent-dark: #d97706;
            --danger: #ef4444;
            --danger-dark: #dc2626;
            --success: #22c55e;
            --warning: #f59e0b;
            --info: #3b82f6;
            
            --surface: #ffffff;
            --surface-elevated: #f8fafc;
            --surface-hover: #f1f5f9;
            --background: #f8fafc;
            --background-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            
            --border: #e2e8f0;
            --border-strong: #cbd5e1;
            --border-focus: var(--primary);
            
            --text: #1e293b;
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
            background: var(--background-gradient) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            color: var(--text) !important;
            line-height: 1.6 !important;
        }
        
        .main .block-container {
            max-width: 1200px !important;
            padding: var(--spacing-xl) var(--spacing-lg) !important;
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
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
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
            box-shadow: var(--shadow-lg), 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
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
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
            box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3) !important;
        }
        
        .stButton[key*="contact"] > button {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%) !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
        }
        
        /* Download Button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--success) 0%, #16a34a 100%) !important;
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
            box-shadow: var(--shadow), 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
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
            box-shadow: var(--shadow), 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
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
            background: rgba(34, 197, 94, 0.1) !important;
            border: 1px solid rgba(34, 197, 94, 0.2) !important;
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
            background: rgba(59, 130, 246, 0.1) !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
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
        
        /* Special Components */
        .ai-summary-box {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--spacing-xl) !important;
            margin: var(--spacing-lg) 0 !important;
            box-shadow: var(--shadow-md) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .ai-summary-box:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), #8b5cf6, var(--secondary));
        }
        
        .ai-summary-box h4 {
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin-bottom: var(--spacing-md) !important;
        }
        
        .priority-alert {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--spacing-lg) !important;
            text-align: center !important;
            font-weight: 600 !important;
            color: var(--danger-dark) !important;
            box-shadow: var(--shadow-md) !important;
            animation: pulse-alert 2s infinite !important;
        }
        
        @keyframes pulse-alert {
            0%, 100% { box-shadow: var(--shadow-md), 0 0 0 0 rgba(239, 68, 68, 0.2); }
            50% { box-shadow: var(--shadow-lg), 0 0 0 10px rgba(239, 68, 68, 0); }
        }
        
        /* Sidebar */
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
    </style>
    """, unsafe_allow_html=True)

def create_modern_container(content, title=None, subtitle=None, gradient=False):
    """Create a modern container with optional title and gradient"""
    gradient_style = ""
    if gradient:
        gradient_style = "background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);"
    
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
        "success": ("var(--success)", "rgba(34, 197, 94, 0.1)"),
        "danger": ("var(--danger)", "rgba(239, 68, 68, 0.1)"),
        "warning": ("var(--warning)", "rgba(245, 158, 11, 0.1)"),
        "info": ("var(--info)", "rgba(59, 130, 246, 0.1)"),
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
