import { useRef } from "react";

const ACCEPTED =
  ".docx,.xlsx,.pptx,.pdf,.png,.jpg,.jpeg";

export default function FileUpload({ files, onChange }) {
  const inputRef = useRef(null);

  const handleChange = (e) => {
    onChange(Array.from(e.target.files));
  };

  return (
    <div className="file-upload">
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED}
        multiple
        onChange={handleChange}
      />
      <button
        type="button"
        className="upload-btn"
        onClick={() => inputRef.current.click()}
      >
        📎 Attach Files
      </button>
      {files.length > 0 && (
        <div className="file-names">
          {files.map((f, i) => (
            <span className="chip" key={i}>
              {f.name}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
