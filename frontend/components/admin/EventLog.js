"use client";

import { useEffect, useState } from "react";
import { BellIcon } from "../icons/BellIcon";

export default function EventLog() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // In a real scenario, we will connect to a WebSocket and listen for event messages.
    // const ws = new WebSocket('ws://localhost:8000/api/v1/ws/events');
    // ws.onmessage = (event) => {
    //   const newEvent = JSON.parse(event.data);
    //   setEvents(prevEvents => [newEvent, ...prevEvents]);
    // };

    // Simulating new events for demonstration
    const placeholderEvents = [
      { id: 1, camera: "Industrial Zone - Cam 1", type: "Smoke Detected", severity: "High", time: new Date().toLocaleTimeString() },
      { id: 2, camera: "River Outflow - Cam 2", type: "Unusual Color", severity: "Medium", time: new Date().toLocaleTimeString() },
    ];
    setEvents(placeholderEvents);

    const interval = setInterval(() => {
        const newEvent = {
            id: Date.now(),
            camera: "Industrial Zone - Cam 1",
            type: "Smoke Detected",
            severity: "High",
            time: new Date().toLocaleTimeString()
        };
        setEvents(prevEvents => [newEvent, ...prevEvents]);
    }, 10000); // Add a new event every 10 seconds

    return () => {
        // ws.close();
        clearInterval(interval);
    }
  }, []);

  const getSeverityClass = (severity) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="rounded-lg border bg-white shadow-sm">
      <div className="flex items-center gap-3 border-b p-4">
        <BellIcon className="h-6 w-6 text-primary" />
        <h2 className="text-lg font-semibold">Real-time Event Log</h2>
      </div>
      <div className="h-96 overflow-y-auto">
        <ul>
          {events.map((event) => (
            <li key={event.id} className="border-b p-4">
              <div className="flex justify-between">
                <span className="font-semibold">{event.camera}</span>
                <span className="text-xs text-gray-500">{event.time}</span>
              </div>
              <p className="text-sm text-gray-700">{event.type}</p>
              <span className={`mt-1 inline-block rounded-full px-2 py-1 text-xs font-medium ${getSeverityClass(event.severity)}`}>
                {event.severity}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}