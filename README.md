# Term Project CMPS-394 (sp26)

You are going to be taking most of what we learned in this class and applying it to a single project. You will need to take a frontend framework of your choice (e.g., React, Vue, Angular) and a backend framework of your choice (e.g., Express, Flask, Django) and create a full-stack application that incorporates the following features:
- A frontend that allows users to interact with the application
    - Users should have to log in to access the application (just one predefined account is fine)
- A backend API that handles user authentication and data storage
    - Once authenticated and logged into the application, users should be able to perform a GET request to retrieve some data from the backend and display it on the frontend. This endpoint should not be accessible without logging in first, and should return a 401 Unauthorized error if accessed without proper authentication
- Use a database to store user information and any other relevant data for your application
- Use Docker to containerize your application and its dependencies (at least locally)
- Your application must be hosted using any service you like and accessible via a public URL
    - There are free options available for hosting frontend, backend, and databases so you should not have to spend anything
    - Depending on your environment, you may not need docker for hosting, but you should still use it for a local setup
    - Environment variables should be used to manage sensitive information like database credentials and API keys, and these should not be hardcoded in your codebase

You will need to explore a few areas we have touched on in this class in more detail to complete this project, so be prepared to do some research and learning on your own. This is a common scenario in real-world development, where you often have to learn new technologies and concepts on the fly to complete a project. The labs and assignments have been designed to get you used to this on a smaller scale.

This will be due before the start of class, 4:59 PM on May 5th. Dr. Russell should be able to visit your public URL, log in, and see a message on the UI indicating a successful GET request.
