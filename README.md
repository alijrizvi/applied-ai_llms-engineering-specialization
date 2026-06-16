# Applied AI Engineering Specialization - LLMs

A polished proof-of-concept demonstrating applied prompt engineering for business analytics.

---

# DocuMind: End-to-End Automated Agentic Workflow System

## 🎯 Project Overview

**DocuMind** is a comprehensive AI Engineering capstone project demonstrating an end-to-end automated agentic workflow system. This project synthesizes five advanced courses in AI/LLM engineering, showcasing the progression from foundational prompt engineering to production-grade agentic systems with RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol) server architecture.

The system is deployed as an interactive Streamlit dashboard, providing a real-world demonstration of autonomous AI agents orchestrating complex multi-step workflows with knowledge retrieval, memory management, and intelligent decision-making.

### **Live Deployment:** [Streamlit Cloud Dashboard](https://end-to-end-ai-eng-automated-agent-capstone-alijr.streamlit.app)

<img width="1417" height="666" alt="Screenshot 2026-06-16 at 10 16 00 AM" src="https://github.com/user-attachments/assets/f1f72385-66c1-496d-93fc-570b298997ec" />

---

## 📚 Learning Path Integration

This capstone project is the culmination of a structured 5-course AI Engineering specialization:

(All courses from **DeepLearning.AI** were taught by Dr. Andrew Ng)

### **Course 1: ChatGPT Prompt Engineering for Developers** (DeepLearning.AI)
- **Focus:** Foundational prompt engineering techniques
- **Key Skills:** Structured prompting, role-based prompting, few-shot learning
- **Application in Capstone:** Core prompt templates for agent reasoning and decision-making

### **Course 2: Building Systems with the ChatGPT API** (DeepLearning.AI)
- **Focus:** Production-grade LLM system orchestration
- **Key Skills:** API integration, workflow design, error handling, cost optimization
- **Application in Capstone:** API pipeline architecture and system reliability patterns

### **Course 3: LangChain for LLM Application Development** (DeepLearning.AI)
- **Focus:** Advanced composition and chaining patterns for LLM applications
- **Key Skills:** Chain orchestration, memory management, tool integration, prompt templates
- **Application in Capstone:** LangChain-based agent framework and workflow composition

### **Course 4: Agentic AI** (DeepLearning.AI)
- **Focus:** Autonomous decision-making systems and multi-step reasoning
- **Key Skills:** Agent design patterns, tool use, planning, reflection loops
- **Application in Capstone:** Core agentic system with autonomous task execution

### **Course 5: Building RAG and MCP Servers with Claude** (Edureka!/Coursera)
- **Focus:** Knowledge retrieval systems and AI server architecture
- **Key Skills:** RAG implementation, vector databases, MCP server design, knowledge management
- **Application in Capstone:** ChromaDB-based RAG store and MCP server integration

---

## 🏗️ Technical Architecture

### **System Components**

─────────────────────────────────────────────────────────────┐ │ Streamlit Frontend (app.py) │ │ Interactive Dashboard & User Interface │ └────────────────────┬────────────────────────────────────────┘ │ ┌────────────────────▼────────────────────────────────────────┐ │ Pipeline Orchestration │ │ (pipeline.py) - Workflow coordination & execution │ └────────────────────┬────────────────────────────────────────┘ │ ┌────────────┼────────────┐ │ │ │ ┌───────▼──┐ ┌──────▼──┐ ┌─────▼──────┐ │ Agents │ │ Memory │ │ RAG Store │ │(agents.py) │(memory.py) │(rag_store.py) └──────────┘ └─────────┘ └────────────┘ │ │ │ └────────────┼────────────┘ │ ┌────────────▼────────────┐ │ LLM Integration │ │ (OpenAI GPT-4 API) │ │ (Claude via MCP) │ └────────────────────────┘ │ ┌────────────▼────────────┐ │ Knowledge Base │ │ (ChromaDB Vector DB) │ │ (MCP Servers) │ └────────────────────────┘


# 📊 Project Insights & Learnings

## Technical Achievements

### 1: End-to-End System Design

* Integrated 5 distinct AI engineering concepts into a cohesive system
* Demonstrated production-ready architecture patterns
* Implemented scalable multi-agent orchestration

### 2: Advanced LLM Orchestration

* Mastered prompt engineering for complex reasoning tasks
* Implemented sophisticated chain composition patterns
* Optimized API usage and cost efficiency

### 3: Knowledge Management at Scale

* Built semantic search capabilities with vector embeddings
* Implemented RAG for context-aware responses
* Designed persistent knowledge storage systems

### 4: Agentic AI Implementation

* Created autonomous decision-making systems
* Implemented tool-use and function calling
* Built reflection and self-correction mechanisms

### 5: Production Deployment

* Deployed interactive dashboard to Streamlit Cloud
* Implemented environment-based configuration
* Designed for scalability and maintainability

## Key Learnings
* **Prompt Engineering is Foundational:** Effective prompts are critical for agent reasoning quality
* **Composition Over Monoliths:** Modular chain design enables flexibility and reusability
* **Memory is Essential:** Proper context management dramatically improves multi-turn interactions
* **RAG Bridges Knowledge Gaps:** Retrieval-augmented generation enables grounding in domain knowledge
* **Agentic Systems Require Careful Design:** Tool selection, planning, and reflection loops are crucial
* **Production Readiness Matters:** Error handling, logging, and monitoring are non-negotiable
