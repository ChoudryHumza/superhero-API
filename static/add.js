document.getElementById('addHeroForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    document.querySelectorAll('.error').forEach(el => el.textContent = '');
    document.getElementById('successMessage').innerHTML = '';
    const formData = new FormData(this);
    const response = await fetch('/add', {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    });
    const data = await response.json();
    if (data.success) {
      document.getElementById('successMessage').innerHTML = `New item successfully created. <a href="/view/${data.new_id}">See it here</a>`;
      this.reset();
      document.getElementById('full_name').focus();
    } else {
      for (const [key, msg] of Object.entries(data.errors)) {
        const errorSpan = document.getElementById(key + '_error');
        if (errorSpan) {
          errorSpan.textContent = msg;
        }
      }
    }
  });
  
  /*

  Detailed Explanation of add.js
Line 1:

document.getElementById('addHeroForm').addEventListener('submit', async function(e) {
What it does:
This line finds the element in the document with the id "addHeroForm", which is expected to be the form used on the "Add New Hero" page.
It then attaches an event listener to this form for the "submit" event.
The event listener is set up with an asynchronous callback function that receives an event object e.
Rationale:
Using addEventListener separates JavaScript logic from HTML and allows multiple event listeners if needed.
Marking the callback as async allows the use of await inside the function, making it easier to handle asynchronous operations (like network requests).
Alternatives:
You could attach the event listener inline with an onsubmit attribute in the HTML, but that mixes markup with logic.
Without async, you’d have to use .then() to handle the asynchronous fetch call.
Consequence of Removal:
If you remove this line or don’t attach a listener, submitting the form would trigger the default browser behavior (page reload) and would not use Ajax to send data.
Line 2:

  e.preventDefault();
What it does:
This prevents the default form submission behavior, which is to send data to the server and reload the page.
Rationale:
Preventing the default action is essential when using Ajax; it allows you to control the submission process and handle responses without a full page refresh.
Alternatives:
You might not call this if you intended a standard form submission. However, here we want an Ajax submission.
Consequence of Removal:
Without preventDefault(), the form would submit normally, likely causing a page reload and bypassing the Ajax code.
Line 3:

  document.querySelectorAll('.error').forEach(el => el.textContent = '');
What it does:
This selects all elements with the class "error" on the page.
It then iterates over each element and sets its textContent to an empty string, effectively clearing any previously displayed error messages.
Rationale:
Clearing error messages ensures that old errors do not persist when a new submission attempt is made.
Alternatives:
You could target error elements individually, but using querySelectorAll is more concise and scalable.
Consequence of Removal:
If not cleared, error messages from previous submissions might confuse the user.
Line 4:

  document.getElementById('successMessage').innerHTML = '';
What it does:
This finds the element with id "successMessage" and clears its content.
Rationale:
Ensures that any previous success messages are removed before processing a new submission.
Consequence of Removal:
Old success messages might remain visible, misleading the user about the current form state.
Line 5:

  const formData = new FormData(this);
What it does:
Creates a new FormData object from the form element (this refers to the form because the event listener is attached to it).
FormData automatically gathers all input values from the form.
Rationale:
FormData makes it easy to package form fields for an Ajax request.
Alternatives:
You could manually construct a data object, but FormData handles file inputs and encoding automatically.
Consequence of Removal:
You’d have to manually collect and format form data, increasing the chance of errors.
Line 6:

  const response = await fetch('/add', {
What it does:
Initiates an HTTP request using the Fetch API to the /add endpoint.
The await keyword pauses the execution of the async function until the promise returned by fetch resolves.
Rationale:
Using fetch with await makes the asynchronous request easier to read and write compared to using .then() chains.
Consequence of Removal:
Without await, you’d have to handle promises manually, making the code less readable.
Lines 7–10 (Fetch Options):

    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: formData
  });
What they do:
method: 'POST': Specifies that the HTTP method is POST, meaning data is being sent to the server.
headers: { 'X-Requested-With': 'XMLHttpRequest' }:
Adds a custom header to indicate that this request was made via Ajax.
This can be used on the server side to differentiate between normal requests and Ajax requests.
body: formData:
Sets the body of the request to the FormData object created earlier, which includes all the form fields.
Rationale:
Clearly defining the method, headers, and body ensures that the server processes the request correctly.
Alternatives:
Without the custom header, the server might not recognize the request as Ajax, though in many cases this is optional.
Consequence of Removal:
Removing method or body would cause the server to receive an incorrect or empty request.
Line 11:

  const data = await response.json();
What it does:
Converts the JSON response from the server into a JavaScript object.
The await keyword ensures the code waits until the conversion is complete.
Rationale:
We expect the server to return JSON (either success with a new hero ID or error messages). Converting this JSON allows us to work with it in our code.
Consequence of Removal:
Without converting to JSON, you wouldn’t be able to access the returned data as a JavaScript object, breaking subsequent logic.
Line 12:

  if (data.success) {
What it does:
Checks if the success property in the returned data is true.
Rationale:
This condition tells us if the server processed the submission successfully.
Consequence of Removal:
Without this check, the code wouldn’t differentiate between a successful submission and errors.
Lines 13–16 (Handling Success):

    document.getElementById('successMessage').innerHTML = `New item successfully created. <a href="/view/${data.new_id}">See it here</a>`;
    this.reset();
    document.getElementById('full_name').focus();
What they do:
Line 13:
Sets the innerHTML of the element with id "successMessage" to a success message including a link to view the newly created hero.
Uses template literals (backticks) for easy string interpolation.
Line 14:
Calls this.reset(), which clears the form inputs.
Line 15:
Sets the focus to the input with id "full_name", preparing it for a new entry.
Rationale:
Providing immediate feedback improves user experience.
Resetting the form prevents duplicate submissions.
Setting focus streamlines further data entry.
Consequence of Removal:
Without resetting or focusing, the user might be confused about the next steps or inadvertently re-submit the same data.
Lines 17–22 (Handling Errors):

  } else {
    for (const [key, msg] of Object.entries(data.errors)) {
      const errorSpan = document.getElementById(key + '_error');
      if (errorSpan) {
        errorSpan.textContent = msg;
      }
    }
  }
});
What it does:
Line 17:
The else block is executed if data.success is false, meaning there were validation errors.
Line 18:
Iterates over the data.errors object using Object.entries(), which returns an array of [key, value] pairs.
Line 19:
For each error, retrieves the corresponding <span> element whose id is constructed by appending '_error' to the key (e.g., for key "full_name", it looks for "full_name_error").
Line 20:
If the element is found, sets its textContent to the error message.
Line 21:
Closes the if block.
Line 22:
Closes the for loop.
Line 23:
Closes the else block.
Line 24:
Closes the event listener callback function.
Rationale:
This loop dynamically displays error messages next to the appropriate form fields based on the keys returned by the server.
Alternatives:
You could manually set error messages for each field, but looping is more maintainable.
Consequence of Removal:
Without this error handling, users wouldn’t receive inline feedback, leading to a poor user experience.

*/