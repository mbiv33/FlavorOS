// Work — built in Slice 3.
export default function WorkPage() {
  return <SurfacePlaceholder title="Work" />;
}

function SurfacePlaceholder({ title }: { title: string }) {
  return (
    <div className="px-1 pt-4">
      <h1 className="m-0 mb-1 text-[28px] font-bold tracking-tight">{title}</h1>
      <div className="text-[13.5px] text-ink-3">
        Surface scheduled for a later slice.
      </div>
    </div>
  );
}
