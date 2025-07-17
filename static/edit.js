document.getElementById('discardButton').addEventListener('click', function() {
    const heroId = this.getAttribute('data-hero-id');
    if (confirm("Are you sure you want to discard changes?")) {
      window.location.href = "/view/" + heroId;
    }
  });
  

  /*
  Line 1:

document.getElementById('discardButton').addEventListener('click', function() {
What it does:
document.getElementById('discardButton') locates the HTML element with the id "discardButton". In our edit.html file, this button is the "Discard Changes" button.
.addEventListener('click', function() { ... }) attaches an event listener to this element for the "click" event. When the button is clicked, the callback function provided will execute.
Rationale:
Using addEventListener decouples JavaScript from HTML, which makes the code easier to maintain and update.
It ensures that when a user clicks the "Discard Changes" button, our specified function runs.
Alternatives:
An alternative would be to add an inline onclick="..." attribute directly in the HTML element. However, this mixes markup with behavior and makes maintenance more difficult.
Consequence of Removal:
If you remove this line or fail to attach an event listener, clicking the "Discard Changes" button would not trigger any action, leaving users without a way to cancel their changes.
Line 2:

  const heroId = this.getAttribute('data-hero-id');
What it does:
this refers to the button element that was clicked (i.e., the "Discard Changes" button).
.getAttribute('data-hero-id') retrieves the value of the data-hero-id attribute from the button. This attribute holds the unique identifier of the hero being edited.
The retrieved value is stored in the constant variable heroId.
Rationale:
Using a custom data attribute (data-hero-id) allows us to pass dynamic data (the hero's ID) from the HTML to our JavaScript without modifying the global state.
Alternatives:
One might alternatively embed the ID in the button’s text or use a hidden field. However, using a data attribute is cleaner and is the HTML5 standard for attaching custom data to elements.
Consequence of Removal:
If this line is removed, the script wouldn't know which hero to reference when discarding changes, and the subsequent redirect would fail or be incorrect.
Line 3:

  if (confirm("Are you sure you want to discard changes?")) {
What it does:
The confirm() function displays a modal dialog box with the message provided and two options: OK and Cancel.
It returns true if the user clicks OK, and false if the user clicks Cancel.
The if statement checks the return value of confirm().
Rationale:
This step is crucial for preventing accidental loss of unsaved changes. It gives the user a chance to confirm their decision.
Alternatives:
One might use a custom modal dialog implemented with HTML/CSS/JavaScript for a more stylized look, but using confirm() is quick and built-in.
Consequence of Removal:
Without this confirmation step, clicking "Discard Changes" would immediately redirect the user, potentially causing accidental loss of data.
Line 4:

    window.location.href = "/view/" + heroId;
What it does:
window.location.href sets the URL of the current window, effectively navigating the browser to a new page.
"/view/" + heroId constructs the URL by concatenating the base path "/view/" with the hero ID. For example, if heroId is "105", the URL becomes "/view/105".
Rationale:
This line redirects the user back to the hero's view page after they confirm discarding changes, allowing them to see the hero's details without the unsaved modifications.
Alternatives:
An alternative might be to use window.location.assign(...), which achieves a similar effect.
Consequence of Removal:
If this line is removed, even if the user confirms, there would be no redirect, and the discard operation would not have any visible effect.
Line 5:

  }
What it does:
This line closes the if block that began with the confirmation.
Rationale:
Properly closing the block is essential for correct code structure and to ensure that only if the user confirms, the redirect happens.
Consequence of Removal:
Not closing the block would result in a syntax error, and the JavaScript would fail to execute.
Line 6:

});
What it does:
Closes the callback function passed to addEventListener and then closes the method call.
Rationale:
It’s essential to properly close the function definition and the event listener attachment.
Consequence of Removal:
Without the closing parentheses and curly brace, you would encounter a syntax error, and the script would not run.
Summary of edit.js
Purpose:
The script attaches a click event listener to the "Discard Changes" button on the edit page.
It retrieves the hero ID from a data attribute, prompts the user for confirmation using a built-in modal dialog, and if confirmed, redirects the user back to the view page for that hero.
Approach:
We use plain JavaScript (without libraries) for simplicity.
Using a data attribute (data-hero-id) is a clean, HTML5-standard method for passing data to JavaScript.
Alternatives:
One could use jQuery for a similar effect, but plain JavaScript is lighter and modern browsers support all needed features.
Instead of confirm(), a custom modal could be implemented for a better UI, but that adds complexity.
Consequence of Removing Lines:
Removing any part of this script would either break the discard functionality or remove the confirmation step, potentially leading to accidental data loss.

*/