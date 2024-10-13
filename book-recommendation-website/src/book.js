// import { useParams } from 'react-router-dom';
// function Book() {
//   const { bookName } = useParams();
//   return (
//     <h1>{bookName}</h1>
//   );
// }

// export default Book;

import React, { useEffect,useState } from 'react';
import { useParams,Link } from 'react-router-dom';
import './book.css';


function Book() {

  const [details, setDetails] = useState([]);
  const { bookName } = useParams();

  //const bookName = "The Giving Tree"
  useEffect(() => {
    if (bookName) {
      search(bookName);
    }
  }, [bookName]);
  const search = async(bookName)=>{
    try {
          const response = await fetch(`http://localhost:5000/api/search?bookName=${encodeURIComponent(bookName)}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
    
          if (!response.ok) {
            throw new Error('Failed to fetch recommendations');
          }
          const data = await response.json();
          if(!data)
            console.log("empty");
          console.log(data);
          setDetails(data);

        } catch (error) {
          console.error('Error fetching recommendations:', error);
        }
}
  return (
    <div>
      <Link to="/">Go Back to Home</Link>

      {details.length > 0 ? (
        <div className="book-container">
          <div className="book-cover">
            <img src={details[0]['Image-URL-L']} alt="Book Cover" />
          </div>
          <div className="book-info">
            <h1 className="book-title">{bookName}</h1>
            <table>
              <tbody>
                <tr>
                  <td><strong className="author-name">Author Name:</strong></td>
                  <td>{details[0]['Book-Author']}</td>
                </tr>
                <tr>
                  <td><strong className="publisher">Published by:</strong></td>
                  <td>{details[0]['Publisher']}</td>
                </tr>
                <tr>
                  <td><strong className="details">Published Year:</strong></td>
                  <td>{details[0]['Year-Of-Publication']}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )
        :
        (
        <h1 className="book-title">{bookName}</h1>
        )
      }
     
    </div>
  );
}

export default Book;
