import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Header } from "./components/header";
import { Footer } from "./components/footer";
import { EditWhiteBg } from "./components/edit-white-bg";
import { EditAddFrameBg } from "./components/edit-add-framer";
import { ThemeProvider } from "./components/theme-provider";

/**
 * The main component of the application.
 *
 * Renders the header, footer, and a tab-based navigation for different
 * image editing functionalities.
 *
 * @returns {JSX.Element} The rendered App component.
 */
function App() {
  return (
    <>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Header />
        <Separator />
        <main className="h-screen">
          <div className="flex justify-center items-center h-full w-full">
            <Tabs defaultValue="white-bg" className="w-[400px]">
              <TabsList>
                <TabsTrigger value="white-bg">Белый фон</TabsTrigger>
                <TabsTrigger value="frame">Рамка</TabsTrigger>
              </TabsList>
              <TabsContent value="white-bg">
                <EditWhiteBg />
              </TabsContent>
              <TabsContent value="frame">
                <EditAddFrameBg />
              </TabsContent>
            </Tabs>
          </div>
        </main>
        <Separator />
        <Footer />
      </ThemeProvider>
    </>
  );
}

export default App;
