import React, { useEffect, useState} from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './Home.js'
import Book from './book.js'
function App() {
  return(
   <Router>
    <Routes>
      <Route path="/" element={<Home/>}>
      </Route>
      <Route path="/:bookName" element={<Book/>}>
      </Route>
      </Routes>
    </Router>
  );
}

export default App;
