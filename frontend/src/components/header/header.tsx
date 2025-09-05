/**
 * The header component of the application.
 *
 * Displays the application title.
 *
 * @returns {JSX.Element} The rendered Header component.
 */
export const Header = () => {
  return (
    <header className="w-full h-16 flex justify-center items-center space-x-4">
      <div>
        <h1 className="font-bold">alice.com</h1>
      </div>
    </header>
  );
};
