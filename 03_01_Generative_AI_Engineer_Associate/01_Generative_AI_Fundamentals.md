# Generative AI Engineer Associate: Theory 80-20%

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

- **Learning Objectives**: 
  - RAG, prompt engineering, fine-tuning, and pre-training.  
  - Identify use cases where RAG can be used to improve the quality, reliability, and accuracy of LLM completions.  
  - Describe the core components of the RAG architecture.  
  - Connect Databricks capabilities with the various components of RAG.  

##### How do Language Models Learn Knowledge?

- Model Pre-Training
  - Training an LLM from scratch.  
  - Requires large datasets (billions to trillions of tokens).  
  
- Model Fine-Tuning  
  - Adapting a pre-trained LLM to specific data sets or domains.  
  - Requires thousands of domain-specific or instruction examples.   

- Passing Contextual Information
  - Combining an LLM with external knowledge retrieval.  
  - Requires an external knowledge base.    
  - How do we use vectors to search and provide relevant context to LLMs?    

Passing Context to LMs Helps Factual Recall
--

- Analogy: taking an exam with open notes.  
- LLMs are evolving to accept a large/infinite input token.  

**Downside of long context**
- High API cost.  
- Lost in the middle. 
- Longer completion interface.  

##### What is RAG?

**R**etrieval **A**ugmented **G**eneration

- It's a pattern that can improve the efficacy of LLM applications.   
- It's done by retrieving data/documents relevant to a query.  

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/RAG_02.PNG)

- The main problem that RAG solves is the `knowledge bag` --> so imagine that you want to ask something to your model whose information was released after the model training.

**RAG Use Cases**
- Q&A chatbots
  - With more accurate information  
- Search Augmentation  
  - Incorporate LLMs with search engines.  
- Content creation and Summarization.  
  Facilitate high-quality development.    
  
#### 01.02 Preparing Data for RAG Solutions

- List potential consequences of improperly prepared data for RAG solutions.  
  - Poor quality of the model.  
  - Lost in the middle: long documents tend to be overlooked.    
  - Inefficient retrieval.  
  - Exposing data.  
  - Wrong embedding model.  
- Importance of chunk strategy.  
- Strategies for preparing RAG solutions.  
- Delta Lake and Unity Catalog support RAG patterns.  
- Map Databricks products for structured and unstructured data preparations.  


**Data Pre processing Overview**
![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/14_Data_Preparation.PNG)

**Recap Data Lake and uc**  
![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/15_recap_data_lake_and_uc.PNG)

**Chunk strategies**

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/16_Chunking_Strategies.PNG)

**Advance Chunking Strategies**

- Sumarization with metadata.

**Challenges on summarization**

- Text mixted with image.  
- Irregular placement of the text.  
- Color.  
- Chart with hierchical information.  
- Multi column text.  
- Imagines with important information.  


**Embedding Model**
- Tip 1: Choose Your Embedding Model Wisely
  - The embedding model should represent BOTH queries and documents
  - Is your current embedding model trained on similar data as yours?
    - Yes -> Yay! You can keep using that model
	- No -> Choose another pre-trained embedding model or Train or fine-tune your own embeddings based on your data


- Tip 2: Ensure similar Embedding Space for both Queries and Documents

 - Use the same embedding model for indexing and querying
 - OR, if you use different embedding models, make sure they are trained on similar data (therefore produce the same embedding space!) This will give you bad results!!

Movie data -> Language Model -> Vector Database (or index) -> Language Model -> User submits query about medical literature.

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/18_Tipps_Embedding.PNG) 

**Data preparation inside Databricks**

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/19_Unstructured_Data_Prep.PNG)

#### 01.03 Vector Search

**Characteristics**  
Vector search involves retrieving information based on numerical vectors,
enabling similarity search rather than exact matches. It leverages high-dimensional vectors to capture the semantic meaning of data.

**Use cases**  
Vector search is used in recommendation systems, semantic search, image and video retrieval, and natural language processing tasks.
 It's particularly useful in applications where context and meaning are more important than exact keywords. **context > exact words**

**How Vector Search supports GenAI**  
Vector search enhances Generative AI by enabling efficient retrieval of semantically similar data,
which can be used to generate contextually relevant responses. It allows GenAI models to access and utilize vast amounts of information more effectively,
improving their performance.

**Process of executing a search using a Vector Database**  
The process involves converting the search query and data into high-dimensional vectors using embeddings.
The vector database then compares these vectors to find the closest matches based on similarity metrics.

**Benefits of Mosaic AI Vector Search**  
Mosaic AI Vector Search offers scalable, high-performance search capabilities that are optimized for handling large datasets.
It provides advanced features such as real-time updates and integration with AI models, enhancing the overall efficiency and accuracy of information retrieval.


**Vector Databases**
- databae optimed to store and retrieve high-dimensional vectors such as embeddings.  
- Rag architecture, contextual informaiton is stored in vectors.  
- Reieves vectos most similar toa specified query vector.  

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/20_Vector_Databases_1.PNG)

Common Use Cases for VD  
- RAG.    
- Recommendation Engines.  
- Similarity Search.  



**Do I need a Vector Database ?**

Pros
  - Scalability - Mil/millions
  - Speed
  - Full-fledged database properties: CRUD, ACL, Persistence & Storage Layer.  
Cons
  - One more system to learn and integrate.  
  - Added costs.  
 
**Proximity Sgtrategies** 
![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/21_Proximity_Strategies.PNG)


**What about vector libraries or pluggins?**  
Could work for small projects.  


**Reranking**
A method of prioritizing documents most relevant to users query

![Description of the image](https://github.com/Enrique1987/databricks/raw/main/03_01_Generative_AI_Engineer_Associate/img/22_Reranking.PNG)
