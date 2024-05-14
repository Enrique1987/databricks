# GenerativeAI curse test

---

### Exam Questions - Chapter: databricsk, Generative AI and NLP

**1) Choose two improvements Generative AI are likely to bring to businesses?**
- A: Advanced language processing capabilities
- B: Faster financial analysis
- C: Enhanced weather predictions
- D: Improved image recognition

**2) Which of these is a tokenization scheme?**
- A: Word embeddings
- B: Bidirectional Encoder Representations from Transformers (BERT)
- C: Image recognition
- D: WordPiece

**3) What do language models do?**
- A: Classify documents into predefined categories
- B: Provide weather forecasts based on historical data
- C: Generate images from textual descriptions
- D: Predict the next word in a sequence based on the context of the preceding words

**4) What tools and hardware does Databricks provide to customers for leveraging Generative AI?**
- A: Tensorflow, Pytorch, and Hugging Face packages, along with A-series NVIDIA GPUs
- B: Only Pytorch
- C: Only Tensorflow
- D: Only Hugging Face

**5) What does NLP stand for?**
- A: Natural Learning Process
- B: Natural Language Processing
- C: Natural Language Programming
- D: Neural Language Processing

**6) Which of the following is a valid application of NLP in the domain of sentiment analysis?**
- A: Product reviews
- B: Weather prediction
- C: Clinical decision support
- D: Image caption generation

**7) What tasks can Generative AI models perform that significantly surpass their predecessors?**
- A: Image recognition
- B: Answering open-ended questions, chat, content summarization, execution of near-arbitrary instructions, translation, content, and code generation
- C: Weather prediction
- D: Financial analysis

**8) What is a potential security risk specific to Generative AI models related to user input?**
- A: Prompt injection
- B: Content summarization
- C: Code generation
- D: Data leakage

**9) What are potential legal and ethical considerations when utilizing Generative AI in applications and the workplace?**
- A: Only issues of data leakage
- B: Issues of data leakage, prompt injection, and intellectual property considerations
- C: Only biased or stereotypical outcomes
- D: Only prompt injection

**10) How does Databricks contribute to the success of generative AI applications?**
- A: By focusing on legal and ethical considerations
- B: By unifying the data and AI platform, allowing customers to develop generative AI solutions faster and more successfully
- C: Only by offering SaaS models
- D: By providing image recognition tools

---

### Correct Answers Table

| Question Number | Correct Answer(s) |
|-----------------|-------------------|
| 1               | B,  D             |
| 2               | D                 |
| 3               | D                 |
| 4               | A                 |
| 5               | B                 |
| 6               | A                 |
| 7               | B                 |
| 8               | A                 |
| 9               | B                 |
| 10              | B                 |

---



### Exam Questions: Chapter Common Applications with LLMs

**1. What is the primary function of a tokenizer when working with Large Language Models (LLMs)?**
- A: To convert text into smaller units called tokens for model input
- B: To organize and classify customer feedback
- C: Faster financial analysis
- D: To download and interact with pre-trained models

**2. Suppose you need a model for translating between two languages. What common NLP tasks might be relevant? Select two**
- A: Translation
- B: Summarization
- C: Text Generation
- D: Zero-Shot Classification

**3. Which key library can be used to download datasets from the Hugging Face Hub?**
- A: Evaluate
- B: Transformers
- C: Pip
- D: Datasets

**4. Which of the following is NOT a common NLP task?**
- A: Sentiment analysis
- B: Translation
- C: Image recognition
- D: Summarization

**5. What is the primary goal of sentiment analysis?**
- A: Classify text into predefined categories
- B: Evaluate the emotional tone in a piece of text
- C: Generate new text
- D: Summarize large documents

**6. How can zero-shot classification be utilized?**
- A: Only for summarization tasks
- B: To classify text with a custom set of topic labels
- C: To generate new text
- D: To evaluate the emotional tone in a piece of text

**7. What is the role of prompts in the context of Large Language Models (LLMs)?**
- A: Only to download datasets
- B: Only to organize and classify customer feedback
- C: To guide the model to generate desired outputs
- D: To host demos and code

**8. What is the purpose of Hugging Face Pipelines inside the context of Generative AI?**
- A: To work with pipelines for natural language processing, computer vision, audio, and multi-modal applications
- B: To evaluate the emotional tone in a piece of text
- C: Only to host demos and code
- D: Only to download datasets

**9. Which is a true statement about prompts?**
- A: Every LLM requires carefully phrased prompts in order to produce a good answer.
- B: Prompts can include human language, programming languages, emojis, and other arbitrary text.
- C: A well-engineered prompt which produces good results for one LLM can be reused successfully with almost any other LLM.
- D: By choosing the model with the most downloads

**10. In the example task of stock market analysis, what is the goal of monitoring Twitter commentary?**
- A: To evaluate the emotional tone in a piece of text
- B: To generate new text
- C: To summarize large document
- D: To use twitter commentary as an early indicator of trends

### Answer Key

| Question Number | Correct Answer(s) |
|-----------------|-------------------|
| 1               | A                 |
| 2               | A, C              |
| 3               | D                 |
| 4               | C                 |
| 5               | B                 |
| 6               | B                 |
| 7               | C                 |
| 8               | A                 |
| 9               | B                 |
| 10              | D                 |

This format clearly separates the questions and answers for easy reference and documentation. Let me know if there's anything else you'd like to adjust!	


### Exam Questions

**1. Which of the following are a vector distance similarity measure? Select two.**
- A: L2 regularization
- B: L2 Euclidean
- C: L1 regularization
- D: Cosine similarity

**2. Which of the following is true about the Facebook AI Similarity Search (FAISS) algorithm?**
- A: It implements cosine distance and forms clusters of dense vectors
- B: It implements L2 distance and forms clusters of sparse vectors
- C: It implements L2 distance and forms clusters of sparse vectors
- D: It implements L2 distance and forms clusters of dense vectors

**3. When might you choose to store vectors in a vector database, as opposed to using only a vector library? Select three.**
- A: You have a large volume of frequently changing data
- B: You have a relatively less stringent latency requirement
- C: You want to persist the embedding vectors in long-term storage
- D: You want to have Create-Read-Update-Delete (CRUD) support to edit or update the vectors, without recomputing the entire vector index

**4. What is the primary difference between K-nearest neighbors (KNN) and Approximate nearest neighbors (ANN) in vector search?**
- A: ANN involves a brute force method for finding the nearest neighbors.
- B: KNN involves a brute force method, while ANN prioritizes speed.
- C: KNN prioritizes speed over exactness.
- D: KNN yields less accurate nearest neighbors compared to ANN.

**5. What is the purpose of indexing algorithms in vector search?**
- A: To prioritize exactness over speed.
- B: To perform brute force searches.
- C: To round off vector values.
- D: To create a data structure called a vector index for efficient searches.

**6. In what scenario might you choose to use a vector library instead of a vector database?**
- A: When you prefer out-of-the-box search capabilities.
- B: When you want specialized databases for unstructured data.
- C: When you need context augmentation.
- D: When you need Create-Read-Update-Delete (CRUD) support.

**7. Describe the process of in-query filtering in vector search and its impact on search efficiency.**
- A: In-query filtering prioritizes brute force methods.
- B: In-query filtering involves applying filter conditions after obtaining search results, leading to slower searches.
- C: In-query filtering is not relevant in vector search.
- D: In-query filtering loads both vector data and scalar data for attribute filtering, enhancing search efficiency.

**8. In vector search, how does post-query filtering contribute to the overall search process?**
- A: Post-query filtering helps in brute force searches.
- B: Post-query filtering identifies the top-K nearest neighbors first and then applies the filter, offering fast approximate nearest-neighbor (ANN) searches.
- C: Post-query filtering applies filter conditions before obtaining search results.
- D: Post-query filtering is irrelevant in vector search.

**9. What is a recommended best practice when applying vector compression methods in vector search?**
- A: Prioritizing brute force searches over compression.
- B: Rounding off vector values for compression.
- C: Ignoring the size of the dataset.
- D: Considering the task at hand and the nature of the data.

**10. How does pre-query filtering impact the scope of similarity search in vector databases?**
- A: Pre-query filtering prioritizes brute force methods in similarity search.
- B: Pre-query filtering applies filter conditions to the vector data and returns a list of results, narrowing the scope of similarity search to eligible vectors that satisfy the filter conditions. Therefore, similarity search is conducted within a specific scope, optimizing efficiency and relevance.
- C: Pre-query filtering prioritizes brute force methods in similarity search.
- D: Pre-query filtering has no impact on similarity search.
- E: Pre-query filtering applies filter conditions after obtaining search results.

### Answer Key

| Question Number | Correct Answer(s)                         |
|-----------------|-------------------------------------------|
| 1               | B, D                                      |
| 2               | D                                         |
| 3               | A, C, D                                   |
| 4               | B                                         |
| 5               | D                                         |
| 6               | A, B, C, D                                |
| 7               | D                                         |
| 8               | B                                         |
| 9               | D                                         |
| 10              | B, C, D, E                                |

This new format should meet your specifications. If there's anything you'd like to change or improve, feel free to let me know!
