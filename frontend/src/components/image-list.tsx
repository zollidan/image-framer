import { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";
import { apiPath } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel";

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
  const [api, setApi] = useState<CarouselApi>();
  const [current, setCurrent] = useState(0);
  const [count, setCount] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(apiPath(`/api/files/list`));

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

  useEffect(() => {
    if (!api) {
      return;
    }

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);

    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);

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
    <div className="mx-auto max-w-xs">
      <Carousel setApi={setApi} className="w-full max-w-xs">
        <CarouselContent>
          {data.map((image) => (
            <CarouselItem key={image.id}>
              <Card>
                <CardContent className="flex aspect-square items-center justify-center p-6">
                  <div className="text-center">
                    <img 
                      src={apiPath(`/api${image.processed_url}`)} 
                      alt={image.original_filename}
                      className="max-w-full max-h-full object-contain"
                    />
                    <p className="mt-2 text-sm text-muted-foreground">{image.original_filename}</p>
                  </div>
                </CardContent>
              </Card>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
      {count > 0 && (
        <div className="text-muted-foreground py-2 text-center text-sm">
          Image {current} of {count}
        </div>
      )}
    </div>
  );
};
