import { FrameGenerator } from "./components/frameGenerator";
import { WhiteBgGenerator } from "./components/whiteBgGenerator";
import { FilesList } from "./components/filesList";
import { Header } from "./components/header";
import { Footer } from "./components/footer";

import { Routes, Route } from "react-router";
function App() {
  return (
    <>
      <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
        <Header />
        <Routes>
          <Route path="/" element={<FrameGenerator />} />
          <Route path="/white-bg" element={<WhiteBgGenerator />} />
          <Route path="/images" element={<FilesList />} />
        </Routes>
        <Footer />
      </div>
    </>
  );
}

export default App;
