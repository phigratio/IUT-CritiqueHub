// import React from "react";
// import axios from "axios";

// const uploadImage = async (img) => {
//   let imgUrl = null;
//   await axios
//     .get(import.meta.env.VITE_SERVER_DOMAIN + "/get-upload-url")
//     .then(async ({ data: { uploadURL } }) => {
//       await axios({
//         method: "PUT",
//         url: uploadURL,
//         headers: {
//           "Content-Type": img.type || "application/octet-stream",
//         },
//         data: img,
//         timeout: 10000,
//       }).then(() => {
//         imgUrl = uploadURL.split("?")[0];
//       });
//     });
//   return imgUrl;
// };

// export default uploadImage;

import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { storage } from "./firebase"; // Make sure Firebase is properly configured
import { v4 as uuidv4 } from "uuid"; // For generating unique file names

const uploadImage = async (img) => {
  if (!img) return null;

  const uniqueFileName = `${uuidv4()}_${img.name}`; // Generate a unique name for the image
  const imageRef = ref(storage, `images/${uniqueFileName}`); // Create a reference in Firebase Storage

  try {
    // Upload the image to Firebase
    const uploadTask = await uploadBytesResumable(imageRef, img);

    // Get the download URL once the upload is complete
    const imgUrl = await getDownloadURL(uploadTask.ref);
    return imgUrl;
  } catch (error) {
    console.error("Error during image upload:", error);
    return null;
  }
};

export default uploadImage;
