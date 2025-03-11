import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import { getDay } from "./../common/date";
import axios from "axios";
import { createContext, useEffect, useState } from "react";
import AnimationWrapper from "./../common/page-animation";
import Loader from "../components/loader.component";
import BlogInteraction from "../components/blog-interaction.component";
import BlogPostCard from "../components/blog-post.component";
import BlogContent from "../components/blog-content.component";
import CommentsContainer, {
  fetchComments,
} from "../components/comments.component";

export const blogStructure = {
  title: "",
  des: "",
  content: [],
  tags: [],
  author: { personal_info: {} },
  banner: "",
  publishedAt: "",
};
export const BlogContext = createContext({});

const BlogPage = () => {
  let { blog_id } = useParams();

  const [blog, setBlog] = useState(blogStructure);
  const [loading, setLoading] = useState(true);
  const [similarBlogs, setSimilarBlogs] = useState(null);
  const [islikedByUser, setLikedByUser] = useState(false);
  const [commentsWrapper, setCommentsWrapper] = useState(false);
  const [totalParentCommentsLoaded, setTotalParentCommentsLoaded] = useState(0);
  const [comparisonData, setComparisonData] = useState([]);

  let {
    title,
    content,
    banner,
    author: {
      personal_info: { fullname, username: author_username, profile_img },
    },
    publishedAt,
    tags,
  } = blog;

  const fetchBlog = () => {
    axios
      .post(import.meta.env.VITE_SERVER_DOMAIN + "/get-blog", { blog_id })
      .then(async ({ data: { blog } }) => {
        blog.comments = await fetchComments({
          blog_id: blog._id,
          setParentCommentCountFun: setTotalParentCommentsLoaded,
        });
        setBlog(blog);

        axios
          .post(import.meta.env.VITE_SERVER_DOMAIN + "/search-blogs", {
            tag: tags[0],
            limit: 6,
            eliminate_blog: blog_id,
          })
          .then(({ data }) => {
            setSimilarBlogs(data.blogs);
          });

        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setLoading(false);
      });
  };

  const fetchComparisonData = async (query) => {
    try {
      const { data } = await axios.get(
        "http://localhost:5001/search-products",
        {
          params: { query },
        }
      );
      console.log("Backend Response:", data); // Log the backend response
      setComparisonData(data.products);
    } catch (error) {
      console.error("Error fetching comparison data:", error);
    }
  };

  useEffect(() => {
    resetStates();
    fetchBlog();
  }, [blog_id]);

  useEffect(() => {
    if (blog.title) {
      console.log("Fetching comparison data for:", blog.title); // Log the query
      fetchComparisonData(blog.title);
    }
  }, [blog]);

  useEffect(() => {
    console.log("Comparison Data:", comparisonData); // Log the comparison data
  }, [comparisonData]);

  const resetStates = () => {
    setBlog(blogStructure);
    setLoading(true);
    setSimilarBlogs(null);
    setLikedByUser(false);
    setCommentsWrapper(false);
    setTotalParentCommentsLoaded(0);
    setComparisonData([]);
  };

  return (
    <AnimationWrapper>
      {loading ? (
        <Loader />
      ) : (
        <BlogContext.Provider
          value={{
            blog,
            setBlog,
            islikedByUser,
            setLikedByUser,
            commentsWrapper,
            setCommentsWrapper,
            totalParentCommentsLoaded,
            setTotalParentCommentsLoaded,
          }}
        >
          <CommentsContainer />
          <div className="max-w-[900px] center py-10 max-lg:px-[5vw]">
            <img src={banner} className="aspect-video" />
            <div className="mt-12">
              <h2>{title}</h2>
              <div className="flex max-sm:flex-col justify-between my-8">
                <div className="flex gap-5 items-start">
                  <img src={profile_img} className="w-12 h-12 rounded-full" />
                  <p className="capitalize">
                    {fullname}
                    <br />@
                    <Link to={`/user/${author_username}`} className="underline">
                      {author_username}
                    </Link>
                  </p>
                </div>
                <p className="text-dark-grey opacity-75 max-sm:mt-6 max-sm:ml-12 max-sm:pl-5">
                  Published on {getDay(publishedAt)}
                </p>
              </div>
            </div>
            <BlogInteraction />
            <div className="my-12 font-gelasio blog-page-content">
              {content[0].blocks.map((block, i) => (
                <div key={i} className="my-4 md:my-8">
                  <BlogContent block={block} />
                </div>
              ))}
            </div>
            <BlogInteraction />
            {comparisonData.length > 0 ? (
              <div className="comparison-table my-12">
                <table className="w-full border-collapse border border-gray-300 mt-4">
                  <thead>
                    <tr className="bg-gray-200">
                      <th className="border border-gray-300 px-4 py-2">
                        Website
                      </th>
                      <th className="border border-gray-300 px-4 py-2">
                        Price
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonData.map((product, index) => (
                      <tr key={index} className="border border-gray-300">
                        <td className="border border-gray-300 px-4 py-2">
                          {product.website}
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                          ${product.price}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 my-12">
                No price comparison data available.
              </p>
            )}
            {similarBlogs != null && similarBlogs.length ? (
              <>
                <h1 className="text-2xl mt-14 mb-10 font-medium">
                  Similar Blogs
                </h1>
                {similarBlogs.map((blog, i) => {
                  let {
                    author: { personal_info },
                  } = blog;
                  return (
                    <AnimationWrapper
                      key={i}
                      transition={{ duration: 1, delay: i * 0.08 }}
                    >
                      <BlogPostCard content={blog} author={personal_info} />
                    </AnimationWrapper>
                  );
                })}
              </>
            ) : (
              ""
            )}
          </div>
        </BlogContext.Provider>
      )}
    </AnimationWrapper>
  );
};

export default BlogPage;
