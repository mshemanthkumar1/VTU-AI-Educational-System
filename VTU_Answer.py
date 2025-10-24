import streamlit as st
from datetime import datetime
import google.generativeai as genai
import time

# Page Configuration
st.set_page_config(
    page_title="VTU CS Answer Generator - FREE AI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap');
    
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        font-family: 'Fira Code', monospace;
    }
    
    .answer-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.8;
    }
    
    .memory-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f39c12;
        margin: 15px 0;
        font-weight: bold;
    }
    
    .key-points {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .ai-free-badge {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)


class FreeAIVTUGenerator:
    """VTU Answer Generator with FREE Google Gemini AI"""
    
    def __init__(self, api_key=None):
        """Initialize with Gemini API"""
        self.api_key = api_key
        self.ai_enabled = False
        
        if self.api_key and len(self.api_key) > 20:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.ai_enabled = True
            except Exception as e:
                self.ai_enabled = False
                self.error = str(e)
        
        # CS Topics Database (Fallback)
        self.cs_topics = {
            "data structure": {
                "definition": "A data structure is a specialized format for organizing, processing, storing, and retrieving data efficiently.",
                "mnemonic": "DASA - Data, Access, Store, Arrange",
                "types": ["Arrays (Fixed size)", "Linked Lists (Dynamic)", "Stacks (LIFO)", "Queues (FIFO)", "Trees (Hierarchical)", "Graphs (Networks)"],
                "memory_tip": "Remember ALSTG: Arrays, Lists, Stacks, Trees, Graphs",
                "advantages": ["Fast access O(1)", "Efficient storage", "Easy manipulation", "Code reusability"],
                "applications": ["Database indexing", "OS memory management", "Compiler design"],
                "exam_tip": "Always draw diagram for stacks/queues. Mention time complexity."
            },
            "algorithm": {
                "definition": "An algorithm is a step-by-step procedure to solve a problem with finite steps.",
                "mnemonic": "FIUDA - Finite, Input, Unambiguous, Definite, Achievable",
                "types": ["Sorting (arrange data)", "Searching (find data)", "Graph (path finding)", "Dynamic (optimal solutions)"],
                "memory_tip": "Remember SSGD: Sort, Search, Graph, Dynamic",
                "advantages": ["Systematic approach", "Reusable code", "Analyzable performance", "Language independent"],
                "applications": ["Google search", "GPS navigation", "Social media feeds"],
                "exam_tip": "Always mention time/space complexity. Draw flowchart if asked."
            },
            "oops": {
                "definition": "Object-Oriented Programming organizes code around objects containing data and methods.",
                "mnemonic": "APIE - Abstraction, Polymorphism, Inheritance, Encapsulation",
                "concepts": [
                    "Encapsulation: Data hiding (Private variables)",
                    "Inheritance: Code reuse (Parent-Child)",
                    "Polymorphism: Many forms (Overloading/Overriding)",
                    "Abstraction: Hide complexity (Abstract classes)"
                ],
                "memory_tip": "Remember APIE like apple pie - sweet and easy!",
                "advantages": ["Code reusability", "Easy maintenance", "Data security", "Real-world modeling"],
                "applications": ["Java applications", "Game development", "GUI design"],
                "exam_tip": "Give real-world example like Car class with properties."
            },
            "dbms": {
                "definition": "Database Management System is software to create, manage, and manipulate databases.",
                "mnemonic": "ACID - Atomicity, Consistency, Isolation, Durability",
                "features": ["Data independence", "ACID properties", "Concurrent access", "Security & backup"],
                "memory_tip": "Remember ACID for transactions - it's battery acid!",
                "advantages": ["Reduced redundancy", "Data integrity", "Multi-user access", "Backup/recovery"],
                "applications": ["Banking systems", "E-commerce", "Airlines booking"],
                "exam_tip": "Draw ER diagram for 8+ marks. Explain ACID with examples."
            },
            "operating system": {
                "definition": "OS is system software managing hardware and providing services to applications.",
                "mnemonic": "PMFI - Process, Memory, File, I/O management",
                "functions": [
                    "Process Management (CPU scheduling)",
                    "Memory Management (RAM allocation)",
                    "File Management (Storage organization)",
                    "I/O Management (Device control)"
                ],
                "memory_tip": "Remember PMFI like 'PM for India' - manages everything!",
                "types": ["Batch OS", "Time-sharing OS", "Distributed OS", "Real-time OS"],
                "applications": ["Windows", "Linux", "MacOS", "Android"],
                "exam_tip": "Draw process states diagram. Explain scheduling algorithms."
            }
        }
    
    def generate_with_gemini(self, question):
        """Generate structured answer using FREE Gemini AI"""
        if not self.ai_enabled:
            return None
        
        try:
            # Structured prompt for memorable answers
            prompt = f"""You are a VTU Computer Science exam expert. Generate a complete, well-structured answer for:

Question: {question}

Format your answer EXACTLY like this structure:

📝 **DEFINITION**
[Clear, concise 2-line definition]

🧠 **MEMORY TIP (Mnemonic)**
[Create a catchy acronym or phrase to remember key points]

🔑 **KEY POINTS** (Number each point)
1. [First main point with brief explanation]
2. [Second main point with brief explanation]
3. [Third main point with brief explanation]
4. [Fourth main point with brief explanation]

✅ **ADVANTAGES** (4 points)
1. [Advantage 1]
2. [Advantage 2]
3. [Advantage 3]
4. [Advantage 4]

🌍 **REAL-WORLD APPLICATIONS** (3 examples)
1. [Application 1]
2. [Application 2]
3. [Application 3]

💡 **EXAM TIP**
[One line tip for VTU exams - like "Always draw diagram" or "Mention time complexity"]

Keep it concise but complete. Make it EASY TO REMEMBER for exams."""

            response = self.model.generate_content(prompt)
            answer = response.text
            
            return {
                "found": True,
                "answer": answer,
                "source": "Google Gemini AI (FREE)",
                "structured": True
            }
            
        except Exception as e:
            return {
                "found": False,
                "error": f"Gemini API Error: {str(e)}"
            }
    
    def generate_from_database(self, question):
        """Generate from local structured database"""
        question_lower = question.lower()
        
        # Find topic
        topic = None
        for key in self.cs_topics.keys():
            if key in question_lower:
                topic = key
                break
        
        if not topic:
            return {
                "found": False,
                "message": f"❌ Topic not found! Available: {', '.join(self.cs_topics.keys())}"
            }
        
        info = self.cs_topics[topic]
        
        # Structured answer format
        answer = f"""📝 **DEFINITION**
{info['definition']}

🧠 **MEMORY TIP (Mnemonic)**
{info.get('mnemonic', 'Remember the key points below')}

"""
        
        # Key Points
        if 'types' in info:
            answer += "🔑 **KEY TYPES**\n"
            for i, t in enumerate(info['types'], 1):
                answer += f"{i}. {t}\n"
        elif 'concepts' in info:
            answer += "🔑 **KEY CONCEPTS**\n"
            for i, c in enumerate(info['concepts'], 1):
                answer += f"{i}. {c}\n"
        elif 'functions' in info:
            answer += "🔑 **KEY FUNCTIONS**\n"
            for i, f in enumerate(info['functions'], 1):
                answer += f"{i}. {f}\n"
        
        answer += f"\n💡 **MEMORY TRICK**\n{info.get('memory_tip', 'Review these points regularly')}\n"
        
        # Advantages
        answer += "\n✅ **ADVANTAGES**\n"
        for i, adv in enumerate(info['advantages'], 1):
            answer += f"{i}. {adv}\n"
        
        # Applications
        answer += "\n🌍 **REAL-WORLD APPLICATIONS**\n"
        for i, app in enumerate(info['applications'], 1):
            answer += f"{i}. {app}\n"
        
        # Exam Tip
        answer += f"\n💡 **VTU EXAM TIP**\n{info.get('exam_tip', 'Practice writing this answer in 10 minutes')}"
        
        return {
            "found": True,
            "answer": answer,
            "source": "Structured Local Database",
            "topic": topic.title(),
            "structured": True
        }
    
    def generate_answer(self, question):
        """Main generation logic"""
        # Try Gemini first
        if self.ai_enabled:
            result = self.generate_with_gemini(question)
            if result and result.get('found'):
                return result
        
        # Fall back to structured database
        return self.generate_from_database(question)


# Initialize
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<p class="main-header">💻 VTU CS Answer Generator</p>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>FREE AI-Powered | Structured & Easy to Remember</h3>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FREE AI Configuration")
    
    st.info("""
    **Google Gemini API - 100% FREE!**
    
    ✅ Unlimited requests
    ✅ No credit card needed
    ✅ Better than ChatGPT for students
    """)
    
    api_key_input = st.text_input(
        "Google Gemini API Key (FREE)",
        type="password",
        value=st.session_state.api_key,
        help="Get FREE API key from: https://makersuite.google.com/app/apikey"
    )
    
    if st.button("🔑 Get FREE API Key", use_container_width=True):
        st.markdown("[Click here to get FREE Gemini API Key](https://makersuite.google.com/app/apikey)")
    
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.session_state.generator = FreeAIVTUGenerator(api_key=api_key_input if api_key_input else None)
    
    if st.session_state.generator is None:
        st.session_state.generator = FreeAIVTUGenerator()
    
    # Display mode
    st.markdown("---")
    if st.session_state.generator.ai_enabled:
        st.markdown('<div class="ai-free-badge">✨ FREE AI ACTIVE</div>', unsafe_allow_html=True)
        st.success("🚀 Google Gemini Connected!\nUnlimited topics available!")
    else:
        st.warning("📚 Offline Mode (5 topics)\nAdd API key for unlimited!")
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Special Features")
    st.success("""
    🧠 **Memory Mnemonics**
    Easy acronyms to remember
    
    📊 **Structured Format**
    Definition → Tips → Points
    
    💡 **Exam Tips**
    VTU-specific advice
    
    🎯 **Quick Recall**
    Designed for fast revision
    """)
    
    st.markdown("---")
    
    # Topics
    st.markdown("### 📚 Offline Topics")
    topics = list(st.session_state.generator.cs_topics.keys())
    for topic in topics:
        st.markdown(f"✓ {topic.title()}")
    
    st.markdown("---")
    st.metric("Questions Asked", len(st.session_state.history))

# Main Content
st.markdown("---")

# Question Input
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### ✍️ Enter Your CS Question")
    question = st.text_area(
        "",
        height=150,
        placeholder="Example: Explain data structures\n\nOr: What is OOPS? Explain its concepts\n\nOr: Define DBMS and its features",
        help="Any CS topic - AI will structure it for easy memory!"
    )

with col2:
    st.markdown("### 📊 Stats")
    if question:
        st.metric("Words", len(question.split()))
        if len(question.split()) >= 5:
            st.success("✅ Good")
        else:
            st.warning("⚠️ Add more")
    else:
        st.info("Type question")

# Generate Button
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    generate_btn = st.button("🚀 Generate Structured Answer", use_container_width=True, type="primary")

# Generate Answer
if generate_btn:
    if not question or len(question.strip()) < 5:
        st.error("⚠️ Please enter a valid question!")
    else:
        with st.spinner("🤖 AI is structuring your answer for easy memory..."):
            time.sleep(1)
            result = st.session_state.generator.generate_answer(question)
            
            if not result.get('found'):
                st.error(result.get('message') or result.get('error'))
            else:
                st.success("✅ Structured Answer Generated!")
                
                # Save history
                st.session_state.history.append({
                    "q": question,
                    "time": datetime.now(),
                    "source": result['source']
                })
                
                # Info
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.info(f"**🤖 Source:** {result['source']}")
                with info_col2:
                    st.info(f"**📊 Format:** Structured & Memorable")
                
                # Highlight box
                st.markdown('<div class="memory-box">🧠 This answer is formatted with mnemonics and memory tips for easy recall!</div>', unsafe_allow_html=True)
                
                # Display Answer
                st.markdown("---")
                st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                st.markdown(result['answer'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Actions
                st.markdown("---")
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    st.download_button(
                        "📥 Download",
                        data=result['answer'],
                        file_name=f"VTU_Answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col_a2:
                    if st.button("📋 Copy Format", use_container_width=True):
                        st.info("Select and copy the answer above!")
                
                with col_a3:
                    if st.button("🔄 New Question", use_container_width=True):
                        st.rerun()

# Sample Questions
st.markdown("---")
st.markdown("### 📝 Try These Questions")

samples = [
    "Explain data structures and types",
    "What is OOPS? List its concepts",
    "Define DBMS and advantages",
    "Explain operating system functions",
    "What are algorithms and their types"
]

cols = st.columns(5)
for i, sample in enumerate(samples):
    with cols[i]:
        if st.button(f"💡 Q{i+1}", use_container_width=True, key=f"s_{i}"):
            st.session_state.current = sample
            st.rerun()

# How to Get API Key
st.markdown("---")
with st.expander("🔑 How to Get FREE Google Gemini API Key (Step-by-Step)"):
    st.markdown("""
    ### **100% FREE - No Credit Card Needed!**
    
    **Step 1:** Visit https://makersuite.google.com/app/apikey
    
    **Step 2:** Click "Get API Key"
    
    **Step 3:** Click "Create API Key"
    
    **Step 4:** Copy the key (starts with "AIza...")
    
    **Step 5:** Paste it in the sidebar above
    
    **That's it!** 🎉
    
    **Benefits:**
    - ✅ Completely FREE
    - ✅ Unlimited requests
    - ✅ No credit card required
    - ✅ Works for any CS topic
    - ✅ Structured answers
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;'>
    <h3 style='color: #667eea;'>💻 VTU CS Answer Generator</h3>
    <p style='font-size: 1.2rem;'><strong>FREE AI</strong> Powered by <strong>Google Gemini</strong></p>
    <p style='margin-top: 15px;'>🧠 Structured Answers | 💡 Memory Mnemonics | 📊 Easy to Remember</p>
    <p style='margin-top: 10px;'>Perfect for VTU CS & Related Streams</p>
    <p style='margin-top: 20px; font-size: 0.9rem;'>© 2025 | Made with ❤️ for VTU Students</p>
</div>
""", unsafe_allow_html=True)
