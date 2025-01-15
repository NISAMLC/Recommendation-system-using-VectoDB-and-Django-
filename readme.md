# Course Recommendation System

This project is a **Course Recommendation System** built with Django and Qdrant, leveraging vector embeddings from a pre-trained `SentenceTransformer` model. The system recommends the most relevant courses based on user input by matching vectorized queries to a vector database.

## Features

- Accepts user input for course search.
- Recommends top 5 courses based on similarity using cosine distance.
- Stores course data as vectors in a Qdrant vector database.
- Displays recommendations in a styled web interface.
- Provides a simple and interactive form for user queries.

## Demo

<img src="output_demo.png" alt="Demo Screenshot" width="800">

## Tech Stack

- **Backend:** Django, Qdrant
- **Frontend:** HTML, CSS (custom styling)
- **Machine Learning:** SentenceTransformer (`all-MiniLM-L6-v2`)
- **Database:** Qdrant (vector database)
- **Other Tools:** Pickle (to save and load vectorized data)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual environment (optional but recommended)
- Required Python libraries (listed in `requirements.txt`)

### Steps to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/NISAMLC/Recommendation-system-using-VectoDB-and-Django-.git

