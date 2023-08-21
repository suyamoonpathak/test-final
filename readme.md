# Your Flask App Name

Welcome to **Your Flask App Name**! This is a web application built using Flask that allows users to ask and answer questions, as well as vote on questions and answers.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Get All Questions](#get-all-questions)
  - [Create a Question](#create-a-question)
  - [Update or Delete a Question](#update-or-delete-a-question)
  - [Create an Answer](#create-an-answer)
  - [Update or Delete an Answer](#update-or-delete-an-answer)
  - [Votes]

## Getting Started

These instructions will help you set up and run the Flask app locally.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Virtualenv (optional but recommended)
- SQLite or your preferred database system

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-flask-app.git
   ```

2. Navigate to the app's directory:
cd test-final

3. Create a virtual environment (optional but recommended):
virtualenv venv
source venv/bin/activate

4. Install the required dependencies:
pip install -r requirements.txt

5.Running the App
flask run


API Endpoints
Here are the main API endpoints available in this app:

User Registration
Endpoint: /api/signup
Method: POST
Description: Register a new user account.

User Login
Endpoint: /api/signin
Method: POST
Description: Log in as an existing user.

Get All Questions
Endpoint: /api/questions
Method: GET
Description: Get all questions along with answers and votes.

Create a Question
Endpoint: /api/<int:user_id>/questions
Method: POST
Description: Create a new question.

Update or Delete a Question
Endpoint: /api/<int:user_id>/questions/<int:question_id>
Method: PUT, DELETE
Description: Update or delete a question (if you are the author).

Create an Answer
Endpoint: /api/<int:user_id>/questions/<int:question_id>/answers
Method: POST
Description: Create an answer for a question.

Update or Delete an Answer
Endpoint: /api/<int:user_id>/questions/<int:question_id>/answers/<int:answer_id>
Method: PUT, DELETE
Description: Update or delete an answer (if you are the author).

Upvote a Question
Endpoint: /api/<int:user_id>/questions/<int:question_id>/upvote
Method: POST
Description: Upvote a question.

Downvote a Question
Endpoint: /api/<int:user_id>/questions/<int:question_id>/downvote
Method: POST
Description: Downvote a question.

Upvote/Downvote an Answer
Endpoint: /api/answers/<int:answer_id>/vote
Method: POST
Description: To Upvote an answer, use value = 1, To Downvote, use value = -1, to remove your selection, use value=0.


<!-- ### Hosted on - ec2-16-171-166-42.eu-north-1.compute.amazonaws.com -->
Forgot to change the host url, I first deployed on ec2 instance, but, since api endpoints were not working, i changed it to render - here's the render url:
https://shipmnts-test.onrender.com/