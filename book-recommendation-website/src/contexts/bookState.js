import bookContext from "./Moviecontext";
//import { useContext,useState } from "react";

function BookState(props){
async function getRec(userPreferences){
const response = fetch('localhost:5000/api/recommendations', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ userPreferences: userPreferences })
})
.then(response => response.json())
.then(data => {
    // Handle the recommendations data
})
.catch(error => {
    console.error('Error:', error);
});
}
 
return (
    <bookContext.Provider value ={{getRec,book_name,setBook_name}}>{props.children}
    </bookContext.Provider>
)
}

export default BookState