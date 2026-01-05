


import { useEffect, useMemo, useRef, useState } from "react";

type FileKind = "pdf" | "word" | "excel";

type UploadedFile = {
  id: string;
  name: string;
  kind: FileKind;
  sizeBytes: number;
  uploadedAt: number;
};

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(1)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(1)} MB`;
  const gb = mb / 1024;
  return `${gb.toFixed(2)} GB`;
}

function kindLabel(k: FileKind) {
  return k === "pdf" ? "PDF" : k === "word" ? "Word" : "Excel";
}

function kindAccept(k: FileKind) {
  if (k === "pdf") return ".pdf,application/pdf";
  if (k === "word")
    return ".doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document";
  return ".xls,.xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
}

function isFileKindAllowed(kind: FileKind, file: globalThis.File) {
  const n = file.name.toLowerCase();
  if (kind === "pdf") return n.endsWith(".pdf");
  if (kind === "word") return n.endsWith(".doc") || n.endsWith(".docx");
  return n.endsWith(".xls") || n.endsWith(".xlsx");
}

/** Django mapper: backend item -> UploadedFile */
function mapBackendItemToUi(item: any): UploadedFile | null {
  if (!item) return null;

  const id = String(item.id ?? "");
  const kind = item.kind as FileKind;
  const name = item.name ?? item.original_name ?? item.originalName ?? "";
  const sizeBytes = Number(item.sizeBytes ?? item.size_bytes ?? item.size ?? 0);

  const uploadedRaw = item.uploadedAt ?? item.uploaded_at ?? item.uploadedAtMs;
  const uploadedAt =
    typeof uploadedRaw === "number"
      ? uploadedRaw
      : uploadedRaw
      ? new Date(uploadedRaw).getTime()
      : Date.now();

  if (!id || !name || !kind) return null;
  return { id, name, kind, sizeBytes, uploadedAt };
}

// ====== ENV (no props) ======
const BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:8000";
const API_KEY = (import.meta as any).env?.VITE_RAG_API_KEY || "";

// Django URLs (adjust if you mounted under /api/)
const LIST_PATH = "api/files/";
const UPLOAD_PATH = "api/files/";
const DELETE_PATH = "api/files"; // we'll call DELETE /files/<uuid>/

const MAX_SIZE_MB = 30;

const File = () => {
  const [kind, setKind] = useState<FileKind>("pdf");
  const [selected, setSelected] = useState<globalThis.File | null>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [loadingList, setLoadingList] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const maxBytes = useMemo(() => MAX_SIZE_MB * 1024 * 1024, []);

  const headers = useMemo(() => {
    const h: Record<string, string> = {};
    if (API_KEY) h["X-RAG-API-KEY"] = API_KEY;
    return h;
  }, []);

  const fullUrl = (path: string) => {
    const b = String(BASE_URL).replace(/\/$/, "");
    const p = path.startsWith("/") ? path : `/${path}`;
    return `${b}${p}`;
  };

  const resetPicker = () => {
    setSelected(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const loadFiles = async () => {
    setError(null);
    setLoadingList(true);
    const companyId = sessionStorage.getItem("company_id");
    if (!companyId) {
      setLoadingList(false);
      return setError("Missing company_id in session. Please re-login.");
    }
    try {
      const res = await fetch(`${fullUrl(LIST_PATH)}?company_id=${encodeURIComponent(companyId)}`, {
        method: "GET",
        headers: { ...headers },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);

      const data = await res.json();
      const rawItems = Array.isArray(data?.items) ? data.items : [];
      const mapped = rawItems.map(mapBackendItemToUi).filter(Boolean) as UploadedFile[];
      setFiles(mapped);
    } catch (e: any) {
      setError(e?.message ?? "Failed to load files.");
    } finally {
      setLoadingList(false);
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const onPick = (f: globalThis.File | null) => {
    setError(null);
    if (!f) return setSelected(null);

    if (!isFileKindAllowed(kind, f)) {
      setSelected(null);
      return setError(`File type mismatch. You selected ${kindLabel(kind)} but the file extension doesn't match.`);
    }
    if (f.size > maxBytes) {
      setSelected(null);
      return setError(`File too large. Max allowed is ${MAX_SIZE_MB} MB.`);
    }
    setSelected(f);
  };

  const upload = async () => {
    setError(null);
    if (!selected) return;

    setUploading(true);
    try {
      const companyId = sessionStorage.getItem("company_id");
      if (!companyId) {
        return setError("Missing company_id in session. Please re-login.");
      }
      const fd = new FormData();
      fd.append("file", selected);
      fd.append("kind", kind);
      fd.append("company", companyId);

      const res = await fetch(fullUrl(UPLOAD_PATH), {
        method: "POST",
        headers: { ...headers }, // do NOT set Content-Type
        body: fd,
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);

      const data = await res.json();
      const created = mapBackendItemToUi(data?.item);
      if (created?.id) {
        setFiles((prev) => [created, ...prev]);
      } else {
        await loadFiles();
      }

      resetPicker();
    } catch (e: any) {
      setError(e?.message ?? "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const remove = async (id: string) => {
    setError(null);
    setDeletingId(id);
    try {
      const url = `${fullUrl(DELETE_PATH)}/${encodeURIComponent(id)}/`;
      const res = await fetch(url, {
        method: "DELETE",
        headers: { ...headers },
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      setFiles((prev) => prev.filter((x) => x.id !== id));
    } catch (e: any) {
      setError(e?.message ?? "Delete failed.");
    } finally {
      setDeletingId(null);
    }
  };

  const accept = kindAccept(kind);

  return (
    <div className="mx-auto w-full  p-4">
      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
       

        {/* Upload box */}
        <div className="px-5 py-4">
          <div className="grid gap-3 md:grid-cols-12">
            <div className="md:col-span-3">
              <label className="mb-1 block text-sm font-medium text-zinc-800">File type</label>
              <select
                value={kind}
                onChange={(e) => {
                  setKind(e.target.value as FileKind);
                  setError(null);
                  if (selected && !isFileKindAllowed(e.target.value as FileKind, selected)) resetPicker();
                }}
                className="w-full rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 outline-none focus:border-zinc-400"
              >
                <option value="pdf">PDF</option>
                <option value="word">Word</option>
                <option value="excel">Excel</option>
              </select>
              <div className="mt-1 text-xs text-zinc-500">Allowed: {accept.split(",")[0]}</div>
            </div>

            <div className="md:col-span-6">
              <label className="mb-1 block text-sm font-medium text-zinc-800">Choose file</label>
              <input
                ref={inputRef}
                type="file"
                accept={accept}
                onChange={(e) => onPick(e.target.files?.[0] ?? null)}
                className="block w-full cursor-pointer rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-700 file:mr-3 file:rounded-lg file:border-0 file:bg-zinc-900 file:px-3 file:py-1.5 file:text-sm file:font-semibold file:text-white hover:file:bg-zinc-800"
              />
              <div className="mt-1 text-xs text-zinc-500">Max size: {MAX_SIZE_MB} MB</div>
            </div>

            <div className="md:col-span-3 md:flex md:items-end">
              <button
                type="button"
                onClick={upload}
                disabled={!selected || uploading}
                className="inline-flex w-full items-center justify-center rounded-xl bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {uploading ? "Uploading…" : "Upload"}
              </button>
            </div>
          </div>

          {selected ? (
            <div className="mt-3 rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="min-w-0">
                  <span className="font-semibold">{selected.name}</span>{" "}
                  <span className="text-zinc-500">({formatBytes(selected.size)})</span>
                </div>
                <button
                  type="button"
                  onClick={resetPicker}
                  className="rounded-lg border border-zinc-200 bg-white px-2 py-1 text-xs font-medium text-zinc-700 hover:bg-zinc-50"
                >
                  Clear
                </button>
              </div>
            </div>
          ) : null}

          {error ? (
            <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {error}
            </div>
          ) : null}
        </div>

        {/* List */}
        <div className="border-t border-zinc-200">
          <div className="flex items-center justify-between px-5 py-3">
            <div className="text-sm font-semibold text-zinc-900">
              Files <span className="text-zinc-500">({files.length})</span>
            </div>
           
          </div>

          {files.length === 0 ? (
            <div className="px-5 pb-5">
              <div className="rounded-xl border border-dashed border-zinc-200 bg-white p-4 text-sm text-zinc-600">
                No files yet. Upload one to see it here.
              </div>
            </div>
          ) : (
            <div className="px-5 pb-5">
              <div className="overflow-hidden rounded-2xl border border-zinc-200">
                <div className="grid grid-cols-12 bg-zinc-50 px-3 py-2 text-xs font-semibold text-zinc-600">
                  <div className="col-span-5">Name</div>
                  <div className="col-span-2">Type</div>
                  <div className="col-span-2">Size</div>
                  <div className="col-span-2">Uploaded</div>
                  <div className="col-span-1 text-right"> </div>
                </div>

                <div className="divide-y divide-zinc-200 bg-white">
                  {files.map((f) => (
                    <div key={f.id} className="grid grid-cols-12 items-center px-3 py-3 text-sm">
                      <div className="col-span-5 min-w-0">
                        <div className="truncate font-medium text-zinc-900">{f.name}</div>
                   
                      </div>

                      <div className="col-span-2">
                        <span className="inline-flex items-center rounded-lg border border-zinc-200 bg-zinc-50 px-2 py-1 text-xs font-semibold text-zinc-700">
                          {kindLabel(f.kind)}
                        </span>
                      </div>

                      <div className="col-span-2 text-zinc-700">{formatBytes(f.sizeBytes)}</div>

                      <div className="col-span-2 text-zinc-600">{new Date(f.uploadedAt).toLocaleString()}</div>

                      <div className="col-span-1 flex justify-end">
                        <button
                          type="button"
                          onClick={() => remove(f.id)}
                          disabled={deletingId === f.id}
                          className="rounded-xl border border-zinc-200 bg-white px-2 py-1.5 text-xs font-semibold text-zinc-800 hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                          {deletingId === f.id ? "…" : "Delete"}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default File;
