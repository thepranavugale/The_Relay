# The_Relay – Assistant Conversation History & Prompt Log

## 1. Introduction

This document summarizes how I used an AI assistant during the development of The_Relay, a research-paper question-answering system.

The assistant helped me understand implementation steps, debug errors, plan experiments, review code, interpret results, and prepare project documentation.

This is a reconstructed summary of the main prompts and interactions, not a verbatim export of the complete conversation history.

## 2. Project Setup and Architecture

**Objective:** Set up the Python project and organize its modules.

**Representative prompts:**
- Help me build The_Relay step by step using Python in VS Code.
- Explain the project folder structure and the purpose of each file.
- Guide me through setting up a virtual environment and installing dependencies.
- Help me configure environment variables safely using a `.env` file.

**Assistant contribution:**
- Suggested a modular project structure.
- Explained virtual environment setup.
- Helped configure dependencies and environment variables.
- Provided incremental implementation guidance.

## 3. Research Paper Loading and Processing

**Objective:** Load research papers and convert their contents into searchable text chunks.

**Representative prompts:**
- Help me download and process research papers using Python.
- Create a paper loader that extracts PDF text and splits it into chunks.
- Explain how to organize processed research-paper data.

**Assistant contribution:**
- Helped implement PDF loading.
- Guided text extraction and chunk creation.
- Helped organize paper metadata, page numbers, and text chunks.

## 4. Retrieval System

**Objective:** Implement TF-IDF-based retrieval.

**Representative prompts:**
- Help me implement a TF-IDF retriever for research-paper chunks.
- Explain how to retrieve the most relevant chunks for a question.
- Help me compare retrieval settings using different top_k values.
- Explain why lexical similarity can return irrelevant research-paper chunks.

**Assistant contribution:**
- Helped implement the `PaperRetriever` class.
- Explained TF-IDF retrieval.
- Guided retrieval comparison experiments.
- Helped identify limitations of lexical retrieval.

## 5. Groq API Integration

**Objective:** Connect the project to a hosted language model.

**Representative prompts:**
- Help me integrate the Groq API into my Python project.
- Create a Groq client with configurable model settings.
- Help me handle API errors and request timeouts.
- Explain how to use a stand-in model for testing without external API calls.

**Assistant contribution:**
- Guided Groq API integration.
- Helped configure the model and API settings.
- Supported implementation of the configurable StandInModel.
- Explained the difference between a real hosted service and a simulated service.

## 6. Citation Validation and Pipeline

**Objective:** Build a complete question-answering pipeline with citation checks.

**Representative prompts:**
- Help me connect retrieval and answer generation into one pipeline.
- Create citation extraction and validation functions.
- Check whether generated citations match the retrieved paper and page references.
- Help me display answers and citation-validation results.

**Assistant contribution:**
- Guided implementation of `pipeline.py`.
- Helped implement citation extraction and validation.
- Explained the difference between citation-reference validity and factual support.

## 7. Reliability Mechanisms

**Objective:** Implement rate limiting, retries, and logging.

**Representative prompts:**
- Help me implement a token-bucket rate limiter.
- Implement exponential backoff with jitter for retry handling.
- Explain how to handle temporary API failures.
- Help me implement application logging.

**Assistant contribution:**
- Guided rate-limiter implementation.
- Helped implement retry handling.
- Explained retryable errors and backoff.
- Supported logging and debugging.

## 8. Testing and Experiments

**Objective:** Evaluate system behavior under different conditions.

**Representative prompts:**
- Help me design steady-load, burst-load, and sustained-concurrency tests.
- Create experiments to compare the real API and stand-in model.
- Help me evaluate answer quality using 15 research questions.
- Compare retrieval settings with top_k values of 2, 4, and 8.
- Simulate reduced request limits and exhausted daily budgets.

**Assistant contribution:**
- Helped plan and implement experiment scripts.
- Guided execution and debugging.
- Helped interpret latency, success rates, retrieval timings, and manual answer grades.
- Helped distinguish simulated results from actual provider measurements.

## 9. Debugging and Result Analysis

**Objective:** Resolve implementation errors and understand experiment outputs.

**Representative prompts:**
- Help me debug Python import errors.
- Explain API rate-limit errors and how to retry failed questions.
- Help me inspect invalid citations and missing answers.
- Explain the output of my experiment scripts.
- Help me merge experiment results into the required CSV format.

**Assistant contribution:**
- Reviewed terminal errors and outputs.
- Suggested corrections to scripts.
- Guided retrying failed API requests.
- Helped inspect and merge experimental records.
- Helped maintain the required results CSV columns.

## 10. Documentation and Final Report

**Objective:** Prepare the project report and submission materials.

**Representative prompts:**
- Help me prepare the final project report using the assignment's required headings.
- Summarize the experimental results accurately.
- Explain the limitations of my experiments.
- Help me fit the final report within the two-page limit.
- Help me prepare the project for GitHub submission.

**Assistant contribution:**
- Helped organize the report into the required 12 sections.
- Supported interpretation of experimental results.
- Helped document limitations and lessons learned.
- Assisted with preparing a concise PDF report.

## 11. GitHub and Submission Preparation

**Objective:** Upload the completed project and prepare submission files.

**Representative prompts:**
- Guide me step by step to upload The_Relay to GitHub.
- Help me configure Git and connect the remote repository.
- Explain Git push errors and how to resolve them.
- Guide me through uploading the final PDF report.
- Help me prepare the remaining submission requirements.

**Assistant contribution:**
- Guided Git initialization and commit creation.
- Helped connect the GitHub remote.
- Guided the first push to the main branch.
- Assisted with uploading the final PDF report.

**GitHub Repository:**  
https://github.com/thepranavugale/The_Relay

## 12. Overall Reflection

I used the AI assistant as a development and learning aid rather than relying on it to complete the entire project independently.

I executed commands, tested the implementation, shared terminal outputs, reviewed experiment results, and made changes based on the debugging and explanations.

This incremental approach helped me understand the system architecture, retrieval behavior, API integration, reliability mechanisms, testing methodology, and project documentation.

The final implementation and experimental results were executed and reviewed in my local development environment.