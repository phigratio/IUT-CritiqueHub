# CRITIQUEHUB

The project is a dynamic review and blogging platform built using the MERN stack, allowing users to share reviews and insights on various products, services, or experiences. The platform   enables others to read and engage with authentic reviews, fostering informed decision-making through community-driven content.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features

- **User Authentication**: Users can log in and register with their email ids or through Google Authentication. 
- **Create, Publish or Edit Blogs**: Any user can create, publish and edit blogs if they are logged in. They can also unpublish the blogs through saving it to the drafts.
- **Likes and Comments**: Users can like and comment on any blogs.They can also hide comments and reply to any comments through nested commenting.
- **Trending and Simillar Blogs**: Users can also see which blogs are in trending now and can see the similar blogs. They can search any blog by the names or tags. 
- **Product Scrapping**:Lastly, the users can see their desired products names and prices from various ecommerce websites and can decide which products they will buy.   

## Installation

### Prerequisites

- **Node.js** (Node.js v18.20.5 recommended)
- **MongoDB**
- **Firebase** account and API configuration
- **Python libraries** for product scrapping
- **Git**

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/phigratio/IUT-CritiqueHub.git
   ```

2.	Navigate to the project directory:
    For Frontend
  ```bash
  cd learning-website-frontend
  ```
   For Backend
   ```bash
  cd server
  ```


3.	Install dependencies:
```bash
npm install
```

4.	Set up Firebase:
	-	Create a Firebase project in your Firebase Console.
	-	Enable Firestore, Authentication, and any other required Firebase services.
	-	Obtain your Firebase configuration and add it to the .env file as follows:
```
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-auth-domain
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-storage-bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
```

5. Set up MongoDB:
   -Create a new connection in your MongoDB Compass or Atlas
    and paste the mongoDB url in your .env file.
```bash
MONGO_URI=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/your_database?retryWrites=true&w=majority

```
   Replace your_username, your_password,your_database with your own.

6. Set up the scrapping :
   -Install necessary packages
   and create a new python script 

```bash
pip install requests beautifulsoup4 lxml selenium scrapy pandas openpyxl

```

```bash
code scraper.py

```

 7.Start the web server:
    -Nevigate to the frontend and give the following command
```bash
npm run dev
```
  -Nevigate to the backend and give the following command
```bash
npm start
```


## Usage

1.	Users can give reviews and create their own blogs.
2.	Users can decide which products they want to buy through product scrapping.

## Acknowledgments

CRITIQUEHUB is built with MERN and Firebase, and we are grateful to the open-source community for providing the tools and resources to make this project possible.