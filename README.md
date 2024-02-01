# QABot-LangChain (WIP)

QABot-LangChain is a powerful backend API designed to function as an Answering bot, leveraging the capabilities of openai model. The set of APIs excels in providing answers to questions based on the content of a document, featuring a modular architecture with two core components: **web** and **worker**.

## Features

- **Modular Architecture:** The system comprises two modules - web and worker - offering a seamless and scalable solution.
- **Web Module:** A FastAPI-based web app responsible for uploading PDF documents and question JSON files as ingestion files. It triggers an event to a Kafka topic, generating a unique task_id mapped to worker job indexing, for future retrieval of answers.
- **Worker Module:** An independent FastAPI worker that listens to a Kafka topic, processes events pushed from the web module. the worker does the following steps parses files, split, indexes, adds embedding, and utilizes Chroma Vector Database as a retriever. The worker warms up once chaining is done and starts querying the questions from OpenAPI servers. The answers are appended under the task_id, created during file upload. Next, the answers are persisted as file task_id.json under output dir, and can be retrieved using the "Get Task by Task ID" API.


## Prerequisites

0. **Get OpenAI Key [here](https://platform.openai.com/account/api-keys)**
1. **Kafka Cluster Running Locally:**
   - `make install-kafka` to install kafka 
   - `make remove-kafka` to cleanup kafka 
   - topic is created automatically when they're first referenced by the producer or consumer (KAFKA_AUTO_CREATE_TOPICS_ENABLE)
2. **Python 3.x:**
   - QABot-LangChain is built using Python 3.x. Ensure that you have Python 3 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

3. **Update the .env File:**
   - Locate the `.env.default` file in the root directory of the project.
   - Fill in the required configurations such as API keys, file paths, and other settings.

   Example `.env` file:
   ```env
   # General FastAPI Configuration
   FASTAPI_ENV=default

   # Kafka Producer Configuration
   KAFKA_PRODUCER_BOOTSTRAP_SERVERS=localhost:9092
   KAFKA_PRODUCER_TOPIC=demollm

   # Kafka Consumer Configuration
   KAFKA_CONSUMER_BOOTSTRAP_SERVERS=localhost:9092
   KAFKA_CONSUMER_TOPIC=demollm

   # Add other configurations as needed
   OPENAI_API_KEY=
   
## Run Web and Worker locally

1. Clone the repository: `git clone https://github.com/13shivam/QABot-LangChain`, `cd /QABot-LangChain`
2. Install dependencies for web and worker components:
   -  `make install-web`
   -  `make install-worker`
3. Add local Kafka configurations in `.env` file as per the guidelines *python dotenv*
4. Run the web component on port 8000: `make run-web`
5. Run the worker component on port 8001: `make run-worker`



## APIs 

### 1. Upload File API

**Request:**

```bash
curl --location 'http://127.0.0.1:8000/v1/upload' \
--header 'Content-Type: application/json' \
--data '{
    "document_file_path" : "fastApiProject/app/example_docs/original1.pdf",
    "question_file_path" : "fastApiProject/app/example_docs/1q.json"
}'
```

**Response:**

```json
{
    "status": 200,
    "task_id": "923fb629-76d5-4a14-8b86-6e3a28a27aa4"
}
```


### 2. Get Task by Task ID

**Sample Curl:**

```bash
curl --location 'http://127.0.0.1:8000/v1/task/{task_id}'
```
**Response:**

```json
[
    {
        "question": "What is public health preparedness?",
        "answer": " Public health preparedness refers to the actions and resources put in place to prevent and respond to public health threats, such as antimicrobial resistance or pandemics. This includes investing in infrastructure, workforce, technology, and strategies to detect, prevent, and contain these threats."
    },
    {
        "question": "What is  SARS-CoV-2 RNA ?",
        "answer": "SARS-CoV-2 RNA is a marker used to detect the presence of COVID-19 in communities through wastewater surveillance. It carries genetic information and can aid in tracking the spread of the virus."
    },
    {
        "question": "How does seven regional labs in CDC’s AR Lab Network work?",
        "answer": " The seven regional labs in CDC's AR Lab Network collaborate with each other during emergencies, such as the COVID-19 pandemic, to maintain critical national testing for antimicrobial resistance. They may offer tests outside of their typical regions or use their sequencing capacity to study new viruses, like SARS-CoV-2. These collaborations demonstrate the flexibility and adaptability of the AR Lab Network and how CDC's investments in antimicrobial resistance can be utilized during a crisis."
    }
]
```

**Answer Output Directory**

```app/output```

### WIP

**1. different retrieval strategies on the fly**

**2. cleanup files, add db layer for management**

**3. docker, k8 and helm support charts**
