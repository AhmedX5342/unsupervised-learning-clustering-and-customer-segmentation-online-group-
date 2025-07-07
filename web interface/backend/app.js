const express = require("express");
const multer = require("multer");
const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");
const path = require("path");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(express.static(path.join(__dirname, "./")));

// Upload route: forwards Excel file to Python API
app.post("/upload", upload.single("file"), async (req, res) => {
  const filePath = req.file.path;

  const form = new FormData();
  form.append("file", fs.createReadStream(filePath), {
    filename: req.file.originalname,
    contentType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  });

  try {
    const response = await axios.post("http://localhost:5000/predict", form, {
      headers: form.getHeaders(),
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
    });

    res.json(response.data);
  } catch (error) {
    console.error("Prediction failed:", error?.response?.data || error.message);
    res.status(500).json({ error: "Prediction failed" });
  } finally {
    fs.unlinkSync(filePath); // cleanup temp file
  }
});

// Start the server
app.listen(3000, () => {
  console.log("Frontend available at http://localhost:3000");
});
