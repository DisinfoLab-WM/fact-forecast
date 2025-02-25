import {db} from "./firebase.js";
import { ref, set } from "firebase/database";

/** 
 * @details base path for adding articles to real time database
 * */ 
const base_path = "countries/USA/articles/";

/**
 * @details set is Firebase api for writing data to the database
 */
set(ref(db, base_path + 'Fake Article Name'), {
    src: "https://fakeArticle.com",
    title: "Fake Article Name",
    description: "This is a fake article",
    author: "fake-author",
    date : "02/24/2025",
    publisher: "unknown",
  });

