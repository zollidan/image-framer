import { useState } from "react";

export const WhiteBgGenerator = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState("Файл не выбран");
  const [isLoading, setIsLoading] = useState(false);
  const [resultImage, setResultImage] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileName(file.name);
    } else {
      setSelectedFile(null);
      setFileName("Файл не выбран");
    }
    setError("");
    setResultImage(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setError("Пожалуйста, выберите файл.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setIsLoading(true);
    setError("");
    setResultImage(null);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/edit/add-white-bg/`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log(data.url);

      if (!response.ok) {
        throw new Error(data.detail || "Произошла неизвестная ошибка");
      }

      setResultImage(import.meta.env.VITE_API_URL + data.url);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 max-w-md w-full border border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
            Создатель белого фона
          </h1>
        </div>
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="relative">
            <label
              htmlFor="file"
              className="block w-full p-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-xl cursor-pointer hover:from-pink-600 hover:to-purple-700 transition-all duration-200 text-center font-medium shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Выбрать фото...
            </label>
            <input
              type="file"
              id="file"
              accept="image/*"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              required
            />
          </div>

          <div className="text-center text-white/70 text-sm">{fileName}</div>

          <button
            type="submit"
            disabled={isLoading || !selectedFile}
            className="w-full p-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
          >
            {isLoading ? "Обработка..." : "Обработать"}
          </button>
        </form>

        {isLoading && (
          <div className="mt-8 flex justify-center">
            <div className="relative">
              <div className="w-12 h-12 border-4 border-white/30 rounded-full animate-spin"></div>
              <div className="absolute top-0 left-0 w-12 h-12 border-4 border-transparent border-t-pink-400 rounded-full animate-spin"></div>
            </div>
          </div>
        )}

        {resultImage && (
          <div className="mt-8 text-center space-y-4">
            <h2 className="text-2xl font-bold text-white mb-4">Готово!</h2>
            <div className="bg-white/10 p-4 rounded-xl border border-white/20">
              <img
                src={resultImage}
                alt="Обработанное изображение"
                className="w-full rounded-lg shadow-lg"
              />
            </div>
            <a
              href={resultImage}
              download
              className="inline-block px-6 py-3 bg-gradient-to-r from-green-500 to-teal-600 text-white rounded-lg font-medium hover:from-green-600 hover:to-teal-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Скачать изображение
            </a>
          </div>
        )}
      </div>
    </div>
  );
};
