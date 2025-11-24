# 💸 **FinAI — Your Intelligent Financial Advisor**

> **Hyper-personalized. Multilingual. Voice-Enabled.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangChain](https://img.shields.io/badge/LangChain-Agents-orange)
![Llama 3](https://img.shields.io/badge/Model-Llama%203.1-purple)

**FinAI** is a robust, multi-agent financial advisory system built for high-speed, context-aware financial planning.  
Leveraging **Llama 3.1 (via Groq)**, it transforms unstructured transaction data into actionable insights through a seamless **voice-enabled interface**.

Architected by **Nithin G** (JSSSTU), this project builds upon the multi-agent reasoning frameworks developed for *AcadMate*.

---

## 🧠 **The Core: Multi-Agent Architecture**

FinAI uses a **System of Agents**, each with a distinct responsibility, working together to provide holistic financial intelligence.

### **1. 👤 Profile Agent**
The central memory & state manager.
- Holds user preferences, history, and financial goals.
- Maintains long-term advisory context.
- Persists data securely to `user_profile.json`.

### **2. 💸 Expense Agent**
Real-time expense parser & classifier.
- Parses transaction text directly from mobile notifications.
- Extracts merchant, amount, and category.
- Supports UPI apps like **GPay**, **PhonePe**, and SMS alerts.

### **3. 📈 Investment Agent**
Your AI financial strategist.
- Uses user profile + expense history.
- Pulls market news via **GNews**.
- Generates personalized investment guidance in clean, readable Markdown.

---

## 🚀 **Key Features**

### 🗣️ **Multilingual Voice Interface**
- Supports **English** and **Kannada** output.
- Uses server-side **Text-to-Speech (gTTS)** for reliable audio playback.

### 📲 **Automated Expense Tracking**
- Reads and processes mobile notifications.
- Updates spending summary in real-time.

### 🛡️ **Persistent Financial Memory**
- Maintains user-specific state over sessions.
- Saves goals, preferences, and transaction history.

### ⚡ **Fast, Low-Latency Model Inference**
- Powered by the **Groq API** for high-speed Llama 3.1 responses.

---

## 🛠 **Tech Stack**

| Domain | Technologies |
|-------|--------------|
| **LLM & Agents** | LangChain, Groq API (Llama 3.1), Pydantic |
| **Backend Framework** | Python, FastAPI |
| **Live Data** | GNews API |
| **Audio Processing** | gTTS (TTS), Google SpeechRecognition (STT), pydub, ffmpeg |
| **Frontend Prototype** | HTML5, Tailwind CSS, Vanilla JS |

---

# ⚙️ **Setup & Installation**

## **1. Prerequisites**
- Python **3.10+**
- Git
- **FFmpeg** (Required for audio processing)

### Install FFmpeg
**Windows**
```bash
choco install ffmpeg
```

## **2. Clone the repo**
```bash
- git clone https://github.com/17nithinnayak/FinAI.git
- cd FinAI
```

## **3. Create Virtual Environment**
```bash
- python -m venv venv
- .\venv\Scripts\activate
```
## **4. Install requirements**
```bash
- pip install -r requirements.txt
```
## **5. Add API Keys**
- You will need:
```bash
Groq API Key (get from GroqCloud)
GNews API Key
```

## **6. Run the Backend**
```bash
- uvicorn main:app --reload --host 0.0.0.0
```
