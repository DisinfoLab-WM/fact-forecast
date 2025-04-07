/**
 * API service for communicating with the backend
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetch articles for a specific country
 * @param {string} country - Country code (e.g., 'USA')
 * @param {number} limit - Maximum number of articles to return (default: 10)
 * @returns {Promise<Object>} - Promise that resolves to the articles response
 */
export async function fetchArticlesByCountry(country, limit = 10) {
  try {
    console.log(`Fetching articles for ${country} with limit ${limit}`);
    console.log(`Request URL: ${API_BASE_URL}/articles/${country}?limit=${limit}`);
    
    const response = await fetch(`${API_BASE_URL}/articles/${country}?limit=${limit}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Server responded with status: ${response.status}`);
      console.error(`Response text: ${errorText}`);
      throw new Error(`Error fetching articles: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log(`Successfully fetched ${data.articles?.length || 0} articles for ${country}`);
    return data;
  } catch (error) {
    console.error(`Error fetching articles for ${country}:`, error);
    throw error;
  }
}

/**
 * Get the cache status from the backend
 * @returns {Promise<Object>} - Promise that resolves to the cache status
 */
export async function getCacheStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/cache-status`);
    
    if (!response.ok) {
      throw new Error(`Error fetching cache status: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching cache status:', error);
    throw error;
  }
}

/**
 * Refresh the cache for specified countries
 * @param {Array<string>} countries - List of country codes to refresh
 * @returns {Promise<Object>} - Promise that resolves to the refresh result
 */
export async function refreshCache(countries) {
  try {
    const response = await fetch(`${API_BASE_URL}/refresh-cache`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ countries }),
    });
    
    if (!response.ok) {
      throw new Error(`Error refreshing cache: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error refreshing cache:', error);
    throw error;
  }
}
