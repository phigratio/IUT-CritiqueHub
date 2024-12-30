import React, { useEffect, useContext, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import logo from "../imgs/logo.png";
import AnimationWrapper from "../common/page-animation";
import defaultBanner from "../imgs/blog banner.png";
import uploadImage from "../common/uploadImage";

import { Toaster, toast } from "react-hot-toast";
import { EditorContext } from "../pages/editor.pages";
import EditorJs from "@editorjs/editorjs";
import { tools } from "./tools.component";
import { UserContext } from "../App";
import { useParams } from "react-router-dom";

const BlogEditor = () => {
  let navigate = useNavigate();
  let{blog_id}= useParams();
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  
  let {
    userAuth: { access_token },
  } = useContext(UserContext);
 
  let {
    blog = {},
    blog: { title = "", banner = "", content = "", tags = [], des = "" } = {},
    setBlog,
    textEditor,
    setTextEditor,
    editorState,
    setEditorState,
  } = useContext(EditorContext);
  
  useEffect(() => {
    if (!textEditor?.isReady) {
      setTextEditor(
        new EditorJs({
          holder: "textEditor",
          data: Array.isArray(content) ? content[0] : content,
          tools: tools,
          placeholder: "Let's Write an Awesome Review",
        })
      );
    }
  }, [textEditor, content, setTextEditor]);
  
  const handlePublishEvent = () => {
    if (!banner.length) {
      return toast.error("Upload a blog banner to publish it");
    }

    if (!title.length) {
      return toast.error("Write blog title to publish it");
    }

    if (textEditor.isReady) {
      textEditor
        .save()
        .then((data) => {
          if (data.blocks.length) {
            setBlog({ ...blog, content: data });
            setEditorState("publish");
          } else {
            return toast.error("Write something in your blog to publish it");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };
  const handleTitleKeyDown = (e) => {
    if (e.keyCode == 13) {
      e.preventDefault();
    }
  };
  const handleTitleChange = (e) => {
    let input = e.target;
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
    setBlog({ ...blog, title: input.value });
  };
  const handleError = (e) => {
    let img = e.target;

    img.src = defaultBanner;
  };
  const handleBannerUpload = async (e) => {
    let img = e.target.files[0];
    if (img) {
      let loadingToast = toast.loading("Uploading...");
      setUploading(true);
      setError(null);
      try {
        const url = await uploadImage(img);
        if (url) {
          toast.dismiss(loadingToast);
          toast.success("Uploaded !!");

          setBlog({ ...blog, banner: url });
        } else {
          toast.dismiss(loadingToast);
          toast.error("Upload Failed");
          setError("Failed to upload image");
        }
      } catch (err) {
        console.error("Error in handleBannerUpload:", err);
        setError("Error uploading image. Please try again.");
      } finally {
        setUploading(false);
      }
    }
  };
  const handleSaveDraft = (e) => {
    if (e.target.className.includes("disable")) {
      return;
    }

    if (!title.length) {
      return toast.error("Write Review Title before saving it as a draft");
    }

    let loadingToast = toast.loading("Saving Draft... ⏳");

    e.target.classList.add("disable");

    if (textEditor.isReady) {
      textEditor.save().then((content) => {
        let blogObj = {
          title,
          banner,
          des,
          content,
          tags,
          draft: true,
        };
        axios
          .post(import.meta.env.VITE_SERVER_DOMAIN + "/create-blog", {...blogObj,id:blog_id}, {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then(() => {
            e.target.classList.remove("disable");
            toast.dismiss(loadingToast);
            toast.success("Saved 👌");

            setTimeout(() => {
              navigate("/");
            }, 500);
          })
          .catch(({ response }) => {
            e.target.classList.remove("disable");
            toast.dismiss(loadingToast);

            return toast.error(response.data.error);
          });
      });
    }
  };
  return (
    <>
      <nav className="navbar">
        <Link to="/" className="flex-none w-10">
          <img src={logo} />
        </Link>
        <p className="max-md:hidden text-black line-clamp-1 w-full">
          {title.length > 0 ? title : "New Blog"}
        </p>

        <div className="flex gap-4 ml-auto">
          <button className="btn-dark py-2" onClick={handlePublishEvent}>
            Publish
          </button>
          <button className="btn-light py-2" onClick={handleSaveDraft}>
            Save Draft
          </button>
        </div>
      </nav>
      <Toaster />
      <AnimationWrapper>
        <section>
          <div className="mx-auto max-w-[900px] w-full">
            <div className="relative aspect-video bg-white border-4 border-grey hover:opacity-80 ">
              <label htmlFor="uploadBanner">
                <img src={banner} onError={handleError} className="z-20" />
                <input
                  id="uploadBanner"
                  type="file"
                  accept=".png, .jpg, .jpeg"
                  hidden
                  onChange={handleBannerUpload}
                />
              </label>
            </div>

            <textArea
              defaultValue={title}
              placeholder="Review Title"
              className="text-4xl font-medium w-full h-20 outline-none resize-none mt-10 leading-tight placeholder:opacity-40"
              onKeyDown={handleTitleKeyDown}
              onChange={handleTitleChange}
            ></textArea>

            <hr className="w-full opacity-10 my-5" />
            <div id="textEditor" className="font-gelasio"></div>
          </div>
        </section>
      </AnimationWrapper>
    </>
  );
};

export default BlogEditor;
