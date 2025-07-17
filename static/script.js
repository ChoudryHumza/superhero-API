// humza choudry section 1 hc3241 

const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const clearButton = document.getElementById('clearButton');

searchButton.addEventListener('click', () => {
    const query = searchInput.value;
    if(query.trim() === ""){
         searchInput.value = "";
         searchInput.focus();
         return;
    }
    window.location.href = "/?search=" + encodeURIComponent(query);
});
searchInput.addEventListener('keyup', (e) => {
    if(e.key === 'Enter'){
         searchButton.click();
    }
});
clearButton.addEventListener('click', () => {
    window.location.href = "/";
});


/*
NOTESSSS:

Detailed Explanation of script.js
General Overview

Purpose of script.js:
This file provides global functionality for the search feature. It attaches event listeners to the search input and search button so that users can trigger a search by clicking the button or pressing Enter. It then constructs a URL with the search query and redirects the browser to that URL.
Block 1: Search Button Click Event

Comment:
// Attach a click event listener to the Search button.
Purpose:
This comment explains that the following code attaches a click event listener to the search button.
Why it's useful:
Comments help future developers understand the code quickly.
Consequence of Removal:
The code will still run, but the purpose might be less clear to someone reading it later.
Attaching the Event Listener:
document.getElementById('searchButton').addEventListener('click', function() {
document.getElementById('searchButton'):
This finds the HTML element with the id "searchButton".
Why it's used:
We need to know which element will trigger the search functionality.
Consequence of Removal:
Without targeting the element, the subsequent code won’t be attached to any button.
.addEventListener('click', function() { ... }):
Attaches a callback function to run when a click event occurs on the search button.
Why it's used:
It’s a modern, unobtrusive method to handle events, separating HTML from JavaScript logic.
Alternative:
An inline onclick attribute in HTML could be used, but that mixes code and markup.
Consequence of Removal:
If removed, clicking the search button would not trigger any action.
Retrieve the Search Query:
const query = document.getElementById('searchInput').value;
document.getElementById('searchInput'):
Finds the search input element.
.value:
Retrieves the current text inside the input field.
const query = ...:
Stores that text in a constant variable query.
Why it's used:
We need the user's query to determine what to search for.
Consequence of Removal:
Without this, you wouldn’t know what term to use for the search.
Check if the Query is Empty:
if (query.trim() === "") {
query.trim():
Removes any extra spaces from the beginning and end of the string.
=== "":
Checks whether the trimmed string is empty.
Why it's used:
To prevent an empty search, which could result in an unnecessary redirect.
Alternative:
One could check using if (!query.trim()), which is functionally equivalent.
Consequence of Removal:
Without this check, pressing the search button with no meaningful input might trigger a redirect to a URL with an empty query parameter, leading to unintended behavior.
Clear and Refocus the Input if Empty:
  document.getElementById('searchInput').value = "";
  document.getElementById('searchInput').focus();
  return;
document.getElementById('searchInput').value = "";:
Explicitly clears the input field.
document.getElementById('searchInput').focus();:
Sets the focus back to the search input, so the user can start typing immediately.
return;:
Exits the function early, so no further code is executed.
Why it's used:
Provides immediate feedback and prevents unnecessary redirection.
Consequence of Removal:
The form might proceed with an empty search, leading to confusing results.
Redirect to the Search Results:
window.location.href = "/?search=" + encodeURIComponent(query);
window.location.href:
This property sets the current URL, causing the browser to navigate to the new URL.
"/?search=" + encodeURIComponent(query):
Constructs the URL by appending the search query as a parameter to the base path ("/").
encodeURIComponent(query):
Encodes special characters in the query so that the URL is valid.
Why it's used:
Redirects the user to the homepage where the server will process the search query and display matching results.
Alternative:
One could use window.location.assign(...), but setting window.location.href is equivalent and straightforward.
Consequence of Removal:
Without this line, the search button would not perform any redirection, and the search would appear to do nothing.
Block 2: Search Input Keyup Event

Attach Keyup Event Listener:
document.getElementById('searchInput').addEventListener('keyup', function(e) {
What it does:
Finds the search input element (with id "searchInput").
Attaches an event listener for the "keyup" event (which is triggered when the user releases a key).
Why it's used:
To enable the search functionality via the Enter key, improving usability.
Consequence of Removal:
Users would have to click the search button; pressing Enter would not trigger a search.
Check if Enter Key is Pressed:
if (e.key === 'Enter') {
What it does:
The event object e has a property key that indicates which key was pressed.
This line checks if the pressed key is "Enter".
Why it's used:
To determine if the user is trying to submit the search via keyboard.
Alternatives:
One might check if (e.keyCode === 13) but using e.key === 'Enter' is more readable and modern.
Consequence of Removal:
Without this check, pressing Enter might not trigger the intended behavior, reducing usability.
Simulate a Click on the Search Button:
document.getElementById('searchButton').click();
What it does:
Programmatically triggers a click event on the search button.
Why it's used:
To reuse the search button’s event listener, so that the same logic for redirection is executed when the user presses Enter.
Alternative:
Duplicate the redirection code in the keyup event, but that would be redundant.
Consequence of Removal:
Pressing Enter in the search input would not initiate a search, degrading the user experience.
Closing Braces:
} });

- **What it does:**  
  - Closes the if statement and the function passed to `addEventListener`.
- **Why it's used:**  
  - Properly closes the code blocks to ensure correct execution.
- **Consequence of Removal:**  
  - Missing braces would cause syntax errors, and the script would not run.

---

### Summary of script.js

- **Purpose:**  
- This script handles search functionality by attaching event listeners to the search button and input field.
- It ensures that when a user clicks the search button or presses Enter in the search field, the browser redirects to the homepage with the search query parameter.
- **Design Decisions:**  
- **Using `addEventListener`:**  
 - Keeps JavaScript separate from HTML, enhancing maintainability.
- **Using `preventDefault()`:**  
 - Stops the default form submission behavior, which is essential for handling search via JavaScript.
- **Input Validation:**  
 - Checking if the query is empty ensures that no unnecessary redirection happens.
- **Redirection via `window.location.href`:**  
 - This method is straightforward and leverages URL parameters to trigger server-side search.
- **Handling Keyup Events:**  
 - Enhances usability by allowing users to press Enter as an alternative to clicking the search button.
- **Potential Issues:**  
- Removing any key part (such as the query validation or the redirection) would break the search functionality.
- Alternatives like using inline event handlers exist, but separating JavaScript into this file is cleaner and more maintainable.

  */