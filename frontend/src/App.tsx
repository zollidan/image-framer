import { Header } from "@/components/header/header";
import { Footer } from "@/components/footer/footer";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { EditWhiteBg } from "@/components/edit-white/edit-white-bg";
import { EditAddFrameBg } from "@/components/edit-add-framer";
import { ImageList } from "@/components/image-list";

function App() {
  return (
    <>
      <Header />
      <Separator />
      <main className="h-screen">
        <div className="flex justify-center items-center h-full w-full">
          <Tabs defaultValue="white-bg" className="w-[400px]">
            <TabsList>
              <TabsTrigger value="white-bg">Белый фон</TabsTrigger>
              <TabsTrigger value="frame">Рамка</TabsTrigger>
              <TabsTrigger value="files" disabled>
                Файлы
              </TabsTrigger>
              <TabsTrigger value="gallery" disabled>
                Сетка
              </TabsTrigger>
            </TabsList>
            <TabsContent value="white-bg">
              <EditWhiteBg />
            </TabsContent>
            <TabsContent value="frame">
              <EditAddFrameBg />
            </TabsContent>
            <TabsContent value="files">
              <ImageList />
            </TabsContent>
          </Tabs>
        </div>
      </main>
      <Separator />
      <Footer />
    </>
  );
}

export default App;
