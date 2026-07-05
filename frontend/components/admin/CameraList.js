"use client";

import { useEffect, useState } from "react";
import VideoPlayer from "./VideoPlayer";
import { CameraIcon } from "../icons/CameraIcon";

export default function CameraList() {
  const [cameras, setCameras] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/cameras')
      .then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then(data => setCameras(data))
      .catch(error => {
        console.error("Failed to fetch cameras:", error);
        const placeholderCameras = [
          { id: 1, name: "Industrial Zone - Cam 1", location: "Sector 12", source: "live" },
          { id: 2, name: "River Outflow - Cam 2", location: "Riverbank Park", source: "live" },
          { id: 3, name: "City Center - Cam 3", location: "Main Street", source: "offline" },
        ];
        setCameras(placeholderCameras);
      });
  }, []);

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {cameras.map((camera) => (
        <div key={camera.id} className="rounded-lg border bg-white shadow-sm">
          <div className="p-4">
            <h3 className="font-semibold text-lg">{camera.name}</h3>
            <p className="text-sm text-gray-500">{camera.location}</p>
          </div>
          <div className="aspect-video bg-gray-100 flex items-center justify-center">
            {camera.source === "live" ? (
              <VideoPlayer cameraId={camera.id} />
            ) : (
              <div className="text-center text-gray-500">
                <CameraIcon className="mx-auto h-12 w-12" />
                <p>Camera Offline</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}