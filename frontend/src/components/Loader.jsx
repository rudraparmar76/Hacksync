import { motion } from "framer-motion";

export default function Loader() {
  return (
    <div className="loader-overlay">
      <motion.div
        className="loader"
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
      />
    </div>
  );
}