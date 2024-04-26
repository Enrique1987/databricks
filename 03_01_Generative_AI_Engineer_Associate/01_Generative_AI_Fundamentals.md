# Generative AI Engineer Associate: Theorie 80-20%



## Index

- [01 Generative AI Basics](#basics)
- [02 Databricks Generative AI and NLP.](#databricks)
- [03 Common Applications with LLM](#commonApplicaiton)
- [04 RAG with Vector Search and Storage](#RAG)
- [05 Multi-stage Reasoning with LLM Chains](#multi-stage)
- [06 Fine-Tuning LLMs](#Fine-Tuning)
- [06 Evaluating LLMs](#Evaluating)
- [06 Society and LLMs](#Society)
- [06 LLMs Operations](#LLM-Operations)


## Generative AI Basics

AI --> ML --> DL --> Generative AI:

Generative AI is a Sub-field of AI that focuses on generating new conent such as: 
	- Images
	- Text Audio
	- Code 
	- Synthetic data
	
**Why now ?**  Large Datasets, Computations Power, Innovative DL models (GANs, Transformes, RLHF)   
**Generative AI Use Cases** Image generator, Video Synthesis, 3D Generation, Audio Generation.

### LLMs and Generative AI

Generative AI:
- LLMs: Trained on massive dataset to achive advanced language processing capabilities. Based on Deep Learning NN
	- How LLM work: Encoding Transformer Model Decoding
	
	Propietary Models: Positive - Speed of development, Quality. Negative :- Cost, Data Privacy, Vendor lock-in
	Open Source Models: Task-tailoring, Inference Costs, Control. Netative:- Upfrom time investment, Data requirements, Skill Sets.
	
	**Fine-tuning** The process of further training a pre-trained model on a specific task or datast to adapt it for a particular application or domain.
	
- Fundation Model: Large ML model trained on vast amount of data fine-tuned for more specific language understanding and generation task.
	
## 02 Databricks Generative AI and NLP.

Some useful NLP definitions

`Token`: Basic building block.   
`Sequence`: Sequential list of tokents.  
`Vocabulary`: Complete list of tokents.  

#### Word Embeddings

The goal of word embedding is to try and conserve teh context that particula token ahst in this vocabulary.

Langue Model can be spliting in two cathegories: 
- Generate content.
- Classify.

#### What is a Large Language Model 

Language Model - Tranformer: NN architecture that processes sequence of variable lenght using a self-attention mechanism. 2017-Present.

#### How Do LLMs Work?
A simplified version of LLM training process.

1)encoding(input-tokenize-embeddings)
2)Pre-Trained-Transormer-Model.
3)DecodingOutput Text

![llm](img/01_LLM_Work.PNG))


Your data, will be your competitive advantage.

#### Summary

- Common LL; business use cases are; contentcretion, process automation, personalization, code generation.  
- LLMs generate outputs for NLP task such as summarization, classificatin, question anwering, content creation, etc.  
- Databricks Lakehouse AI is a data-centrig Genrative AI platform.  
- With Databricks + MosaicML customers can build their own custom models in a secure enviorment using their own data.
- NLP
	- Is a field of methods to process text.
	- Is useful summarization, tanslation, classificationm, etc.
	- Tokens are the smalles builidng blocks to convert text to numerical vectors, aka N-dimensional embeddings.
	- Language models (LMs) predict words by looking at word probabilities.  
	- LLMs are just LMs with transormer architecutres, but bigger.  
	
	
#### Language Modeling

**TF-IDF**
	TF-IDF, short for Term Frequency-Inverse Document Frequency, is a numerical statistic used in natural language processing to reflect the importance of a word
	to a document in a collection or corpus. It increases proportionally with the number of times a word appears in a document but is offset by the frequency
	of the word in the corpus, helping to adjust for the fact that some words appear more frequently in general.  

**Bag of words**
	
The Bag of Words model is a simplifying representation used in natural language processing where text (such as a sentence or a document) is represented as the bag (multiset) of its words, disregarding grammar and even word order but keeping multiplicity.
Consider the sentence: "The cat chased the mouse."
In the Bag of Words model, this sentence would be represented as a set of word occurrences. The model doesn't care about the order of words, just their presence.
If we create a simple count for each word, the representation might look like this:

- The: 2
- cat: 1
- chased: 1
- mouse: 1

This count indicates the frequency of each word in the sentence. 
The words "the", "cat", "chased", and "mouse" are the individual tokens, and their respective counts reflect how many times they appear in the sentence.





