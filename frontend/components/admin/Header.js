import { CameraIcon } from "../icons/CameraIcon";

export default function Header() {
  return (
    <header className="flex h-16 items-center border-b bg-white px-4 shadow-sm md:px-6">
      <div className="flex items-center gap-3">
        <CameraIcon className="h-6 w-6 text-primary" />
        <h1 className="text-lg font-semibold text-foreground">Envirolens Admin Dashboard</h1>
      </div>
    </header>
  );
}