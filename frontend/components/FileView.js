
export default function FileView({ file }) {
  return (
    <iframe
      src={file}
      width="100%"
      height="100%"
      title="File Viewer"
    />
  )
}
