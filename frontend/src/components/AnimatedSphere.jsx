import React from "react";
import { motion } from "framer-motion";

export default function AnimatedSphere({
  variant = "cyan",
  label = "",
  delay = 0,
  image
}) {
  return (
    <motion.div
      className="sphere-wrapper"
      animate={{ y: [0, -20, 0] }}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut",
        delay
      }}
    >
      <div className={`sphere ${variant}`}>
        <div className="sphere-glow" />
        <div className="sphere-inner" />

        {/* 🔥 IMAGE IN CENTER */}
        {image && (
          <div className="sphere-image">
            <img src={image} alt={label} />
          </div>
        )}
      </div>

{label && (
  <div className={`sphere-label ${variant}`}>
    {label}
  </div>
)}
    </motion.div>
  );
}