import Header from "../components/admin/Header";
import Sidebar from "../components/admin/Sidebar";
import CameraList from "../components/admin/CameraList";
import EventLog from "../components/admin/EventLog";

export default function AdminDashboard() {
  return (
    <div className="flex min-h-screen w-full flex-col bg-gray-50">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold mb-6 text-foreground">Live Camera Feeds</h2>
              <CameraList />
            </div>
            <div className="lg:col-span-1">
               {/* The EventLog component will have its own title */}
              <h2 className="text-2xl font-bold mb-6 text-foreground invisible">Events</h2>
              <EventLog />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}