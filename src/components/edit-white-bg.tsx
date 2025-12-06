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

interface ImageData {
  filename: string;
  url: string;
}

export const EditWhiteBg = () => {
  const [sliderValue, setSliderValue] = useState<number[]>([1.3]);
  const [image, setImage] = useState<ImageData | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleProcess = () => {
    if (!selectedFile) {
      setError("Пожалуйста, выберите файл");
      return;
    }

    setIsLoading(true);
    const reader = new FileReader();

    reader.onload = (event) => {
      const img = new Image();
      img.src = event.target?.result as string;

      img.onload = () => {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        if (!ctx) {
          setError("Ошибка контекста Canvas");
          setIsLoading(false);
          return;
        }

        const scaleFactor = sliderValue[0];

        const newWidth = img.width * scaleFactor;
        const newHeight = img.height * scaleFactor;

        canvas.width = newWidth;
        canvas.height = newHeight;

        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, newWidth, newHeight);

        const x = (newWidth - img.width) / 2;
        const y = (newHeight - img.height) / 2;

        ctx.drawImage(img, x, y);

        canvas.toBlob((blob) => {
          if (blob) {
            const url = URL.createObjectURL(blob);
            setImage({
              filename: `framed_${selectedFile.name}`,
              url: url,
            });
          } else {
            setError("Ошибка при создании файла");
          }
          setIsLoading(false);
        }, selectedFile.type);
      };

      img.onerror = () => {
        setError("Не удалось загрузить изображение");
        setIsLoading(false);
      };
    };

    reader.readAsDataURL(selectedFile);
  };

  const handleSave = () => {
    if (image) {
      const link = document.createElement("a");
      link.href = image.url;
      link.download = image.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="space-y-2">
      {error ? (
        <Alert variant="destructive" className="w-full max-w-sm">
          <AlertCircleIcon className="h-4 w-4" />
          <AlertTitle>{error}</AlertTitle>
        </Alert>
      ) : null}

      <Card className="w-full max-w-sm">
        {image ? (
          <>
            <CardHeader>
              <CardTitle>Готовое фото</CardTitle>
              <CardDescription>Рамка успешно добавлена</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="border rounded overflow-hidden bg-gray-100">
                <img
                  src={image.url}
                  alt={image.filename}
                  className="w-full h-auto object-contain max-h-[400px]"
                />
              </div>
            </CardContent>
            <CardFooter className="flex-col space-y-2">
              <Button
                variant="secondary"
                className="w-full cursor-pointer"
                onClick={handleSave}
              >
                Сохранить
              </Button>
              <Button
                variant="default"
                className="w-full cursor-pointer"
                onClick={() => {
                  setImage(null);
                  setSelectedFile(null);
                }}
              >
                Новое фото
              </Button>
            </CardFooter>
          </>
        ) : (
          <>
            <CardHeader>
              <CardTitle>Добавление белой рамки</CardTitle>
              <CardDescription>
                Загрузите фото, чтобы добавить поля
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="file">Выберите файл</Label>
                  <Input
                    id="file"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    disabled={isLoading}
                  />
                  {selectedFile && (
                    <p className="text-sm text-muted-foreground">
                      Выбран: {selectedFile.name}
                    </p>
                  )}
                </div>

                <div className="grid gap-2">
                  <div className="flex justify-between">
                    <Label>Размер рамки</Label>
                    <span className="text-sm text-muted-foreground">
                      x{sliderValue}
                    </span>
                  </div>
                  <Slider
                    value={sliderValue}
                    min={1.05}
                    max={2}
                    step={0.05}
                    onValueChange={setSliderValue}
                  />
                  <p className="text-xs text-muted-foreground">
                    1.0 = без рамки, 2.0 = двойной размер
                  </p>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex-col gap-2">
              <Button
                type="submit"
                className="w-full cursor-pointer"
                onClick={handleProcess}
                disabled={isLoading || !selectedFile}
              >
                {isLoading ? "Обработка..." : "Обработать"}
              </Button>
            </CardFooter>
          </>
        )}
      </Card>
    </div>
  );
};
