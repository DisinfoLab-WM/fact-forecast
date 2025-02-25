# Fact Forecast

The DisinfoLab engineering team project for Spring 2025.

HELLO THIS IS A TEST COMMIT TO MAKE SURE THAT EVERYTHING IS WORKING ON MY END

## Adding Firebase to Your Project 
[ this step is already completed but for future use is outlined here]
You would do this after creating a Firebase project on the Firebase.com website which manages several backend services related to database management and storage. 
- Install firebase using `npm install firebase ` in whichever directory you are using Firebase. 
- Navigate to project settings to find the configuration code below in the Your Apps section and paste the configuration code as is into a js/tsx file in your project or src directory.
- Obscure the API key part by using an environment variable to contain the api key

### Setting up Firebase in your local project version
- first make sure you're starting out from your project directory in terminal  
-  `cd backend` 
- run `npm install` (want firebase downloaded in the backend directory)
- Setup your own env variable by adding .env file to your root/project directory
- format should look exactly like the env.example file but replace <put your firebase key here> with the firebase api key that you can find on Firebase
- - After adding your firebase key to your .env file, your firebase is now configured and you can send/retrieve data through your local codebase. 
- Create a new js file in the backend directory and test out using the firebase api to query our project database and run using node and logging results to your terminal. 
- ( for details on firebase code details look at firebase.js file)
- current firebase route is countries/USA/articles/ (where you can add different USA articles underneath) or you can add a different country's article under countries/[insert country]/articles/


### Finding the Firebase Api Key: 

1. Go To Console on Firebase using the email that grants access to the disinfoPractice project on Firebase.com
2. Navigate to disinfoPractice project
3. Click on **project settings** (gear icon) which is next to the Project Overview tab in the sidebar 
4. . Scroll down to find the apiKey information within the firebase config code (located underneath Your Apps section)
It will look like this: 
```const firebaseConfig = {
  apiKey: "[API-key located here]",
  authDomain: "disinfopractice.firebaseapp.com",
  databaseURL: "https://disinfopractice-default-rtdb.firebaseio.com",
  projectId: "disinfopractice",
  storageBucket: "disinfopractice.firebasestorage.app",
  messagingSenderId: "834128285827",
  appId: "1:834128285827:web:486cffa240652d86550bb6",
  measurementId: "G-KNXV99Q533"
};
```
5. Copy the api key and add it to your .env file (no quotes necessary)  
