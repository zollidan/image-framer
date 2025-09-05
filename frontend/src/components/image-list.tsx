import { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";

/**
 * Represents a processed image record.
 *
 * @property {string} processed_url - The URL of the processed image.
 * @property {number} id - The unique identifier of the image record.
 * @property {string} original_filename - The original filename of the image.
 */
interface Image {
  processed_url: string;
  id: number;
  original_filename: string;
}

/**
 * A component that fetches and displays a list of processed images.
 *
 * It handles loading and error states, and renders a list of links
 * to the processed images.
 *
 * @returns {JSX.Element} The rendered ImageList component.
 */
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
