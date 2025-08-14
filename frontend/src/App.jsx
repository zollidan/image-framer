import { FrameGenerator } from "./components/FrameGenerator";
import { WhiteBgGenerator } from "./components/whiteBgGenerator";
import { Header } from "./components/header";
import { Routes, Route } from "react-router";
function App() {
  return (
    <>
      <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
        <Header />
        <Routes>
          <Route path="/" element={<FrameGenerator />} />
          <Route path="/white-bg" element={<WhiteBgGenerator />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
