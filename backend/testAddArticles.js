import {db} from "./firebase.js";
import { ref, set } from "firebase/database";

const base_path = "countries/USA/articles/";
set(ref(db, base_path + 'Fake Article Name'), {
    src: "https://fakeArticle.com",
    title: "Fake Article Name",
    description: "This is a fake article",
    author: "fake-author",
    date : "02/24/2025",
    publisher: "unknown",
  });

