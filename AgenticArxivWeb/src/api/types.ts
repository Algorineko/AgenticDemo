export type Role = "user" | "assistant";

export interface Paper {
  id: string;
  title: string;
  authors: string[];
  summary?: string | null;
  published?: string | null;
  updated?: string | null;
  pdf_url?: string | null;
  primary_category?: string | null;
  categories: string[];
  comment?: string | null;
  links: string[];
}

export type PdfAssetStatus = "NOT_DOWNLOADED" | "DOWNLOADING" | "READY" | "FAILED";

export interface PdfAsset {
  paper_id: string;
  pdf_url: string;
  local_path: string;
  status: PdfAssetStatus;
  size_bytes: number;
  sha256?: string | null;
  downloaded_at?: string | null;
  updated_at: string;
  error?: string | null;
}

export type TranslateAssetStatus = "NOT_TRANSLATED" | "TRANSLATING" | "READY" | "FAILED";

export interface TranslateAsset {
  paper_id: string;
  input_pdf_path: string;
  output_mono_path: string;
  output_dual_path?: string | null;
  status: TranslateAssetStatus;
  service?: string | null;
  threads: number;
  translated_at?: string | null;
  updated_at: string;
  error?: string | null;
}

export interface ReactStep {
  thought: string;
  action: string;
  observation: string;
}

export interface ChatResponse {
  session_id: string;
  message: string;
  reply: string;
  history: ReactStep[];
  papers: Paper[];
  pdf_assets: PdfAsset[];
  translate_assets: TranslateAsset[];
}
