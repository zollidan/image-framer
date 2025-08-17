import React from "react";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

export const SortableImage = ({ image, handleDelete }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: image.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="image-item"
    >
      <img
        src={`${import.meta.env.VITE_API_URL}/s3/file/${image.s3_filename}`}
        alt={image.original_filename}
      />
      <button className="delete-button" onClick={() => handleDelete(image.id)}>
        &times;
      </button>
    </div>
  );
};
