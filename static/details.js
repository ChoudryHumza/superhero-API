// humza choudry section 1 hc3241

// THIS PAGE DOESNT DO MUCH FOR NOW. READ NOTE AT THE VERY BOTTOM. FOR NOW SERVER.PY AND DETAILS.HTML WORK TOGETHER TO DISPLAY THE DETAILS. THIS HERE IS PUT FOR LATER DYNAMIC REASONS. 

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
    if (e.key === 'Enter') {
         searchButton.click();
    }
});
clearButton.addEventListener('click', () => {
    window.location.href = "/";
});


/*
check notes on details.html for why i have template in both .js and .html

API Configuration & DOM Element Selection
js
Copy code
const API_TOKEN = 'a50448b352b3804680843ce2279cc856';
const BASE_URL = `https://www.superheroapi.com/api.php/${API_TOKEN}`;
What It Does:
– Declares a constant named API_TOKEN holding your unique API key.
– Declares a constant BASE_URL using a template literal that combines the base API URL with your token.
Why It’s Used:
– To centralize the API configuration so that every API call uses the correct URL and authentication.
What Happens If Removed:
– API calls would lack the necessary URL/token, causing failures.
Alternative:
– You might store these values in a configuration file, but for a small project, this is sufficient.
js
Copy code
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const clearButton = document.getElementById('clearButton');
const heroDetailsDiv = document.getElementById('heroDetails');
What It Does:
– Uses document.getElementById() to select key elements on the details page:
searchInput: The text field where users enter search queries.
searchButton: The button that triggers a search.
clearButton: The button to clear the search.
heroDetailsDiv: The container where the hero’s details will be displayed.
Why It’s Used:
– To have references to these elements so they can be updated dynamically.
What Happens If Removed:
– Without these references, the script cannot update the page or attach event handlers.
2. Storing the Original Hero ID
js
Copy code
const originalHeroId = (function() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
})();
What It Does:
– Immediately executes an anonymous function (an IIFE) to parse the URL’s query string using URLSearchParams and retrieves the value for the parameter id.
– Assigns that value to originalHeroId.
Why It’s Used:
– To remember which hero’s details were originally loaded so that if the user performs a search and then clears it, the page can restore the original hero’s details.
What Happens If Removed:
– The script would lose track of the original hero, and the “Clear” functionality wouldn’t be able to restore the correct content.
Alternative:
– You could extract the ID later in the code, but storing it immediately simplifies later restoration.
3. Search Button Event Listener (Details Page)
js
Copy code
searchButton.addEventListener('click', () => {
  const query = searchInput.value;
  if(query.trim() === "") {
    searchInput.value = "";
    searchInput.focus();
    return;
  }
  window.location.href = "/?search=" + encodeURIComponent(query);
});
What It Does:
– Attaches a click event listener to the search button. – When clicked, retrieves the search query from the input. – Uses trim() to remove any whitespace from both ends of the query. – If the trimmed query is empty, it clears the input and sets focus back to it, then exits the function. – Otherwise, it redirects the browser to the homepage with the search query appended as a query parameter (e.g., /?search=Batman).
Why It’s Used:
– To ensure that searches containing only whitespace are ignored. – To trigger a server-side search by redirecting with the query in the URL.
What Happens If Removed:
– Users might trigger searches with only whitespace, or no search would be initiated on button click.
Alternative:
– Instead of redirecting, you could use AJAX to update the page dynamically. However, the requirement is to perform server-side search.
4. Search Input Enter Key Listener
js
Copy code
searchInput.addEventListener('keyup', (e) => {
  if (e.key === 'Enter') {
    searchButton.click();
  }
});
What It Does:
– Adds an event listener to the search input that listens for the "keyup" event. – Checks if the key pressed is "Enter". – If it is, simulates a click on the search button.
Why It’s Used:
– To improve usability so that the user can press Enter to perform a search.
What Happens If Removed:
– The user would have to manually click the search button every time.
Alternative:
– You might directly call the search function, but simulating a click keeps behavior consistent.
5. Clear Button Event Listener (Details Page)
js
Copy code
clearButton.addEventListener('click', () => {
  searchInput.value = '';
  clearButton.style.display = 'none';
  window.location.href = "/view/" + originalHeroId;
});
What It Does:
– When the clear button is clicked, clears the search input. – Hides the clear button. – Redirects the browser back to the details page for the original hero by navigating to /view/<originalHeroId>.
Why It’s Used:
– To allow the user to cancel a search and return to the original hero details.
What Happens If Removed:
– Users wouldn’t have a way to clear the search and revert to the default details view.
Alternative:
– Instead of a full page redirect, you could reset the dynamic content on the page using JavaScript. But here, a redirect is used for server-side processing.
6. Helper Function to Get Query Parameter
js
Copy code
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}
What It Does:
– Defines a function that creates a URLSearchParams object from the current URL’s query string. – Returns the value associated with the parameter passed in.
Why It’s Used:
– To simplify reading URL query parameters throughout the script.
What Happens If Removed:
– You’d have to manually parse the URL every time you need a parameter.
Alternative:
– Use other methods of URL parsing, but URLSearchParams is modern and efficient.
7. Determining Which Hero to Display
js
Copy code
const heroId = getQueryParam('id');
if (heroId === "professor") {
  displayProfessorDetails();
} else if (heroId) {
  fetchHeroDetails(heroId);
} else {
  heroDetailsDiv.innerHTML = '<p>No hero specified.</p>';
}
What It Does:
– Uses the helper function getQueryParam('id') to read the id parameter from the URL query string. – If the hero id is exactly "professor", it calls displayProfessorDetails(). – Otherwise, if any hero id exists, it calls fetchHeroDetails(heroId) to retrieve hero data from the API. – If no hero id is provided, it sets the innerHTML to display “No hero specified.”
Why It’s Used:
– This conditional logic ensures the correct content is displayed based on the URL.
What Happens If Removed:
– The details page would not know which hero to display and would likely show an error.
Alternative:
– You might extract the ID from the URL path instead, if your routing is designed that way. In our case, we still use query parameters.
8. Fetching Hero Details from the API
js
Copy code
async function fetchHeroDetails(id) {
  heroDetailsDiv.innerHTML = '<p>Loading hero details...</p>';
  try {
    const response = await fetch(`${BASE_URL}/${id}`);
    const hero = await response.json();
    displayHeroDetails(hero);
  } catch (error) {
    heroDetailsDiv.innerHTML = `<p>Error fetching hero details: ${error}</p>`;
  }
}
What It Does:
– Declares an asynchronous function that takes an id parameter. – Sets a loading message in the hero details container. – Uses fetch() to call the API endpoint for the specified hero id. – Uses await to wait for the API call to complete and then converts the response to JSON. – Calls displayHeroDetails(hero) to render the fetched hero data. – If an error occurs, catches it and displays an error message.
Why It’s Used:
– To dynamically load hero details from the API based on the hero id.
What Happens If Removed:
– The details page wouldn’t retrieve or display any dynamic data for a hero.
Alternative:
– Could use XMLHttpRequest or a library like Axios, but fetch() is standard and modern.
9. Displaying Standard Hero Details
js
Copy code
function displayHeroDetails(hero) {
  heroDetailsDiv.innerHTML = `
    <img src="${hero.image.url}" alt="${hero.name}">
    <h1>${hero.name}</h1>
    <div class="hero-section">
      <h2>Biography</h2>
      <p><strong>Full Name:</strong> ${hero.biography['full-name']}</p>
      <p><strong>Alter Egos:</strong> ${hero.biography['alter-egos']}</p>
      <p><strong>Aliases:</strong> ${hero.biography.aliases.join(', ')}</p>
      <p><strong>Place of Birth:</strong> ${hero.biography['place-of-birth']}</p>
      <p><strong>First Appearance:</strong> ${hero.biography['first-appearance']}</p>
      <p><strong>Publisher:</strong> ${hero.biography.publisher}</p>
      <p><strong>Alignment:</strong> ${hero.biography.alignment}</p>
    </div>
    <div class="hero-section">
      <h2>Power Stats</h2>
      <p><strong>Intelligence:</strong> ${hero.powerstats.intelligence}</p>
      <p><strong>Strength:</strong> ${hero.powerstats.strength}</p>
      <p><strong>Speed:</strong> ${hero.powerstats.speed}</p>
      <p><strong>Durability:</strong> ${hero.powerstats.durability}</p>
      <p><strong>Power:</strong> ${hero.powerstats.power}</p>
      <p><strong>Combat:</strong> ${hero.powerstats.combat}</p>
    </div>
    <div class="hero-section">
      <h2>Appearance</h2>
      <p><strong>Gender:</strong> ${hero.appearance.gender}</p>
      <p><strong>Race:</strong> ${hero.appearance.race}</p>
      <p><strong>Height:</strong> ${hero.appearance.height.join(' / ')}</p>
      <p><strong>Weight:</strong> ${hero.appearance.weight.join(' / ')}</p>
      <p><strong>Eye Color:</strong> ${hero.appearance['eye-color']}</p>
      <p><strong>Hair Color:</strong> ${hero.appearance['hair-color']}</p>
    </div>
    <div class="hero-section">
      <h2>Work</h2>
      <p><strong>Occupation:</strong> ${hero.work.occupation}</p>
      <p><strong>Base:</strong> ${hero.work.base}</p>
    </div>
    <div class="hero-section">
      <h2>Connections</h2>
      <p><strong>Group Affiliation:</strong> ${hero.connections['group-affiliation']}</p>
      <p><strong>Relatives:</strong> ${hero.connections.relatives}</p>
    </div>
  `;
}
What It Does:
– Uses a template literal to build a large HTML string that displays all the hero’s details:
An image with the hero’s photo.
A main heading with the hero’s name.
Several sections (wrapped in elements with the class hero-section) for Biography, Power Stats, Appearance, Work, and Connections. – Inserts this HTML into the heroDetailsDiv.
Why It’s Used:
– To present all the data for a standard hero in a structured, styled format.
If Removed:
– The details page wouldn’t show any information for standard heroes.
Alternative:
– Instead of using a large template literal, you could construct elements individually and append them, but this method is concise and readable.
10. Displaying Custom Professor Details
js
Copy code
function displayProfessorDetails() {
  heroDetailsDiv.innerHTML = `
    <img src="https://www.cs.columbia.edu/~chilton/web/images/headshots/chilton-banner-headshot.jpg" alt="Professor Lydia Chilton">
    <h1>Professor Lydia Chilton</h1>
    <div class="hero-section">
      <h2>Biography &amp; Research</h2>
      <p>Lydia Chilton’s area of study is Human-Computer Interaction. Her research in AI+Design explores how artificial intelligence can empower creative problem-solving, innovation, and design.</p>
      <p>Her work is applied in creating media for journalism, developing technology for public libraries, improving risk communication during hurricanes, helping scientists explain their work, and boosting mental health in marginalized communities.</p>
    </div>
    <div class="hero-section">
      <h2>Academic Background</h2>
      <p>PhD from the University of Washington (2016)</p>
      <p>Master’s in Engineering from MIT (2009)</p>
      <p>SB from MIT (2007)</p>
      <p>Former postdoctoral fellow at Stanford University, now at Columbia Engineering since 2017.</p>
    </div>
    <div class="hero-section">
      <h2>Research &amp; Teaching</h2>
      <p>Research Areas: Graphics &amp; User Interfaces, Natural Language Processing, Artificial Intelligence &amp; Machine Learning, HCI, Design Automation, Generative AI &amp; LLMs.</p>
      <p>She leads the Computational Design Lab to build AI tools that enhance productivity by combining human creativity with computational power.</p>
      <p>She teaches courses such as User Interface Design and Designing with Generative AI.</p>
    </div>
    <div class="hero-section">
      <h2>Fun Facts</h2>
      <p>Professor Chilton has lived in Beijing three times and her Chinese name is 高雅丽 (Gao1 Ya3Li4).</p>
      <p>She even recreated famous paintings on the walls of her MIT undergraduate dorm!</p>
      <p>Contact: 612 CEPSR | lc3251@columbia.edu | (212) 853-8456</p>
    </div>
  `;
}
What It Does:
– Directly sets the innerHTML of the heroDetailsDiv to a custom HTML template for Professor Lydia Chilton. – This includes her image, her name as an <h1>, and several sections that provide her biography, academic background, research & teaching, and fun facts.
Why It’s Used:
– Because Professor Chilton’s details are unique and not fetched from the API, they are hard-coded in this function.
If Removed:
– If the hero id is “professor”, the details page wouldn’t display her custom details.
Alternative:
– You could also store this template in a separate file and load it, but hardcoding here is acceptable for a small project.
Overall Flow of details.js
API and DOM Setup:
– The script sets up the API credentials and selects necessary elements (search input, buttons, and hero details container).

Storing Original Hero ID:
– The original hero id is extracted from the URL’s query parameters and stored in originalHeroId. This ensures that if the user clears a search, the page can restore the original hero’s details.

Search and Clear Event Handlers:
– The search button’s click event checks for non-whitespace input. If valid, it redirects to the homepage with the search query (triggering a server-side search).
– The Enter key in the search input simulates a click on the search button.
– The clear button resets the search input and redirects the browser to /view/<originalHeroId> to restore the original details.

Determining Which Details to Display:
– The helper function getQueryParam('id') is used to get the hero id from the URL query string.
– Based on the value:

If the id equals "professor", displayProfessorDetails() is called.
Otherwise, if an id exists, fetchHeroDetails(heroId) is called to fetch and display that hero’s details.
If no id is found, a “No hero specified.” message is shown.
Fetching Data from the API:
– The fetchHeroDetails(id) function shows a loading message, makes an API call to fetch the hero’s data, converts it to JSON, and calls displayHeroDetails(hero) to render the data.

Displaying Data:
– displayHeroDetails(hero) constructs the HTML to show all the hero’s information in multiple sections. – displayProfessorDetails() constructs a custom HTML template for Professor Chilton.

Alternative Approaches and Effects
Using URL Path Instead of Query String:
– Instead of using getQueryParam('id'), you might design your routing so that the hero id is part of the URL path (like /view/5). In that case, you’d extract the id differently.
Client-Side vs. Server-Side Search:
– The code here redirects to the homepage for search results. An alternative is to use AJAX to update the page without reloading. However, our requirement is to use server-side search.
Element Creation:
– Instead of using innerHTML with a large template literal, you could create each element via document.createElement() and use .appendChild(), which can be more modular. For a small project, using template literals is simpler.

*/