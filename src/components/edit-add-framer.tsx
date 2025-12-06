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
import { useState } from "react";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";

interface ImageResult {
  filename: string;
  url: string;
}

// Укажите здесь путь к вашей рамке (должна лежать в папке public)
const FRAME_SRC = "/frame.png";

export const EditAddFrameBg = () => {
  const [image, setImage] = useState<ImageResult | null>(null);
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
      setSelectedFile(file);
      setError(null);
    }
  };

  // Вспомогательная функция для загрузки картинки в объект Image
  const loadImage = (src: string): Promise<HTMLImageElement> => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous"; // Важно, если рамка на другом домене
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error("Не удалось загрузить изображение"));
      img.src = src;
    });
  };

  const handleProcess = async () => {
    if (!selectedFile) {
      setError("Пожалуйста, выберите файл");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // 1. Читаем файл пользователя
      const userImageUrl = URL.createObjectURL(selectedFile);

      // 2. Параллельно загружаем фото пользователя и рамку
      const [userImg, frameImg] = await Promise.all([
        loadImage(userImageUrl),
        loadImage(FRAME_SRC), // Загружаем рамку из статики
      ]);

      // 3. Создаем Canvas по размеру ОРИГИНАЛЬНОГО фото
      const canvas = document.createElement("canvas");
      canvas.width = userImg.width;
      canvas.height = userImg.height;

      const ctx = canvas.getContext("2d");
      if (!ctx) throw new Error("Ошибка контекста Canvas");

      // 4. Рисуем фото пользователя (фон)
      ctx.drawImage(userImg, 0, 0);

      // 5. Рисуем рамку поверх
      // Четвертый и пятый аргументы заставляют рамку растянуться под размер canvas

      // Если у вас JPG рамка с белым фоном, раскомментируйте строку ниже:
      // ctx.globalCompositeOperation = 'multiply';

      ctx.drawImage(frameImg, 0, 0, canvas.width, canvas.height);

      // Сбрасываем режим наложения (если меняли)
      ctx.globalCompositeOperation = "source-over";

      // 6. Конвертируем результат в Blob/URL
      canvas.toBlob((blob) => {
        if (!blob) throw new Error("Ошибка создания файла");

        const processedUrl = URL.createObjectURL(blob);
        setImage({
          filename: `framed_${selectedFile.name}`,
          url: processedUrl,
        });

        // Освобождаем память от старой ссылки
        URL.revokeObjectURL(userImageUrl);
        setIsLoading(false);
      }, selectedFile.type); // Сохраняем исходный формат (jpg/png)
    } catch (err) {
      console.error(err);
      setError(
        "Ошибка обработки. Проверьте, что файл рамки '/frame.png' существует в папке public."
      );
      setIsLoading(false);
    }
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
              <CardDescription>Рамка наложена и растянута</CardDescription>
            </CardHeader>
            <CardContent>
              <img
                src={image.url}
                alt={image.filename}
                className="shadow-sm w-full h-auto"
              />
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
                onClick={() => setImage(null)}
              >
                Новое фото
              </Button>
            </CardFooter>
          </>
        ) : (
          <>
            <CardHeader>
              <CardTitle>Наложение рамки</CardTitle>
              <CardDescription>
                Рамка автоматически растянется под размер фото
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="file">Выберите фото</Label>
                  <Input
                    id="file"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    disabled={isLoading}
                  />
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
                {isLoading ? "Обработка..." : "Наложить рамку"}
              </Button>
            </CardFooter>
          </>
        )}
      </Card>
    </div>
  );
};
