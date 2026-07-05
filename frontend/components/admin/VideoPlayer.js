"use client";

import { useEffect, useRef } from "react";

export default function VideoPlayer({ cameraId }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${cameraId}`);

    ws.onmessage = (event) => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const data = JSON.parse(event.data);

      // Assuming the backend sends the image as a base64 string
      const image = new Image();
      image.src = `data:image/jpeg;base64,${data.frame}`;
      image.onload = () => {
        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);

        // Draw bounding boxes if they exist
        if (data.boxes) {
          data.boxes.forEach(box => {
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.strokeRect(box.x1, box.y1, box.x2 - box.x1, box.y2 - box.y1);
          });
        }
      };
    };

    return () => {
      ws.close();
    };
  }, [cameraId]);

  return <canvas ref={canvasRef} className="w-full h-auto rounded-md" />;
}