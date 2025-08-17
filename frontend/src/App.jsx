import { Header } from "./components/header";
import { Routes, Route } from "react-router";
import { ImageGrid } from "./components/imageGrid";

function App() {
  return (
    <>
      <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
        <Header />
        <Routes>
          <Route path="/" element={<ImageGrid />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
