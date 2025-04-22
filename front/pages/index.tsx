import Head from "next/head";
import styles from "../styles/Home.module.css";
import VideoStream from "../components/VideoStream";
import Advice from "../components/Advice";
import { useState, useEffect, useRef } from "react";
import DemoVideo from "../components/DemoVideo";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([
    { from: "bot", text: "Hi! How can I help you today?" },
  ]);
  const [featuresOpen, setFeaturesOpen] = useState(false);
  const [webcamOpen, setWebcamOpen] = useState(false);
  const webcamRef = useRef<HTMLVideoElement>(null);
  const [loading, setLoading] = useState(false);

  async function sendToGemini(message: string): Promise<string> {
    const apiKey = "AIzaSyDDZPiXRKGHjGKPFYSv3bFrV_BPG_ZxSeQ";
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
    const body = {
      contents: [
        {
          parts: [
            {
              text: "You are a helpful assistant that only answers health, wellness, and safety related questions. If a user asks about anything else, politely respond that you can only discuss health-related topics.",
            },
            { text: message },
          ],
        },
      ],
    };
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      return (
        data?.candidates?.[0]?.content?.parts?.[0]?.text ||
        "Sorry, I couldn't get a response."
      );
    } catch {
      return "Sorry, there was an error contacting the AI service.";
    }
  }

  useEffect(() => {
    if (typeof window === "undefined") return;
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const apply = () => setDarkMode(mq.matches);
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      document.body.classList.toggle("dark", darkMode);
    }
  }, [darkMode]);

  useEffect(() => {
    let stream: MediaStream | null = null;
    if (webcamOpen && typeof window !== "undefined" && navigator.mediaDevices) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((s) => {
          stream = s;
          if (webcamRef.current) {
            webcamRef.current.srcObject = stream;
            webcamRef.current.play();
          }
        })
        .catch(() => {});
    }
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [webcamOpen]);

  return (
    <div className={styles.container}>
      <Head>
        <title>ICI - AI Powered Human Fall Detection</title>
        <meta
          name="description"
          content="AI-powered human fall detection with real-time video streaming."
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
        />
      </Head>
      <header className={styles.header}>
        <div className={styles.logo}>
          <img
            src="/ICU.svg"
            alt="ICU Logo"
            style={{
              height: 36,
              width: "auto",
              display: "block",
              color: "#18382B",
            }}
          />
        </div>
        <nav>
          <a href="#">Home</a>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              setFeaturesOpen(true);
            }}
          >
            Features
          </a>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              document
                .getElementById("safety-tips")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            Blog
          </a>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              document
                .getElementById("footer")
                ?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            About
          </a>
        </nav>
        <div>
          <button className={styles.cta} onClick={() => setWebcamOpen(true)}>
            Try a Demo
          </button>
        </div>
      </header>
      {featuresOpen && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(24, 56, 43, 0.25)",
            zIndex: 3000,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
          onClick={() => setFeaturesOpen(false)}
        >
          <div
            style={{
              background: "#fff",
              borderRadius: 16,
              boxShadow: "0 4px 32px rgba(24,56,43,0.18)",
              padding: "2rem 2.5rem",
              minWidth: 340,
              maxWidth: "90vw",
              maxHeight: "80vh",
              overflowY: "auto",
              position: "relative",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              style={{
                position: "absolute",
                top: 12,
                right: 18,
                background: "none",
                border: "none",
                fontSize: "2rem",
                color: "#18382b",
                cursor: "pointer",
                lineHeight: 1,
              }}
              aria-label="Close features"
              onClick={() => setFeaturesOpen(false)}
            >
              ×
            </button>
            <h2 style={{ marginBottom: "1.2rem", color: "#18382b" }}>
              Application Features
            </h2>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                color: "#18382b",
                fontSize: "1.05rem",
              }}
            >
              <thead>
                <tr>
                  <th
                    style={{
                      borderBottom: "1px solid #eaf4ee",
                      borderTop: "1px solid #eaf4ee",
                      padding: "0.5rem",
                      textAlign: "left",
                      background: "#f8faf9",
                    }}
                  >
                    Feature
                  </th>
                  <th
                    style={{
                      borderBottom: "1px solid #eaf4ee",
                      borderTop: "1px solid #eaf4ee",
                      padding: "0.5rem",
                      textAlign: "left",
                      background: "#f8faf9",
                    }}
                  >
                    Description
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      accessibility_new
                    </span>
                    Real-time Fall Detection
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    Detects human falls instantly using AI-powered video
                    analysis.
                  </td>
                </tr>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      videocam
                    </span>
                    Live Video Streaming
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    Streams video in real-time for monitoring and verification.
                  </td>
                </tr>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      notification_important
                    </span>
                    Instant Alerts
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    Sends immediate notifications to caregivers or staff when a
                    fall is detected.
                  </td>
                </tr>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      lock
                    </span>
                    Privacy Protection
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    Ensures data privacy and secure video handling.
                  </td>
                </tr>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      monitoring
                    </span>
                    Analytics Dashboard
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                      borderBottom: "1px solid #f0f4f2",
                    }}
                  >
                    Provides insights and statistics on fall incidents and
                    response times.
                  </td>
                </tr>
                <tr>
                  <td
                    style={{
                      padding: "0.5rem",
                      verticalAlign: "top",
                    }}
                  >
                    <span
                      className="material-symbols-outlined"
                      style={{ verticalAlign: "middle", marginRight: 8 }}
                    >
                      devices
                    </span>
                    Multi-Device Support
                  </td>
                  <td
                    style={{
                      padding: "0.5rem",
                    }}
                  >
                    Accessible from desktop, tablet, and mobile devices.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
      {webcamOpen && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(24, 56, 43, 0.25)",
            zIndex: 4000,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
          onClick={() => setWebcamOpen(false)}
        >
          <div
            style={{
              background: "#fff",
              borderRadius: 16,
              boxShadow: "0 4px 32px rgba(24,56,43,0.18)",
              padding: "2rem 2.5rem",
              minWidth: 340,
              maxWidth: "90vw",
              maxHeight: "80vh",
              overflowY: "auto",
              position: "relative",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              style={{
                position: "absolute",
                top: 12,
                right: 18,
                background: "none",
                border: "none",
                fontSize: "2rem",
                color: "#18382b",
                cursor: "pointer",
                lineHeight: 1,
              }}
              aria-label="Close webcam"
              onClick={() => setWebcamOpen(false)}
            >
              ×
            </button>
            <h2 style={{ marginBottom: "1.2rem", color: "#18382b" }}>
              Live Demo
            </h2>
            <DemoVideo />
            <div style={{ color: "#888", fontSize: "0.98rem" }}>
              The video feed is powered by Flask and Mediapipe.
            </div>
          </div>
        </div>
      )}
      <main>
        <section className={styles.hero}>
          <div>
            <h1>AI Powered Human Fall Detection</h1>
            <p>
              Real-time safety monitoring using AI and video streaming. Protect
              your loved ones and ensure rapid response to falls.
            </p>
            <button className={styles.cta} onClick={() => setWebcamOpen(true)}>
              Get Started
            </button>
          </div>
          <VideoStream />
        </section>
        <section className={styles.trusted}>
          <p>Trusted by leading Hospitals</p>
          <div className={styles.logos}>
            <img
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8GeTr4PU0yQ6DIRb_FieQ_phiYdetSeFsDQ&s"
              alt="Company 1"
            />
            <img
              src="https://www.cliniquelesoliviers.net/sites/all/themes/zayatine/skins/img/logo-zayatine-fr.svg"
              alt="Company 2"
            />
            <img
              src="https://www.clinique-elyosr-maternite.com/assets/img/groupe-el-yosr.png"
              alt="Company 3"
            />
          </div>
        </section>
        <Advice />
        <section id="safety-tips" className={styles.advice}></section>
      </main>
      <footer className={styles.footer} id="footer">
        <div className={styles.logo}>
          <img
            src="/ICU.svg"
            alt="ICU Logo"
            style={{
              height: 36,
              width: "auto",
              display: "block",
            }}
          />
        </div>
        <div className={styles.footerLinks}>
          <div>
            <h4>Company</h4>
            <a href="#">About us</a>
            <a href="#">Careers</a>
            <a href="#">Press</a>
            <a href="#">News</a>
            <a href="#">Media kit</a>
            <a href="#">Contact</a>
          </div>
          <div>
            <h4>Resources</h4>
            <a href="#">Blog</a>
            <a href="#">Newsletter</a>
            <a href="#">Events</a>
            <a href="#">Help centre</a>
            <a href="#">Tutorials</a>
            <a href="#">Support</a>
          </div>
          <div>
            <h4>Social</h4>
            <a href="#">Twitter</a>
            <a href="#">LinkedIn</a>
            <a href="#">Facebook</a>
            <a href="#">GitHub</a>
            <a href="#">AngelList</a>
            <a href="#">Dribbble</a>
          </div>
          <div>
            <h4>Legal</h4>
            <a href="#">Terms</a>
            <a href="#">Privacy</a>
            <a href="#">Cookies</a>
            <a href="#">Licenses</a>
            <a href="#">Settings</a>
            <a href="#">Contact</a>
          </div>
        </div>
      </footer>
      {!chatOpen && (
        <button
          className={styles.chatBotButton}
          onClick={() => setChatOpen(true)}
          aria-label="Open chat bot"
        >
          <span className="material-symbols-outlined">robot_2</span>
        </button>
      )}
      {chatOpen && (
        <div
          className={styles.chatBackdrop}
          onClick={() => setChatOpen(false)}
          aria-label="Close chat bot"
        />
      )}
      <div
        className={`${styles.chatPanel} ${
          chatOpen ? styles.chatPanelOpen : ""
        }`}
      >
        <div className={styles.chatPanelHeader}>
          <span>ICU Chat Bot</span>
          <button
            className={styles.chatPanelClose}
            onClick={() => setChatOpen(false)}
            aria-label="Close chat bot"
          >
            ×
          </button>
        </div>
        <div className={styles.chatPanelBody}>
          {chatMessages.map((msg, idx) => (
            <div
              key={idx}
              className={styles.chatPanelMessage}
              style={
                msg.from === "user"
                  ? { background: "#dbeee2", textAlign: "right" }
                  : {}
              }
            >
              {msg.from === "bot" ? <b>Bot:</b> : <b>You:</b>} {msg.text}
            </div>
          ))}
          {loading && (
            <div className={styles.chatPanelMessage}>
              <b>Bot:</b> <span style={{ color: "#888" }}>Thinking…</span>
            </div>
          )}
        </div>
        <form
          className={styles.chatPanelInputBar}
          onSubmit={async (e) => {
            e.preventDefault();
            if (chatInput.trim() === "") return;
            setChatMessages([
              ...chatMessages,
              { from: "user", text: chatInput },
            ]);
            setLoading(true);
            const userMessage = chatInput;
            setChatInput("");
            const reply = await sendToGemini(userMessage);
            setChatMessages((msgs) => [...msgs, { from: "bot", text: reply }]);
            setLoading(false);
          }}
        >
          <input
            className={styles.chatPanelInput}
            type="text"
            placeholder="Type your message…"
            autoComplete="off"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            disabled={loading}
          />
          <button
            className={styles.chatPanelSend}
            type="submit"
            disabled={loading}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
