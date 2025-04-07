import { fetchArticlesByCountry } from './services/api.js';

let narrativeContainer = document.querySelector("#narratives");
let loadingIndicator = null;

/**
 * Create a loading indicator
 */
function showLoading() {
    // Create loading indicator if it doesn't exist
    if (!loadingIndicator) {
        loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.innerHTML = `
            <div class="spinner"></div>
            <p>Loading articles...</p>
        `;
    }
    narrativeContainer.appendChild(loadingIndicator);
}

/**
 * Hide the loading indicator
 */
function hideLoading() {
    if (loadingIndicator && loadingIndicator.parentNode) {
        loadingIndicator.parentNode.removeChild(loadingIndicator);
    }
}

/**
 * Create a narrative card for an article
 * @param {Object} article - The article data
 */
function createNarrative(article) {
    const title = article.metadata.articleTitle;
    const source = article.metadata.siteName;
    const date = new Date(article.metadata.datePublished).toLocaleDateString();
    
    // Extract first paragraph or a portion of the article text for the description
    let description = '';
    if (article.content && article.content.articleText) {
        // Get the first 250 characters of the article text
        const fullText = article.content.articleText;
        description = fullText.substring(0, 250) + (fullText.length > 250 ? '...' : '');
    }
    
    let newNarrative = document.createElement('div');
    newNarrative.className = 'narrative-card';
    newNarrative.innerHTML = `
        <h3 class="narrative-title">${title}</h3>
        <div class="narrative-meta">
            <span class="narrative-source">${source}</span>
            <span class="narrative-date">${date}</span>
        </div>
        <p class="narrative-description">${description}</p>
        <a href="${article.metadata.url}" target="_blank" class="read-more">Read Full Article</a>
    `;
    
    narrativeContainer.appendChild(newNarrative);
}

/**
 * Create an error message
 * @param {string} message - The error message to display
 */
function createErrorMessage(message) {
    let errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.innerHTML = `
        <p>${message}</p>
        <button id="retry-button">Retry</button>
    `;
    narrativeContainer.appendChild(errorElement);
    
    // Add event listener to retry button
    document.getElementById('retry-button').addEventListener('click', () => {
        const countryElement = document.querySelector('#selectedCountry');
        if (countryElement && countryElement.textContent !== 'No Country') {
            loadArticlesForCountry(countryElement.textContent);
        }
    });
}

/**
 * Empty the narratives container
 */
export function emptyNarratives() {
    while (narrativeContainer.firstChild) {
        narrativeContainer.removeChild(narrativeContainer.firstChild);
    }
}

/**
 * Load articles for a specific country
 * @param {string} country - The country code
 */
export async function loadArticlesForCountry(country) {
    console.log(`Loading articles for country: ${country}`);
    
    if (!country || country === 'No Country') {
        console.log('No country selected, skipping article load');
        return;
    }
    
    emptyNarratives();
    showLoading();
    
    try {
        console.log(`Attempting to fetch articles for ${country}`);
        const data = await fetchArticlesByCountry(country, 10);
        hideLoading();
        
        console.log('API response:', data);
        
        if (data.articles && data.articles.length > 0) {
            console.log(`Found ${data.articles.length} articles for ${country}`);
            data.articles.forEach((article, index) => {
                console.log(`Creating narrative for article ${index + 1}`);
                createNarrative(article);
            });
        } else {
            console.warn(`No articles found for ${country}`);
            createErrorMessage(`No articles found for ${country}`);
        }
    } catch (error) {
        hideLoading();
        console.error(`Error loading articles for ${country}:`, error);
        createErrorMessage(`Failed to load articles for ${country}. Please try again later.`);
    }
}
