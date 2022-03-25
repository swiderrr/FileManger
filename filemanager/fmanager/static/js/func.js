//function uploadFile(){
//        var file = document.getElementById("files").files[0];
//
//
//
//
//import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.6.6/firebase-app.js';
//import { getStorage, ref, uploadBytes } from "firebase/storage";
//
//
//// Set the configuration for your app
//    const config = {
//            apiKey: 'AIzaSyDEFfPE6-WHc59sGp0LO8fsf3uwJ8QH7Ck',
//            authDomain: 'filemanager-6b90c.firebaseapp.com',
//            databaseURL: 'https://filemanager-6b90c-default-rtdb.europe-west1.firebasedatabase.app/',
//            storageBucket: 'gs://filemanager-6b90c.appspot.com'
//        };
//
//const firebaseApp = initializeApp(config);
//const storage = getStorage();
//const storageRef = ref(storage);
//uploadBytes(storageRef, file).then((snapshot) => {
//  console.log('Uploaded a blob or file!');
//    }
// }
//
//
//// Get a reference to the storage service, which is used to create references in your storage bucket
