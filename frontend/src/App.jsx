import { FrameGenerator } from "./components/FrameGenerator";
import { Header } from "./components/header";
function App() {
  return (
    <>
      <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
        <Header />
        <FrameGenerator />
      </div>
    </>
  );
}

export default App;
