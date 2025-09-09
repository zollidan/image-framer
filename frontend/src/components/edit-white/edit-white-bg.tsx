import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";
import { apiPath } from "@/lib/api";

/**
 * Represents an image with its filename and URL.
 *
 * @property {string} filename - The original filename of the image.
 * @property {string} url - The URL of the processed image.
 */
interface Image {
  filename: string;
  url: string;
}

/**
 * A component for adding a white background to an image.
 *
 * This component provides a UI with a file input, a slider to adjust the
 * background size, and handles the API call to process the image. It also
 * displays the processed image or an error message.
 *
 * @returns {JSX.Element} The rendered EditWhiteBg component.
 */
export const EditWhiteBg = () => {
  const [sliderValue, setSliderValue] = useState<number[]>([1.3]);
  const [image, setImage] = useState<Image | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        setError("Пожалуйста, выберите изображение");
        return;
      }

      if (file.size > 40 * 1024 * 1024) {
        setError("Файл слишком большой.");
        return;
      }

      setSelectedFile(file);
      setError(null);
    }
  };
  const handleSubmit = async () => {
    if (!selectedFile) {
      setError("Пожалуйста, выберите файл");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile, selectedFile.name);

      const params = new URLSearchParams({
        bg_coefficient: sliderValue[0].toString(),
      });

      const response = await fetch(
        apiPath(`/api/edit/add-white-bg/?${params}`),
        {
          method: "POST",
          headers: {
            accept: "application/json",
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(`Ошибка: ${response.statusText}`);
      }

      const data = await response.json();
      setImage(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Произошла ошибка при обработке изображения"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      {error ? (
        <>
          <Alert variant="destructive" className="w-full max-w-sm">
            <AlertCircleIcon />
            <AlertTitle>{error}</AlertTitle>
          </Alert>
        </>
      ) : null}
      <Card className="w-full max-w-sm">
        {image ? (
          <>
            <CardHeader>
              <CardTitle>Готовое фото</CardTitle>
              <CardDescription>мяу мяу???</CardDescription>
            </CardHeader>
            <CardContent>
              <img
                src={apiPath(`/api${image.url}`)}
                alt={"Processed image with name: " + image.filename}
                className="shadow-sm"
              />
            </CardContent>
            <CardFooter className="flex-col space-y-2">
              <Button variant="secondary" className="w-full cursor-pointer">
                Сохранить
              </Button>
              <Button
                variant="default"
                className="w-full cursor-pointer"
                onClick={() => setImage(null)}
              >
                Новое фото
              </Button>
            </CardFooter>
          </>
        ) : (
          <>
            <CardHeader>
              <CardTitle>Добавление белой рамки на фото</CardTitle>
              <CardDescription>
                мяу мяу мяу мяу мяу мяу мяу мяу мяу мяу
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form>
                <div className="flex flex-col gap-6">
                  <div className="grid gap-2">
                    <Label htmlFor="file">File</Label>
                    <Input
                      id="file"
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      disabled={isLoading}
                    />
                  </div>
                  <Label>Ширина белой рамки: {sliderValue}</Label>
                  <Slider
                    defaultValue={sliderValue}
                    min={1}
                    max={2}
                    step={0.1}
                    onValueChange={setSliderValue}
                  />
                </div>
              </form>
            </CardContent>
            <CardFooter className="flex-col gap-2">
              <Button
                type="submit"
                className="w-full cursor-pointer"
                onClick={handleSubmit}
              >
                Обработать
              </Button>
            </CardFooter>
          </>
        )}
      </Card>
    </div>
  );
};
