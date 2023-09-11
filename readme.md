# Choose Your Own Adventure REST API 

## Description
Thi REST API project, named "Choose your own Adventure" is designed to manage interactive storytelling. It provides a platform for creating, sharing, and playing interactive stories. Users can create stories, add text segments with choices, and other users can play these stories by making choices at each stage. The API also supports features like liking, rating, and commenting on stories.



## Swagger Documentation
For comprehensive API documentation, including interactive exploration of endpoints, refer to our Swagger Documentation. This documentation allows you to understand, test, and utilize the API effectively:

https://chooseyourownadventure.pythonanywhere.com/swagger/




## Testing API Endpoints

You can use the REST Client extension in Visual Studio Code (VSCode) to interact with the Choose Your Own Adventure REST API and test various endpoints. The REST Client extension allows you to write and execute HTTP requests directly from your code editor.

### Prerequisites

Before you start testing the API, make sure you have the following prerequisites:

- [Visual Studio Code (VSCode)](https://code.visualstudio.com/download)
- [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) installed in VSCode.

### Testing Endpoints

1. In `test.rest`, you can write HTTP requests using a simple and intuitive syntax. Here's an example:

```http
# GET request to retrieve a specific story (replace with your desired story ID)
GET https://chooseyourownadventure.pythonanywhere.com/api/stories/1
Content-Type: application/json


