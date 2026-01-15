# DeliberateAI Frontend

A modern React + Vite application for collaborative AI-powered decision making.

## Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## Features

- **Authentication**: Email/password signup with Firebase, Google OAuth support
- **Password Strength**: Real-time validation with visual requirements checklist
- **Home Page**: Hero section with animated spheres, feature showcase, deliberation process
- **Routing**: React Router v6 with 3 main routes (/, /login, /signup)
- **Animations**: Framer Motion for smooth transitions and scroll-triggered animations
- **Responsive Design**: Mobile, tablet, and desktop support
- **Dark Theme**: Beautiful dark UI with gradient accents (cyan, purple, orange)

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.jsx        # Homepage with hero and features
│   │   └── Auth.jsx        # Login/signup forms
│   ├── components/
│   │   ├── Header.jsx      # Navigation header
│   │   ├── Footer.jsx      # Footer with links
│   │   ├── AnimatedSphere.jsx  # Bobbing animated spheres
│   │   ├── FeatureCard.jsx # Feature showcase cards
│   │   └── AuthWrapper.jsx # Auth page wrapper
│   ├── main.jsx            # React Router setup
│   ├── App.css             # All component styles
│   └── index.css           # Base styles & CSS variables
├── index.html              # Entry point
├── package.json            # Dependencies
└── vite.config.js          # Vite configuration
```

## Configuration

### Firebase Setup

Update the Firebase config in `src/pages/Auth.jsx`:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

## Technologies

- **React** 18.2.0 - UI library
- **React Router** 6.0 - Routing
- **Vite** 5.0 - Build tool
- **Framer Motion** 10.16 - Animations
- **Firebase** 10.13 - Authentication
- **React Intersection Observer** - Scroll animations

## Ports

- Development: `http://localhost:5173`
- Building: See `vite.config.js`

## License

All rights reserved © 2024 DeliberateAI
