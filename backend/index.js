const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');
const csv = require('csv-parser');
const app = express();
const port = 5000;

app.use(cors());
app.use(bodyParser.json());

app.get('/api/books', (req, res) => {
  const results = [];
  const filePath = './Popular_Books.csv';
  fs.createReadStream(filePath)
    .pipe(csv({
      separator: ';',
      quote: '"',
      escape: '"',
      skipLines:1,
      headers: ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']
    }))
    .on('data', (data) => {
      const title = data['Book-Title'];
      const imageLink = data['Image-URL-L'];
      if (title && imageLink) {
        results.push({
          title,
          imageLink
        });
      }
    })
    .on('end', () => {
      console.log('CSV file successfully processed');
      res.json(results);
    })
    .on('error', (err) => {
      console.error('Error reading CSV file:', err);
      res.status(500).json({ error: 'Failed to read CSV file' });
    });
});


app.post('/api/recommendations', (req, res) => {
  const { bookName } = req.body;
  const userPreferences = JSON.stringify({ bookName });
  const pythonProcess = spawn('python', ['./test.py', userPreferences]);

  let dataString = '';
  pythonProcess.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  pythonProcess.stdout.on('end', () => {
    try {
      const recommendations = JSON.parse(dataString);
      res.json({ recommendations });
    } catch (error) {
      console.error('Error parsing JSON:', error);
      res.status(500).json({ error: 'Failed to parse recommendations' });
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
});



const books = [];



// Read CSV file and populate books array
fs.createReadStream('./filtered_Books.csv')
  .pipe(csv({
    separator: ';',
    quote: '"',
    escape: '"',
  }))
  .on('data', (row) => {
    books.push(row); // Push each row (book data) into the books array
  })
  .on('end', () => {
    console.log('CSV file successfully processed');
    console.log('Total books:', books.length);
  })
  .on('error', (err) => {
    console.error('Error reading CSV file:', err);
  });

// Search endpoint
app.get('/api/search', (req, res) => {
  const { bookName } = req.query; // Assuming bookName parameter is passed like '/api/search?bookName=bookTitle'
  
  if (!bookName) {
    return res.status(400).json({ error: 'bookName parameter "bookName" is required' });
  }

  // Filter books based on the bookName
  const results = books.filter(book =>
    book['Book-Title'].toLowerCase().includes(bookName.toLowerCase())
  );

  console.log('Search bookName:', bookName);
  console.log('Search results:', results);

  res.json(results);
});

app.listen(port,function(){
  console.log('server running on',port)
})

