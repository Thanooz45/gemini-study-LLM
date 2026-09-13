# 🎓 AI Study Companion

An interactive AI-powered tutoring application built with **Streamlit** and the **Google GenAI SDK**, powered by **Gemini Flash**. The assistant adapts its explanations to match your preferred learning style through customizable pedagogical personas.

🔗 **Live Demo:** [study-llm-workspace.streamlit.app](https://study-llm-workspace.streamlit.app/)

---

## ✨ Features

- **Multiple Tutor Personas:**
  - **Friendly Guide:** Enthusiastic and beginner-friendly, using intuitive everyday analogies.
  - **Academic Professor:** Rigorous, formal terminology with structured breakdowns and theoretical context.
  - **Socratic Tutor:** Promotes active recall by asking guided questions instead of providing direct answers.
- **Real-Time Streaming Responses:** Outputs stream token-by-token for low perceived latency.
- **Flexible Authentication:** Reads `GEMINI_API_KEY` seamlessly from Streamlit Secrets / environment variables, with support for direct manual input via the sidebar.
- **Responsive UI:** Custom CSS styling designed for clean readability across desktop and mobile browsers.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** Streamlit
- **LLM Engine:** Google Gemini API (`gemini-3.6-flash` / `gemini-2.5-flash`)
- **SDK:** `google-genai`
- **Language:** Python 3.10+

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd <your-repo-name>
