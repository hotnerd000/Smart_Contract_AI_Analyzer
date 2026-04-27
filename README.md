# 🛡️ AI Smart Contract Auditor Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Web3](https://img.shields.io/badge/Web3-Smart%20Contracts-purple)
![AI](https://img.shields.io/badge/AI-LLM-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

![Demo](demo.gif)

## 🚀 Overview
This project is an **AI-powered Smart Contract Auditor Agent** designed to analyze blockchain contracts dynamically using an agent-based architecture.

Unlike traditional analyzers, this system **decides what to do next** based on the current state:
👉 Think → Act → Observe → Repeat

---

## 🚀 Features

- 🤖 AI-powered smart contract analysis  
- 🧠 Agent-based decision system (dynamic step selection)  
- 🔁 Multi-model fallback via OpenRouter (Nemotron, Gemma, Mistral)  
- 🔍 Static vulnerability detection (Reentrancy, Delegatecall, tx.origin, etc.)  
- 🌐 Smart contract fetching via Etherscan API  
- 📊 AI-generated risk scoring and explanations  
- 🧾 Structured JSON output for integration  
- 📡 Step-by-step logging system for debugging  
- ⚡ Retry + fallback handling for rate-limited models  
- 🧱 Clean modular architecture  

---

## 🤖 AI Agent Architecture

This project implements a simple but powerful agent loop:

1. 🧠 Decide next action  
2. ⚙️ Execute tool (fetch, analyze, AI)  
3. 📊 Observe result  
4. 🔁 Repeat until done  

---

## 🛠 Tech Stack

- 🐍 Python  
- 🤖 OpenRouter API  
- 🌐 Etherscan API  
- 📊 Logging system  
- 🧠 AI Agent architecture  

---

## 🧠 How It Works

1. User enters a contract address  
2. Tool fetches verified source code from Etherscan  
3. Static analysis detects known vulnerabilities  
4. AI analyzes deeper patterns and provides insights  
5. Results are merged and displayed in terminal  

---

## 🛠️ Tech Stack

- Python
- Requests (API calls)
- OpenRouter (LLMs)
- Etherscan API (contract source)
- dotenv (environment variables)

---

## 📁 Project Structure

- main.py → Entry point  
- agent.py → Agent loop & decision logic  
- tools.py → Tool functions  
- analyzer.py → Static vulnerability detection  
- etherscan.py → Contract fetching  
- logger.py → Logging system  
- config.py → API setup  

---

## 🎥 Demo

```bash
$ python main.py
```

🔎 Smart Contract AI Analyzer

Enter contract address: 0xdAC17F...

🚨 Risk Score: 6/10 (MEDIUM)

⚠️ Detected Issues:
- Reentrancy Risk (high)

🧠 AI Insights:
...

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/hotnerd000/AI_Resume_Analyzer.git
cd smart-contract-ai-analyzer
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
OPENROUTER_API_KEY=your_api_key_here
ETHERSCAN_API_KEY=your_etherscan_key_here
```

---

## ▶️ Usage

Run the tool:

```bash
python main.py
```

Then enter a contract address:

```text
Enter contract address: 0xdAC17F958D2ee523a2206206994597C13D831ec7
```

---

## 📊 Example Output

```
🚨 Risk Score: 6/10 (MEDIUM)

⚠️ Detected Issues:
- Reentrancy Risk (high)
- Missing Access Control (medium)

🧠 AI Insights:
The contract shows moderate risk due to external call usage...
```

---

## 🔍 Detected Vulnerabilities

- Reentrancy attacks
- Missing access control
- tx.origin misuse
- delegatecall risks
- Integer overflow (older Solidity)
- Selfdestruct usage

---

## ⚠️ Limitations

- Keyword-based detection (not full static analysis)  
- Depends on verified contracts  
- AI responses may vary 

---

## 🎯 Why This Project Matters

This project demonstrates:
- 🧠 AI Agent system design  
- 🔗 Web3 security analysis  
- ⚙️ Production-level engineering patterns  

---

## 🔮 Future Improvements

- 🔍 Integrate Slither for deeper analysis  
- 🤖 Multi-agent system  
- 🌐 Web dashboard for visualization  
- 📊 Dataset generation for training  

---

## 💼 Use Cases

- Web3 developers testing contracts
- Security researchers
- DeFi project teams
- Freelancers offering audit pre-check tools

---

## 👨‍💻 Author

Built by Hotnerd000

AI + Web3 Developer specializing in:
- Smart contract analysis
- AI-powered tools
- Blockchain security

Available for freelance projects.

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!
