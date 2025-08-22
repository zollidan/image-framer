import { Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";

import { useTheme } from "@/components/theme-provider";

export function ModeToggle() {
  const { setTheme } = useTheme();

  //   const themes = ["light", "dark", "system"];

  return (
    <div className="bottom-2 right-2 absolute">
      <Button onClick={() => setTheme("dark")}>
        <Moon />
      </Button>
    </div>
  );
}
