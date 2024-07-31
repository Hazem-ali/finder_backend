// Import necessary libraries
const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs"); // To read the photo file

// Function to post data
async function postData() {
  // Create a new FormData instance
  const form = new FormData();
  const token =
    "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyMTM4Nzc2LCJpYXQiOjE3MjIwMzA3NzYsImp0aSI6Ijc3Y2RlNzViYTk0ZDQ3NGE4OTQxYWY4NGIyOTQwOTA3IiwidXNlcl9pZCI6M30.DJ4h3yog4gA8x8Rck4fWGeXpNMgC7W0yMYnkqTXF-1k";
  // Append individual fields
  form.append("name", "hazoooma");
  form.append("status", "forbidden");
  form.append("notes", "notes hazooma");
  form.append("national_id", "132164");

  // Read the photo file (assuming the photo file is in the same directory and named 'photo.jpg')
  const photoPath = "./mofty.jpg";
  const photoStream = fs.createReadStream(photoPath);
  const photoPath_2 = "./unnamed.jpg";
  const photoStream_2 = fs.createReadStream(photoPath_2);

  form.append("photos_data", photoStream); 
  form.append("photos_data", photoStream_2);



  try {
    const response = await axios.post("http://localhost:8000/suspects/", form, {
      headers: {
        ...form.getHeaders(), 
        Authorization: token,
      },
    });

    console.log("Server response:", response.data);
  } catch (error) {
    console.error("Error posting data:", error);
  }
}

postData();
