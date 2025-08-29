import { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";

interface Image {
  processed_url: string;
  id: number;
  original_filename: string;
}

export const ImageList = () => {
  const [data, setData] = useState<Image[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/files/list`);

        if (!res.ok) {
          throw new Error(`HTTP error: Status ${res.status}`);
        }

        const jsonData = await res.json();
        setData(jsonData);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return (
      <div>
        <Alert variant="destructive">
          <AlertCircleIcon />
          <AlertTitle>{error.message}</AlertTitle>
        </Alert>
      </div>
    );
  }

  return (
    <div>
      <ul>
        {data.map((image) => (
          <li key={image.id}>
            <a href={image.processed_url}>{image.original_filename}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};
