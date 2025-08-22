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

export const EditWhiteBg = () => {
  const [sliderValue, setSliderValue] = useState<number[]>([1.3]);

  const handleSubmit = () => {
    console.log(sliderValue);
  };
  return (
    <div>
      <Card className="w-full max-w-sm">
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
                <Input type="file" required />
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
      </Card>
    </div>
  );
};
