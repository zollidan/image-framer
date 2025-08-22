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

export const EditAddFrameBg = () => {
  const handleSubmit = () => {
    console.log("Submit button clicked");
  };
  return (
    <div>
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Добавление пленочной рамки на фото</CardTitle>
          <CardDescription>
            мяу мяу мяу мяу мяу мяу мяу мяу мяу мяу выбор рамки и добавление
            новой позже
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="file">File</Label>
                <Input type="file" required />
              </div>
            </div>
            <Button variant="default" disabled className="mt-4">
              Добавить рамку
            </Button>
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
