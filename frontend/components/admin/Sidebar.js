import { LayoutDashboardIcon } from "../icons/LayoutDashboardIcon";

export default function Sidebar() {
  return (
    <aside className="hidden w-64 flex-col border-r bg-gray-50 p-4 sm:flex">
      <nav className="flex flex-col space-y-1">
        <a
          href="#"
          className="flex items-center gap-3 rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground"
        >
          <LayoutDashboardIcon className="h-4 w-4" />
          Dashboard
        </a>
      </nav>
    </aside>
  );
}