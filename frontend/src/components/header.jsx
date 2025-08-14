export const Header = () => {
  return (
    <header className="w-full h-16 flex justify-center items-center space-x-6">
      <nav>
        <ul className="flex space-x-4">
          <li>
            <a href="/">Рамка</a>
          </li>
          <li>
            <a href="/white-bg">Белый фон</a>
          </li>
        </ul>
      </nav>
    </header>
  );
};
