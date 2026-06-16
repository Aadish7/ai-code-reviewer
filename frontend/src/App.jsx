import { useEffect, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function App() {
  const [repos, setRepos] = useState([]);
  const [pulls, setPulls] = useState([]);
  const [review, setReview] = useState("");
  const [selectedRepo, setSelectedRepo] = useState("");
  const [loading, setLoading] = useState(false);

  const [username, setUsername] =
    useState("Aadish7");

  const searchRepositories = () => {
    axios
      .get(
        `http://127.0.0.1:8000/repos/${username}`
      )
      .then((response) => {
        setRepos(response.data);
        setPulls([]);
        setReview("");
      })
      .catch(console.error);
  };

  useEffect(() => {
    searchRepositories();
  }, []);

  const loadPullRequests = (
    repoName
  ) => {
    setSelectedRepo(repoName);

    axios
      .get(
        `http://127.0.0.1:8000/pulls/${username}/${repoName}`
      )
      .then((response) => {
        setPulls(response.data);
      })
      .catch(console.error);
  };

  const reviewPR = (
    prNumber
  ) => {
    setLoading(true);

    axios
      .get(
        `http://127.0.0.1:8000/review-pr/${username}/${selectedRepo}/${prNumber}`
      )
      .then((response) => {
        setReview(
          response.data.review
        );
      })
      .finally(() =>
        setLoading(false)
      );
  };

  const reviewRepository = (
    repoName
  ) => {
    setLoading(true);

    axios
      .get(
        `http://127.0.0.1:8000/review-repo/${username}/${repoName}`
      )
      .then((response) => {
        setReview(
          response.data.review
        );
      })
      .finally(() =>
        setLoading(false)
      );
  };

  return (
    <div
      style={{
        background: "#0d1117",
        color: "white",
        minHeight: "100vh",
        padding: "30px",
      }}
    >
      <h1>
        AI Code Reviewer
      </h1>

      <h2>
        Search GitHub User
      </h2>

      <input
        value={username}
        onChange={(e) =>
          setUsername(
            e.target.value
          )
        }
        style={{
          padding: "10px",
          width: "300px",
        }}
      />

      <button
        onClick={
          searchRepositories
        }
        style={{
          marginLeft: "10px",
        }}
      >
        Search
      </button>

      <h2>
        Repositories
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fill,minmax(300px,1fr))",
          gap: "20px",
        }}
      >
        {repos.map((repo) => (
          <div
            key={repo.id}
            style={{
              background:
                "#161b22",
              padding: "20px",
              borderRadius:
                "12px",
            }}
          >
            <h3>
              {repo.name}
            </h3>

            <p>
              ⭐ Stars:{" "}
              {
                repo.stargazers_count
              }
            </p>

            <p>
              🍴 Forks:{" "}
              {repo.forks_count}
            </p>

            <p>
              💻 Language:{" "}
              {repo.language ||
                "Unknown"}
            </p>

            <button
              onClick={() =>
                loadPullRequests(
                  repo.name
                )
              }
            >
              Pull Requests
            </button>

            <button
              style={{
                marginLeft:
                  "10px",
              }}
              onClick={() =>
                reviewRepository(
                  repo.name
                )
              }
            >
              Review Repo
            </button>
          </div>
        ))}
      </div>

      <h2
        style={{
          marginTop: "40px",
        }}
      >
        Pull Requests
      </h2>

      {pulls.map((pr) => (
        <div
          key={pr.id}
          style={{
            background:
              "#161b22",
            padding: "10px",
            marginBottom:
              "10px",
            borderRadius:
              "10px",
          }}
        >
          #{pr.number} -{" "}
          {pr.title}

          <button
            style={{
              marginLeft:
                "10px",
            }}
            onClick={() =>
              reviewPR(
                pr.number
              )
            }
          >
            Review PR
          </button>
        </div>
      ))}

      <h2
        style={{
          marginTop: "40px",
        }}
      >
        AI Review
      </h2>

      {loading && (
        <p>
          🤖 Reviewing...
        </p>
      )}

      {!loading &&
        review && (
          <div
            style={{
              background:
                "#161b22",
              padding: "20px",
              borderRadius:
                "12px",
            }}
          >
            <ReactMarkdown>
              {review}
            </ReactMarkdown>
          </div>
        )}
    </div>
  );
}

export default App;