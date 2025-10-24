// app.config.js
require('dotenv').config(); 

module.exports = {
  expo: {
    name: "CoherenceRider",
    slug: "coherencerider",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    splash: {
      image: "./assets/splash.png",
      resizeMode: "contain",
      backgroundColor: "#1a1a1a"
    },
    assetBundlePatterns: ["**/*"],
    ios: {
      supportsTablet: true
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/icon.png",
        backgroundColor: "#1a1a1a"
      },
      package: "org.xai.coherencerider",
      versionCode: 1
    },
    plugins: [
      "expo-sensors",
      "expo-location",
      "expo-camera",
      "expo-media-library",
      "expo-av"
    ],
    // The Global Variables are defined here!
    extra: {
      // EAS_PROJECT_ID is often generated after your first build, 
      // but can be set via env var or hardcoded for a new repo.
      eas: {
        projectId: process.env.EAS_PROJECT_ID || "your-eas-project-id" 
      },
      // Backend URL (Default is Termux local server)
      backendUrl: process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:5001',
    }
  }
};
