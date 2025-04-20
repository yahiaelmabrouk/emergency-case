import React from "react";
import styles from "../styles/Home.module.css";

export default function VideoStream() {
  return (
    <div className={styles.videoStream}>
      {/* Video feed */}
      <div className={styles.videoFrame}>
        <video
          src="/Intro.mp4" // Path to the video in the public folder
          autoPlay
          loop
          muted
          playsInline
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: "18px",
          }}
        />
      </div>

      <span className={styles.videoLabel}>Intro Video</span>
    </div>
  );
}
