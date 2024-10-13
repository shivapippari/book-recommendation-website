import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './App.css';
function Home() {
  const [bookName, setBookName] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [booksAuthor, setBooksAuthor] = useState([]);
  const [booksPublisher, setBooksPublisher] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isClicked, setIsClicked] = useState(false);
  const [books, setBooks] = useState([]);
  // const fetchBooks = async () => {
  //   try {
  //     // Set loading to true
  //     const response = await fetch('http://localhost:5000/api/books');
  //     if (!response.ok) {
  //       throw new Error('Failed to fetch books');
  //     }
  //     const data = await response.json();
  //     setBooks(data);
  //   } catch (error) {
  //     console.error('Error fetching books:', error);
  //   } finally {
  //     setIsLoading(false); // Set loading to false after fetching
  //   }
  // };

  // useEffect(() => {
  //   fetchBooks();
  // }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ bookName }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
      setIsClicked(true);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const truncateTitle = (title, maxLength) => {
    if (title && title.length > maxLength) {
      return title.substring(0, maxLength) + '...'; // Adjust to append ellipsis or any text
    }
    if(!title)
      setRecommendations([]);
    return title;
  };

  return (
    <div className="App">
      <header>
        <h1>Book Recommendation</h1>
      </header>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={bookName}
          onChange={(e) => setBookName(e.target.value)}
          placeholder="Enter book name"
        />
        {isLoading ?
          (<div className="spinner-border text-primary" role="status">
            <span className="sr-only">Loading...</span>
          </div>)
          : (
            <button type="submit">Submit</button>
          )}
      </form>
      {/* Recommendation section */}
      <div className="book-list">
        {isLoading ? (
          <p>Loading books...</p>
        ) : (
          <>
            {(!isClicked || (recommendations && recommendations.length > 0)) ? (
              <ul>
                {recommendations.map((book, index) => (
                  <li key={index} className="book-item card">
                    <Link to={`/${book.title}`}>
                      <img src={book.image_url} alt={book.title} />
                      <p>{truncateTitle(book.title, 30)}</p>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <h5>The Book you are trying to search or the book related to it are not found</h5>
            )}

          </>
        )
  }
      </div>
      </div>
  )
};
          
export default Home;