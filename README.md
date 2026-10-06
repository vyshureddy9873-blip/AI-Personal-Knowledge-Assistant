# 📚 AI Personal Knowledge Assistant

## 📌 Project Overview

AI Personal Knowledge Assistant is a local AI-powered application that allows users to upload PDF documents and ask questions about their own documents.

The system extracts information from uploaded PDFs, stores the document information in a local knowledge base, retrieves relevant information for a user's question, and uses a local AI model to generate a short and clear answer.

The application is designed to provide a simple and private way to interact with personal documents using AI.

---

## 🎯 Objectives

The main objectives of this project are:

- To allow users to upload PDF documents.
- To extract useful information from PDF files.
- To create a searchable personal knowledge base.
- To retrieve relevant information based on user questions.
- To generate natural-language answers using a local AI model.
- To display the source document and page used for the answer.
- To keep the document processing local for better privacy.

---

## ✨ Features

### 📄 PDF Upload

Users can upload one or more PDF documents through the Streamlit interface.

### 🧠 Personal Knowledge Base

The uploaded document information is stored in a local ChromaDB collection.

### 💬 Natural Language Questions

Users can ask questions in normal language instead of searching for exact keywords.

### 🤖 AI Answers

Ollama with the Llama 3.2 model generates short and clear answers based on the retrieved document information.

### 📑 Source References

The application displays the PDF file name and page number used to generate the answer.

### 🔒 Local Processing

The project uses a local AI model through Ollama, so no cloud AI API key is required.

### 🗑️ Knowledge Base Management

Users can clear the existing knowledge base and create a new one.

---

## 🏗️ System Architecture

```text
                 📄 PDF Document
                       │
                       ▼
                PDF Text Extraction
                       │
                       ▼
                  Text Chunking
                       │
                       ▼
                   ChromaDB
              Local Knowledge Base
                       │
                       │
              💬 User Question
                       │
                       ▼
                Relevant Search
                       │
                       ▼
                Relevant Context
                       │
                       ▼
                  Ollama
                 Llama 3.2
                       │
                       ▼
                 🤖 AI Answer
                       │
                       ▼
              📑 Source + Page
