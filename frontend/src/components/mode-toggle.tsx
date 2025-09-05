import { Moon, Sun, SunMoon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/components/theme-provider";

/**
 * A component that provides a button to toggle the color theme.
 *
 * It cycles through "light", "dark", and "system" themes.
 *
 * @returns {JSX.Element} The rendered ModeToggle component.
 */
export function ModeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    if (theme === "light") {
      setTheme("dark");
    } else if (theme === "dark") {
      setTheme("system");
    } else {
      setTheme("light");
    }
  };

  const getIcon = () => {
    switch (theme) {
      case "light":
        return <Sun className="h-4 w-4" />;
      case "dark":
        return <Moon className="h-4 w-4" />;
      case "system":
        return <SunMoon className="h-4 w-4" />;
      default:
        return <Sun className="h-4 w-4" />;
    }
  };

  const getTooltip = () => {
    switch (theme) {
      case "light":
        return "Переключить на тёмную тему";
      case "dark":
        return "Переключить на системную тему";
      case "system":
        return "Переключить на светлую тему";
      default:
        return "Переключить тему";
    }
  };

  return (
    <Button
      onClick={toggleTheme}
      variant="ghost"
      size="icon"
      title={getTooltip()}
    >
      {getIcon()}
    </Button>
  );
}
