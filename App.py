import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import base64
from io import BytesIO
import json

# Set page configuration
st.set_page_config(
    page_title="Excel & Power BI Mastery",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced blue theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0A1F33 0%, #0E2A47 50%, #15395C 100%);
        color: #FFFFFF;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #0A1F33;
        padding: 8px 8px 0 8px;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E4D73;
        color: #FFFFFF;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2A7BB0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00B4D8 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 8px rgba(0, 180, 216, 0.3);
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #1E4D73 0%, #15395C 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        border: 1px solid #2A7BB0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00B4D8 0%, #0077B6 100%);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00B4D8 0%, #0077B6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0096C7 0%, #005B8A 100%);
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 180, 216, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #1E4D73 0%, #15395C 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background-color: #0E2A47;
        padding: 1.5rem;
        border-radius: 0 0 8px 8px;
    }
    
    /* Text */
    p, li, .stMarkdown {
        color: #E6F1FF !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Special boxes */
    .tip-box {
        background: linear-gradient(135deg, #1E4D73 0%, #2A7BB0 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #00B4D8;
        margin: 1.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .exercise-box {
        background: linear-gradient(135deg, #1E3D5C 0%, #2A5C7B 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #FF9E4A;
        margin: 1.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .success-box {
        background: linear-gradient(135deg, #1E4D3C 0%, #2A7B5A 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #4CAF50;
        margin: 1.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #0A1F33;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #2A7BB0;
    }
    
    /* Dataframes */
    .stDataFrame {
        background-color: #0A1F33;
        border-radius: 8px;
        border: 1px solid #2A7BB0;
    }
    
    /* Input widgets */
    .stTextInput > div > div > input {
        background-color: #0E2A47;
        color: white;
        border: 1px solid #2A7BB0;
    }
    
    .stSelectbox > div > div {
        background-color: #0E2A47;
        color: white;
        border: 1px solid #2A7BB0;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E4D73 0%, #15395C 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #2A7BB0;
    }
    
    /* Divider */
    .stHorizontalBlock {
        border-bottom: 2px solid #2A7BB0;
        padding-bottom: 1.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for user progress and data
if 'user_progress' not in st.session_state:
    st.session_state.user_progress = {
        'excel_basics': 0,
        'excel_formulas': 0,
        'excel_charts': 0,
        'excel_pivottables': 0,
        'excel_advanced': 0,
        'powerbi_basics': 0,
        'powerbi_dax': 0,
        'powerbi_visuals': 0,
        'powerbi_dashboards': 0,
        'powerbi_service': 0,
        'data_analysis': 0,
        'data_modeling': 0,
        'business_intelligence': 0
    }

if 'completed_modules' not in st.session_state:
    st.session_state.completed_modules = []

if 'user_skill_level' not in st.session_state:
    st.session_state.user_skill_level = 'Beginner'

if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame(columns=['timestamp', 'module', 'time_spent', 'score'])

if 'learning_path' not in st.session_state:
    st.session_state.learning_path = []

if 'spaced_repetition' not in st.session_state:
    st.session_state.spaced_repetition = {}

if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = {}

# App title
st.markdown('<h1 style="text-align: center; color: #00B4D8; margin-bottom: 2rem; font-size: 3.5rem;">📊 Excel & Power BI Mastery Platform</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "📚 Learning Hub", "🛠️ Practice Lab", "📈 Progress Analytics"])

# Expanded learning content with detailed lessons
learning_content = {
    'excel_basics': {
        'title': 'Excel Fundamentals',
        'description': 'Master the essential Excel skills needed for data manipulation and analysis.',
        'lessons': [
            {
                'title': 'Excel Interface & Navigation',
                'content': '''
                - Ribbon, Quick Access Toolbar, and Formula Bar overview
                - Worksheet navigation techniques and shortcuts
                - Understanding workbooks vs. worksheets
                - Customizing the Excel interface for efficiency
                - Using the Status Bar for quick insights
                - Different view modes and their purposes
                ''',
                'video_link': 'https://www.example.com/excel-interface',
                'duration': '25 min',
                'exercise': 'Customize your Excel interface and create a navigation shortcut sheet'
            },
            {
                'title': 'Data Entry & Selection Mastery',
                'content': '''
                - Efficient data entry techniques and best practices
                - Advanced selection methods (keyboard vs. mouse)
                - AutoFill for sequences, patterns, and custom lists
                - Flash Fill for intelligent data extraction and formatting
                - Data validation for controlled input
                - Using forms for structured data entry
                ''',
                'video_link': 'https://www.example.com/data-entry',
                'duration': '35 min',
                'exercise': 'Create a data entry form for a customer database'
            },
            {
                'title': 'Formatting Excellence',
                'content': '''
                - Advanced font and cell formatting options
                - Custom number formats for specialized display
                - Conditional formatting with formulas
                - Cell styles and themes for consistency
                - Format Painter advanced techniques
                - Using templates for standardized formatting
                ''',
                'video_link': 'https://www.example.com/formatting',
                'duration': '40 min',
                'exercise': 'Format a financial report with conditional formatting and custom styles'
            },
            {
                'title': 'Workbook Management',
                'content': '''
                - Advanced save options and file formats
                - AutoRecover and version history management
                - Workbook protection and security features
                - Sharing and collaboration techniques
                - Inspecting workbooks for issues
                - Managing workbook properties and metadata
                ''',
                'video_link': 'https://www.example.com/workbook-management',
                'duration': '30 min',
                'exercise': 'Create a protected workbook with specific user permissions'
            },
            {
                'title': 'Advanced Worksheet Techniques',
                'content': '''
                - 3D references across multiple worksheets
                - Grouping worksheets for simultaneous operations
                - Custom views for different user perspectives
                - Worksheet outlining and subtotals
                - Data consolidation from multiple sheets
                - Advanced hiding and protection techniques
                ''',
                'video_link': 'https://www.example.com/worksheet-techniques',
                'duration': '45 min',
                'exercise': 'Create a consolidated report from multiple department worksheets'
            }
        ],
        'difficulty': 'Beginner',
        'estimated_time': '3.5 hours',
        'resources': [
            'Excel Interface Cheat Sheet',
            'Data Entry Best Practices Guide',
            'Formatting Template Library',
            'Workbook Security Checklist'
        ],
        'prerequisites': [],
        'badge': 'Excel Basics Master'
    },
    'excel_formulas': {
        'title': 'Excel Formulas & Functions',
        'description': 'Master Excel\'s powerful formula language for advanced data analysis.',
        'lessons': [
            {
                'title': 'Formula Fundamentals',
                'content': '''
                - Formula syntax and structure deep dive
                - Relative, absolute, and mixed referencing
                - Formula auditing and error checking
                - Using the Function Wizard effectively
                - Array formulas and dynamic arrays
                - Best practices for formula efficiency
                ''',
                'video_link': 'https://www.example.com/formula-fundamentals',
                'duration': '40 min',
                'exercise': 'Create a complex calculation sheet with various reference types'
            },
            {
                'title': 'Statistical & Mathematical Functions',
                'content': '''
                - Advanced SUM, COUNT, and AVERAGE variations
                - Statistical functions: MEDIAN, MODE, STDEV, VAR
                - Mathematical functions: ROUND, TRUNC, INT, MOD
                - Random number generation with RAND and RANDBETWEEN
                - Aggregate functions for conditional calculations
                - Using SUMPRODUCT for advanced calculations
                ''',
                'video_link': 'https://www.example.com/statistical-functions',
                'duration': '50 min',
                'exercise': 'Build a statistical analysis dashboard for sales data'
            },
            {
                'title': 'Logical Functions Mastery',
                'content': '''
                - Nested IF statements and alternatives
                - Boolean logic with AND, OR, NOT
                - IFS, SWITCH, and CHOOSE functions
                - Using IFERROR and IFNA for error handling
                - Combining logical functions with other function types
                - Practical applications for decision-making models
                ''',
                'video_link': 'https://www.example.com/logical-functions',
                'duration': '45 min',
                'exercise': 'Create a grading system with multiple conditional criteria'
            },
            {
                'title': 'Lookup & Reference Functions',
                'content': '''
                - VLOOKUP and HLOOKUP advanced techniques
                - INDEX-MATCH powerful combinations
                - XLOOKUP modern lookup capabilities
                - OFFSET and INDIRECT for dynamic references
                - Using CHOOSE for scenario analysis
                - Advanced applications with multiple criteria
                ''',
                'video_link': 'https://www.example.com/lookup-functions',
                'duration': '60 min',
                'exercise': 'Build a dynamic dashboard with multiple lookup techniques'
            },
            {
                'title': 'Text & Date Functions',
                'content': '''
                - Text manipulation with LEFT, RIGHT, MID, FIND, SEARCH
                - Advanced text functions: TEXTJOIN, CONCAT, SUBSTITUTE
                - Date and time calculations and formatting
                - Working with business days and holidays
                - Date intelligence functions: DATEDIF, EDATE, EOMONTH
                - Practical applications for project planning
                ''',
                'video_link': 'https://www.example.com/text-date-functions',
                'duration': '50 min',
                'exercise': 'Create a project timeline with automated date calculations'
            },
            {
                'title': 'Advanced Function Combinations',
                'content': '''
                - Array formulas and dynamic array functions
                - LAMBDA functions for custom calculations
                - Using FILTER, SORT, UNIQUE, and SEQUENCE
                - Complex nested function strategies
                - Optimizing formulas for performance
                - Real-world complex modeling examples
                ''',
                'video_link': 'https://www.example.com/advanced-functions',
                'duration': '70 min',
                'exercise': 'Build a complex financial model using advanced function combinations'
            }
        ],
        'difficulty': 'Beginner to Intermediate',
        'estimated_time': '6 hours',
        'resources': [
            'Function Reference Guide',
            'Formula Optimization Checklist',
            'Common Formula Patterns',
            'Advanced Lookup Techniques'
        ],
        'prerequisites': ['excel_basics'],
        'badge': 'Excel Formulas Expert'
    },
    'data_analysis': {
        'title': 'Data Analysis Techniques',
        'description': 'Advanced analytical methods for deriving insights from data in Excel and Power BI.',
        'lessons': [
            {
                'title': 'Exploratory Data Analysis',
                'content': '''
                - Data profiling and quality assessment
                - Descriptive statistics and summary metrics
                - Distribution analysis with histograms and box plots
                - Correlation analysis and visualization
                - Outlier detection and treatment strategies
                - Data transformation techniques
                ''',
                'video_link': 'https://www.example.com/exploratory-analysis',
                'duration': '55 min',
                'exercise': 'Perform EDA on a sales dataset and create a summary report'
            },
            {
                'title': 'Statistical Analysis Methods',
                'content': '''
                - Hypothesis testing fundamentals
                - T-tests and Z-tests for means comparison
                - ANOVA for multiple group comparisons
                - Chi-square tests for categorical data
                - Regression analysis basics
                - Interpreting statistical results
                ''',
                'video_link': 'https://www.example.com/statistical-methods',
                'duration': '65 min',
                'exercise': 'Conduct hypothesis tests on customer demographic data'
            },
            {
                'title': 'Predictive Analytics',
                'content': '''
                - Time series analysis and forecasting
                - Moving averages and exponential smoothing
                - Regression-based forecasting
                - Using the Forecast Sheet feature in Excel
                - Introduction to machine learning concepts
                - Evaluating predictive model accuracy
                ''',
                'video_link': 'https://www.example.com/predictive-analytics',
                'duration': '70 min',
                'exercise': 'Create a sales forecast for the next quarter using multiple methods'
            },
            {
                'title': 'Optimization Techniques',
                'content': '''
                - Linear programming concepts
                - Using Solver for optimization problems
                - Scenario analysis with Data Tables
                - Goal Seek for reverse calculations
                - Monte Carlo simulation basics
                - Decision analysis under uncertainty
                ''',
                'video_link': 'https://www.example.com/optimization-techniques',
                'duration': '60 min',
                'exercise': 'Optimize a production plan using Solver'
            }
        ],
        'difficulty': 'Advanced',
        'estimated_time': '4.5 hours',
        'resources': [
            'Statistical Analysis Guide',
            'Forecasting Methods Comparison',
            'Solver Parameter Templates',
            'Data Analysis Case Studies'
        ],
        'prerequisites': ['excel_formulas', 'excel_pivottables'],
        'badge': 'Data Analysis Specialist'
    }
}

# Quiz questions with detailed explanations
quiz_questions = {
    'excel_basics': [
        {
            'question': 'Which shortcut selects the entire worksheet?',
            'options': ['Ctrl+A', 'Ctrl+Shift+Space', 'Alt+A', 'Shift+Space'],
            'correct': 1,
            'explanation': 'Ctrl+Shift+Space selects the entire worksheet in Excel. Ctrl+A selects the current region if the cursor is in a data range, or the entire worksheet if not.',
            'points': 10,
            'difficulty': 'Easy'
        },
        {
            'question': 'How do you autofill a series of dates in Excel?',
            'options': ['Use the Fill Handle', 'Use the AutoComplete feature', 'Use the Series dialog box', 'Both 1 and 3'],
            'correct': 3,
            'explanation': 'You can use either the Fill Handle by dragging or the Series dialog box (Home > Fill > Series) to autofill dates. The Series dialog offers more control over the pattern.',
            'points': 15,
            'difficulty': 'Medium'
        },
        {
            'question': 'Which feature automatically completes data entry based on patterns it detects?',
            'options': ['AutoComplete', 'Flash Fill', 'Quick Analysis', 'AutoFill'],
            'correct': 1,
            'explanation': 'Flash Fill (introduced in Excel 2013) automatically detects patterns in your data entry and completes the remaining entries without formulas.',
            'points': 10,
            'difficulty': 'Easy'
        },
        {
            'question': 'What does the Format Painter tool do?',
            'options': [
                'Applies artistic effects to cells',
                'Copies formatting from one cell to another',
                'Paints cells with a selected color',
                'Creates painterly charts from data'
            ],
            'correct': 1,
            'explanation': 'The Format Painter copies formatting from one cell or range and applies it to another. Double-clicking the Format Painter button locks it for multiple applications.',
            'points': 10,
            'difficulty': 'Easy'
        },
        {
            'question': 'How do you protect a worksheet in Excel?',
            'options': [
                'Review tab > Protect Sheet',
                'Home tab > Format > Protect Sheet',
                'File > Info > Protect Workbook',
                'Both 1 and 3 are correct'
            ],
            'correct': 3,
            'explanation': 'You can protect a worksheet from the Review tab or from File > Info > Protect Workbook. The latter offers additional protection options for the entire workbook structure.',
            'points': 15,
            'difficulty': 'Medium'
        }
    ],
    'excel_formulas': [
        {
            'question': 'Which function adds up all the numbers in a range of cells?',
            'options': ['COUNT', 'AVERAGE', 'SUM', 'TOTAL'],
            'correct': 2,
            'explanation': 'The SUM function adds all the numbers in a range of cells. SUMIF and SUMIFS provide conditional summing capabilities.',
            'points': 5,
            'difficulty': 'Easy'
        },
        {
            'question': 'What does VLOOKUP do?',
            'options': ['Looks for values vertically', 'Looks for values horizontally', 'Creates a vertical layout', 'Verifies lookup values'],
            'correct': 0,
            'explanation': 'VLOOKUP looks for a value in the first column of a table and returns a value in the same row from a specified column. It has been largely superseded by XLOOKUP in newer Excel versions.',
            'points': 10,
            'difficulty': 'Easy'
        },
        {
            'question': 'Which function would you use to find the highest value in a range?',
            'options': ['MAX', 'HIGH', 'TOP', 'PEAK'],
            'correct': 0,
            'explanation': 'The MAX function returns the largest value in a set of values. Use MAXIFS for conditional maximum values.',
            'points': 5,
            'difficulty': 'Easy'
        },
        {
            'question': 'What is the main advantage of XLOOKUP over VLOOKUP?',
            'options': [
                'XLOOKUP can return arrays',
                'XLOOKUP defaults to exact match',
                'XLOOKUP can search in any direction',
                'All of the above'
            ],
            'correct': 3,
            'explanation': 'XLOOKUP has several advantages over VLOOKUP, including the ability to return arrays, default exact matching, search in any direction, and not requiring a separate column index number.',
            'points': 15,
            'difficulty': 'Medium'
        },
        {
            'question': 'Which function would you use to combine text from multiple cells?',
            'options': ['COMBINE', 'MERGE', 'CONCAT', 'JOIN'],
            'correct': 2,
            'explanation': 'The CONCAT function (or CONCATENATE in older versions) combines text from multiple cells into one cell. TEXTJOIN offers additional functionality with delimiters.',
            'points': 10,
            'difficulty': 'Easy'
        },
        {
            'question': 'What does the IFERROR function do?',
            'options': [
                'Checks if a cell contains an error',
                'Returns a custom result when a formula generates an error',
                'Prevents all errors in a worksheet',
                'Highlights cells containing errors'
            ],
            'correct': 1,
            'explanation': 'IFERROR returns a custom result when a formula generates an error, and the standard result when no error is detected. It is useful for cleaning up the appearance of worksheets with potential errors.',
            'points': 15,
            'difficulty': 'Medium'
        }
    ]
}

# Practice exercises with solutions
practice_exercises = {
    'excel_basics': [
        {
            'title': 'Professional Data Entry System',
            'description': 'Create a comprehensive data entry system with validation and formatting.',
            'objectives': [
                'Implement data validation rules',
                'Create custom number formats',
                'Use conditional formatting',
                'Protect worksheet structure'
            ],
            'steps': [
                'Create a new workbook with a structured data entry table',
                'Add data validation for specific columns (e.g., dropdown lists, date restrictions)',
                'Apply custom number formats for ID numbers, phone numbers, etc.',
                'Use conditional formatting to highlight important values or outliers',
                'Protect the worksheet to allow data entry only in specific cells',
                'Create a user guide section with instructions'
            ],
            'solution_file': 'data_entry_system_solution.xlsx',
            'difficulty': 'Intermediate',
            'estimated_time': '45 minutes',
            'skills': ['Data Validation', 'Formatting', 'Worksheet Protection']
        },
        {
            'title': 'Advanced Formatting Workbook',
            'description': 'Create a professionally formatted financial report with advanced Excel features.',
            'objectives': [
                'Apply advanced cell formatting',
                'Create and use custom styles',
                'Implement conditional formatting with formulas',
                'Use sparklines for data visualization'
            ],
            'steps': [
                'Import or create a dataset with financial information',
                'Create custom cell styles for headers, totals, and important figures',
                'Apply conditional formatting using formulas to highlight key metrics',
                'Add sparklines to show trends within cells',
                'Create a consistent color scheme throughout the report',
                'Use cell protection to prevent modification of formulas'
            ],
            'solution_file': 'formatting_workbook_solution.xlsx',
            'difficulty': 'Intermediate',
            'estimated_time': '60 minutes',
            'skills': ['Advanced Formatting', 'Conditional Formatting', 'Data Visualization']
        }
    ],
    'excel_formulas': [
        {
            'title': 'Advanced Sales Commission Calculator',
            'description': 'Build a sophisticated commission calculator with tiered rates and multiple conditions.',
            'objectives': [
                'Use nested IF statements or IFS function',
                'Implement VLOOKUP or XLOOKUP for rate tables',
                'Create dynamic summary reports',
                'Use data validation for inputs'
            ],
            'steps': [
                'Create a rate table with tiered commission structure',
                'Build an input area for salesperson data and sales figures',
                'Use appropriate lookup functions to determine commission rates',
                'Calculate commissions with proper conditional logic',
                'Create a summary section with totals and averages',
                'Add data validation to ensure accurate inputs'
            ],
            'solution_file': 'commission_calculator_solution.xlsx',
            'difficulty': 'Advanced',
            'estimated_time': '75 minutes',
            'skills': ['Lookup Functions', 'Logical Functions', 'Data Validation']
        },
        {
            'title': 'Dynamic Financial Dashboard',
            'description': 'Create an interactive financial dashboard with formulas and controls.',
            'objectives': [
                'Use advanced date functions',
                'Implement dropdowns for period selection',
                'Create dynamic charts based on formulas',
                'Build a responsive layout'
            ],
            'steps': [
                'Set up a financial dataset with date, revenue, and expense columns',
                'Create formulas to calculate key metrics (growth rates, profit margins, etc.)',
                'Add dropdown controls for period selection (month, quarter, year)',
                'Build charts that update based on selection',
                'Create a visually appealing dashboard layout',
                'Add conditional formatting to highlight performance'
            ],
            'solution_file': 'financial_dashboard_solution.xlsx',
            'difficulty': 'Advanced',
            'estimated_time': '90 minutes',
            'skills': ['Date Functions', 'Charting', 'Dashboard Design']
        }
    ]
}

# Case studies for real-world application
case_studies = {
    'excel_basics': [
        {
            'title': 'Small Business Inventory Management System',
            'description': 'Design an inventory management solution for a small retail business.',
            'scenario': '''
            A small boutique needs to track inventory levels, sales, and reordering. They currently use a paper-based system 
            but want to transition to Excel for better tracking and reporting. The system should track:
            - Product details (SKU, name, category, supplier)
            - Current stock levels and reorder points
            - Sales data and trends
            - Supplier information and lead times
            ''',
            'tasks': [
                'Design an inventory tracking spreadsheet with appropriate columns',
                'Create data validation for product categories and suppliers',
                'Set up conditional formatting to highlight low stock items',
                'Create a dashboard showing key inventory metrics',
                'Protect the worksheet to prevent accidental changes to formulas',
                'Add a reordering recommendation system'
            ],
            'learning_outcomes': [
                'Designing effective spreadsheets for business use',
                'Implementing data validation and conditional formatting',
                'Creating basic dashboards for quick insights',
                'Protecting worksheets to maintain data integrity',
                'Developing automated recommendation systems'
            ],
            'data_provided': 'Sample product list and sales data',
            'solution_file': 'inventory_management_solution.xlsx'
        }
    ],
    'excel_formulas': [
        {
            'title': 'Sales Performance Analytics Platform',
            'description': 'Build a comprehensive sales analytics platform with advanced formulas.',
            'scenario': '''
            A medium-sized company wants to analyze sales performance across regions, products, and salespeople.
            They need a system that can:
            - Calculate individual and team performance metrics
            - Compare performance against targets
            - Identify trends and patterns in sales data
            - Generate commission calculations automatically
            - Provide insights for strategic decision-making
            ''',
            'tasks': [
                'Design a data structure to store sales transactions',
                'Create a parameter table for commission rates and targets',
                'Build formulas to calculate key performance indicators',
                'Implement lookup functions to assign rates and targets',
                'Create a summary dashboard with dynamic visualizations',
                'Add scenario analysis capabilities for what-if planning'
            ],
            'learning_outcomes': [
                'Designing complex data structures in Excel',
                'Implementing advanced formula combinations',
                'Creating dynamic reporting systems',
                'Building what-if analysis capabilities',
                'Developing performance measurement frameworks'
            ],
            'data_provided': 'Sales transaction data and target information',
            'solution_file': 'sales_analytics_solution.xlsx'
        }
    ]
}

# Dashboard Tab
with tab1:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>🚀 Welcome to Your Learning Journey!</h2>
            <p>This platform is designed to transform you into an Excel and Power BI expert through comprehensive lessons, hands-on practice, and real-world applications.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completed = len([p for p in st.session_state.user_progress.values() if p == 100])
        total = len(st.session_state.user_progress)
        st.metric("Modules Completed", f"{completed}/{total}", f"{round(completed/total*100)}%")
    
    with col3:
        hours_studied = round(len(st.session_state.user_data) * 0.5, 1)
        st.metric("Hours Studied", hours_studied, "+5.2h this week")
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Progress overview
        st.markdown("""
        <div class="card">
            <h3>📈 Your Learning Progress</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress chart
        progress_data = {
            'Module': [learning_content[m]['title'] for m in st.session_state.user_progress.keys() if m in learning_content],
            'Progress': [st.session_state.user_progress[m] for m in st.session_state.user_progress.keys() if m in learning_content],
            'Category': ['Excel' if 'excel' in m else 'Power BI' if 'powerbi' in m else 'Other' for m in st.session_state.user_progress.keys() if m in learning_content]
        }
        progress_df = pd.DataFrame(progress_data)
        
        fig = px.bar(progress_df, x='Module', y='Progress', color='Category', 
                     title='Module Completion Progress', color_discrete_sequence=['#00B4D8', '#0077B6', '#FF9E4A'])
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommended next steps
        st.markdown("""
        <div class="card">
            <h3>🎯 Recommended Next Steps</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Find next recommended module
        for module, progress in st.session_state.user_progress.items():
            if progress < 100 and module in learning_content:
                module_data = learning_content[module]
                st.markdown(f"""
                <div class="card">
                    <h4>{module_data['title']}</h4>
                    <p>{module_data['description']}</p>
                    <p><strong>Difficulty:</strong> {module_data['difficulty']} | <strong>Time:</strong> {module_data['estimated_time']}</p>
                    <div class="stProgress">
                """, unsafe_allow_html=True)
                st.progress(progress/100)
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button(f"Continue {module_data['title']}", key=f"cont_{module}"):
                    st.session_state.current_module = module
                    st.rerun()
                break
    
    with col2:
        # Skill assessment
        st.markdown("""
        <div class="card">
            <h3>📊 Skill Assessment</h3>
        </div>
        """, unsafe_allow_html=True)
        
        skill_level = st.selectbox(
            "Your current skill level:",
            ["Beginner", 'Intermediate', 'Advanced'],
            index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.user_skill_level)
        )
        
        if skill_level != st.session_state.user_skill_level:
            st.session_state.user_skill_level = skill_level
            st.success("Skill level updated!")
        
        # Badges earned
        st.markdown("""
        <div class="card">
            <h3>🏆 Badges Earned</h3>
        </div>
        """, unsafe_allow_html=True)
        
        badges = []
        for module, progress in st.session_state.user_progress.items():
            if progress == 100 and module in learning_content and 'badge' in learning_content[module]:
                badges.append(learning_content[module]['badge'])
        
        if badges:
            for badge in badges:
                st.markdown(f"""
                <div class="success-box">
                    <h4>⭐ {badge}</h4>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Complete modules to earn badges!")
        
        # Upcoming reviews
        st.markdown("""
        <div class="card">
            <h3>🔄 Spaced Repetition</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mock review schedule
        review_modules = []
        for module in st.session_state.user_progress.keys():
            if st.session_state.user_progress[module] > 50 and random.random() > 0.7:
                review_modules.append(module)
        
        if review_modules:
            for module in review_modules[:3]:
                if module in learning_content:
                    st.info(f"Review {learning_content[module]['title']} soon")
        else:
            st.info("No reviews scheduled yet")

# Learning Hub Tab
with tab2:
    st.markdown("""
    <div class="card">
        <h2>Learning Hub</h2>
        <p>Explore our comprehensive curriculum designed to take you from beginner to advanced level in Excel and Power BI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Module selection
    module_options = {key: data['title'] for key, data in learning_content.items()}
    selected_module = st.selectbox(
        "Choose a module to learn:",
        options=list(module_options.keys()),
        format_func=lambda x: module_options[x],
        key="module_select"
    )
    
    # Display module content
    if selected_module in learning_content:
        module_data = learning_content[selected_module]
        
        st.markdown(f"""
        <div class="card">
            <h2>{module_data['title']}</h2>
            <p>{module_data['description']}</p>
            <div style="display: flex; gap: 20px;">
                <div><strong>Difficulty:</strong> {module_data['difficulty']}</div>
                <div><strong>Time:</strong> {module_data['estimated_time']}</div>
                <div><strong>Prerequisites:</strong> {', '.join([learning_content[p]['title'] for p in module_data['prerequisites']]) if module_data['prerequisites'] else 'None'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress = st.session_state.user_progress[selected_module]
        st.progress(progress / 100)
        st.caption(f"Progress: {progress}%")
        
        # Lessons
        st.markdown("### 📖 Lessons")
        for i, lesson in enumerate(module_data['lessons']):
            with st.expander(f"Lesson {i+1}: {lesson['title']} ({lesson['duration']})"):
                st.markdown(lesson['content'])
                
                if lesson.get('exercise'):
                    st.markdown(f"""
                    <div class="exercise-box">
                        <h4>💪 Exercise</h4>
                        <p>{lesson['exercise']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if lesson.get('video_link'):
                    st.video(lesson['video_link'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Mark as Completed", key=f"complete_{selected_module}_{i}"):
                        st.session_state.user_progress[selected_module] = min(100, progress + (100 / len(module_data['lessons'])))
                        st.success("Lesson marked as completed!")
                        st.rerun()
                with col2:
                    if st.button("Take Notes", key=f"notes_{selected_module}_{i}"):
                        st.session_state.current_lesson = {
                            'module': selected_module,
                            'lesson': i,
                            'title': lesson['title']
                        }
        
        # Quiz section
        if selected_module in quiz_questions:
            st.markdown("### 🧠 Knowledge Check")
            if st.button("Take Quiz", key=f"quiz_{selected_module}"):
                st.session_state.current_quiz = selected_module
            
            if 'current_quiz' in st.session_state and st.session_state.current_quiz == selected_module:
                score = 0
                total_points = 0
                
                for i, question in enumerate(quiz_questions[selected_module]):
                    st.markdown(f"**{i+1}. {question['question']}** ({question['difficulty']} - {question['points']} points)")
                    answer = st.radio(
                        "Select your answer:",
                        options=question['options'],
                        key=f"q_{selected_module}_{i}",
                        index=None
                    )
                    
                    if answer:
                        if answer == question['options'][question['correct']]:
                            score += question['points']
                            st.success(f"✅ Correct! {question['explanation']}")
                        else:
                            st.error(f"❌ Incorrect. {question['explanation']}")
                    
                    total_points += question['points']
                    st.markdown("---")
                
                if score > 0:
                    st.markdown(f"### 📊 Quiz Results: {score}/{total_points} points ({round(score/total_points*100)}%)")
                    
                    if score / total_points >= 0.7:
                        st.balloons()
                        st.success("Congratulations! You've passed this quiz.")
                        if st.session_state.user_progress[selected_module] < 100:
                            st.session_state.user_progress[selected_module] = min(100, st.session_state.user_progress[selected_module] + 10)
                    else:
                        st.warning("Keep studying and try again later.")
        
        # Resources
        if module_data.get('resources'):
            st.markdown("### 📚 Resources")
            for resource in module_data['resources']:
                st.markdown(f"- {resource}")
        
        # Case studies
        if selected_module in case_studies:
            st.markdown("### 🎯 Real-World Case Studies")
            for case in case_studies[selected_module]:
                with st.expander(case['title']):
                    st.markdown(case['description'])
                    st.markdown("**Tasks:**")
                    for task in case['tasks']:
                        st.markdown(f"- {task}")
                    st.markdown("**Learning Outcomes:**")
                    for outcome in case['learning_outcomes']:
                        st.markdown(f"- {outcome}")
                    
                    if st.button("Start Case Study", key=f"case_{selected_module}_{case['title']}"):
                        st.info("Case study instructions would appear here")

# Practice Lab Tab
with tab3:
    st.markdown("""
    <div class="card">
        <h2>Practice Lab</h2>
        <p>Apply what you've learned with these hands-on exercises and challenges.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📝 Excel Exercises</h3>
        </div>
        ""', unsafe_allow_html=True)
        
        # Display Excel exercises
        for module, exercises in practice_exercises.items():
            if module.startswith('excel'):
                for exercise in exercises:
                    with st.expander(f"{exercise['title']} ({exercise['difficulty']})"):
                        st.markdown(exercise['description'])
                        st.markdown("**Objectives:**")
                        for objective in exercise['objectives']:
                            st.markdown(f"- {objective}")
                        st.markdown("**Estimated Time:** " + exercise['estimated_time'])
                        st.markdown("**Skills:** " + ", ".join(exercise['skills']))
                        
                        if st.button("Start Exercise", key=f"start_{exercise['title']}"):
                            st.session_state.current_exercise = exercise
                            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Power BI Challenges</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder for Power BI exercises
        powerbi_exercises = [
            {
                "title": "Sales Dashboard",
                "description": "Create an interactive sales performance dashboard",
                "level": "Intermediate",
                "time": "45 min"
            },
            {
                "title": "Customer Analytics Report",
                "description": "Analyze customer data and create visual insights",
                "level": "Advanced",
                "time": "60 min"
            }
        ]
        
        for exercise in powerbi_exercises:
            with st.expander(f"{exercise['title']} ({exercise['level']})"):
                st.write(exercise['description'])
                st.caption(f"Estimated time: {exercise['time']}")
                if st.button("Start Exercise", key=f"powerbi_{exercise['title']}"):
                    st.info("Power BI exercise instructions would appear here")
    
    # Data playground
    st.markdown("""
    <div class="card">
        <h3>🔧 Data Playground</h3>
        <p>Practice with sample datasets and test your skills.</p>
    </div>
    """, unsafe_allow_html=True)
    
    dataset_option = st.selectbox(
        "Choose a sample dataset:",
        ["Sales Data", "HR Analytics", "Financial Data", "Marketing Campaign", "Supply Chain"]
    )
    
    if dataset_option:
        # Generate sample data based on selection
        if dataset_option == "Sales Data":
            data = {
                'Date': pd.date_range('2023-01-01', periods=100, freq='D'),
                'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], 100),
                'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
                'Sales': np.random.randint(100, 5000, 100),
                'Units': np.random.randint(1, 100, 100),
                'Customer_Rating': np.random.randint(1, 6, 100)
            }
            df = pd.DataFrame(data)
        elif dataset_option == "HR Analytics":
            data = {
                'Employee': [f'Emp{1000+i}' for i in range(50)],
                'Department': np.random.choice(['Sales', 'Marketing', 'IT', 'HR', 'Finance'], 50),
                'Salary': np.random.randint(40000, 120000, 50),
                'Tenure': np.random.randint(1, 15, 50),
                'Performance': np.random.randint(1, 11, 50),
                'Engagement': np.random.randint(1, 6, 50)
            }
            df = pd.DataFrame(data)
        
        # Display dataset
        st.dataframe(df.head(10))
        
        # Dataset statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Data Types", len(df.dtypes.unique()))
        
        # Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="Download Dataset",
                data=df.to_csv(index=False),
                file_name=f"{dataset_option.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        with col2:
            if st.button("Analyze with Excel"):
                st.info("This would open Excel with the dataset for analysis")
        with col3:
            if st.button("Visualize with Power BI"):
                st.info("This would open Power BI with the dataset for visualization")

# Progress Analytics Tab
with tab4:
    st.markdown("""
    <div class="card">
        <h2>Progress Analytics</h2>
        <p>Track your learning journey and see your skills improve over time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skill progression
        st.markdown("""
        <div class="card">
            <h3>📊 Skill Progression</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate mock skill progression data
        skills = ['Formulas', 'Charts', 'PivotTables', 'DAX', 'Data Modeling', 'Dashboard Design']
        levels = [random.randint(20, 100) for _ in skills]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=levels,
            theta=skills,
            fill='toself',
            name='Current Skills',
            line_color='#00B4D8'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Learning statistics
        st.markdown("""
        <div class="card">
            <h3>📈 Learning Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate mock learning data
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        time_spent = np.random.randint(10, 120, 30)
        modules = np.random.choice(list(st.session_state.user_progress.keys()), 30)
        
        learning_history = pd.DataFrame({
            'Date': dates,
            'Time_Spent': time_spent,
            'Module': modules
        })
        
        # Time spent chart
        fig = px.line(learning_history, x='Date', y='Time_Spent', 
                     title='Time Spent Learning (Last 30 Days)')
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Achievement timeline
        st.markdown("""
        <div class="card">
            <h3>🏆 Achievement Timeline</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mock achievement data
        achievements = [
            {'date': '2023-01-15', 'achievement': 'Completed Excel Basics', 'points': 100},
            {'date': '2023-02-03', 'achievement': 'Mastered 25 Formulas', 'points': 50},
            {'date': '2023-02-28', 'achievement': 'Created First Dashboard', 'points': 75},
            {'date': '2023-03-15', 'achievement': 'Power BI Fundamentals Certified', 'points': 150}
        ]
        
        for achievement in achievements:
            st.markdown(f"""
            <div class="success-box">
                <h4>{achievement['date']}</h4>
                <p>{achievement['achievement']}</p>
                <p>+{achievement['points']} points</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Module distribution
        st.markdown("""
        <div class="card">
            <h3>📚 Module Distribution</h3>
        </div>
        """, unsafe_allow_html=True)
        
        module_counts = learning_history['Module'].value_counts()
        fig = px.pie(values=module_counts.values, names=module_counts.index,
                    title='Time Distribution Across Modules')
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Learning analytics
    st.markdown("""
    <div class="card">
        <h3>🔍 Learning Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Learning Hours", "42.5", "+5.2h")
    with col2:
        st.metric("Average Session Length", "38min", "+4min")
    with col3:
        st.metric("Peak Learning Time", "10:00 AM", "-1h")
    
    # Weekly learning pattern
    st.markdown("#### 📅 Weekly Learning Pattern")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [2.5, 3.2, 1.8, 2.7, 3.5, 4.2, 2.0]
    
    fig = px.bar(x=days, y=hours, title='Average Daily Learning Hours')
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        xaxis_title='Day of Week',
        yaxis_title='Hours'
    )
    st.plotly_chart(fig, use_container_width=True)

# This is a sample sequence generator that might have been causing the error
# If you need to create a sequence of numbers and their squares and cubes, use this:
def generate_number_sequence(n):
    seq = pd.DataFrame({"n": np.arange(1, n+1), "n^2": np.arange(1, n+1)**2, "n^3": np.arange(1, n+1)**3})
    return seq

# Example usage (uncomment if needed):
# number_sequence = generate_number_sequence(10)
# st.write(number_sequence)
