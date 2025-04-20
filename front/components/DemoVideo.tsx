import React from "react";
import styles from "../styles/Home.module.css";

export default function VideoDemo() {
  return (
    <div className={styles.videoStream}>
      {/* Video feed */}
      <div className={styles.videoFrame}>
        <img
          src="http://127.0.0.1:5000/video_feed"
          alt="Video Stream"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: "18px",
          }}
        />
      </div>

      <span className={styles.videoLabel}>Real-Time Pose Estimation</span>
    </div>
  );
}
