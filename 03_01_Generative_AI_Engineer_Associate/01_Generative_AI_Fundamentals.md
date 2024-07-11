# Generative AI Engineer Associate: Theorie 80-20%


## Index

- [01 Generative AI Solution Development](#01-generative-ai-solution-development)
  - [01.01 Retrieval-Augmented Generation (RAG)](#0101-retrieval-augmented-generation-rag)
  - [01.02 Preparing Data for RAG Solutions](#0102-preparing-data-for-rag-solutions)
  - [01.03 Vector Search](#0103-vector-search)
  - [01.04 Assembling and Evaluating a RAG Application](#0104-assembling-and-evaluating-a-rag-application)
  - [01.05 DBC](#0105-dbc)
- [02 Generative AI Application Development](#02-generative-ai-application-development)
  - [02.01 Foundations of Compound AI Systems](#0201-foundations-of-compound-ai-systems)
  - [02.02 Building Multi-stage Reasoning Chains](#0202-building-multi-stage-reasoning-chains)
  - [02.03 Agents and Cognitive Architectures](#0203-agents-and-cognitive-architectures)
  - [02.04 DBC](#0204-dbc)
- [03 Generative AI Application Evaluation and Governance](#03-generative-ai-application-evaluation-and-governance)
  - [03.01 The Importance of Evaluating GenAI Applications](#0301-the-importance-of-evaluating-genai-applications)
  - [03.02 Securing and Governing GenAI Applications](#0302-securing-and-governing-genai-applications)
  - [03.03 Gen AI Evaluation Techniques](#0303-gen-ai-evaluation-techniques)
  - [03.04 End-to-end App. Evaluation](#0304-end-to-end-app-evaluation)
  - [03.05 DBC](#0305-dbc)
- [04 Generative AI Application Deployment and Monitoring](#04-generative-ai-application-deployment-and-monitoring)
  - [04.01 Model Deployment Fundamentals](#0401-model-deployment-fundamentals)
  - [04.02 Batch Deployment](#0402-batch-deployment)
  - [04.03 Real-time Deployment](#0403-real-time-deployment)
  - [04.04 AI System Monitoring](#0404-ai-system-monitoring)
  - [04.05 LLMOps Concepts](#0405-llmops-concepts)
  - [04.06 DBC](#0406-dbc)

### 01 Generative AI Solution Development

#### 01.01 Retrieval-Augmented Generation (RAG)

- **Leaning Objetives**: 
  - RAG, prompt engineering, fine-tuning, and pre-training.  
  - Identify use cases where RAG can be used to improve the quality,realiability and accuracy of LLM completions.  
  - Describe the core components of the RAG architecture.  
  - Connect Databricks capabilities with the various components of RAG.  

##### How do Language Models Learng Knowledge ?

- Model Pre-Training
  - Training an LLM from scratch.  
  - Requires large datasts (billions to trillions of tokens).  
  
- Model Fine Tuning  
  - Adapting a pre-trained LLM to specific data sets or domains.  
  - Requires thousand of domain-specific or instruction examples.   

- Passing Contextual Information
  - Combining an LLM with external knowledge retrieval.  
  - Requires external knowledge base.    
  - How do we use vectors to search and provide relevant context to LLMs?    


Passing Context to LMs Helps Factual Recall
--

- Analogy: take a exam with open notes.  
- LLM are evolving to accept a large/infinite input token.  

**Downside of long context**
- Hihgh API cost.  
- Lost in the middle. 
- Longer completion interface.  

##### What is RAG ?

**R**etrival **A**ugmented **G**eneration

- Its a pattern that can improve the efficacy of LLMs applications.   
- Its done by retriving data/documents relevant to a query.  

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/RAG_02.PNG)
![Description of the image 2](.img/RAG_02.PNG)

- The main problem that RAG solve is the `knowledge bag` --> so imagine that you want to ask someting to your model wich information was relase afther the model training..

**RAG Uses Cases**
- Q&A chatbots
  - With more accurate information  
- Search Augmentation  
  - Incorporate LLMs with search engines.  
- Content creation and Summarization.  
  Facilitate high quality development.    
  
