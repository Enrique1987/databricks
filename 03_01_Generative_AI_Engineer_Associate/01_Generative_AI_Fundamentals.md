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









