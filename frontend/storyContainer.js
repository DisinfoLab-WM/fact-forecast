import newCustomView from "./customMapView";

let narrativeContainer = document.querySelector("#narratives");

export function getNArticles(country, n) {
  let request_url = `/dummy/?n=${n}&country=${country}`;
  console.log(request_url);
  fetch(request_url)
    .then((prom) => prom.json())
    .then((data) =>
      data.forEach((art) => createNarrative(art.title, art.description)),
    );
}

function createNarrative(narrativeTitle, briefDescription) {
  let newNarrative = document.createElement("div");
  newNarrative.innerHTML = `
    <h3 class="narrative-title">${narrativeTitle}</h3>
    <p class="narrative-description">${briefDescription}</p>
`;
  narrativeContainer.appendChild(newNarrative);
}

export function emptyNarratives() {
  while (narrativeContainer.firstChild) {
    narrativeContainer.removeChild(narrativeContainer.firstChild);
  }
}
// random stuff for example work
export function createRandomNarrative() {
  let narrative = getRandomNarrative();
  createNarrative(narrative.title, narrative.description);
}

function getRandomNarrative() {
  const randomIndex = Math.floor(Math.random() * trendingNarratives.length);
  const randomNarrative = trendingNarratives[randomIndex];
  return randomNarrative;
}

const trendingNarratives = [
  {
    title: "Democratic Digital Strategy",
    description:
      "The Democratic Party is implementing a new digital strategy involving collaborations with online influencers to enhance engagement and resonate with modern audiences. Spearheaded by Senator Cory Booker, the initiative aims to double online interactions within a year. While it has seen early successes, it has also faced criticism from both liberals and conservatives regarding its authenticity.",
  },
  {
    title: "Use of Wartime Law for Deportations",
    description:
      "Trump administration officials are defending the use of wartime laws to deport Venezuelan migrants, a move that has sparked legal debates and controversy.",
  },
  {
    title: "Gelatin Consumption Craze",
    description:
      "There's a growing trend on social media platforms, especially TikTok, where users are creating and consuming gelatin-based recipes for their perceived health benefits. Gelatin is believed to support skin elasticity, hydration, and overall health. However, experts caution about the high sugar content in many gelatin-based recipes.",
  },
  {
    title: "Cottage Cheese Shortage in Australia",
    description:
      "A viral recipe known as the Hot Honey Sweet Potato Beef Bowl has led to a surge in demand for cottage cheese in Australia, causing shortages in supermarkets. Influencers Michael Finch and Danielle Mitchell popularized the dish, highlighting the impact of social media trends on consumer behavior.",
  },
  {
    title: "Park Shooting Arrests",
    description:
      "Three suspects have been arrested in connection with a mass shooting at a park, prompting discussions about public safety and gun control measures.",
  },
  {
    title: "Segway Scooter Recall",
    description:
      "Segway has recalled 220,000 scooters due to fall hazards, affecting consumers and prompting safety reviews.",
  },
  {
    title: "George Foreman's Passing",
    description:
      "Legendary boxing champion George Foreman has passed away at the age of 76, marking the end of an era in sports history.",
  },
  {
    title: "Super Bowl Champions Visit the White House",
    description:
      "President Trump has extended an invitation to the Kansas City Chiefs to visit the White House following their Super Bowl victory, continuing the tradition of honoring sports champions.",
  },
  {
    title: "Pope Francis' Health",
    description:
      "Pope Francis has been discharged from the hospital to continue his recovery at the Vatican, appearing frail but stable.",
  },
  {
    title: "Iceland's Minister Resigns",
    description:
      "Iceland's minister for children has resigned following revelations of a relationship with a teenager, sparking political and public reactions.",
  },
];
