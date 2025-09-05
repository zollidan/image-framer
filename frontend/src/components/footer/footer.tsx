import { ModeToggle } from "@/components/mode-toggle";

/**
 * The footer component of the application.
 *
 * Displays copyright information, a link to the GitHub repository,
 * and a theme mode toggle button.
 *
 * @returns {JSX.Element} The rendered Footer component.
 */
export const Footer = () => {
  return (
    <footer className="w-full h-16 flex justify-between items-center space-x-4 px-12">
      <p className="text-sm">
        © 2025 alice.com / 1.0.0 / made with react & fastapi
      </p>
      <div className="flex items-center space-x-2">
        <p className="text-sm">
          <a href="https://github.com/zollidan/image-framer">github</a>
        </p>
        <ModeToggle></ModeToggle>
      </div>
    </footer>
  );
};
