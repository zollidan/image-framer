import { useState, useEffect } from "react";

export const FilesList = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${import.meta.env.VITE_API_URL}/files/list`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Ошибка сети: ${response.status}`);
        }
        return response.json();
      })
      .then((fetchedData) => {
        setData(fetchedData);
      })
      .catch((error) => {
        setError(error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Загрузка данных...</p>;
  if (error) return <p>Ошибка: {error.message}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Галерея:</h1>
      {data && data.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {data.map((file) => (
            <div
              key={file.id}
              className="relative aspect-square overflow-hidden rounded-lg shadow-md"
            >
              <img
                src={import.meta.env.VITE_API_URL + file.processed_url}
                alt={file.original_filename}
                className="absolute inset-0 w-full h-full object-cover"
                loading="lazy"
              />
            </div>
          ))}
        </div>
      ) : (
        <p>Фотографии не найдены.</p>
      )}
    </div>
  );
};
