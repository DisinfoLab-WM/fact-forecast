import {db} from "./firebase.js";
import { ref, set } from "firebase/database";


set(ref(db, 'countries/USA/Fake Article Name'), {
    src: "https://fakeArticle.com",
    title: "Fake Article Name",
    description: "This is a fake article",
    author: "fake-author",
    date : "02/24/2025",
    publisher: "unknown",
  });

